# EtherCAT 网页参考：CoE、SDO/PDO、动态 PDO、EoE、TwinCAT 任务

## 读取触发

当用户提到以下任一内容时读取本文件：

- CoE、对象字典 OD、添加对象、SDO、PDO、FoE、EoE。
- `0x1600/0x1A00`、`0x1C12/0x1C13`、动态 PDO、PDO Mapping/Assign。
- `APPL_InputMapping()`、`APPL_OutputMapping()`、`PDO_InputMapping()`、`PDO_OutputMapping()`。
- TwinCAT PLC 任务、PLC cycle、base time、Separate Input Update、输入从站到输出从站延时。
- EoE 通信速率低、Mailbox 轮询、上位机通过 EtherCAT 网口诊断。

## 核心来源

1. `[EtherCAT] CoE协议与服务数据(SDO)和过程数据(PDO)`
2. `[EtherCAT] CoE添加对象字典内容`
3. `[EtherCAT]从站实现动态PDO功能`
4. `[EtherCAT]EOE通信速率分析和改善`
5. `[EtherCAT]从输入从站读取数据写入输出从站的时序分析`
6. `[EtherCAT]从输入从站读取数据后写入输出从站的延时测量`
7. `[EtherCAT]TwinCAT中创建PLC任务`

详见 `ethercat-web-knowledge-index.md`。

## 通信模型

网页文章将 EtherCAT 主从通信按数据链路访问方式区分为：

| 方式 | 典型用途 | 特点 |
|---|---|---|
| 寄存器访问 | ESC 配置/状态，如 DL Status、AL Control/Status | 主站直接访问 ESC 寄存器；权限由寄存器定义 |
| Mailbox | SDO、FoE、EoE 等非周期数据 | 请求-应答，非实时，容量和轮询限制明显 |
| Process Data / Buffer | PDO 周期实时数据 | 生产者-消费者模型，依赖 SM/FMMU/DPRAM buffer |

CoE 关系：

- SDO：CoE + Mailbox，用于参数、对象字典读写。
- PDO：CoE 对象字典描述 + Process Data 传输，用于周期实时数据。
- FoE/EoE：走 Mailbox，但不依赖 CoE OD 解释数据含义。

## 添加 CoE 对象字典内容

优先路径：使用 SSC Tool OD 工具/Excel 修改对象定义并重新生成 XML 与协议栈代码。

适用：

- 新增 SDO 参数。
- 新增 PDO 输入/输出数据。
- 保证 ESI XML、对象字典代码和 mapping 自动一致。

手工路径：同步修改 ESI XML 与从站程序。

风险：

- XML 有对象，代码没有对象：TwinCAT 能看到但 SDO/PDO 访问失败。
- 代码有对象，XML 没对象：主站无法自动配置或 mapping。
- PDO bit length、subindex、access、rx/tx 属性不一致：SAFEOP/OP 切换失败或 WcState 异常。

## 动态 PDO 设计

动态 PDO 的关键是 `0x1C12/0x1C13` 与 `0x160x/0x1A0x` 两层都要处理。

| 类型 | 0x1C12/0x1C13 | 0x160x/0x1A0x | 例子 |
|---|---|---|---|
| 固定 Assign + 固定 Mapping | 固定 | 固定 | 简单 IO 例程 |
| 可变 Assign + 固定 Mapping | 可选不同 PDO 集 | 固定 | CIA402 按模式选择不同 PDO |
| 可变 Assign + 可变 Mapping | 可变 | 可变 | 主站灵活组合 PDO entry |

实现动态 Mapping 时：

1. 允许主站写 `0x160x/0x1A0x` 的 subindex 0 和 entries。
2. 在 PREOP 或允许的配置窗口修改，OP 中不要无保护改 mapping。
3. 在 `APPL_GenerateMapping()` 重新计算 input/output size。
4. 在 `APPL_InputMapping()`/`APPL_OutputMapping()` 按当前 mapping entries 遍历，不要假设固定顺序。
5. 校验对象是否可映射、bit length 是否匹配、总长度是否超出 SM/FMMU 限制。

## PDO 时序与延时

厂商 输入从站 A 到输出从站 B 的时序模型：

```text
A 从站采样输入
  -> 主站 PDO 输入帧经过 A，读取 A 的输入
  -> 数据帧返回主站
  -> PLC/NC 任务处理 input -> output
  -> 下一周期主站 PDO 输出帧下发 B 的输出
  -> B 从站收到输出并更新 IO
```

关键结论：

- ESC 硬件在报文到达时立即和 DPRAM 交换。
- 从站 MCU 若没有在报文到来前写好 TxPDO，将错过当前周期。
- 默认 3-buffer 能降低竞争，但不能消除应用任务与报文到达的相位问题。
- 若使用 Separate Input Update，最小延时大于 Pre ticks，最大延时约等于 PLC 周期 + Pre ticks。

用于伺服时的对应启发：

- TxPDO 反馈值必须在 Sync0/报文到来前准备好。
- RxPDO 命令应在 PDI/SM2 事件后尽快形成快照，供控制周期使用。
- 不要在异步后台随意更新位置/速度反馈对象，容易造成一周期延迟或撕裂。

## EoE 速率诊断

EoE 是 EtherCAT 网络中的以太网隧道：

- 通过 Mailbox 封装标准以太网帧。
- 可用于伺服参数配置、诊断、内置 Web Server、网桥设备等。
- 默认 SSC 邮箱通常轮询，且 EtherCAT 从站不能主动发帧，只能等主站帧到来时被动交换。

因此：

- EoE 速率不能按 100M 以太网预期。
- 提升方向是优化主站 mailbox 轮询、邮箱大小、任务周期、协议处理路径，而不是只看 PHY 带宽。
- 不要把 EoE 低速和 PDO/NC 实时通信混为一类问题。

## TwinCAT PLC 任务

用于 IO 联动或延时测量时：

1. 创建 PLC 工程。
2. 编写 ST 逻辑，如 `output2 := input1;`。
3. 编译并链接 PLC 变量到从站 IO。
4. 设置 PLC task 周期；必要时修改 base time 以获得更细周期粒度。
5. 运行 PLC，必要时设置 autostart boot project。
6. 若要调通信延时，记录 PLC 周期、EtherCAT 周期、Separate Input Update Pre ticks 和从站更新时刻。

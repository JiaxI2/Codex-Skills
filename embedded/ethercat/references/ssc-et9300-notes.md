# SSC/ET9300 工程笔记

## 典型代码结构

SSC 工程通常分为三层：

1. PDI/硬件适配：ESC 读写、PDI 总线、AL Event、Sync0/Sync1 中断。
2. 通用 EtherCAT 协议栈：ESM、Mailbox、CoE、FoE、EoE、Process Data。
3. 用户应用：对象字典变量、PDO Copy、CiA402 状态机、运动控制接口。

常见文件：

| 文件 | 作用 |
|---|---|
| `ecat_def.h` | SSC 配置宏 |
| `ecatappl.c` | 应用钩子、PDO Input/Output Mapping |
| `coeappl.c` | CoE 应用钩子 |
| `cia402appl.c` | CiA402 示例/适配逻辑 |
| `cia402appl.h` | CiA402 对象、轴结构、状态定义 |
| 生成的 OD 文件 | 对象字典元数据和变量声明 |

## 周期执行建议

推荐将 PDO 交互与应用更新做成确定性快照流程：

```text
SM2 event / Sync0
  -> APPL_OutputMapping：RxPDO -> 命令快照
  -> CiA402 状态机处理 0x6040/0x6060/目标量
  -> 与电机控制核交互
  -> 反馈快照准备完成
  -> APPL_InputMapping：反馈快照 -> TxPDO
```

关键原则：

- 不要让电机控制核直接读写 SSC 对象变量。
- 跨核/跨中断传递 32/64 位位置和速度时使用双缓冲、序列锁或关中断快照。
- `APPL_InputMapping` 应拷贝稳定反馈，不应现场计算复杂数据。
- Sync0 ISR 中不要执行日志格式化、慢速串口输出、SDO/FoE 文件操作。

## 对象字典设计

- 厂商自定义参数放在 `0x2000–0x5FFF`。
- CiA402/Profile 对象放在 `0x6000–0x9FFF`。
- 修改 xlsx/OD Tool 后必须检查生成代码 diff、ESI diff、PDO 长度和对象访问属性。
- 需要固定 padding 或特殊布局时，优先手工定义 PDO Mapping 和 SM Assignment。

## ESI 与固件一致性

每次改 PDO 后必须确认：

1. 固件对象字典存在该对象。
2. 对象数据类型、位宽、访问权限正确。
3. ESI 中 PDO Entry 顺序与固件 Copy 顺序一致。
4. 0x1C12/0x1C13 指向正确 PDO。
5. TwinCAT 已重载 ESI、删除旧实例并重新扫描。
6. EEPROM/SII 已更新或确认从 ESI 加载。

## 多轴实现

每个轴必须独立维护：

- Controlword/Statusword。
- Mode request/display。
- Target/Actual。
- Error Code/Fault State。
- Following error/limit state。
- Rx/Tx 更新计数和超时。

不要把单轴示例的全局对象直接复制到多轴工程。多轴应有明确的对象偏移、结构数组、PDO 组合策略和 TwinCAT 链接说明。

## 状态转换钩子

### PREOP→SAFEOP

- 校验 PDO 配置。
- 初始化轴对象和默认模式。
- 准备输入数据为有效，或通过对象/状态明确标记无效。
- 不要提前使能功率级。

### SAFEOP→OP

- 确认输出数据已经有效。
- 启动或绑定 Sync0/Application Cycle。
- CiA402 FSA 仍然决定伺服使能，不要因为 EtherCAT 到 OP 就直接打开驱动。

### OP→SAFEOP/INIT

- 执行 Abort connection option code 或项目定义的降级策略。
- 清理 follows command/ready 标志。
- 对电机控制核发送安全停机或保持策略。

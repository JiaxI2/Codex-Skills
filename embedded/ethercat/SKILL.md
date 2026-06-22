---
name: ethercat-cia402
description: 用于 EtherCAT 从站、CiA402/DS402 伺服驱动、TwinCAT 联调、PDO/SDO/CoE、ESI/XML、DC/Sync0/Sync1 同步、SSC/ET9300、Working Counter/WcState、AL/ESM、0x6040/0x6041/0x6060/0x6061、CSP/CSV/CST/PP/HM、NC 轴 Ready、invalid IO data、多轴同步和伺服使能问题的分析、代码审查与修复。不要用于普通以太网、与 EtherCAT/CiA402 无关的纯电机控制调参、通用嵌入式 C 任务。
---

# EtherCAT CiA402 Skill

本 Skill 面向嵌入式 EtherCAT 伺服驱动开发，重点覆盖 EtherCAT 从站固件、CiA402 驱动规约、TwinCAT 轴配置、PDO/SDO/CoE 映射、DC 同步、SSC/ET9300 工程、多轴实时性诊断、FSoE/安全相关接口边界，以及与电机控制核之间的共享内存交互。

## 默认立场

从协议层向应用层分层定位，从观测证据反推根因。不要直接把 EtherCAT、CiA402、电机控制、上位机配置混为一个问题。

1. 先分层：PHY/链路、ESC/DLL、AL/ESM、Mailbox/CoE/FoE/EoE、PDO/SM/FMMU、DC 同步、CiA402 FSA、运动控制应用、电源级/抱闸/安全链路。
2. 除非缺少关键证据导致无法继续判断，否则先给出可执行检查路径，再说明需要用户补充什么。
3. 用户要求改代码时，优先做最小安全补丁；除非用户明确要求重构，不要大规模重写已工作的工程结构。
4. 保持仓库编码、命名、缩进和生成代码边界。中文嵌入式工程默认保留现有 GBK/ANSI 编码，转换编码前必须询问用户。
5. EtherCAT Safety/FSoE、STO、抱闸、电源使能、故障复位、Fault Reaction 都按安全关键路径处理。必须说明假设、失效模式和回归测试。
6. 标准相关判断必须标明来源层级：CiA402/IEC 61800-7、ETG.6010、ETG.1000、SSC/ET9300、厂商手册、TwinCAT 实测行为或项目代码推断。
7. 对“现在能跑”的代码保持保守：先定位风险点，再建议局部补丁，避免为了规范化破坏现场可用功能。

## 首次响应模板

遇到新的 EtherCAT 问题，按以下结构输出：

```markdown
## 判断
[一句话说明最可能的问题层级和方向]

## 关键依据
- [对象值、状态位、TwinCAT 报错、代码路径、时序或日志证据]

## 优先检查
1. [最快验证项]
2. [第二验证项]
3. [隔离实验]

## 可能根因
| 优先级 | 根因 | 证据 | 验证方法 | 修复方向 |
|---|---|---|---|---|

## 建议改动
[最小代码/配置改动；注明风险和回归测试]
```

代码审查时追加：

```markdown
## 代码风险点
## 修改建议
## 回归测试
```

对象字典/PDO/ESI 问题追加：

```markdown
## 对象清单
| Index | 名称 | 方向 | PDO | 访问属性 | 备注 |
|---|---|---|---|---|---|
```


## 网页知识库本地参考路由

当问题涉及 EtherCAT 网页文章中的工程实现细节时，除通用 ETG/CiA402 规则外，按以下逻辑读取 `references/`。这些 ref 已把网页端文章内容转写为本地工程化摘要、检查清单和排障路径；回答时优先读取本地 ref，不需要再访问网页。

| 问题关键词 | 先读取 | 再结合 |
|---|---|---|
| `Module/Slot`、`MDP`、`DependOnSlot`、`MAX_AXES`、`0xF000/0xF010/0xF030/0xF050`、CIA402 多轴、TwinCAT 多生成 Axis | `web-cia402-mdp-multiaxis.md` | `ssc-et9300-notes.md`、`ethercat-cia402-quick-reference.md` |
| `0x1A`、`0x1B`、`0x2C`、`Sync0WdCounter`、`DC_CheckWatchdog`、PDI/Sync 中断、`AL_EVENT_ENABLED`、`DC_SUPPORTED`、`ECAT_TIMER_INT` | `web-ssc-sync-errors.md` | `twincat-diagnostics.md`、`troubleshooting-playbooks.md` |
| CoE、OD、SDO、PDO、动态 PDO、`0x1600/0x1A00`、`0x1C12/0x1C13`、EoE、TwinCAT PLC 任务、输入到输出延时 | `web-coe-pdo-eoe-twincat.md` | `ssc-et9300-notes.md` |
| PHY、Link、MII、MDC/MDIO、`0x110 DL Status`、EEPROM、Flash 模拟 EEPROM、ESC_CTR、IO_CFG、RUN_LED/ERR_LED、扫描不到从站、地址别名、Explicit Device ID | `web-phy-eeprom-hardware.md` | `troubleshooting-playbooks.md` |
| 不确定是哪类网页知识点 | `ethercat-web-knowledge-index.md` | 根据索引跳转专题 ref |

使用边界：网页知识库内容是 SDK/芯片/例程层实现参考，不替代 ETG.1000、ETG.6010、CiA402/IEC 61800-7 的规范定义。回答时应明确“规范语义”和“示例实现”两层，不要把网页示例中的默认配置误判为所有 EtherCAT 从站都必须如此。



## 开源项目蒸馏与 MCP 路由

当问题涉及 EtherCAT 主站源码、从站源码、开源 CiA402、LinuxCNC、ROS2 或 MCP 工具化时，按以下逻辑读取新增 ref：

| 问题关键词 | 优先读取 | 用途 |
|---|---|---|
| SOEM、IgH、EtherLab、主站、scan slaves、WKC、domain、SDO upload、Linux 实时主站 | `ethercat-master-source-map-soem-igh.md` | 主站源码心智模型、周期任务、WKC/SDO/DC 诊断 |
| SSC、ET9300、SOES、从站栈、PDI、ESC、OutputMapping、InputMapping、FoE、EEPROM/SII | `ethercat-slave-source-map-ssc-soes.md` | 从站固件架构、PDO/ESM/CoE/FoE、bring-up 检查 |
| ecat_servo、hal-cia402、CiA402 开源实现、6040/6041、6060/6061、CSP/CSV/CST、homing、fault reset | `cia402-open-source-implementation-map.md` | CiA402 状态机工程实现与主/从站分层 |
| TwinCAT、LinuxCNC、ROS2、ros2_control、HAL、NC Ready、axis not ready、controller not active | `twincat-linuxcnc-ros2-diagnostics-map.md` | 上位控制器诊断路径和跨平台故障矩阵 |
| MCP、Agent 工具化、ESI parser、ADS、SOEM 只读诊断、tshark 抓包、J-Link/串口日志 | `ethercat-mcp-design.md` | MCP 模块拆分、权限模型、下一步实施路线 |
| 不确定应该参考哪个开源项目或 ref | `ethercat-project-selection-guide.md` | 项目选型、蒸馏优先级、维护规则 |
| 知识库长期维护、ref 增长、版本计划 | `ethercat-maintenance-roadmap.md` | 可扩展目录、正确性检查、版本化路线 |

使用边界：开源项目 ref 只用于工程模式和源码入口参考；协议语义仍以 ETG.1000、ETG.6010、CiA402/IEC 61800-7、ET9300/SSC 为准。对具体 API、文件路径、release 行为不确定时，应让代码库/MCP 实时读取仓库，而不是凭 ref 断言。

## 需要检查的证据

不要一次性索要全部资料。根据问题层级选择最少证据。

### 主站/TwinCAT 侧

- EtherCAT 状态：INIT/PREOP/SAFEOP/OP、AL Status Code、WcState、Working Counter、DC Diagnostics、Sync0/Sync1 Error、Process Data Watchdog。
- NC 轴状态：Ready、Active、Error、Encoder valid、Drive valid、Link Mapping、Cycle Time、Scaling。
- ESI/XML：Vendor ID、Product Code、Revision、PDO Mapping、SM Assignment、DC Mode、Startup SDO、默认 Mode of Operation。
- 主站周期：NC Task、PLC Task、EtherCAT Task、Sync0 Cycle、Sync0 Shift、Interpolation 或 Subordinated Cycles。

### 从站/固件侧

- ESC/SSC 配置：PDI 类型、AL Event、SM2/SM3、FMMU、Watchdog、Sync0 ISR。
- CoE 对象：0x1000、0x1001、0x1018、0x1600..0x17FF、0x1A00..0x1BFF、0x1C12、0x1C13、0x1C32、0x1C33。
- CiA402 对象：0x603F、0x6040、0x6041、0x6060、0x6061、0x6064、0x607A、0x6071、0x6072、0x6077、0x6078、0x60B8/0x60B9、0x60F4、0x60FF、0x6502。
- 代码路径：`APPL_OutputMapping`、`APPL_InputMapping`、`ECAT_Application`、`CiA402_*`、PREOP→SAFEOP、SAFEOP→OP、Sync0/Application Cycle ISR、共享内存到电机控制核的交互。
- 运行计数：RxPDO 接收计数、TxPDO 更新计数、Sync0 计数、丢周期计数、运动环时间戳、SM Watchdog 计数、错误环形日志。

## CiA402 实现规则

### 0x6060/0x6061

- `0x6060 Modes of operation` 是主站请求模式；`0x6061 Modes of operation display` 是驱动实际接受并运行的模式。
- 不允许只在 ESI 中写默认 CSP 就认为运行时已经进入 CSP。固件必须有明确的模式接受、校验、拷贝和拒绝路径。
- 若支持运行中动态切换 CSP/CSV/CST/PP/HM，RxPDO 应映射 0x6060，TxPDO 应映射 0x6061；否则至少通过 Startup SDO 和固件默认值确保一致。
- `0x6502 Supported drive modes` 必须真实反映支持的模式，否则 TwinCAT/NC 可能选择错误的轴类型或模式。

### 0x6040/0x6041

- 始终先解码 FSA 基本状态：Ready to Switch On、Switched On、Operation Enabled、Fault、Switch On Disabled、Quick Stop。
- `Statusword bit12` 是模式相关位：
  - PP：通常是 Set-point acknowledge。
  - CSP/CSV/CST：通常按 Drive follows command/command valid 语义处理。
- 不要把 PP 的 bit12 清零逻辑直接复用到 CSP/CSV/CST。TwinCAT NC Ready/Active 常依赖该位和实际值有效性。
- Fault Reset 只处理边沿或明确命令，不要长时间保持复位动作。

### CSP/CSV/CST

- CSP 典型 RxPDO：0x6040 Controlword、0x607A Target position、可选 0x6060 Mode、0x6072 Max torque。
- CSP 典型 TxPDO：0x6041 Statusword、0x6064 Position actual value、可选 0x6061 Mode display、0x60F4 Following error。
- CSV 典型 RxPDO：0x6040、0x60FF Target velocity、可选 0x6060。
- CST 典型 RxPDO：0x6040、0x6071 Target torque、可选 0x6060、0x6072。
- 多模式合并 PDO 时，不要重复映射 Controlword/Statusword；保证字节长度、顺序、对齐、ESI、固件对象字典完全一致。

### PP/HM

- PP 的 set-point acknowledge、target reached、new set-point 位与 CSP 的 follows command 不是同一个时序模型。
- HM 需要明确 Homing start、Homing attained、Homing error、Target reached 的位含义；绝对编码器回零不等于强制把实际位置清零。

## SSC/ET9300 工程规则

### 代码边界

- 平台/PDI/硬件访问：ESC 读写、PDI、Sync0/Sync1 中断。
- 通用协议栈：ESM、Mailbox、CoE、FoE、EoE、Process Data。
- 应用层：对象字典变量、PDO Copy、CiA402 轴状态、运动控制接口。
- 不要在生成对象字典文件中手工堆逻辑。手工逻辑应放在应用层 `.c/.h` 或清晰标注的用户区。

### 周期数据路径

目标顺序：

```text
SM2 event / Sync0
  -> APPL_OutputMapping 将 RxPDO 拷贝到命令快照
  -> CiA402/Application 使用快照更新状态机和目标量
  -> 与电机控制核交互，必要时使用双缓冲/序列锁
  -> 准备反馈快照
  -> APPL_InputMapping 将反馈拷贝到 TxPDO
```

避免：

- 多上下文直接写 TxPDO 对象。
- 未加快照读取 32/64 位位置、速度、时间戳。
- 电机环读取半更新的 RxPDO。
- 在 Sync0 ISR 内做重日志、SDO 慢操作、复杂格式化输出。

### 多轴

- 每轴状态、模式显示、目标、反馈、错误码必须独立，不要多个轴共享全局 0x6060/0x6061 或全局状态字，除非设备明确是单轴。
- 多轴对象偏移、PDO 长度和 SM/FMMU 必须按轴数验证。
- 共享内存结构必须有版本号、长度、对齐和一致性标记。

## TwinCAT 诊断优先级

### OP 之前失败

1. 看 AL Status Code。
2. 看 Mailbox/CoE Startup SDO 是否失败。
3. 看 ESI 与对象字典是否匹配。
4. 看 PDO/SM Assignment 长度是否被拒绝。

### OP 后 invalid IO / WcState

1. 看 WcState 是 EtherCAT 设备级、端子级、还是 NC Encoder/Drive 变量级。
2. 看 Working Counter 是否周期性跳变。
3. 看 DC Diagnostics 和 Sync0/Sync1 错误。
4. 看 Process Data Watchdog 是否触发。
5. 看 TxPDO 是否由非同步任务更新，是否存在共享内存撕裂。
6. 协议和时序排除后，再看 PHY 计数、线缆、屏蔽、拓扑。

### NC 轴 Not Ready

1. 解码 0x6041。
2. 检查 bit0/1/2 是否置位、bit3 是否为 0。
3. 检查 0x6061 是否等于目标模式。
4. CSP/CSV/CST 检查 bit12 是否按 follows command 置位。
5. 检查 0x6064 是否周期更新且 Encoder valid。
6. 检查 NC Link 和 Scaling。

## 常见问题 Playbook

### 0x6060=8，但 0x6061=0

判断：固件只接收了模式请求，未接受/未显示实际模式，或模式显示被初始化覆盖。

检查：

1. TwinCAT 是否通过 SDO 或 RxPDO 写入 0x6060=8。
2. 固件中 0x6060 背后变量在 PREOP→SAFEOP、SAFEOP→OP 后是否仍为 8。
3. 模式校验是否允许 CSP。
4. 0x6061 是否只在模式接受后更新。
5. 0x6502 是否声明 CSP 支持。
6. 是否存在轴初始化把 0x6061 清回 0。

修复：实现 `requested_mode -> validate -> accepted_mode -> mode_display` 的明确路径，并加入拒绝原因日志。

### TwinCAT 仍按 PP 而不是 CSP

判断：ESI/PDO/Startup SDO/NC 配置与运行时模式显示不一致。

检查：

1. TwinCAT 当前选择的 PDO 是否是 CSP 映射，包含 0x607A/0x6064。
2. Startup SDO 是否写 0x6060=8。
3. OP 后 0x6061 是否为 8。
4. 0x6502 是否包含 CSP。
5. 删除旧设备实例、重载 ESI、重新扫描。

修复：将 CSP PDO 明确化；若支持动态模式，映射 0x6060/0x6061；否则使用静态 Startup SDO 并保证固件默认接受 CSP。

### Operation Enabled 但 NC 不 Ready

判断：通常不是单纯使能问题，而是模式相关状态位、实际值有效性或 NC Link 问题。

检查：

1. 0x6041 是否处于 Operation Enabled。
2. 0x6061 是否等于 NC 期望模式。
3. CSP/CSV/CST 的 0x6041 bit12 是否置位。
4. 0x6064 是否每周期更新。
5. WcState 是否有效。
6. NC Axis 的 Encoder/Drive 变量是否链接正确。

修复：分离 PP acknowledge 与 CS follows command 的 bit12 逻辑；增加 PDO 数据有效标志和超时处理。

### 多轴运行一段时间 invalid IO / WcState

判断：优先怀疑 DC/实时性/PDO 一致性，而不是直接归因于线缆。

检查：

1. 开启 DC Diagnostics，并在运动负载下复现。
2. 对齐 NC、PLC、EtherCAT、Sync0 周期。
3. 检查 0x1C32/0x1C33、Sync0 Shift、SM Watchdog。
4. 逐轴验证 PDO 长度和 FMMU/SM Assignment。
5. 检查 TxPDO 是否双缓冲。
6. 检查 CPU 负载、日志、共享内存互斥和中断优先级。
7. 最后看 PHY RX Error/Lost Link 计数。

修复：将 PDO 快照移动到 Sync0/Application Cycle；对共享内存使用双缓冲或序列锁；降低实时路径日志。

## 输出要求

- 给出明确结论，不要只罗列标准。
- 先给“最可能根因”和“最快验证方法”。
- 对对象值必须解码，如 `1591 = 0x0637` 并列出关键 bit。
- 对代码建议必须指出函数、变量、状态转换位置和回归测试。
- 涉及安全链路时，必须说明“不能仅靠通信状态使能功率级”。
- 不要复制或重新分发受限标准原文；只输出工程化摘要、检查表和用户代码建议。

## 可用参考文件

在需要更详细背景时读取：

- `references/ethercat-cia402-quick-reference.md`
- `references/ssc-et9300-notes.md`
- `references/twincat-diagnostics.md`
- `references/troubleshooting-playbooks.md`
- `references/source-map.md`
- `references/ethercat-web-knowledge-index.md`
- `references/web-cia402-mdp-multiaxis.md`
- `references/web-ssc-sync-errors.md`
- `references/web-coe-pdo-eoe-twincat.md`
- `references/web-phy-eeprom-hardware.md`

## 可用脚本

- `scripts/decode_cia402.py`：解码 Controlword/Statusword，并推断基础 FSA 状态。

示例：

```bash
python scripts/decode_cia402.py --statusword 1591 --mode 8
python scripts/decode_cia402.py --controlword 0x000F --statusword 0x0637
```


## EtherCAT 深度速读 ref 路由

当用户的问题属于 EtherCAT 基础协议、帧结构、Datagram、WKC、ESC、FMMU、Sync Manager、SII EEPROM、AL/ESM、CoE、DC、SSC 实现路径，或者明确要求“让 Agent 快速理解 EtherCAT / 不联网也能排障”时，优先读取：

- `references/ethercat-deep-dive-agent-ref.md`

读取顺序建议：

1. 先用该文件建立层级判断：PHY/Link -> ESC/SII -> FMMU/SM -> AL/ESM -> CoE/SDO -> PDO/WKC -> DC/Sync -> CiA402/NC。
2. 再根据具体问题进入专门 ref：
   - CiA402/状态字/控制字/TwinCAT NC：`ethercat-cia402-quick-reference.md`、`twincat-diagnostics.md`。
   - SSC/ET9300 映射和同步：`ssc-et9300-notes.md`。
   - 网页工程知识按主题拆分：`web-cia402-mdp-multiaxis.md`、`web-ssc-sync-errors.md`、`web-coe-pdo-eoe-twincat.md`、`web-phy-eeprom-hardware.md`。
3. 不要把该 ref 当作正式规范逐字引用；它是 Agent 的工程心智模型和排障索引。涉及一致性认证、二进制编码、对象精确定义时回到 ETG/CiA 文档或项目源代码。

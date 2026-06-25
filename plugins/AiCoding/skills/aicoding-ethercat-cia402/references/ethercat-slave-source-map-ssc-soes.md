# EtherCAT 从站源码蒸馏：SSC / ET9300 / SOES

> 用途：让 Agent 快速理解 EtherCAT 从站固件如何由 ESC/PDI、Mailbox、CoE、PDO、ESM、应用层组成，并能定位从站扫描、SAFEOP/OP、PDO、DC、FoE OTA 的问题。
>
> 正确性核对：协议语义以 ETG.1000/ET9300 为准，开源实现以 SOES 官方仓库描述为参考。最后核对日期：2026-06-20。

## 1. 从站固件的四层模型

```text
硬件层
  PHY / ESC / PDI / EEPROM-SII / IRQ / Sync0-Sync1
协议栈层
  ESM / Mailbox / CoE / FoE / EoE / Process Data / Watchdog
对象层
  Object Dictionary / PDO Mapping / SM Assignment / Device Identity
应用层
  CiA402 轴状态机 / 电机控制接口 / 安全接口 / OTA / 诊断日志
```

从站开发中最常见的错误，是把“对象字典变量”“PDO 拷贝”“电机控制共享内存”“CiA402 状态机”混在一个上下文里。Agent 审查代码时必须分清：

| 层级 | 可修改内容 | 禁忌 |
|---|---|---|
| ESC/PDI | 寄存器读写、中断、SPI/HBI/并口访问 | 在 ISR 中做慢日志/SDO/FoE 写 Flash |
| Stack | ESM、Mailbox、CoE、FoE、PDO 调度 | 随意改标准状态机 |
| OD/PDO | 对象定义、映射、访问属性 | 手工改生成文件但不同步 ESI |
| Application | CiA402、电机控制接口、安全逻辑 | 多上下文无锁写同一对象 |

## 2. SSC / ET9300 阅读路线

ET9300/SSC 是工程上最重要的从站实现参考。Agent 应按文件角色而不是文件名死记，因为不同 SSC Tool 版本和厂商移植会改名。

### 文件角色

| 角色 | 常见内容 | 排障点 |
|---|---|---|
| Hardware/PDI access | ESC read/write、IRQ、timer、Sync0/Sync1 ISR | 扫描不到、Link OK 但无响应、中断未触发 |
| Stack core | ESM、AL control/status、Mailbox、CoE、FoE、EoE | PREOP/SAFEOP/OP 转换失败、SDO abort |
| Object dictionary | `0x1000`、`0x1018`、`0x1600/0x1A00`、应用对象 | ESI 与 OD 不一致、PDO 长度错 |
| Process data | `PDO_OutputMapping()`、`ECAT_Application()`、`PDO_InputMapping()` | OP 后 WKC/invalid IO、反馈不更新 |
| Application | CiA402、设备业务逻辑、电机/安全/OTA | 0x6061 不更新、0x6041 bit12 错、Fault 处理错 |

### 典型执行链

```text
主站写 SM2/RxPDO
  -> ESC 触发 SM event 或 Sync0
  -> 栈调用 OutputMapping，把 RxPDO 解包为对象/快照
  -> Application/CiA402 消费命令，更新状态机和目标量
  -> 电机控制或业务逻辑生成反馈
  -> InputMapping 把反馈打包到 TxPDO
  -> 主站读 SM3/TxPDO
```

如果 TwinCAT 报 `invalid IO data` 或 WKC 周期性异常，Agent 应优先检查：

1. `OutputMapping/InputMapping` 是否和 ESI 的 PDO 顺序、字节数、位宽完全一致。
2. `ECAT_Application` 是否在正确同步上下文执行。
3. Sync0/SM event 是否配置一致；不要 FreeRun 和 DC 模式混用逻辑。
4. 32/64 位反馈是否被中断/另一个核撕裂读取。
5. OP 后是否因 watchdog、DC、process data invalid 被栈降状态。

## 3. SOES 阅读路线

SOES 适合学习“轻量从站栈”而不是替代所有商用认证流程。它的价值在于源码直接、概念紧凑，适合 Agent 建立从站内部模型。

### SOES 重点能力

- ESC 访问抽象：可通过不同 PDI 接口读写 ESC。
- Mailbox + CoE：对象字典、SDO 读写、分段传输。
- PDO：固定/动态 PDO 映射。
- FoE：可作为 bootstrap/OTA 模板参考。
- 同步：SM synchronization、DC Sync0。
- 可运行于 polling、中断或混合模式。

### 适合蒸馏的模式

| 主题 | 从 SOES 学什么 | 不要误用 |
|---|---|---|
| 最小从站 | 初始化、ESM、Mailbox、PDO 基本链路 | 不要直接假设等同 SSC 生成工程 |
| ESC 读写 | 地址偏移 HAL、平台移植边界 | 不要把具体 ESC 驱动硬编码到通用 Skill |
| 动态 PDO | OD/PDO map 与应用结构关系 | 不要忽略 ESI 同步更新 |
| FoE | 升级文件传输状态机 | 不要在安全关键产品中直接套用未验证模板 |

## 4. 从站 Bring-up 检查表

### A. 扫描不到从站

```text
PHY Link -> ESC 电源/时钟/复位 -> PDI strap -> EEPROM/SII -> station alias -> 主站网卡
```

检查：

- Link LED、PHY 寄存器、ESC DL status。
- EEPROM/SII 是否有效；Vendor/Product/Revision 是否合理。
- PDI 类型与硬件 strap 是否一致。
- ESC IRQ/SYNC 引脚是否被误配置为普通 GPIO。
- TwinCAT 是否缓存旧 ESI。

### B. PREOP 失败

- Mailbox SM0/SM1 地址/长度。
- CoE 支持声明与实际对象字典。
- Startup SDO abort code。
- Identity object `0x1018` 与 ESI 是否一致。

### C. SAFEOP 失败

- RxPDO/TxPDO mapping 数量、顺序、位宽。
- SM2/SM3 assignment `0x1C12/0x1C13`。
- FMMU 长度和方向。
- Output/input process data size。

### D. OP 后失败

- Process data watchdog。
- Sync0/Sync1 中断是否准时。
- `PDO_OutputMapping` 与 `PDO_InputMapping` 是否越界。
- TxPDO invalid 标记、application ready 标记、AL error code。
- 多轴共享结构是否存在未对齐/半更新。

## 5. CiA402 从站代码审查重点

| 对象 | 从站责任 | 常见错误 |
|---|---|---|
| `0x6040` | 解析控制字边沿和状态转换请求 | Fault reset 当作电平长期执行 |
| `0x6041` | 输出 FSA 状态和模式相关位 | PP 的 bit12 逻辑误用于 CSP |
| `0x6060` | 接收请求模式 | 写入后未校验支持模式 |
| `0x6061` | 显示实际模式 | 初始化覆盖为 0，或未在 OP 更新 |
| `0x607A/0x60FF/0x6071` | 接收位置/速度/转矩目标 | 目标量在错误模式下仍被消费 |
| `0x6064/0x606C/0x6077` | 输出反馈 | 非同步更新导致 TwinCAT NC 读到撕裂值 |
| `0x603F` | 错误码 | Fault 已置位但无可读错误码 |

## 6. FoE / OTA 从站边界

FoE 只负责文件传输语义，不负责镜像安全性。Agent 处理 OTA 问题时必须追问或检查：

- 文件长度、目标分区、manifest、CRC/签名。
- A/B slot 与 bootloader 选择逻辑。
- 下载中断电恢复策略。
- BOOT->INIT 或 FoE 完成时写 Flash 的位置。
- 写 Flash 期间是否影响 EtherCAT watchdog/状态机。

## 7. 可维护蒸馏规则

- SSC/ET9300 相关 ref 只描述稳定结构和检查路径，不复制受限文档原文。
- SOES 相关 ref 只作为开源实现心智模型，不替代 ETG/SSC 认证要求。
- 每次更新从站代码生成工具或 ESI 模板后，必须同步检查 OD/PDO/ESI 三者一致性。

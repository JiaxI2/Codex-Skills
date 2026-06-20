# EtherCAT 网页参考：SSC 同步、中断和 0x1A/0x1B/0x2C 错误

## 读取触发

当用户提到以下任一内容时读取本文件：

- 运行中掉 OP、AL Status Code `0x1A`、`0x1B`、`0x2C`。
- `Sync0WdCounter`、`DC_CheckWatchdog()`、`CheckIfEcatError()`、`ECAT_CheckTimer()`。
- `AL_EVENT_ENABLED`、`DC_SUPPORTED`、`ECAT_TIMER_INT`、`ESC_SM_WD_SUPPORTED`。
- PDI 中断、Sync0/Sync1 中断、ResetOut、1 ms Timer、DC watchdog。
- 多轴实时性、Sync0 漏中断、SM Watchdog、WcState 周期性错误。

## 核心来源

1. `[EtherCAT]从站运行过程中报错(错误码：0x1A\0x1B\0x2C)的代码分析`
2. `[EtherCAT]一种竞争态引起从站报错0x2C的分析`
3. `[EtherCAT]SSC从站协议栈中的中断配置参数和中断优先级设置`
4. `[EtherCAT]从站产生PDI中断和Sync中断的逻辑`
5. `[EtherCAT]同步模式介绍与SSC Tool设置`

详见 `ethercat-web-knowledge-index.md`。

## 错误码含义与代码路径

| AL Status Code | 网页文章解释 | 优先代码路径 | 优先验证 |
|---|---|---|---|
| `0x1A` | Synchronization error，网络抖动或当前 DC 周期未收到有效 PDO 帧导致同步丢失 | `CheckIfEcatError()`、`bSmSyncSequenceValid`、DC 同步状态 | TwinCAT DC Diagnostics、Sync0 shift、主站帧到达与 Sync0 相位 |
| `0x1B` | SyncManager watchdog，周期性过程数据超出 watchdog 阈值未到达 | SM watchdog、SM2/SM3、PDO 通信 | SM Watchdog 设置、WcState、主站任务周期、PDO 是否持续下发 |
| `0x2C` | Fatal SYNC error，监控逻辑认为 ESC 未再收到 SYNC 硬件中断 | `DC_CheckWatchdog()`、`Sync0_Isr()`、`Sync0WdCounter` | Sync0 ISR 计数、1 ms Timer、竞态、关中断时间、NVIC 优先级 |

## SSC Tool 参数逻辑

| 参数 | 作用 | 建议 |
|---|---|---|
| `AL_EVENT_ENABLED` | 使能 PDI IRQ / AL event 处理路径 | 常规 SM/DC 同步建议为 1；只使用 Sync 中断处理 PDI 时才考虑 0 |
| `DC_SUPPORTED` | 使能 Sync0/Sync1 IRQ 处理路径 | 伺服/CiA402/DC 同步建议为 1 |
| `ECAT_TIMER_INT` | 在 1 ms Timer 中断中处理 EtherCAT watchdog 检查 | 通常建议为 1，但要处理 `Sync0WdCounter` 竞态和优先级 |
| `ESC_SM_WD_SUPPORTED` | 使用硬件 SyncManager watchdog | 实时 PDO 应开启并与主站周期匹配 |

## 中断优先级建议

网页文章引用 ETG 建议：

```text
PDI > SYNC0/SYNC1 > Timer
```

但实际项目要结合控制动作：

- 如果 PDI 与 Sync0 很接近，主站应通过 Sync0 Shift 避免二者重叠。
- 若主站帧抖动大，可能导致 `0x1A`。
- 若 Timer 中断抢占或关 ESC 中断时间过长，可能导致 PDI/Sync 响应延迟。
- `DISABLE_ESC_INT()` / `ENABLE_ESC_INT()` 不应包住耗时逻辑。

## 0x2C 竞态 Playbook

现象：设备已进入 OP，运行中偶发 `0x2C Fatal SYNC error`，但示波器/逻辑分析仪可见 Sync0 仍存在。

优先怀疑：软件 watchdog 计数器竞态，而不是硬件 Sync0 真丢失。

检查：

1. 是否存在 `Sync0WdCounter++` 与 `Sync0WdCounter = 0` 分别在不同上下文执行。
2. RV32 等平台上自增是否非原子读-改-写。
3. `DC_CheckWatchdog()` 是在 mainloop、1 ms Timer，还是其他中断中调用。
4. Sync0/Sync1 中断优先级是否能打断 Timer。
5. 是否有长时间关 ESC 中断或高优先级耗时 ISR。

修复方向：

- 对 `Sync0WdCounter` 更新做临界区或原子操作。
- 避免在 mainloop 中无保护地运行 watchdog 更新。
- 缩短关中断窗口。
- 记录 Sync0 ISR timestamp、Timer timestamp、counter 修改前后值，确认竞态。

## 同步模式选择

| 同步模式 | 触发 | 适用 |
|---|---|---|
| Free Run | 从站内部循环/事件 | 非实时或早期 bring-up，不推荐用于伺服闭环同步 |
| SM-Synchron | 收到过程数据帧产生 SyncManager/PDI 中断 | 简单 IO、对跨轴同步要求不高的场景 |
| DC-Synchron | 分布式时钟触发 Sync0/Sync1 | 多轴伺服、CSP/CSV/CST、对同步严格的场景 |

DC 同步必须检查：

- Sync0 Cycle 与 NC/PLC/EtherCAT Task 一致。
- Sync0 Shift 足够大，保证 Sync0 前收到主站数据。
- DC Diagnostics 无持续抖动/同步错误。
- 从站 `0x1C32/0x1C33` 与 ESI/TwinCAT 设置一致。

## PDI 与 Sync 中断逻辑

片上 ESC MCU 的 ESC 典型中断：

```text
PDI / ESC IRQ
Sync0 IRQ
Sync1 IRQ
ResetOut IRQ
1 ms Timer IRQ（MCU软件，用于 watchdog）
```

PDI 中断来源：

- `AL Event Request Register 0x220` 与 `AL Event Mask Register 0x204` 做与逻辑。
- bit0：AL Control 写入，请求 ESM 状态变化。
- bit2/bit3：DC Sync0/Sync1 事件可路由到 PDI。
- bit7~bit15：SyncManager0~7 中断。
- 默认 SSC 通常只使能 SM2 中断，即主站发 RxPDO 到从站时触发。

设计要求：

- 如果使用独立 Sync0/Sync1 IRQ，不希望 Sync 事件再触发 PDI，应正确配置 0x204 mask。
- PDI 通信任务与 Sync 控制任务要明确分工，不要在两个中断里重复搬运同一 PDO 缓冲。

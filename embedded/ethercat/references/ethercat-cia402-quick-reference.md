# EtherCAT/CiA402 快速参考

本文件是工程化速查，不替代官方标准、ETG 文档或厂商手册。用于帮助 Agent 快速定位 EtherCAT 伺服驱动问题。

## 分层诊断图

| 层级 | 主要检查项 | 常见症状 |
|---|---|---|
| PHY/Link | Link State、RX Error、Lost Link、线缆、屏蔽、拓扑 | 掉线、偶发 WC 错误 |
| ESC/DLL | FMMU、SM、Watchdog、PDI 时序 | Invalid IO data、SM Watchdog、过程数据长度错误 |
| AL/ESM | INIT/PREOP/SAFEOP/OP、AL Status Code | 无法进 OP、回退 SAFEOP |
| Mailbox/CoE | SDO、OD、Startup 参数、Emergency | SDO Abort、启动参数失败、模式默认值错误 |
| PDO/过程数据 | 0x1600/0x1A00、0x1C12/0x1C13、RxPDO/TxPDO 映射 | WC 错误、0x6064 不更新、字节偏移错误 |
| DC/同步 | Sync0/Sync1、0x1C32/0x1C33、主站周期 | 多轴抖动、运行一段时间 invalid IO |
| CiA402 | 0x6040、0x6041、0x6060、0x6061、0x6502 | NC 不 Ready、模式错误、状态位不匹配 |
| 运动应用 | Target/Actual、Enable、Fault、抱闸、限位、共享内存 | 不随动、使能故障、功率级异常 |

## CoE 对象组

| 对象 | 含义 |
|---|---|
| 0x1000 | Device Type |
| 0x1001 | Error Register |
| 0x1018 | Identity Object |
| 0x1600-0x17FF | RxPDO Mapping |
| 0x1A00-0x1BFF | TxPDO Mapping |
| 0x1C12 | Sync Manager 2 PDO Assignment，通常对应 RxPDO |
| 0x1C13 | Sync Manager 3 PDO Assignment，通常对应 TxPDO |
| 0x1C32 | SM2 同步/时序参数 |
| 0x1C33 | SM3 同步/时序参数 |
| 0x603F | Error Code |
| 0x6040 | Controlword |
| 0x6041 | Statusword |
| 0x6060 | Modes of operation，请求模式 |
| 0x6061 | Modes of operation display，实际模式 |
| 0x6064 | Position actual value |
| 0x607A | Target position |
| 0x60FF | Target velocity |
| 0x6071 | Target torque |
| 0x6077 | Torque actual value |
| 0x60F4 | Following error actual value |
| 0x6502 | Supported drive modes |

## CiA402 模式

| 模式 | 值 | 常见用途 |
|---|---:|---|
| Profile Position, PP | 1 | 驱动内部位置规划 |
| Velocity Mode, VL | 2 | 旧式速度模式 |
| Profile Velocity, PV | 3 | 速度规划 |
| Profile Torque, TQ | 4 | 转矩规划 |
| Homing, HM | 6 | 回零/找原点 |
| Interpolated Position, IP | 7 | 插补位置 |
| Cyclic Synchronous Position, CSP | 8 | 主站周期位置给定 |
| Cyclic Synchronous Velocity, CSV | 9 | 主站周期速度给定 |
| Cyclic Synchronous Torque, CST | 10 | 主站周期转矩给定 |

## 最小 PDO 建议

### CSP

RxPDO：

- 0x6040 Controlword
- 0x607A Target position
- 可选但常用：0x6060 Modes of operation、0x6072 Max torque

TxPDO：

- 0x6041 Statusword
- 0x6064 Position actual value
- 可选但常用：0x6061 Modes of operation display、0x60F4 Following error actual value

### CSV

RxPDO：

- 0x6040 Controlword
- 0x60FF Target velocity
- 可选：0x6060 Modes of operation

TxPDO：

- 0x6041 Statusword
- 0x6064 Position actual value
- 可选：0x606C Velocity actual value、0x6061 Modes display

### CST

RxPDO：

- 0x6040 Controlword
- 0x6071 Target torque
- 可选：0x6060 Modes of operation、0x6072 Max torque

TxPDO：

- 0x6041 Statusword
- 0x6077 Torque actual value
- 可选：0x6064 Position actual value、0x6061 Modes display

## 状态字重点

| Bit | 常见含义 | 备注 |
|---:|---|---|
| 0 | Ready to switch on | FSA 基础状态 |
| 1 | Switched on | FSA 基础状态 |
| 2 | Operation enabled | 伺服运行使能状态 |
| 3 | Fault | 故障 |
| 4 | Voltage enabled | 电压已使能 |
| 5 | Quick stop | 该位为 1 通常表示 Quick stop 未激活 |
| 6 | Switch on disabled | 禁止上电 |
| 7 | Warning | 警告 |
| 9 | Remote | 主站远程控制 |
| 10 | Mode specific | PP Target reached / HM 等模式相关 |
| 11 | Internal limit active | 内部限幅 |
| 12 | Mode specific | PP acknowledge；CS follows command |
| 13 | Mode specific | Following/Homing error 等 |

## 经验判断

- `0x6060=8` 只能说明请求 CSP，不能说明实际进入 CSP；必须看 `0x6061=8`。
- NC 轴不 Ready 时，先看 0x6041 bit12、0x6061、0x6064 是否更新，而不是先调 PID。
- 多轴运行一段时间后 WcState/invalid IO，优先查 DC、PDO 快照、SM Watchdog、共享内存一致性。
- 单轴正常不代表多轴实时路径正确；多轴会放大 PDO 长度、同步、CPU 负载、共享内存撕裂问题。

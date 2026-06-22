# EtherCAT 上位控制与诊断蒸馏：TwinCAT / LinuxCNC / ROS2

> 用途：让 Agent 快速区分 EtherCAT 协议问题、主站配置问题、运动控制框架问题和驱动 CiA402 问题。
>
> 正确性核对：TwinCAT/SSC 诊断以 ET9300/已有 TwinCAT 实测经验为主；LinuxCNC、hal-cia402、ROS2 EtherCAT driver、FCAT/fastcat 以官方仓库/文档为工程参考。最后核对日期：2026-06-20。

## 1. 三类上位控制器的本质差异

| 平台 | 主要角色 | 诊断入口 | 典型问题 |
|---|---|---|---|
| TwinCAT | 商用 EtherCAT 主站 + NC/PLC | EtherCAT device state、WcState、DC diag、NC axis | ESI/PDO/DC/NC Ready/Axis scaling |
| LinuxCNC | CNC 实时运动控制 + HAL | HAL pin、servo-thread、lcec、IgH state | read/write 顺序、HAL pin、servo period、PDO XML |
| ROS2 | 机器人软件框架 + ros2_control | lifecycle、hardware interface、command/state interface | mode switch、fault reset、周期线程、控制器接口 |

## 2. TwinCAT 诊断路径

### A. 从站状态

```text
INIT -> PREOP -> SAFEOP -> OP
```

| 卡点 | 优先检查 |
|---|---|
| INIT/PREOP | EEPROM/SII、ESI 缓存、Identity、Mailbox SM0/SM1 |
| PREOP/SAFEOP | Startup SDO、PDO mapping、SM assignment、FMMU |
| SAFEOP/OP | Process data watchdog、Output valid、DC/Sync0、应用 ready |
| OP 后掉回 | WKC、Lost frames、DC drift、Sync error、PHY 计数 |

### B. WcState / invalid IO data

优先级：

1. 设备是否 OP。
2. WKC actual 是否等于 expected。
3. 哪个变量报 invalid：Drive、Encoder、NC Axis、PLC link。
4. DC Diagnostics 是否有 Sync0/Sync1 error。
5. TxPDO 是否每周期更新；状态字/位置实际值是否撕裂。
6. 多轴下是否某一轴 PDO 长度或 offset 破坏后续轴。

### C. NC Axis Not Ready

```text
0x6041 FSA 状态
  -> 0x6061 是否等于目标模式
  -> bit12 是否按当前模式有效
  -> 0x6064 是否周期变化/有效
  -> Encoder scaling/Drive scaling/Link 是否正确
```

CSP 下不要把 `0x6041 bit12` 当作 PP 的 set-point acknowledge；它更接近“驱动正在跟随主站命令”。如果该位为 0，NC 可能不会让轴进入可运行状态。

## 3. LinuxCNC 诊断路径

LinuxCNC 的 EtherCAT 使用通常由 IgH 主站 + LinuxCNC HAL driver + CiA402 HAL 组件组成。核心顺序：

```text
lcec.read-all
  -> cia402.N.read-all
  -> motion / pid / kinematics
  -> cia402.N.write-all
  -> lcec.write-all
```

如果顺序错，可能出现：

- 控制字晚一拍或反馈晚一拍。
- motion 使用旧反馈。
- 驱动状态机永远进不到 Operation enabled。
- Homing/scaling 逻辑混乱。

### LinuxCNC 检查清单

| 检查项 | 含义 |
|---|---|
| `ethercat-conf.xml` | 从站、PDO、SDO、DC 配置是否正确 |
| HAL pins | controlword/statusword/actual position/target position 是否连接 |
| servo-thread | read/motion/write 顺序是否正确 |
| cia402 component | 是否负责状态转换、homing、scaling |
| IgH master state | master/slave/domain/wkc 是否正常 |

## 4. ROS2 / ros2_control 诊断路径

ROS2 EtherCAT 的常见结构：

```text
EtherCAT master
  -> EtherCAT driver
  -> hardware_interface
  -> ros2_control controller
  -> command/state interfaces
```

CiA402 插件通常负责：

- Drive state transition。
- Fault reset。
- 多周期模式：position(8)、velocity(9)、effort/torque(10)、homing(6)。
- 未控制时保持当前实际位置，避免模式切换或控制器未接管时突跳。

### ROS2 检查清单

| 现象 | 优先检查 |
|---|---|
| 硬件能 OP，控制器不动 | hardware interface 是否 export 正确 command/state interface |
| fault reset 无效 | reset_fault 是否上升沿，驱动错误源是否仍存在 |
| mode 切换突跳 | 未控制时目标是否保持 last position，NaN/默认值策略是否正确 |
| 控制器启动后抱闸释放异常 | 自动使能策略、Operation enabled、brake output、安全策略 |
| 多轴周期抖动 | ROS executor、实时线程、EtherCAT cycle、controller update rate |

## 5. 跨平台通用故障矩阵

| 问题 | TwinCAT | LinuxCNC | ROS2 | 从站侧共同检查 |
|---|---|---|---|---|
| 状态进不了 OP | AL status / Startup SDO | IgH slave state | driver log | ESI/OD/PDO/SM/FMMU |
| OP 后 WKC 错 | WcState / DC diag | domain state / wkc | master backend log | Sync0/SM watchdog/TxPDO 更新 |
| 轴不 Ready | NC axis / 6041/6061 | HAL pins / cia402 | state interface | CiA402 FSA/mode display/bit12 |
| 运动方向/比例错 | NC scaling | HAL scaling | URDF/YAML scaling | 6091/6092/608F/单位换算 |
| 回零异常 | NC homing config | cia402 homing pins | homing command interface | 6098/607C/6064 offset |

## 6. Agent 回答策略

1. 先问或推断使用平台：TwinCAT、LinuxCNC、ROS2、自研主站。
2. 对 TwinCAT：优先要截图/值：WcState、AL status、DC diag、NC Axis 状态、0x6041/0x6061。
3. 对 LinuxCNC：优先要 HAL 顺序、ethercat XML、HAL pin 值、servo period、IgH state。
4. 对 ROS2：优先要 YAML/URDF、hardware interface log、controller manager 状态、mode/fault reset interface。
5. 最后才进入电机控制算法。

## 7. 可维护蒸馏规则

- 平台文档变化快，保留“诊断思路”和“关键变量”，不要固化太多 UI 步骤。
- 每次新增平台支持，按同一模板补充：状态入口、周期顺序、配置文件、CiA402 对象、典型错误。

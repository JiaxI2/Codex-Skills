# 参考仓库矩阵：架构思想、主控/生态、可复刻能力

> 用途：当客户提供当前主控或项目类型时，判断是否可以借鉴某个参考仓库，并明确询问是否需要复刻对应能力。

## 1. moteus

- 仓库：https://github.com/mjbots/moteus
- 类型：高性能 brushless servo actuator，包含 firmware、PCB、client library、diagnostic tools。
- 主控/生态：moteus r4.11 README 标注 CPU 为 STM32G4；通信为 CAN-FD；控制率 15-30kHz、PWM switching rate 15-60kHz。
- 代码位置：
  - `fw/`：brushless controller firmware
  - `hw/`：硬件设计
  - `lib/`：client side software
  - `utils/`：diagnostic tools
  - `docs/`：文档
- 架构精华：
  - 固件、硬件、工具、文档一体化交付。
  - 面向高动态机器人执行器。
  - 伺服控制器自带绝对磁编码器、高速 CAN-FD 和诊断工具。
- 当前项目主控匹配时：
  - STM32G4 / CAN-FD / 一体化伺服 / 机器人关节驱动可优先参考。
  - 应询问客户是否需要复刻：CAN-FD register protocol、参数系统、诊断工具、控制周期组织、单驱动器一体化产品结构。
- 禁止：不确认功率级、编码器、采样电路和安全策略前直接复刻控制参数。

## 2. Open Dynamic Robot Initiative / open-motor-driver-initiative

- 仓库：https://github.com/open-dynamic-robot-initiative/open-motor-driver-initiative
- 类型：开源 brushless motor driver，面向腿足机器人研究。
- 主控/生态：README 明确为 TI TMS320F2838x MCU；用于 sensored FOC 控制 PMSM/BLDC；强调多 CPU、硬件加速器、SPI/FSI/EtherCAT/USART/CAN-FD/Ethernet/USB 等高速通信。
- 代码位置：
  - `firmware/`：电机驱动固件
  - `hardware/`：硬件
  - `doc/`：文档
  - `simulations/LTspice/`：仿真
- 架构精华：
  - 针对工业级伺服受限问题提供开放式控制设计。
  - 适合自定义控制律、自定义通信总线和传感器集成。
  - 同一系统架构支持不同轴数、功率范围和形态。
- 当前项目主控匹配时：
  - TI F2838x / EtherCAT / 多轴机器人 / 自定义高带宽通信场景应优先参考。
  - 应询问客户是否需要复刻：F2838x 多核分工、EtherCAT/CAN-FD/FSI 通信、sensored FOC、多轴驱动板架构、机器人执行器接口。
- 禁止：只因为用了 TI C2000 就默认引入完整 ODRI 架构；必须确认轴数、功率、电流采样、编码器和通信需求。

## 3. PX4

- 仓库：https://github.com/PX4/PX4-Autopilot
- 类型：无人机/无人系统开源 autopilot stack。
- 主控/生态：支持 NuttX、Linux、macOS；常见 Pixhawk/NuttX 目标板。
- 代码位置：
  - `src/modules/`：飞控模块
  - `src/drivers/`：设备驱动
  - `boards/`：目标板配置
  - `ROMFS/`：系统启动/配置资源
  - `msg/`：uORB 消息
- 架构精华：
  - 模块化任务、消息总线、参数、日志、目标板适配、SITL/HITL。
  - 适合作为复杂嵌入式系统的模块调度和发布流程参考。
- 当前项目主控匹配时：
  - Pixhawk / NuttX / STM32H7/F7 / Linux 边缘控制器可参考。
  - 应询问客户是否需要复刻：modules/drivers/boards 分层、参数系统、日志系统、消息总线、仿真/回放测试。
- 禁止：把 PX4 的飞控模块命名直接套到电机伺服项目。

## 4. ArduPilot

- 仓库：https://github.com/ardupilot/ardupilot
- 类型：多机型 autopilot 系统。
- 主控/生态：支持多种嵌入式硬件和 Linux；工程中常见 AP_HAL、vehicle、library、board abstraction 思路。
- 代码位置：
  - `libraries/`：AP_HAL、传感器、控制、日志、协议等库
  - `ArduCopter/`、`ArduPlane/`、`Rover/`、`ArduSub/`：机型应用
  - `Tools/`：构建、测试、仿真工具
- 架构精华：
  - vehicle abstraction、参数系统、日志、硬件抽象层、长期工程维护。
  - 适合参考跨平台、跨机型的业务架构。
- 当前项目主控匹配时：
  - 复杂机器人/飞控/多平台产品可参考。
  - 应询问客户是否需要复刻：参数系统、日志回放、硬件抽象层、机型/产品线分离。

## 5. Betaflight

- 仓库：https://github.com/betaflight/betaflight
- 类型：高性能 FPV flight controller firmware。
- 主控/生态：README 说明支持 STM32 F4、G4、F7、H7 targets；支持 DShot、Blackbox、目标板配置。
- 代码位置：
  - `src/main/`：主固件
  - `src/main/target/`：目标板配置
  - `src/main/drivers/`：驱动
  - `src/main/flight/`：飞行控制
  - `src/main/blackbox/`：黑匣子日志
- 架构精华：
  - 多目标板维护、feature flag、blackbox、强实时姿态控制链路。
  - 适合参考高频控制任务、日志和目标板适配。
- 当前项目主控匹配时：
  - STM32 F4/G4/F7/H7 强实时控制产品可参考。
  - 应询问客户是否需要复刻：target 配置体系、blackbox、CLI 参数、DShot/高速输出、目标板裁剪机制。

## 6. TI Motor Control SDK / C2000Ware MotorControl SDK

- 仓库/入口：
  - https://github.com/TexasInstruments/motor-control-sdk
  - https://www.ti.com/tool/C2000WARE-MOTORCONTROL-SDK
- 类型：TI 官方电机控制 SDK。
- 主控/生态：
  - C2000Ware MotorControl SDK：C2000 MCU，工业驱动、机器人、家电、汽车三相电机控制。
  - TI motor-control-sdk：ARM R5F CPU、PRU-ICSS、位置/电流 sense、实时控制库、Industrial Communications SDK。
- 架构精华：
  - 厂商级驱动、控制库、DCL、SFRA、Datalog、SysConfig/MCU+ SDK、工业通信组合。
  - 适合做 TI 平台的基准实现和发布依据。
- 当前项目主控匹配时：
  - TI C2000 / AM243x / AM263x 必须优先检索对应 SDK 示例。
  - 应询问客户是否需要复刻：DCL 控制器、SFRA、Datalog、PRU-ICSS 实时链路、Industrial Communications SDK、EtherCAT-connected dual-servo reference。

## 7. 其他已纳入长期参考

- Dummy-Robot：https://github.com/peng-zhihui/Dummy-Robot
  - 参考 UserApp、Robot 业务层、机械臂命令、多轴同步、参数保存。
- ODrive：https://github.com/odriverobotics/ODrive
  - 参考 Axis / Motor / Encoder / Controller / FOC / Oscilloscope 边界。
- VESC/BLDC：https://github.com/vedderb/bldc
  - 参考 `motor/mcpwm_foc.c`、`motor/foc_math.c`、`hwconf/`、`applications/`。

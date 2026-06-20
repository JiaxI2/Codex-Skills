# 电机控制参考仓库矩阵

## 1. VESC / BLDC

- 仓库：https://github.com/vedderb/bldc
- 类型：高成熟度 BLDC/PMSM 控制固件。
- 主控/生态：典型 STM32 + ChibiOS + 多硬件配置。
- 代码位置：
  - `motor/mcpwm_foc.c`：FOC 主控制、电流环、补偿、ADC/PWM 时序。
  - `motor/foc_math.c`：FOC 数学、SVPWM。
  - `motor/mc_interface.c`：电机控制接口。
  - `hwconf/`：硬件配置。
- 精华：FOC、SVPWM、ADC/PWM 同步、BEMF/dq 补偿、PID、保护、调试变量。
- 使用方式：吸收算法和时序思想，不照搬全局宏和硬件绑定。

## 2. ODrive

- 仓库：https://github.com/odriverobotics/ODrive
- 类型：开源多轴伺服控制器。
- 主控/生态：STM32 系列历史实现；C++ 对象化。
- 代码位置：
  - `Firmware/MotorControl/axis.cpp`
  - `Firmware/MotorControl/motor.cpp`
  - `Firmware/MotorControl/controller.cpp`
  - `Firmware/MotorControl/encoder.cpp`
  - `Firmware/MotorControl/foc.cpp`
  - `Firmware/MotorControl/oscilloscope.cpp`
- 精华：Axis/Motor/Encoder/Controller/FOC/Oscilloscope 边界，多轴对象模型，诊断和示波器。
- 使用方式：吸收对象边界，不强制照搬 C++ 组件图。

## 3. moteus

- 仓库：https://github.com/mjbots/moteus
- 主控/生态：moteus r4.11 README 标注 CPU 为 STM32G4，CAN-FD，控制率 15-30kHz，PWM switching 15-60kHz。
- 代码位置：
  - `fw/`：brushless controller firmware
  - `lib/`：client side software
  - `utils/`：diagnostics
  - `docs/`：文档
- 精华：高动态机器人执行器，一体化伺服、磁编码器、CAN-FD、参数和诊断工具。
- 主控匹配时询问客户是否需要复刻：
  - CAN-FD register protocol
  - 参数/诊断命令
  - 高动态伺服控制周期组织
  - 编码器 offset/校准思想

## 4. Open Dynamic Robot Initiative / open-motor-driver-initiative

- 仓库：https://github.com/open-dynamic-robot-initiative/open-motor-driver-initiative
- 主控/生态：TI TMS320F2838x；sensored FOC for PMSM/BLDC；面向腿足机器人。
- 代码位置：
  - `firmware/`
  - `hardware/`
  - `doc/`
  - `simulations/LTspice/`
- 精华：F2838x 多核/外设资源、开放工业级伺服、custom control、custom communication、sensor integration。
- 主控匹配时询问客户是否需要复刻：
  - F2838x 多核/CLA/高速外设架构
  - EtherCAT/CAN-FD/FSI 通信思路
  - 多轴驱动板设计
  - sensored FOC 控制链路

## 5. TI SDK

- 仓库/入口：
  - https://github.com/TexasInstruments/motor-control-sdk
  - https://www.ti.com/tool/C2000WARE-MOTORCONTROL-SDK
- 主控/生态：C2000 MCU；AM243x/AM263x ARM R5F + PRU-ICSS。
- 精华：
  - DCL 控制器
  - Datalog
  - SFRA
  - Transformation algorithms
  - Observer algorithms
  - SDFM/ADC/position sense
  - PRU-ICSS 实时通信与采样
- 主控匹配时询问客户是否需要复刻：
  - 官方 lab 框架
  - DCL/SFRA/Datalog
  - PRU-ICSS current/position sense
  - EtherCAT-connected dual-servo reference

## 6. Betaflight

- 仓库：https://github.com/betaflight/betaflight
- 主控/生态：STM32 F4/G4/F7/H7 target。
- 代码位置：
  - `src/main/target/`
  - `src/main/drivers/`
  - `src/main/flight/`
  - `src/main/blackbox/`
- 精华：高频控制、blackbox、目标板适配、DShot 输出、CLI 参数。
- 使用方式：参考日志、目标板裁剪、强实时调试，不当作 PMSM FOC 模板。

## 7. PX4 / ArduPilot

- PX4：https://github.com/PX4/PX4-Autopilot
- ArduPilot：https://github.com/ardupilot/ardupilot
- 精华：控制模块、参数、日志、仿真、硬件抽象、长期工程化。
- 使用方式：参考系统级 App/任务调度/日志参数，不作为底层电流环模板。

## 8. Dummy-Robot

- 仓库：https://github.com/peng-zhihui/Dummy-Robot
- 精华：机械臂 App、多轴命令、shadow target、同步触发、参数保存。
- 使用方式：参考 App 层和多轴动作协调，不作为 PMSM FOC 电流环模板。

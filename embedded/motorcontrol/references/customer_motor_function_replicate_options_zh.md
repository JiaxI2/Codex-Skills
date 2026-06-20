# 客户功能复刻方案速查：电机控制 App 与算法方向

> 用途：当客户项目涉及 PMSM/BLDC/伺服/机器人关节/机械臂/机器狗/飞控 ESC/多轴驱动时，Agent 应用本文快速说明参考仓库的核心电机控制功能、大概做法、优劣势和复刻边界，方便客户选择方案。

## 0. 使用规则

1. 先判断目标：**力矩伺服、速度驱动、位置伺服、机器人关节、飞控电调、多轴机械臂、工业伺服**。
2. 再判断主控：STM32G4、STM32F4/F7/H7、TI F2838x、TI AM243x/AM263x、Pixhawk/NuttX、FPGA/SoC。
3. 最后输出可选复刻项：采样时序、FOC/SVPWM、三环控制、前馈补偿、日志/Trace、参数/调试协议、多轴同步、保护状态机。
4. 不允许默认复制开源代码；必须区分“思想复用、接口复刻、代码参考、禁止照搬”。

---

## 1. VESC / BLDC：FOC、SVPWM、补偿、保护和调试最强参考

**适用场景**：PMSM/BLDC 驱动器、FOC 电流环、SVPWM、参数调试、工具链、复杂保护。

**核心技术/功能**：

- 中心对齐 PWM 下的 ADC 采样时序设计。
- FOC：Clarke/Park、Id/Iq PI、解耦补偿、BEMF 前馈、逆 Park、SVPWM。
- SVPWM 独立数学实现，可作为算法平台化参考。
- 速度/位置控制、HFI、观测器、弱磁、保护、温度/电压/电流限制。
- `mc_interface` 统一电机控制接口。
- 调参、运行状态、命令接口和工具链生态。

**大概做法**：

```text
PWM 定时器产生同步采样点
    -> ADC/DMA 获取相电流和母线电压
    -> offset 修正 + 电角度
    -> FOC 电流环
    -> dq 补偿 / BEMF / Vbus 限幅
    -> SVPWM duty
    -> PWM shadow 更新
    -> 状态/故障/调试变量输出
```

**适合复刻**：

- FOC/SVPWM 算法流程。
- ADC/PWM 同步采样思想。
- Id/Iq PI 的 anti-windup、输出限幅、Vbus 限幅。
- 补偿策略：BEMF、dq 交叉耦合、弱磁、死区/摩擦/offset。
- 调试变量和故障保护分层。

**优势**：

- 控制细节丰富，接近真实产品复杂度。
- 适合补强电流环、补偿、保护和调试。
- 覆盖多硬件配置和工具链。

**劣势/风险**：

- GPLv3；商业项目通常只建议吸收思想，不复制代码。
- 宏、全局状态、硬件条件编译较多。
- 代码复杂，直接移植成本高。

**参考入口**：

```text
https://github.com/vedderb/bldc
motor/mcpwm_foc.c          # FOC 主控制、ADC/PWM/补偿/保护
motor/foc_math.c           # SVPWM、数学变换、FOC 辅助函数
motor/mc_interface.c       # 电机控制统一接口
motor/mcpwm.c              # 传统 PWM/电机控制
hwconf/                    # 硬件配置
commands.c                 # 命令和调试接口
```

**客户确认问题**：

```text
是否需要参考 VESC 的 FOC/SVPWM 细节？
是否需要类似 VESC Tool 的参数调试和运行监控？
是否接受只复刻算法思想，不复制 GPLv3 代码？
```

---

## 2. ODrive：Axis/Controller/Encoder/Motor/FOC 边界和伺服控制流程

**适用场景**：多轴伺服、机器人关节、位置/速度/电流控制、轨迹发生器、诊断。

**核心技术/功能**：

- `Axis` 作为独立控制对象，包含状态机、校准、故障和组件。
- `Controller` 负责位置/速度/电流指令和轨迹控制。
- `Encoder` 负责位置反馈、估算、校准。
- `Motor / FOC` 负责电流环和相电压/PWM 控制。
- `TrapTrajectory` 用于梯形轨迹。
- `Oscilloscope` 和错误码用于诊断。

**大概做法**：

```text
Axis 状态机
    -> 校准/闭环控制/故障处理
    -> Controller 生成 Iq/torque/velocity target
    -> Encoder/Estimator 提供反馈
    -> Motor/FOC 执行电流控制
    -> PWM impl 更新输出
    -> Oscilloscope/diagnostics 观测
```

**适合复刻**：

- `axis_ctx` 多轴对象边界。
- Controller / Encoder / Motor / FOC 职责划分。
- 梯形轨迹和伺服状态机。
- 诊断/示波器/错误码。

**优势**：

- 对多轴伺服非常直观。
- 组件边界比 VESC 更清晰。
- 适合作为 C99 项目重构时的对象模型参考。

**劣势/风险**：

- C++ 对象模型不一定适合安全 C 项目直接复制。
- 公开仓库主要是 ODrive v3.x，最新产品源码不完全公开。
- 硬件和 STM32 定时器实现仍需隔离。

**参考入口**：

```text
https://github.com/odriverobotics/ODrive
Firmware/MotorControl/axis.cpp
Firmware/MotorControl/controller.cpp
Firmware/MotorControl/encoder.cpp
Firmware/MotorControl/foc.cpp
Firmware/MotorControl/motor.cpp
Firmware/MotorControl/trapTraj.cpp
Firmware/MotorControl/oscilloscope.cpp
Firmware/MotorControl/current_limiter.hpp
```

**客户确认问题**：

```text
是否需要复刻 Axis 状态机和多轴对象模型？
是否需要轨迹发生器、编码器校准、示波器诊断？
是否采用 C++ 对象，还是用 C99 struct + function 复刻行为？
```

---

## 3. moteus：机器人关节伺服、CAN-FD 和高控制率产品化参考

**适用场景**：机器人关节、机器狗、机械臂、小型高动态伺服执行器。

**主控/特征**：STM32G4、CAN-FD、高控制率、高 PWM switching、固件/硬件/工具一体化。

**核心技术/功能**：

- 一体化 brushless servo controller。
- CAN-FD register/diagnostic 通信。
- 参数、诊断、标定和工具链。
- 面向机器人关节的高动态控制。

**大概做法**：

```text
机器人上位机/主控
    -> CAN-FD command/register
    -> moteus 关节伺服
    -> 本地高频电流/位置/速度控制
    -> 状态反馈/诊断/参数配置
```

**适合复刻**：

- CAN-FD 参数/诊断协议风格。
- 机器人关节伺服产品化形态。
- 固件、硬件、工具统一交付方式。
- 高控制率下的执行器接口设计。

**优势**：

- 与机器人关节高度匹配。
- 主控和性能指标明确，便于客户选型。
- 适合作为“高端开源关节伺服”对标。

**劣势/风险**：

- 硬件强相关，不能直接套到不同功率板。
- 默认不是 EtherCAT/CiA402 工业伺服。
- 安全、OTA、量产升级需要另行补足。

**参考入口**：

```text
https://github.com/mjbots/moteus
fw/
hw/
lib/
utils/
README.md
```

**客户确认问题**：

```text
是否目标是机器人关节伺服，而不是通用变频器/工业驱动？
是否使用 STM32G4 或相近 MCU？
是否需要 CAN-FD register/diagnostic 协议？
```

---

## 4. Open Dynamic Robot Initiative / open-motor-driver：TI F2838x 扭矩控制机器人执行器

**适用场景**：机器狗、腿足机器人、低减速比关节、力矩控制机械臂、TI C2000 工业伺服。

**主控/特征**：open-motor-driver-initiative 基于 TI TMS320F2838x，面向 PMSM/BLDC 有感 FOC。

**核心技术/功能**：

- torque-controlled robot actuator。
- PMSM/BLDC sensored FOC。
- 执行器硬件、机械、编码器、电机、驱动和机器人系统协同设计。
- 适合低成本、低复杂度、可复现动态机器人。

**大概做法**：

```text
机器人控制器
    -> torque/current command
    -> TI F2838x motor driver
    -> sensored FOC
    -> actuator mechanics
    -> joint torque/position feedback
```

**适合复刻**：

- TI C2000/F2838x 电机控制链路。
- 力矩控制 actuator 模块思想。
- 机器人关节硬件/软件/机械协同设计流程。
- 对 EtherCAT/CiA402 多轴伺服项目的 DSP 侧参考。

**优势**：

- 与高端机器人和 TI C2000 强相关。
- 比一般 STM32 FOC demo 更接近工业/机器人伺服。
- 执行器系统思路完整。

**劣势/风险**：

- 复刻范围大，涉及机械、电机、编码器、功率板、主控。
- 仓库和资料较分散。
- 不是拿来即用的产品固件。

**参考入口**：

```text
https://github.com/open-dynamic-robot-initiative/open-motor-driver-initiative
https://github.com/open-dynamic-robot-initiative/open_robot_actuator_hardware
https://open-dynamic-robot-initiative.github.io/
```

**客户确认问题**：

```text
是否使用 TI F2838x / C2000？
是否目标为力矩控制机器人执行器？
是否要复刻 actuator module，而不是只复刻 FOC 算法？
```

---

## 5. TI Motor Control SDK / C2000Ware：官方电机控制和工业通信基准

**适用场景**：TI C2000、F2838x、AM243x、AM263x、工业伺服、多轴驱动、EtherCAT/工业通信集成。

**核心技术/功能**：

- C2000Ware MotorControl SDK：高性能电机控制资源、Universal Project & Lab、DriverLib/SysConfig/CCS。
- TI motor-control-sdk：ARM R5F、PRU-ICSS、实时位置/电流 sense、实时控制库、工业通信 SDK 集成。
- 官方示例、工具链、文档和评估板支持。

**大概做法**：

```text
TI SDK/SysConfig
    -> ePWM/ADC/CLA 或 R5F/PRU 实时路径
    -> FOC / current sense / position sense
    -> Industrial communication
    -> lab validation / CCS debug
```

**适合复刻**：

- TI 官方 ePWM/ADC/CLA/R5F/PRU 实时链路。
- SysConfig/CCS 工程生成和配置方式。
- 工业通信 + 电机控制结合方式。
- 多轴电机控制官方基线。

**优势**：

- 厂商官方方案，客户接受度高。
- 对 TI 平台开发效率高。
- 适合建立量产基线或客户评审基线。

**劣势/风险**：

- 与 TI 工具链和 SDK 强绑定。
- 迁移到非 TI 平台成本高。
- 官方 demo 仍需补足产品级 OTA、参数区、安全、故障状态机。

**参考入口**：

```text
https://www.ti.com/tool/C2000WARE-MOTORCONTROL-SDK
https://github.com/TexasInstruments/motor-control-sdk
https://software-dl.ti.com/processor-industrial-sw/esd/motor_control_sdk/am243x/docs/api_guide_am243x/index.html
```

**客户确认问题**：

```text
是否以 TI SDK 作为官方基线？
是否需要复刻 ePWM/ADC/CLA 或 R5F/PRU 实时链路？
是否需要工业通信 SDK 一体化？
```

---

## 6. Betaflight：飞控强实时、Blackbox 和电调协议链路

**适用场景**：飞控、电调协议、姿态控制、高频 PID、黑匣子日志、目标板适配。

**核心技术/功能**：

- 高频飞控任务与 PID 调参。
- DShot / Multishot / Oneshot / Proshot 等电调协议。
- Blackbox 日志用于飞行性能调试。
- target/board 配置支持大量 STM32 F4/G4/F7/H7 飞控板。

**大概做法**：

```text
IMU/Sensor drivers
    -> filtering
    -> flight PID loop
    -> mixer
    -> DShot/motor output
    -> Blackbox logging
```

**适合复刻**：

- Blackbox 类调试记录。
- 高频控制循环观测和调参。
- DShot/电调协议输出。
- 多目标板 target 管理。

**优势**：

- 强实时调试和日志体系成熟。
- 多目标板维护经验丰富。
- 对高频控制和噪声滤波有参考价值。

**劣势/风险**：

- 不是 PMSM FOC 伺服模板。
- 面向飞控姿态控制，不等同于工业驱动器。
- 仅适合借鉴调试、协议、目标板和控制循环组织。

**参考入口**：

```text
https://github.com/betaflight/betaflight
src/main/flight/
src/main/blackbox/
src/main/drivers/
src/main/target/
src/main/io/
```

**客户确认问题**：

```text
是否需要 Blackbox 形式的高频日志？
是否需要 DShot 或飞控 ESC 输出协议？
是否需要多目标板维护机制？
```

---

## 7. PX4 / ArduPilot：高层控制、参数、日志、仿真，不作为 FOC 代码模板

**适用场景**：无人机、机器人系统级控制、参数/日志/调度/仿真/硬件在环。

**核心技术/功能**：

- PX4：uORB、modules、drivers、boards、parameters、logger、SITL/HITL。
- ArduPilot：AP_HAL、AP_Param、AP_Logger、vehicle abstraction、scheduler。
- 对电机控制 Skill 的价值主要是：参数、日志、调试、回放、任务调度和系统级安全状态。

**大概做法**：

```text
Sensor/Driver
    -> middleware/topic 或 HAL
    -> controller modules
    -> parameters/logger
    -> actuator output
    -> SITL/HITL 回归
```

**适合复刻**：

- 参数系统。
- 日志/回放/SITL/HITL。
- 多目标板和驱动模型。
- 控制器调参与安全状态机。

**优势**：

- 系统工程成熟，验证工具链完整。
- 适合客户需要“可维护、可诊断、可回归”的复杂产品。

**劣势/风险**：

- 不直接提供 PMSM FOC 电流环模板。
- 对小型 MCU 可能过重。
- 飞控业务模型需要大幅裁剪。

**参考入口**：

```text
https://github.com/PX4/PX4-Autopilot
src/modules/
src/drivers/
boards/
msg/
Tools/

https://github.com/ardupilot/ardupilot
libraries/AP_HAL/
libraries/AP_Param/
libraries/AP_Logger/
libraries/AP_Scheduler/
ArduCopter/
ArduPlane/
```

**客户确认问题**：

```text
是否需要日志、参数、仿真回归能力？
是否需要借鉴飞控控制链路，而不是 FOC 底层代码？
是否需要把电机驱动器接入更大的机器人/飞控系统？
```

---

## 8. 推荐组合

### 机器人关节伺服

```text
moteus + ODrive + ODRI
    moteus：产品化关节伺服形态
    ODrive：Axis/Controller/Encoder/Motor/FOC 边界
    ODRI：力矩控制机器人执行器系统
```

### 工业伺服 / TI 平台

```text
TI SDK + ODRI + ODrive
    TI SDK：官方 ePWM/ADC/CLA/R5F/PRU 基线
    ODRI：F2838x 机器人执行器参考
    ODrive：多轴对象和控制器边界
```

### 强实时 FOC / 电机算法

```text
VESC + TI SDK + ODrive
    VESC：FOC/SVPWM/补偿/保护细节
    TI SDK：厂商实时链路
    ODrive：控制对象边界
```

### 飞控/ESC/高频日志

```text
Betaflight + PX4 + ArduPilot
    Betaflight：Blackbox、DShot、高频控制
    PX4：uORB、模块、SITL/HITL
    ArduPilot：AP_HAL、参数、日志、长期维护
```

---

## 9. 客户选择模板

```text
根据当前主控和目标产品，建议参考：
1. <仓库A>：复刻 <功能/接口/行为>，不复制 <硬件绑定代码/许可证风险代码>。
2. <仓库B>：复刻 <功能/接口/行为>，不复制 <复杂框架/飞控业务模型>。

请确认：
A. 只吸收思想。
B. 复刻接口和行为，重新实现代码。
C. 参考开源代码实现，先做许可证和安全风险评估。
D. 不使用该参考方案。
```

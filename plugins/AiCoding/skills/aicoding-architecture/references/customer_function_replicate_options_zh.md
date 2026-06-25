# 客户功能复刻方案速查：嵌入式架构方向

> 用途：当客户的主控、产品形态或业务目标与参考仓库接近时，Agent 应先用本文快速说明参考仓库的核心技术、功能、大概做法、优劣势和适合复刻的边界，然后提交给客户选择。不得默认照搬。

## 0. 使用规则

1. **先匹配主控/生态**：STM32G4、TI C2000 F2838x、TI AM243x/AM263x、Pixhawk/NuttX、STM32 F4/G4/F7/H7 飞控板、机器人关节伺服、多轴机械臂等。
2. **再匹配功能诉求**：参数系统、日志系统、通信协议、升级方式、多轴同步、故障保护、硬件目标板管理、仿真/回放、量产发布。
3. **最后询问客户是否复刻**：只能复刻思想、接口和行为；是否参考代码实现要另行评估许可证、质量、安全和维护成本。
4. **输出必须区分**：
   - 可直接借鉴的架构思想；
   - 可重新实现的功能行为；
   - 不建议照搬的代码/目录/宏/全局状态；
   - 需要客户确认的范围。

---

## 1. Dummy-Robot：机械臂 App、多轴命令与同步思想

**主控/生态**：STM32 系列 + 下位机电机驱动 + CAN/UART + 上位机/机器人系统。

**核心技术/功能**：

- `UserApp` 与机器人核心库分离，便于二次开发。
- CAN / UART 协议用于主控与电机驱动通信。
- 多轴运动命令：如关节运动、轨迹模式、调参模式。
- 多轴同步：先下发各轴目标到影子区，再通过同步命令统一开始执行。
- 参数保存：使用模拟 EEPROM 或非易失存储保存参数。

**大概做法**：

```text
上位机/主控 App
    -> 轨迹/多轴命令生成
    -> 每轴目标写入驱动器 shadow command
    -> 广播同步触发
    -> 轴驱动器按本地闭环执行
```

**适合复刻的能力**：

- 机械臂/机器人 App 层命令模型。
- 多轴 shadow target + sync apply。
- 用户可扩展应用层。
- 参数读写和默认参数恢复。

**优势**：

- 对客户容易解释，系统级结构完整。
- 多轴同步思想清晰，适合机械臂和机器人。
- App 与底层驱动有基本解耦。

**劣势/风险**：

- 不是 PMSM/BLDC FOC 底层强实时参考。
- 电机驱动偏闭环步进/专用驱动，不适合作为三相电流环模板。
- 工业量产升级、签名、A/B、回滚链路不足。

**参考入口**：

```text
https://github.com/peng-zhihui/Dummy-Robot
README.md
2.Firmware/
2.Firmware/*/UserApp/
```

**客户确认问题**：

```text
是否需要复刻 Dummy-Robot 的多轴 shadow 同步命令？
是否需要复刻 UserApp 形式的客户二次开发入口？
是否需要复刻 CAN/UART 命令模式，还是改成 EtherCAT/CANopen/自定义协议？
```

---

## 2. ODrive：Axis 对象、控制组件边界和诊断模型

**主控/生态**：ODrive v3.x 主要是 STM32F4 生态；新一代产品源码不完全公开，旧仓库仍适合参考对象边界。

**核心技术/功能**：

- `Axis` 作为控制单元，包含状态机、校准、控制器、电机、编码器、故障。
- `Controller / Encoder / Motor / FOC / CurrentLimiter / TrapTrajectory / Oscilloscope` 等真实变化点清楚。
- 控制链路把采样、控制更新、PWM 更新分阶段。
- 支持轨迹控制、编码器校准、电流/速度/位置控制、诊断观测。

**大概做法**：

```text
Axis 状态机
    -> Controller 生成目标
    -> Encoder / Estimator 提供反馈
    -> Motor / FOC 执行转矩/电流控制
    -> PWM Impl 更新硬件
    -> Oscilloscope / error flags 做诊断
```

**适合复刻的能力**：

- `axis_ctx` 或 `Axis` 对象边界。
- 控制器、编码器、电机、FOC 的职责拆分。
- 轨迹发生器和控制器解耦。
- 诊断/示波器数据抽样。

**优势**：

- 多轴伺服对象模型清楚。
- 适合中高端伺服、机器人关节、电机驱动器。
- 便于把电机控制 Skill 与嵌入式架构 Skill 连接起来。

**劣势/风险**：

- C++ 对象化较重，不能直接照搬到 C99/安全项目。
- 部分实现与 STM32 定时器、PWM、板级硬件绑定。
- ODrive 公开仓库主要面向 v3.x，最新商业产品源码不完全公开。

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
是否需要复刻 ODrive 的 Axis 状态机？
是否需要复刻 Controller / Encoder / Motor / FOC 这种组件边界？
是否需要示波器/Trace/错误码诊断能力？
```

---

## 3. VESC / BLDC：强实时电机控制和硬件配置分离

**主控/生态**：以 STM32 电机控制器生态为主，包含多硬件配置和 VESC Tool 生态。

**核心技术/功能**：

- FOC、BLDC、DC 电机控制固件。
- 电流环、SVPWM、采样时序、补偿、保护、调参、通信和工具链。
- `hwconf` 管理不同硬件配置。
- `motor` 目录集中电机控制实现。
- 固件 metadata、flash helper、package 脚本可作为发布/升级工程参考。

**大概做法**：

```text
硬件配置 hwconf
    -> ADC/PWM/Timer/DMA 配置
    -> FOC/SVPWM 电流环
    -> mc_interface 统一电机接口
    -> commands / app 层协议和调参
    -> VESC Tool / 日志 / 参数
```

**适合复刻的能力**：

- FOC/SVPWM 的算法组织。
- PWM/ADC 同步采样的强实时链路。
- 硬件配置与电机控制主逻辑分离。
- 调试变量、运行状态、故障保护和参数系统。
- 固件 metadata / 打包 / flash helper 的工程化思路。

**优势**：

- 电机控制细节成熟，覆盖面广。
- 调参、保护、补偿、工具链思路丰富。
- 适合补强电机控制 Skill 的算法细节。

**劣势/风险**：

- GPLv3 许可证对商业闭源项目有重大约束。
- 宏、全局状态、硬件条件编译较多。
- 代码复杂，不适合直接复制到功能安全或强规范项目。

**参考入口**：

```text
https://github.com/vedderb/bldc
motor/mcpwm_foc.c
motor/foc_math.c
motor/mc_interface.c
motor/mcpwm.c
hwconf/
applications/
commands.c
firmware_metadata.h
flash_helper.c
package_firmware.py
```

**客户确认问题**：

```text
是否只参考 VESC 的 FOC/SVPWM/补偿思想，而不复制 GPL 代码？
是否需要类似 VESC Tool 的参数和调试生态？
是否需要多硬件 hwconf 配置模型？
```

---

## 4. moteus：STM32G4 高动态机器人关节伺服

**主控/生态**：moteus r4.11 使用 STM32G4，CAN-FD 通信，高控制率和高 PWM switching rate，面向机器人关节伺服。

**核心技术/功能**：

- 一体化 brushless servo actuator/controller。
- CAN-FD 通信和 register/diagnostic 协议。
- 适合机器人关节伺服的参数、诊断、标定、固件/硬件一体化交付。
- 固件、硬件、库和工具在同一仓库中组织。

**大概做法**：

```text
Servo Controller
    -> 高频电机控制周期
    -> 传感器/编码器反馈
    -> CAN-FD register/diagnostic 通信
    -> 参数配置/标定/诊断工具
    -> 机器人关节执行器交付
```

**适合复刻的能力**：

- STM32G4 + CAN-FD 关节伺服架构。
- register/diagnostic 协议风格。
- 控制器、工具、硬件文档一体化交付。
- 机器人关节产品化文档和参数思路。

**优势**：

- 非常贴近机器人关节执行器。
- 主控、通信、功率级、控制率信息明确。
- 对客户展示“可产品化的开源伺服方案”很有价值。

**劣势/风险**：

- 与 moteus 硬件强相关，不能直接移植到任意功率板。
- 不等价于 EtherCAT/CiA402 工业伺服。
- 若客户需要安全认证、工业现场升级，需要额外补架构。

**参考入口**：

```text
https://github.com/mjbots/moteus
README.md
fw/
hw/
lib/
utils/
```

**客户确认问题**：

```text
当前是否使用 STM32G4 或类似 Cortex-M4/M33 电机控制 MCU？
是否需要 CAN-FD register/diagnostic 协议？
是否需要复刻 moteus 的一体化关节伺服交付方式？
```

---

## 5. Open Dynamic Robot Initiative：扭矩控制机器人和 TI F2838x 电机驱动

**主控/生态**：ODRI open-motor-driver-initiative 基于 TI TMS320F2838x；机器人执行器硬件面向腿足机器人和机械臂。

**核心技术/功能**：

- 开源扭矩控制机器人硬件/软件体系。
- 模块化 actuator：无刷电机 + 编码器 + 减速/传动 + 驱动器。
- open-motor-driver-initiative 面向 PMSM/BLDC 有感 FOC。
- 适合低成本、低复杂度、可复现的腿足机器人/机械臂执行器。

**大概做法**：

```text
Actuator Module
    -> PMSM/BLDC sensored FOC drive
    -> torque/current command
    -> robot joint mechanics
    -> 多关节 robot controller
```

**适合复刻的能力**：

- TI F2838x 多轴/伺服驱动的工程方向。
- torque-controlled actuator 模块定义。
- 机器人关节硬件、机械、固件、上位机协同设计。
- 低减速比/动态机器人执行器设计思想。

**优势**：

- 与高端机器人/机器狗/机械臂高度相关。
- TI F2838x 对工业伺服、EtherCAT、多核/CLA 很有参考价值。
- 可向客户展示“执行器模块 + 整机机器人”的完整路线。

**劣势/风险**：

- 仓库和资料分散，复刻成本高。
- 机械、功率、电机、传感器强耦合，不能只复制软件。
- 工业量产、安全认证、OTA 仍需另行补齐。

**参考入口**：

```text
https://github.com/open-dynamic-robot-initiative
https://github.com/open-dynamic-robot-initiative/open-motor-driver-initiative
https://github.com/open-dynamic-robot-initiative/open_robot_actuator_hardware
https://open-dynamic-robot-initiative.github.io/
```

**客户确认问题**：

```text
当前是否使用 TI F2838x / C2000？
是否需要复刻 ODRI 的扭矩控制 actuator 模块？
是否需要把电机驱动、机械关节、上位机控制一起设计？
```

---

## 6. PX4：模块化飞控、uORB、参数、日志和目标板生态

**主控/生态**：Pixhawk/NuttX/Linux/macOS；常见目标包含 STM32H7/F7 等飞控板。

**核心技术/功能**：

- 模块化飞控架构。
- uORB 发布/订阅中间件。
- boards / drivers / modules / parameters / logger / SITL-HITL 生态。
- 目标板配置、参数、日志、仿真和回归能力完整。

**大概做法**：

```text
Drivers/Sensors
    -> uORB topics
    -> Control modules
    -> Mixer/Actuator outputs
    -> Logger / Parameters / Commander / Navigator
    -> SITL/HITL/Board targets
```

**适合复刻的能力**：

- 参数系统。
- 日志/回放/调试数据链路。
- 模块化调度和消息总线。
- 多目标板 board config。
- 仿真/硬件在环测试流程。

**优势**：

- 大型嵌入式系统工程范式成熟。
- 参数、日志、目标板、SITL/HITL 非常适合量产架构 Skill 参考。
- 模块边界清楚，适合复杂系统。

**劣势/风险**：

- 不适合直接作为电机 FOC 代码模板。
- uORB/模块化对小 MCU 可能过重。
- 飞控业务模型与伺服驱动不同，需要裁剪。

**参考入口**：

```text
https://github.com/PX4/PX4-Autopilot
src/modules/
src/drivers/
boards/
msg/
ROMFS/
Tools/
```

**客户确认问题**：

```text
是否需要类似 PX4 的参数系统和日志系统？
是否需要 SITL/HITL 或仿真回归？
是否需要多目标板统一维护？
```

---

## 7. ArduPilot：长期产品线、AP_HAL、参数和多机型抽象

**主控/生态**：Pixhawk/ChibiOS/Linux/SITL，多机型长期维护。

**核心技术/功能**：

- 多 vehicle abstraction：Plane / Copter / Rover / Sub / Heli 等。
- `AP_HAL` 硬件抽象。
- `AP_Param` 参数系统。
- `AP_Logger` 日志系统。
- 任务调度、传感器、姿态/导航/控制库长期演进。

**大概做法**：

```text
Vehicle Layer
    -> AP_* libraries
    -> AP_HAL
    -> Board/OS Impl
    -> Parameters / Logger / Scheduler
```

**适合复刻的能力**：

- 长期产品线的硬件抽象和 vehicle abstraction。
- 参数、日志、任务调度体系。
- 多平台、多机型复用方式。
- 大规模嵌入式 C++ 工程组织。

**优势**：

- 长期维护、工程成熟度高。
- 参数/日志/调度/硬件抽象很值得借鉴。
- 适合多产品线或多型号设备。

**劣势/风险**：

- 代码体量大，学习成本高。
- 不适合小型电机驱动器直接套用。
- 飞控业务与电机伺服驱动不是同一层级。

**参考入口**：

```text
https://github.com/ardupilot/ardupilot
ArduCopter/
ArduPlane/
Rover/
libraries/AP_HAL/
libraries/AP_Param/
libraries/AP_Logger/
libraries/AP_Scheduler/
```

**客户确认问题**：

```text
是否需要长期多产品线参数/日志/硬件抽象？
是否需要类似 AP_HAL 的跨平台适配？
是否需要支持多个设备型号共享一套控制库？
```

---

## 8. Betaflight：高频飞控、目标板适配、DShot 和 Blackbox

**主控/生态**：STM32 F4/G4/F7/H7 等飞控板。

**核心技术/功能**：

- 高频姿态控制和飞控任务调度。
- DShot / Multishot / Oneshot 等电调协议。
- Blackbox 飞行记录器。
- target/board 配置和大量硬件目标维护。
- 传感器滤波、PID 调参、实时性能优化。

**大概做法**：

```text
Target/Board Config
    -> Drivers/Sensors
    -> Flight control loop
    -> Mixer/Motor protocol
    -> Blackbox logging
    -> Configurator tuning
```

**适合复刻的能力**：

- target/board 管理。
- Blackbox 日志和调参观测。
- 高频控制任务组织。
- 电调协议输出链路。
- 参数/配置器交互思路。

**优势**：

- 强实时调试和黑匣子数据链很实用。
- 多 target 支持成熟。
- 对飞控、云台、姿态控制类项目很有价值。

**劣势/风险**：

- 不是 PMSM FOC 伺服驱动模板。
- 强依赖飞控场景和电调协议。
- 对工业伺服/CiA402/EtherCAT 不直接适用。

**参考入口**：

```text
https://github.com/betaflight/betaflight
src/main/target/
src/main/drivers/
src/main/flight/
src/main/blackbox/
src/main/rx/
src/main/io/
```

**客户确认问题**：

```text
是否需要 Blackbox 类调试日志？
是否需要多 target 板级适配？
是否需要 DShot/飞控电调协议链路？
```

---

## 9. TI Motor Control SDK / C2000Ware MotorControl SDK：厂商电机控制基准工程

**主控/生态**：C2000 DSP、F2838x/F2800x、AM243x/AM263x ARM R5F + PRU-ICSS、Code Composer Studio、SysConfig、Industrial Communications SDK。

**核心技术/功能**：

- C2000 高性能电机控制库、实验工程、Universal Project & Lab。
- ePWM、ADC、CLA、DriverLib、SysConfig 的官方组织方式。
- AM243x/AM263x 方向包含 R5F 控制库、实时位置/电流 sense、PRU-ICSS、工业通信 SDK 集成。
- 厂商文档、例程、工具链和参考硬件组合。

**大概做法**：

```text
TI SDK / SysConfig
    -> Board/peripheral init
    -> ePWM/ADC/CLA/R5F/PRU real-time path
    -> Motor control library / examples
    -> Industrial communication integration
    -> Lab-based validation
```

**适合复刻的能力**：

- ePWM + ADC + CLA/R5F 的实时链路。
- 官方 FOC/电机控制实验工程结构。
- SysConfig/CCS 工程配置方式。
- 工业通信 + 电机控制的 SDK 集成方式。
- 多轴/工业伺服方向的官方基准。

**优势**：

- 厂商官方支持，适合客户评审和量产导入。
- 与 TI DSP/工业通信/实时控制高度匹配。
- 对 F2838x、AM243x、AM263x 项目尤其重要。

**劣势/风险**：

- SDK/工具链绑定强，迁移到非 TI 平台成本高。
- 工程可能依赖 SysConfig、CCS、特定 SDK 版本。
- 官方例程不等于完整产品，需要补 Bootloader、OTA、参数区、安全和发布流程。

**参考入口**：

```text
https://www.ti.com/tool/C2000WARE-MOTORCONTROL-SDK
https://github.com/TexasInstruments/motor-control-sdk
https://software-dl.ti.com/processor-industrial-sw/esd/motor_control_sdk/am243x/docs/api_guide_am243x/index.html
solutions/ 或 examples/
driverlib/
SysConfig 工程配置
Industrial Communications SDK 相关示例
```

**客户确认问题**：

```text
当前是否使用 TI C2000、F2838x、AM243x 或 AM263x？
是否需要基于 TI 官方 SDK 建立量产基线？
是否需要复刻 TI ePWM/ADC/CLA/R5F/PRU 实时控制链路？
是否需要工业通信 SDK 与电机控制一体化？
```

---

## 10. 客户选择建议模板

```text
根据当前主控和目标产品，我建议优先参考：
1. <仓库A>：用于 <能力A>，建议复刻 <接口/行为/流程>，不建议复制 <代码/目录/宏>。
2. <仓库B>：用于 <能力B>，建议复刻 <接口/行为/流程>，不建议复制 <代码/目录/宏>。

请确认以下选择：
A. 只吸收架构/算法思想，不复刻代码。
B. 复刻接口和行为，但重新实现代码。
C. 参考开源代码实现，先做许可证和安全风险评估。
D. 不参考该仓库。
```

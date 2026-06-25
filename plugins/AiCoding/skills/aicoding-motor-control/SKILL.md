---
name: aicoding-motor-control
description: 设计、审查和实现嵌入式电机控制 App 与控制算法，适用于 PMSM、BLDC、伺服、机器人关节、飞控 ESC 和多轴驱动。用于 PWM/ADC/Encoder 同步时序、电流环中断语义、FOC、SVPWM、PI/PID、三环带宽、前馈与解耦补偿、滤波、offset、保护、多轴同步、调试和测试。仅在控制链路或算法是主问题时使用；目录分层、平台抽象、Bootloader、OTA、量产和发布架构改用 architecture。涉及 C 实现时同时使用 c99，涉及定点或滤波细节时同时使用 dsp。
---

# 电机控制 App 与算法

默认使用中文输出。

## 核心边界

- 聚焦控制链路、实时采样、控制算法、保护、调试和验证。
- 将目录分层、平台抽象、Bootloader、OTA、量产和发布门禁交给 `architecture`。
- 涉及 C 实现时同时使用 `C99`。
- 涉及定点数学、滤波、饱和或数值稳定性时同时使用 `dsp`。
- 涉及具体 ARM 中断、NVIC、cache 或寄存器时同时使用 `arm`。

## 工作流

### 1. 建立控制上下文

优先从代码、原理图和配置中识别，缺失且影响方案时再询问：

- 电机类型、参数、极对数、母线和功率级；
- 主控、PWM 频率和计数模式；
- 电流采样拓扑、ADC 时序和转换延迟；
- 编码器或观测器类型、时间戳和延迟；
- 控制模式、环路更新率、机械负载和通信周期；
- 保护阈值、停机策略和可观测变量。

### 2. 用事件语义还原实时链路

不要根据 ISR 名称推断控制顺序。验证：

```text
PWM 同步事件
  -> ADC 采样与完成
  -> 锁存同周期编码器角度
  -> offset 修正与 FOC
  -> SVPWM
  -> PWM shadow 更新
```

确认每个样本和角度属于同一 `cycle_id`，并测量 deadline、overrun 和 jitter。时序细节读取 `references/pwm_adc_encoder_timing_zh.md`。

### 3. 选择采样和更新策略

在波谷、波峰、双采单更和双采双更之间，根据采样窗口、ADC 带宽、计算时间和 shadow load 点选择。用户未给出足够数据时，列出推荐起点、成立条件和需要测量的参数，不武断指定高复杂度方案。

### 4. 设计环路与补偿

- 区分更新频率和闭环带宽；
- 电流环默认 PI，并包含输出限幅、积分限幅和 anti-windup；
- 速度和位置环按噪声、延迟、机械共振和负载确定带宽；
- 仅在基础相序、方向、offset、极对数和闭环稳定后增加前馈或补偿。

需要带宽、补偿和测试细节时读取 `references/pid_bandwidth_compensation_zh.md`。

### 5. 处理多轴和故障

保持每轴独立状态，使用统一 `cycle_id` 或 timestamp、shadow command 和同步 apply。定义单轴停机、全轴停机或降级策略。读取 `references/multi_axis_sync_debug_zh.md` 获取同步误差和调试检查项。

### 6. 使用参考项目

仅在主控和问题匹配时读取：

- `references/repo_reference_matrix_motor_zh.md`：快速匹配 VESC、ODrive、moteus、ODRI、TI SDK 等；
- `references/customer_motor_function_replicate_options_zh.md`：比较算法思想、接口行为、代码参考和许可证边界。

不得因主控相同就默认复刻；先确认目标功能、功率级、传感器、安全要求和许可证。

### 7. 验证

读取 `references/testing_validation_zh.md`。至少覆盖 bring-up 顺序、三环阶跃、正反转、低速、高速限压、负载扰动、多轴同步和故障注入。没有波形、trace 或测量数据时，不宣称参数已调好或实时性已满足。

## 输出

按任务规模输出必要部分：

1. 平台、控制目标和已确认假设；
2. PWM/ADC/Encoder 事件链与 deadline；
3. 环路带宽、限幅、前馈和补偿策略；
4. 多轴同步与故障策略；
5. 观测变量、测试步骤和通过标准；
6. 参考项目匹配与待用户确认的复刻范围。

正式审查可使用 `assets/motor_control_review_template_zh.md`；需要确认复刻方式时使用 `assets/implementation_replicate_decision_template_zh.md`。

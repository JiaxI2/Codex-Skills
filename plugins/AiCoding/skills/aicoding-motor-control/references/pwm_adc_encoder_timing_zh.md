# PWM / ADC / Encoder 同步时序

## 1. 必须由用户选择采样/更新策略

```text
波谷采样
波峰采样
双采单更
双采双更
```

选择时必须检查：

```text
PWM 频率和中心对齐/边沿对齐模式
ADC 采样保持时间和转换时间
DMA/SDFM/ADCINT 延迟
FOC 计算时间
PWM shadow load 点
编码器读取延迟
电流采样窗口是否避开开关噪声
```

## 2. 参考项目思路

### VESC

- `motor/mcpwm_foc.c` 中体现了围绕 PWM/ADC/DMA 完成点执行 FOC 的强实时路径。
- `motor/foc_math.c` 中 `foc_svm()` 体现 SVPWM 数学平台化。
- 可吸收：采样时序、SVPWM、补偿和调试变量。

### ODrive

- `Firmware/MotorControl` 中将 Axis/Motor/Encoder/Controller/FOC 分开。
- 可吸收：控制周期中先采集 timing critical input，再更新控制和 PWM timing 的思想。

### moteus

- README 显示控制率 15-30kHz、PWM switching 15-60kHz、STM32G4 和 CAN-FD。
- 可吸收：高动态伺服控制周期、紧凑一体化执行器设计、诊断工具。

### TI SDK / ODRI

- TI C2000 / AM R5F + PRU 方向应优先利用 ePWM/ADC/SDFM/CLA/PRU-ICSS 的硬件同步能力。
- 不要按 STM32 TIM/ADC 名称照搬。

## 3. 输出模板

```text
推荐采样点：波谷 / 波峰 / 双采单更 / 双采双更
理由：
计算窗口：
ADC 完成点：
编码器锁存点：
PWM shadow load 点：
overrun 检测：
用户需确认：
```

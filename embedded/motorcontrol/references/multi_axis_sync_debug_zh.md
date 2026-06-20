# 多轴同步、抖动抑制与调试

## 1. 多轴同步

必须具备：

```text
统一 cycle_id / timestamp
每轴独立 axis_ctx
shadow command
同步 apply
故障隔离策略
同步误差观测
```

参考：

```text
Dummy-Robot：多轴命令、shadow target、广播同步。
ODrive：Axis/Motor/Encoder/Controller 边界。
ODRI：腿足机器人、多轴驱动系统架构。
PX4/ArduPilot：系统级参数、日志、任务调度。
Betaflight：Blackbox/高频调试数据。
```

## 2. 抖动抑制

检查来源：

```text
通信周期抖动
控制周期 overrun
编码器噪声
速度估算噪声
PWM 更新点不确定
机械共振
齿槽/摩擦/死区
```

手段：

```text
统一同步时基
固定控制 dt
shadow update
速度/电流滤波
notch/low-pass
轨迹 S 曲线
速度/加速度前馈
摩擦/重力补偿
```

## 3. 调试变量

必须记录：

```text
cycle_id、control_time、overrun
Id/Iq、Vd/Vq、duty、theta_e
pos/vel/err、cmd_pos/cmd_vel/cmd_iq
PID P/I/D、sat/anti-windup
Vbus/temp/fault
sync_error、communication_jitter
```

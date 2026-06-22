# CiA402 开源实现蒸馏：ecat_servo / hal-cia402 / ROS2 CiA402 Plugin

> 用途：让 Agent 快速理解 CiA402 在真实代码中通常怎么实现：状态机、控制字/状态字、模式切换、CSP/CSV/CST、homing、fault reset、抱闸/高压/使能动作如何分层。
>
> 正确性核对：状态语义以 CiA402/ETG.6010 为准；开源实现仅作为工程模式参考。最后核对日期：2026-06-20。

## 1. CiA402 不等于电机控制算法

CiA402 是驱动接口规约：主站通过对象字典和 PDO 控制驱动状态、模式、目标值、反馈值。FOC、电流环、位置环、抱闸、高压上电、安全链路是驱动内部实现。

```text
主站/NC/ROS2/LinuxCNC
  -> 0x6040 Controlword + 目标值 + 0x6060 Mode request
  -> 从站 CiA402 FSA
  -> 电机控制/电源/抱闸/安全链路动作
  -> 0x6041 Statusword + 实际值 + 0x6061 Mode display
```

Agent 看到“电机不动”时，不应直接调 PI 参数；应先确认：状态机是否 Operation enabled、模式是否实际接受、mode-specific status bit 是否有效、目标/反馈是否在 PDO 中更新。

## 2. 开源实现中的三种参考模式

| 项目类型 | 价值 | 学习重点 |
|---|---|---|
| 从站伺服实现 | 从设备侧实现 CoE/CiA402 | 状态机如何驱动应用 flag，高压/抱闸/错误如何被应用层执行 |
| LinuxCNC HAL 组件 | 从主站侧把 PDO 转成运动控制接口 | read/write 顺序、状态控制、scaling、homing |
| ROS2 CiA402 plugin | 从机器人软件侧封装 CiA402 轴 | ros2_control command/state interface、mode 切换、fault reset、安全默认目标 |

## 3. 状态机实现分层

### 推荐结构

```c
// 伪代码
read_controlword_and_mode_request();
validate_mode_request();
update_cia402_fsa(controlword, internal_faults, quick_stop, safety_state);
update_application_flags();    // enable_voltage, quick_stop, operation_enabled, brake_release
apply_mode_specific_command(); // CSP/CSV/CST/PP/HM
update_statusword_and_mode_display();
write_feedback_pdo();
```

### 不推荐结构

```c
// 反例
if (controlword == 0x000F) servo_on = 1;
statusword = 0x0637;
mode_display = mode_request;
```

这种硬编码会在 fault、quick stop、safety halt、mode switching、homing、TwinCAT NC ready 时失效。

## 4. 0x6040/0x6041 的实现关注点

| 主题 | 正确实现倾向 | 常见错误 |
|---|---|---|
| Fault reset | 对 bit7 上升沿动作，清除可恢复错误后回 Switch on disabled | 长时间保持 reset，或 reset 后不清错误源 |
| Quick stop | 根据 option code 和安全策略进入 Quick Stop Active 或 Disable Operation | 忽略 bit2，导致主站认为快速停机失败 |
| Operation enabled | 只有电源、抱闸、安全、控制环都满足时才置状态 | 状态字提前置位但电机侧未准备 |
| bit12 | 按当前 mode display 解释 | PP 的 acknowledge 和 CSP follows command 混用 |
| bit10 | Target reached / Status toggle 等语义随模式变化 | 跨模式复用同一含义 |

## 5. Mode switching 的工程规则

ETG.6010 推荐动态切换时把 `0x6060` 放 RxPDO，把 `0x6061` 放 TxPDO，并同时映射各模式必要对象。Agent 审查开源或项目代码时应查：

1. 是否支持静态模式还是动态模式。
2. `requested_mode` 是否经过 `supported_modes` 校验。
3. `mode_display` 是否只在内部切换完成后更新。
4. 切换中是否同时保持旧模式和新模式的 PDO 数据有效。
5. 状态字模式相关位是否跟随 `0x6061`，不是跟随 `0x6060`。

## 6. CSP/CSV/CST 对照

| 模式 | 主站轨迹发生位置 | 从站主要任务 | 必要对象 |
|---|---|---|---|
| CSP = 8 | 主站/NC/机器人控制器 | 跟随周期目标位置，输出实际位置 | `0x607A`、`0x6064`、`0x6040/0x6041` |
| CSV = 9 | 主站 | 跟随周期目标速度 | `0x60FF`、`0x606C` |
| CST = 10 | 主站 | 跟随周期目标转矩/电流 | `0x6071`、`0x6077` |
| HM = 6 | 驱动或主站辅助 | 完成回零逻辑并更新位置基准 | `0x6098/0x6099/0x609A` 等 |
| PP = 1 | 驱动内部轨迹规划 | 接收目标位置并内部规划 | `0x607A/0x6081/0x6083/0x6084` |

## 7. 代码审查问题清单

### 从站侧

- `0x6061` 是否可能被初始化/故障路径清 0。
- CSP 下 `Statusword bit12` 是否在 Operation enabled 且实际跟随时置 1。
- PP 下 `set-point acknowledge` 是否只在新 setpoint 流程中变化。
- fault reaction 是否先让功率级进入安全状态，再改变 FSA 状态。
- 多轴是否每轴独立控制字、状态字、模式、错误码。

### LinuxCNC/ROS2 主站侧

- read-all 是否在 motion 前，write-all 是否在 motion 后。
- command interface 未控制时是否输出安全默认目标，例如保持当前实际位置。
- fault reset 是显式命令还是自动 reset；自动 reset 不适合所有安全场景。
- mode switching 是否会在未准备目标值时产生突跳。
- scaling 是否与驱动单位一致。

## 8. Agent 回答模板

```markdown
## CiA402 判断
问题属于：[状态机 / 模式切换 / PDO 映射 / 主站控制层 / 驱动内部执行]

## 必查对象
- 0x6040 = ...
- 0x6041 = ...
- 0x6060 = ...
- 0x6061 = ...
- 0x603F = ...

## 状态机路径
[Shutdown -> Switch on -> Enable operation / Fault reset / Quick stop]

## 模式相关位
当前 0x6061 = [mode]，所以 0x6041 bit10/12/13 应按 [mode] 解释。

## 最小修复
[只改状态机或映射，不动电机控制核心]
```

## 9. 可维护蒸馏规则

- 开源项目只用于工程模式参考；状态位语义以 CiA402/ETG.6010 为准。
- 每次引入新驱动器，先做“对象支持矩阵”：6040/6041/6060/6061/6502/607A/6064/60FF/6071/6077。
- 不把某个项目的自动使能、自动 fault reset、默认目标策略当成通用规范。

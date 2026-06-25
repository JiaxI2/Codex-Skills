# EtherCAT 开源项目选型与蒸馏路线

> 用途：让 Agent 根据任务快速选择应参考哪个开源项目/规范/文档，不再把 SOEM、IgH、SOES、SSC、LinuxCNC、ROS2、CiA402 实现混成一类。
>
> 最后核对日期：2026-06-20。

## 1. 先按任务选项目

| 任务 | 优先参考 | 原因 |
|---|---|---|
| 写最小 EtherCAT 主站工具 | SOEM | C 语言、轻量、示例直接、适合扫描/SDO/PDO 验证 |
| Linux 实时生产主站 | IgH / EtherLab | 内核/实时/domain 模型，适合 LinuxCNC/工业控制 |
| 学习从站栈内部 | SOES | 小 footprint，源码直接，便于理解 ESC/CoE/PDO/FoE |
| 做正式从站固件 | SSC/ET9300 + ETG 文档 | 工业主流从站栈路径，配套 ESI/OD/认证流程 |
| 做 CiA402 从站伺服 | ecat_servo + ETG.6010 | 可看状态机如何驱动应用 flag，但规范语义仍以 ETG/CiA 为准 |
| LinuxCNC 伺服轴 | linuxcnc-ethercat + hal-cia402 | HAL read/write 顺序、state/scaling/homing |
| ROS2 机器人轴 | ethercat_driver_ros2 / FCAT stack | ros2_control、YAML/URDF、command/state interface |
| TwinCAT 现场排障 | TwinCAT docs + ET9300 + 本 Skill playbook | WcState、DC、NC Ready、ESI/PDO 映射 |
| FoE OTA | ET9300 FoE + 项目 bootloader | FoE 只是传输，镜像校验/分区/回滚另做 |

## 2. 代码库蒸馏优先级

### P0：必须蒸馏

1. SOEM：主站最小闭环。
2. SOES：从站最小闭环。
3. SSC/ET9300：正式从站工程结构。
4. ETG.6010：CiA402 EtherCAT 伺服共同行为。

### P1：高价值蒸馏

1. hal-cia402：CiA402 状态机接 LinuxCNC 的工程方式。
2. linuxcnc-ethercat：IgH 与 HAL 驱动、XML 配置、实时线程。
3. ethercat_driver_ros2：ROS2/ros2_control 中 CiA402 轴封装。
4. ecat_servo：CoE/CiA402 从站伺服实现参考。

### P2：场景型蒸馏

1. fastcat / fcat / jsd：机器人系统里 SOEM 上层抽象。
2. KickCAT：C++ thin stack，适合学习轻量 C++ 结构，但不作为主参考。
3. pysoem：Python 诊断工具可用，但不作为实时控制主站。

## 3. Agent 如何使用本选型表

收到用户问题后：

```text
是协议原理？ -> ethercat-deep-dive-agent-ref.md
是主站源码/工具？ -> ethercat-master-source-map-soem-igh.md
是从站固件/SSC？ -> ethercat-slave-source-map-ssc-soes.md
是 CiA402 状态机/模式？ -> cia402-open-source-implementation-map.md
是 TwinCAT/LinuxCNC/ROS2？ -> twincat-linuxcnc-ros2-diagnostics-map.md
是 MCP/工具化？ -> ethercat-mcp-design.md
```

## 4. 维护性原则

1. **不要复制大段源码。** 只保留源码入口、调用链、排障路径、对象表。
2. **每个 ref 都写 `last_checked`。** 当前版本为 2026-06-20。
3. **每个 ref 都声明 source level：** 规范、官方文档、开源实现、论坛经验、项目经验。
4. **每个开源项目只提稳定抽象。** 具体文件路径和 API 可能变动，应由代码库 MCP 实时读取。
5. **把规范和实现分开。** 开源项目的做法不能覆盖 ETG/CiA402 语义。
6. **敏感/厂商材料中性化。** 厂商 SDK 只保留“MCU/ESC/PDI/同步/故障模式”的抽象。

## 5. 下一步推荐

1. 把当前 Skill 的所有 ref 做成索引表：关键词 -> ref -> 检查项 -> 典型输出。
2. 做 `ethercat-project-mcp`：先实现 ESI 解析和日志分析。
3. 做 `ethercat-master-mcp`：先基于 SOEM 实现只读 scan/read_sdo/read_cia402。
4. 再接 TwinCAT ADS，只读轴状态和变量。
5. 最后考虑写操作和自动修复。

# EtherCAT 网页知识库索引与读取路由

> 目的：把 EtherCAT 网页文章整理为可离线使用的工程化参考。本文保存本地摘要、适用场景、关键词和跳转逻辑，不保留品牌词、原始域名和大段网页原文。
>
> 使用原则：先根据问题关键词读本索引，再转到专题 ref。若专题 ref 已覆盖问题，不需要联网检索。

## 何时优先读哪一个 ref

| 用户问题关键词 | 优先读取 |
|---|---|
| `Module/Slot`、`MDP`、`DependOnSlot`、`MAX_AXES`、`0xF000/0xF010/0xF030/0xF050`、CIA402 多轴、TwinCAT 多生成 Axis | `references/web-cia402-mdp-multiaxis.md` |
| `0x1A`、`0x1B`、`0x2C`、`Sync0WdCounter`、`DC_CheckWatchdog`、`PDI中断`、`SYNC0/SYNC1`、`AL_EVENT_ENABLED`、`DC_SUPPORTED`、`ECAT_TIMER_INT` | `references/web-ssc-sync-errors.md` |
| `CoE`、`OD`、`SDO`、`PDO`、动态 PDO、`0x1600/0x1A00`、`0x1C12/0x1C13`、`APPL_InputMapping`、`APPL_OutputMapping`、EoE、PLC 任务、输入到输出延时 | `references/web-coe-pdo-eoe-twincat.md` |
| PHY、Link、MII、MDC/MDIO、`0x110 DL Status`、EEPROM、Flash 模拟 EEPROM、`CREATE_EEPROM_CONTENT`、ESC 引脚、RUN_LED/ERR_LED、扫描不到从站、地址别名、Explicit Device ID | `references/web-phy-eeprom-hardware.md` |

## 24 篇文章的本地化用途

| # | 文章主题 | 归档专题 | 本地化用途 |
|---:|---|---|---|
| 1 | CIA402 例程中的 MDP OD 处理 | MDP/多轴 | 解释 Device 区与 Modules 区对象来源、`DependOnSlot`、`SlotIndexIncrement=0x800`、`SlotPdoIncrement=0x10`，以及 `ApplicationObjDic`、`DefCiA402AxisObjDic`、`LocalAxes`、`CiA402_Init()`、`APPL_GenerateMapping()` 的运行时 OD 构建逻辑。 |
| 2 | CIA402 例程 2 轴扩展为 8 轴 | MDP/多轴 | 总结 `MAX_AXES`、`0x1C12/0x1C13`、`0xF000/0xF010/0xF030/0xF050`、ESI `ChannelInfo`、`Slots`、Product Code/Revision 缓存等修改点。 |
| 3 | Module/Slot 概念与 OD 分配 | MDP/多轴 | 把 ETG.5001 MDP 的 Module、Slot、SlotGroup、ModuleGroup、ModulePdoGroup 转换为多轴伺服、IO 耦合器、网关的建模规则。 |
| 4 | 竞争态引起 0x2C | 同步/中断 | 解释 `Sync0WdCounter++` 与 `Sync0_Isr()` 清零在不同上下文中的非原子读改写竞争，给出临界区/原子/时间戳验证方法。 |
| 5 | 运行中 0x1A/0x1B/0x2C | 同步/中断 | 建立 `0x1A Synchronization error`、`0x1B SM watchdog`、`0x2C Fatal SYNC error` 与 `CheckIfEcatError()`、`ECAT_CheckTimer()`、`DC_CheckWatchdog()` 的定位路径。 |
| 6 | 输入从站到输出从站延时测量 | CoE/PDO/时序 | 用 PLC 周期、Separate Input Update、Pre ticks 和报文相位解释最小/最大延时，辅助判断“为什么不是同周期生效”。 |
| 7 | EoE 通信速率分析和改善 | CoE/PDO/EoE | 说明 EoE 基于 Mailbox 封装，受主站轮询、邮箱大小、锁步机制和任务周期限制，不能按 100M PHY 带宽预期。 |
| 8 | 输入数据写入输出数据的时序分析 | CoE/PDO/时序 | 说明 ESC DPRAM 3-buffer、主站帧到达相位和从站 TxPDO 更新时刻；用于诊断“反馈晚一拍”。 |
| 9 | 从站地址、地址别名、Explicit Device ID | PHY/EEPROM/地址 | 区分 ESC `0x10` 地址、`0x12` 地址别名、应用层 Explicit Device ID、`APPL_GetDeviceID()`、`0x120/0x134` 交互和 EEPROM checksum。 |
| 10 | SSC 中断配置参数和优先级 | 同步/中断 | 汇总 `AL_EVENT_ENABLED`、`DC_SUPPORTED`、`ECAT_TIMER_INT`、PDI、Sync0/Sync1、1 ms Timer 的作用和优先级建议。 |
| 11 | 动态 PDO 实现 | CoE/PDO | 区分固定 PDO、可变 Assign、可变 Mapping；强调 `0x1C12/0x1C13`、`0x160x/0x1A0x`、`APPL_GenerateMapping()` 和 Mapping 函数必须一致。 |
| 12 | 从设备 EEPROM 数据 | PHY/EEPROM | 解释 EEPROM 配置区、前 8 word 上电加载、checksum、增强链路检测和 Flash 模拟 EEPROM 的调试影响。 |
| 13 | RUN_LED/ERR_LED 使用 GPIO | PHY/硬件 | 当 ESC 硬件 LED 引脚不可用时，使用 `ESC_SUPPORT_ECAT_LED=0`、`UC_SET_ECAT_LED=1`、`HW_SetLed()` 由 GPIO 控制。 |
| 14 | ESC 引脚功能说明 | PHY/硬件 | 归纳 PHY Reset、LED_RUN、LED_ERR、LINK_ACT、NMII_LINK 等 ESC_CTR 二级 pinmux 与 `IO_CFG` 配置链。 |
| 15 | TwinCAT 扫描 CIA402 多生成 Axis | MDP/多轴 | 用 ESI `Devices/Device` 与 `Modules/Module` 的 Profile/Channel 描述冲突解释 NC 轴数量异常。 |
| 16 | EEPROM 存储与烧录方案 | PHY/EEPROM | 总结外部 EEPROM 与 Flash 模拟 EEPROM 两种路径，以及 `CREATE_EEPROM_CONTENT=1` 生成 `eeprom.h` 的固件集成方法。 |
| 17 | ESC 配置 PHY 示例 | PHY/硬件 | 提炼 PHY LED/Link 信号配置要求：给 ESC 的 Link 必须稳定、极性正确、不要用 blink 信号当 Link。 |
| 18 | ESC 使用 PHY 注意事项 | PHY/硬件 | 说明每个 ESC 端口对应一个 PHY、用 `0x110 DL Status` 查端口状态、MII 延迟、共享时钟、PHY 地址和 reset 时序。 |
| 19 | CoE 添加对象字典内容 | CoE/OD | 比较 SSC Tool/Excel 重新生成与手工同步修改两种路径；强调 XML、OD 代码、PDO mapping 必须一致。 |
| 20 | CoE、SDO、PDO 关系 | CoE/OD | 建立寄存器访问、Mailbox、Process Data 三层模型；SDO 走 CoE+Mailbox，PDO 走 Process Data/FMMU。 |
| 21 | 主站扫描不到从站 | PHY/EEPROM | 建立扫描失败排查顺序：主站网卡、PHY Link、Port0、ESC `0x110`、EEPROM checksum，再到 CoE/CiA402。 |
| 22 | 同步模式与 SSC Tool 设置 | 同步/中断 | 对比 Free Run、SM-Synchron、DC-Synchron，并说明 Sync0 shift、AL event、DC 中断配置对伺服同步的影响。 |
| 23 | TwinCAT 创建 PLC 任务 | TwinCAT/PLC | 用于 IO 联动、延时测量、PLC 周期/base time/变量链接/autostart 的配置检查。 |
| 24 | PDI 中断和 Sync 中断逻辑 | 同步/中断 | 说明 `AL Event Request 0x220`、`AL Event Mask 0x204`、SM2 中断、Sync0/Sync1 中断和 PDI 路由关系。 |

## 使用边界

- 网页知识库是工程实现参考，不替代 ETG.1000、ETG.6010、CiA402/IEC 61800-7 的规范语义。
- 当网页示例与用户项目代码冲突时，优先以用户项目代码、ESI、TwinCAT 在线日志和实际芯片手册为准。
- 对网页内容只做摘要、重组和工程化转述；需要完整原文、图片或代码时，由用户提供目标片段后再分析。

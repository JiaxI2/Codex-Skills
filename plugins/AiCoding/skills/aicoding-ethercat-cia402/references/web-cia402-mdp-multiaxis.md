# EtherCAT 网页参考：CIA402、MDP、Module/Slot、多轴

## 读取触发

当用户提到以下任一内容时读取本文件：

- ECAT_CIA402、CIA402 例程、2 轴改 8 轴、多轴伺服。
- MDP、Module/Slot、ModuleIdent、DependOnSlot、SlotIndexIncrement、SlotPdoIncrement。
- 0xF000、0xF010、0xF030、0xF050、0x1C12、0x1C13。
- TwinCAT 扫描 CIA402 例程多生成 Axis 或 NC 轴数量异常。
- 运行时 OD、ESI XML 与 `cia402appl.h`/`APPL_GenerateMapping()` 不一致。

## 核心来源

1. `[EtherCAT]Module/Slot概念与OD分配`
2. `[EtherCAT]以CIA402例程为例介绍MDP设备的OD处理`
3. `[EtherCAT]将CIA402例程从2轴改为8轴`
4. `[EtherCAT]TwinCAT扫描CIA402例程时会添加3个Axis的情况说明`
5. `[EtherCAT]从站实现动态PDO功能`

详见 `ethercat-web-knowledge-index.md`。

## 工程化规则

### 1. MDP 思维模型

网页文章把 ETG.5001 MDP 的核心解释为：设备内部的子单元抽象为 `Module`，可放置 Module 的位置抽象为 `Slot`。ESI 不再把所有运行时 OD 静态写死，而是描述 Slot 集合和 Module 库，由主站根据配置拼装运行时 OD。

适用对象：

- 多轴伺服：每个轴可视为一个 Module/Channel。
- IO 耦合器：每个端子或子设备可视为 Module。
- 网关：下挂子总线节点可视为 Module。

### 2. Device 区与 Modules 区的 OD 不要混淆

- `Device/Profile/Dictionary/Objects`：设备本体对象，始终存在，如 `0x1000`、`0x1018`、`0x1C12`、`0x1C13`、`0xF000`、`0xF030`。
- `Modules/Module/Profile/Dictionary/Objects`：某个 Module 装入某个 Slot 后才出现的对象，例如 `0x6040`、`0x6041`、`0x607A`、`0x6064`。
- `DependOnSlot="true"`：对象索引不固定，需要按 Slot 实例号偏移。

典型偏移：

```text
实际 OD 索引       = 模板索引 + slot_index * SlotIndexIncrement
实际 PDO 映射索引  = 模板 PDO 索引 + slot_index * SlotPdoIncrement
```

CIA402 双轴默认示例常见：

```text
SlotIndexIncrement = 0x800
SlotPdoIncrement   = 0x10
Axis0: 0x6040/0x6041/0x607A/0x6064, 0x1602/0x1A02
Axis1: 0x6840/0x6841/0x687A/0x6864, 0x1612/0x1A12
```

### 3. CIA402 运行时 OD 构建路径

检查 ECAT_CIA402 例程时，重点看：

```text
ApplicationObjDic[]        // 设备级对象：0x1C12、0x1C13、0xF000、0xF010、0xF030、0xF050...
DefCiA402AxisObjDic[]      // 单轴模板对象：0x160x、0x1A0x、0x6040、0x6041、0x6060、0x6061...
LocalAxes[MAX_AXES]        // 每轴独立数据和 ObjDic 指针
CiA402_Init()              // 初始化轴数据、复制模板、修正 PDO entry 索引、绑定 pVarPtr、修正对象索引
APPL_GenerateMapping()     // INIT->PREOP 时按 0x1C12/0x1C13 激活/去激活轴并注册 CoE OD
```

排查原则：

1. `ESI Slots/Modules`、`0xF0xx`、`MAX_AXES` 三者必须一致。
2. 每个轴的 `ObjDic`、对象变量、PDO Mapping entry 必须独立。
3. `0x1C12/0x1C13` 决定当前激活哪些轴和哪些 PDO。
4. 如果对象能在 ESI 看到但 SDO 读不到，重点查 `APPL_GenerateMapping()` 是否注册了该轴对象。

### 4. 2 轴改 8 轴检查表

修改 CIA402 例程从 2 轴到 8 轴时，至少检查：

- `MAX_AXES` 改为 8。
- `0x1C12`、`0x1C13` 的 entries、默认值、对象描述按 8 轴扩展。
- `0xF000` 的 Max Modules / Index Distance 与 8 轴匹配。
- `0xF010` Module Profile List 按 8 个 slot/channel 设置。
- `0xF030` Configured Module Ident List、`0xF050` Detected Module Ident List 按 8 轴扩展。
- ESI 增加更多 `Profile/ChannelInfo`。
- ESI 增加更多 `Slots/Slot`，并保证每个 Slot 允许的 ModuleIdent 正确。
- 修改 Device Name/Product Code/Revision，避免 TwinCAT 使用旧 ESI 缓存或混淆不同设备。
- TwinCAT 删除旧设备、重载 ESI、重新扫描。

### 5. TwinCAT 多生成 Axis 的处理

现象：CIA402 2 轴例程被 TwinCAT 扫描时，自动添加 3 个 Axis，但实际最多只能绑定 2 个。

优先检查 ESI：

- 不应在 `Devices/Device` 和 `Modules/Module` 两处重复/冲突描述 `ProfileNo`。
- `Devices/Device` 下第 2 个 channel 的 `AddInfo` 应符合 CiA402 Servo drive 语义，网页文章建议从 `0` 修正到 `2`。
- 修正后重新导入 ESI、删除旧设备、重新扫描；正常应只添加实际支持的 NC 轴数量。

### 6. 动态 PDO 与 MDP 的关系

网页文章将 PDO 情况分为三类：

1. 固定 PDO Assign + 固定 PDO Mapping。
2. 可变 PDO Assign + 固定 PDO Mapping：如 CIA402 例程通过 `0x1C12/0x1C13` 在多个固定映射中选择。
3. 可变 PDO Assign + 可变 PDO Mapping：主站可修改 `0x160x/0x1A0x` 的 entry。

若用户要在 CIA402 中实现动态 PDO：

- 修改 `0x1602/0x1A02` 等 PDO Mapping 对象的 access、entry 数、默认值、最大 entry 数。
- `APPL_OutputMapping()`、`APPL_InputMapping()` 不能再硬编码固定顺序，应按 Mapping Entry 逐项解析。
- ESI、OD、代码三方必须一致。
- 多轴下还要叠加 Slot 偏移：对象索引偏移 `0x800`，PDO 映射索引偏移 `0x10`。

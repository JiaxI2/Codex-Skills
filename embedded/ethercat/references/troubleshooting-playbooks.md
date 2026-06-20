# EtherCAT/CiA402 排障 Playbook

## A. 0x6060=8，但 0x6061=0

**最可能层级：CiA402 应用模式接受路径。**

检查：

1. TwinCAT 是否真的写入 0x6060=8。
2. 固件中 0x6060 背后变量是否被 PDO 写入。
3. PREOP→SAFEOP 或 SAFEOP→OP 是否把模式清零。
4. 模式校验表是否允许 CSP。
5. 接受模式后是否写 0x6061。
6. 0x6502 是否声明支持 CSP。
7. ESI 默认值是否与 Startup SDO、固件默认值冲突。

建议修复：

- 增加 `requested_mode`、`accepted_mode`、`display_mode` 三个状态。
- 增加拒绝原因：unsupported mode、not ready、PDO invalid、safety not ready。
- 0x6061 只反映实际接受模式，不要直接等于 ESI 默认值。

## B. TwinCAT 仍按 PP 而不是 CSP

**最可能层级：ESI/PDO/Startup SDO/NC 轴配置。**

检查：

1. 当前 PDO 是否为 CSP 映射。
2. RxPDO 是否包含 0x607A，TxPDO 是否包含 0x6064。
3. 是否通过 Startup SDO 写入 0x6060=8。
4. 0x6061 在 OP 后是否为 8。
5. 0x6502 是否正确。
6. TwinCAT 是否还缓存旧 ESI 或旧设备实例。

建议修复：

- 明确区分 PP/CSP PDO。
- 支持动态模式时，映射 0x6060/0x6061。
- 删除旧设备实例，重载 ESI，重新 Scan。

## C. Operation Enabled 但 NC Not Ready

**最可能层级：状态字模式位或实际值有效性。**

检查：

1. 解码 0x6041。
2. bit0/1/2 是否置位，bit3 是否清零。
3. 0x6061 是否为预期模式。
4. CSP/CSV/CST 的 bit12 是否按 follows command 置位。
5. 0x6064 是否周期更新。
6. WcState 是否有效。
7. NC Link 和 Scaling 是否正确。

建议修复：

- PP 的 set-point acknowledge 和 CSP 的 follows command 分开实现。
- 只要命令有效、实际反馈有效、无跟随错误且已 Operation Enabled，CSP bit12 应保持正确状态。
- 增加 TxPDO stale timeout，超时后清 Drive valid/follows command。

## D. 多轴运行一段时间 invalid IO / WcState

**最可能层级：DC/实时性/过程数据一致性。**

检查：

1. 启用 DC Diagnostics，在运动中复现。
2. 比较 NC、PLC、EtherCAT、Sync0 周期。
3. 检查 0x1C32/0x1C33 和 Sync0 Shift。
4. 验证 PDO 大小、SM/FMMU 分配和全部轴对象偏移。
5. 检查 Process Data Watchdog。
6. 检查 TxPDO 是否双缓冲。
7. 检查 CPU 负载和实时路径日志。
8. 检查 PHY 错误计数。

建议修复：

- 将 PDO 快照放到 Sync0/Application Cycle。
- 共享内存使用双缓冲/序列锁。
- 减少实时路径日志和非必要计算。
- 对每轴增加 Rx/Tx 更新计数，定位是哪一轴或全局周期先异常。

## E. SAFEOP 到 OP 失败

**最可能层级：PDO/SM/FMMU 或 Startup SDO。**

检查：

1. AL Status Code。
2. Startup SDO 是否 abort。
3. 0x1C12/0x1C13 是否与 ESI 一致。
4. 固件对象字典是否包含所有 PDO Entry。
5. 对象 bit length 是否正确。
6. EEPROM/SII 是否仍是旧版本。

建议修复：

- 固定 PDO 先跑通，再做动态 PDO。
- 每次改 ESI 后重新扫描和更新 EEPROM。
- 对不支持写的对象，不要放入 Startup SDO 写列表。

---
name: ethercat
description: EtherCAT 嵌入式固件 skill，用于从站协议栈、ESC/PDI/SPI 访问、CoE 对象字典、PDO/SDO、FoE、ESI 文件、分布式时钟、watchdog 和 EtherCAT 状态机调试或评审。涉及 C 实现细节时结合 c99-standard-c 使用。默认使用中文输出。
---

# EtherCAT 固件

默认使用中文回答和生成说明。仅在用户明确要求英文，或项目/主站交付规范要求英文时使用英文。

使用此 skill 处理 EtherCAT 固件设计、实现、调试和评审。涉及代码修改时结合 `c99-standard-c` 和 `review`。

## 工作流程

1. 确认从站协议栈、ESC 器件、PDI 模式、周期时间、SyncManager/FMMU 配置、PDO 映射和所需 EtherCAT 状态。
2. 将对象字典、ESI、PDO 布局和固件结构视为同一个合约，保持同步。
3. 验证状态转换：INIT、PREOP、SAFEOP、OP、错误确认、watchdog 和故障恢复。
4. 对 FoE/OTA/bootloader 路径，验证长度、序号、超时、CRC/hash、Flash 擦写对齐、回滚和掉电行为。
5. 对分布式时钟，验证同步模式、锁存时序、抖动预算和控制环集成。

## 检查项

- 不在未检查对齐、大小端和长度的情况下把原始过程数据强转为 packed struct。
- 对象字典类型、访问权限、默认值和持久化行为必须与代码一致。
- PDO 映射变更必须同步到 ESI 和主站期望。
- watchdog 和通信丢失行为必须让应用进入安全状态。
- ESC 寄存器访问要遵守副作用、时序和 PDI 同步要求。

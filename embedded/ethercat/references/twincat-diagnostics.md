# TwinCAT EtherCAT/CiA402 诊断清单

## ESI 和设备识别

1. 将 ESI XML 放到正确的 TwinCAT ESI 目录。
2. 重启 TwinCAT 或 Reload Device Descriptions。
3. 删除旧设备实例后重新扫描。
4. 检查 Vendor ID、Product Code、Revision、Serial 行为。
5. 若使用 EEPROM/SII，更新 EEPROM 后断电重扫。
6. 测试改动 PDO 时，不要沿用旧的设备实例。

## Online 状态

重点检查：

- EtherCAT State：周期控制期望 OP。
- AL Status Code：记录准确代码。
- WcState：必须 valid。
- Working Counter：输入、输出 WKC 应稳定。
- DC Status：无 Sync0/Sync1 错误。
- Process Data Watchdog：不能超时。

## PDO 页检查

逐项确认：

- RxPDO/TxPDO 对象和固件一致。
- Byte length 与固件 Mapping 长度一致。
- 每个对象 bit length 正确。
- 合并 PDO 中不重复映射 Controlword/Statusword，除非固件明确处理。
- Padding 只在固件同样预期时存在。
- 动态模式切换需要 0x6060/0x6061。

## NC 轴链接

| NC 变量 | 设备对象 |
|---|---|
| Controlword / Drive_Out control | 0x6040 |
| Statusword / Drive_In status | 0x6041 |
| Target position | CSP 使用 0x607A |
| Actual position | 0x6064 |
| Target velocity | CSV/PV 使用 0x60FF |
| Actual velocity | 常用 0x606C |
| Mode command | 动态切换时使用 0x6060 |
| Mode display | 诊断/动态切换时使用 0x6061 |

NC Active/Ready 问题重点看：

- Drive Error 和 NC Error。
- Encoder valid。
- Drive valid。
- CSP/CSV/CST 模式下 0x6041 bit12。
- 0x6061 mode display。
- Position/Encoder scaling。

## Distributed Clocks

多轴周期同步运动建议：

1. 启用从站支持的 DC 模式。
2. Sync0 cycle 与过程数据周期一致。
3. 根据固件时序设置 Sync0 Shift：确认输出映射、应用计算、输入映射的先后关系。
4. 在运动状态下看 DC Diagnostics，不只看空闲状态。
5. 对齐 NC Task、PLC Task、EtherCAT Task、Sync0。
6. 排除实时路径中的日志、共享内存等待、长临界区。

## WcState / invalid IO 排查顺序

多轴同时或随机轴报 invalid IO data：

1. 记录整个从站是否掉 OP，还是只有 NC 轴报错。
2. 看 WcState 跳变位置：Device、Box、Terminal、NC Encoder/Drive。
3. 验证全部轴使能后的 PDO 字节长度。
4. 开启 DC Diagnostics 并与报错时间关联。
5. 检查 TxPDO 是否来自非同步任务。
6. 检查 Process Data Watchdog。
7. 检查共享内存快照/双缓冲。
8. 最后再查线缆、PHY 计数和拓扑。

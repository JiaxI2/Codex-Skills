# EtherCAT MCP 设计清单：可扩展、可维护、默认只读

> 用途：指导后续把 EtherCAT 调试能力做成 MCP。目标不是让 Agent 直接乱写设备，而是建立“可观测、可复现、可回滚”的诊断工具层。
>
> 设计原则：先只读，再有限写；先离线文件分析，再在线设备访问；所有危险动作必须显式确认。

## 1. MCP 总体架构

```text
Agent
  -> ethercat-docs-mcp       # 离线知识库检索
  -> ethercat-project-mcp    # 源码/ESI/日志分析
  -> ethercat-master-mcp     # SOEM/IgH/TwinCAT 后端只读诊断
  -> ethercat-twincat-mcp    # ADS/Automation Interface 读状态
  -> ethercat-capture-mcp    # Wireshark/tshark 抓包解析
  -> ethercat-lab-mcp        # 串口/J-Link/RTT/日志读取
```

建议分层实现，不要做一个巨型 MCP。每个 MCP 都定义清楚输入、输出、权限和风险等级。

## 2. 必做 MCP 列表

### 2.1 `ethercat-docs-mcp`：离线文档 RAG

**优先级：最高。**

功能：

- 检索本 Skill 的 `references/`。
- 检索 ETG/CiA402/ET9300 蒸馏版摘要。
- 按关键词路由到 ref：WKC、FMMU、SM、DC、CiA402、SSC、FoE、TwinCAT。
- 输出“来源层级”：规范/SSC/开源实现/项目代码/用户日志。

接口建议：

```text
search_docs(query, scope?)
get_ref(name)
route_topic(query) -> [ref files]
explain_term(term)
```

维护策略：

- refs 版本化；每个 ref 有 `last_checked` 和 `source_level`。
- 禁止把受限文档原文全文索引给外部用户；只索引工程化摘要。

### 2.2 `ethercat-project-mcp`：源码/ESI/日志分析

**优先级：最高。**

功能：

- 解析 ESI XML：PDO、SM、FMMU、DC、InitCmd、Identity。
- 解析 TwinCAT/IgH/SOEM 日志。
- 搜索工程中的 `0x6040/0x6041/0x6060/0x6061`、`PDO_OutputMapping`、`InputMapping`、Sync0 ISR。
- 对比 ESI 与 C 对象字典/PDO mapping。

接口建议：

```text
parse_esi(path)
compare_esi_with_code(esi_path, source_root)
find_cia402_objects(source_root)
analyze_log(path, kind)
check_pdo_consistency(esi_path, expected_json?)
```

输出结构：

```json
{
  "severity": "error|warning|info",
  "layer": "ESI|OD|PDO|DC|CiA402|TwinCAT|SSC",
  "evidence": "...",
  "fix_hint": "..."
}
```

### 2.3 `ethercat-master-mcp`：SOEM/IgH 在线只读诊断

**优先级：高。**

功能：

- 扫描从站。
- 读取主站/从站状态。
- 读取 AL status code、WKC、domain state。
- SDO upload 常见对象。
- 读取 ESC 寄存器只读项，例如 DL status、AL status、DC time。

接口建议：

```text
scan_slaves()
get_slave_state(slave)
get_wkc_stats()
read_sdo(slave, index, subindex, datatype?)
read_cia402(slave)  # 603F/6040/6041/6060/6061/6064/607A
read_esc_reg(slave, address, length)
```

默认禁用：

```text
write_sdo()
force_state()
fault_reset()
foe_download()
```

这些写操作必须二次确认，并输出风险提示。

### 2.4 `ethercat-twincat-mcp`：TwinCAT/ADS 诊断

**优先级：高。**

功能：

- 通过 ADS 读 PLC/NC/EtherCAT 设备变量。
- 读取轴状态、WcState、Drive/Encoder valid、当前模式、错误码。
- 可选：读取 TwinCAT 工程 XML/TMC/tsproj。

接口建议：

```text
list_ads_routes()
read_ads_symbol(symbol)
read_axis_state(axis_name)
read_ecat_device_state(device_path)
read_cia402_via_ads(axis_or_slave)
```

维护策略：

- ADS 路由和 AMS Net ID 不写进仓库。
- 只读默认；写 PLC/NC 变量必须显式确认。

### 2.5 `ethercat-capture-mcp`：抓包解析

**优先级：中高。**

功能：

- 调用 `tshark` 解析 pcapng。
- 提取 EtherCAT datagram、command、address、length、WKC。
- 标记 WKC 变化、CoE SDO abort、FoE error。
- 输出周期抖动和丢包时间点。

接口建议：

```text
parse_pcap(path)
find_wkc_anomalies(path)
extract_sdo_transactions(path)
extract_foe_transactions(path)
summary_dc_timing(path)
```

### 2.6 `ethercat-lab-mcp`：实验室硬件观测

**优先级：中。**

功能：

- 读取串口/RTT/J-Link 日志。
- 拉取 MCU 变量快照，尤其 Sync0 count、RxPDO count、TxPDO count、CiA402 state。
- 配合 Agent 对齐主站日志和从站日志时间戳。

接口建议：

```text
read_serial(port, baud, duration)
read_rtt(channel, duration)
read_symbol_snapshot(symbols)
align_logs(master_log, slave_log)
```

## 3. MCP 权限模型

| 等级 | 操作 | 默认 |
|---|---|---|
| L0 | 离线文档/源码/日志读取 | 允许 |
| L1 | 在线只读：SDO upload、状态读取、ADS read | 允许，但标注目标设备 |
| L2 | 在线低风险写：清日志、读配置缓存刷新 | 需确认 |
| L3 | 控制类写：SDO download、状态强制、fault reset、NC enable | 严格确认 |
| L4 | 运动/安全/固件：启动轴、FoE OTA、写 Flash、安全 IO | 默认禁止，必须人工确认和现场安全条件 |

## 4. 下一步实施路线

### 第 1 阶段：离线能力

1. 建 `ethercat-docs-mcp` 或简单本地检索工具。
2. 建 `ethercat-project-mcp` 的 `parse_esi()` 与 `check_pdo_consistency()`。
3. 给当前 Skill 增加 `mcp-design` ref 和使用说明。

### 第 2 阶段：只读在线诊断

1. SOEM 后端：实现 `scan_slaves/read_sdo/read_cia402/get_wkc`。
2. IgH 后端：封装命令行或库 API。
3. TwinCAT 后端：ADS read，先读变量和状态，不写。

### 第 3 阶段：闭环排障

1. 把主站 WKC、TwinCAT WcState、从站 Sync0 count、CiA402 state 对齐到统一报告。
2. 生成“故障时间线”。
3. 只在人工确认后允许执行 fault reset 或 SDO 写。

## 5. 可扩展目录建议

```text
tools/
  mcp/
    ethercat-docs-mcp/
    ethercat-project-mcp/
    ethercat-master-mcp/
    ethercat-twincat-mcp/
    ethercat-capture-mcp/
  schemas/
    esi-summary.schema.json
    cia402-snapshot.schema.json
    diagnosis-report.schema.json
  fixtures/
    esi/
    logs/
    pcap/
```

统一输出 schema 比工具本身更重要。只要 schema 稳定，后端可以从 SOEM 换 IgH，也可以从 TwinCAT ADS 换工程 XML 解析。

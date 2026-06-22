# EtherCAT Skill / Ref / MCP 维护路线图

> 用途：确保 EtherCAT 知识库可长期扩展，不因 ref 越堆越多而失控。

## 1. 当前知识库分层

```text
L0 规范蒸馏
  ETG.1000 / ETG.6010 / CiA402 / ET9300
L1 协议速读
  ethercat-deep-dive-agent-ref.md
L2 工程专题
  SSC、TwinCAT、网页知识库转写、多轴、CoE/PDO、PHY/EEPROM
L3 开源实现
  SOEM/IgH/SOES/CiA402/LinuxCNC/ROS2/fastcat
L4 工具化
  MCP、脚本、ESI 检查、日志分析、在线只读诊断
```

## 2. 新增 ref 时的模板

每个 ref 必须包含：

```yaml
purpose: 这个 ref 解决什么问题
source_level: spec | official-doc | open-source | project-experience | forum-experience
last_checked: YYYY-MM-DD
use_when:
  - 触发关键词
  - 典型问题
not_for:
  - 不适用边界
maintenance:
  - 怎么更新
```

正文必须包括：

1. 一句话判断模型。
2. 关键对象/寄存器/函数入口。
3. 检查路径。
4. 常见错误。
5. 最小修复策略。

## 3. 正确性检查机制

| 检查项 | 方法 |
|---|---|
| 规范语义 | 对照 ETG/CiA/ET9300 蒸馏 ref |
| 开源项目事实 | 对照官方 README/文档，记录 last_checked |
| 代码路径 | 不确定时写“常见入口/请由 repo MCP 实时确认” |
| 危险操作 | 写入、使能、运动、OTA、fault reset 默认禁止 |
| 厂商敏感词 | 打包前 grep 扫描 |

## 4. 推荐仓库结构

```text
ethercat-cia402/
  SKILL.md
  README.md
  references/
    00-index.md
    protocol/
    slave/
    master/
    cia402/
    diagnostics/
    mcp/
  scripts/
    decode_cia402.py
    parse_esi.py        # 下一步可加
    check_pdo_map.py    # 下一步可加
  evals/
    evals.json
```

当前为了兼容旧 Skill，新增 ref 仍放在 `references/` 根目录。后续 ref 超过 20 个时建议按子目录重排。

## 5. 版本化建议

- `v0.1`：手工 ref + decode script。
- `v0.2`：新增开源项目蒸馏 + MCP 设计。
- `v0.3`：新增 ESI parser / PDO checker。
- `v0.4`：新增 SOEM 只读 MCP。
- `v0.5`：新增 TwinCAT ADS 只读 MCP。
- `v1.0`：形成“离线知识库 + 代码/ESI/日志分析 + 在线只读诊断”的稳定闭环。

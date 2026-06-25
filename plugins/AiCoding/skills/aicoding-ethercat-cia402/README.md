# ethercat-cia402 中文 Skill

这是一个面向 Codex Agent Skills 的 EtherCAT/CiA402 中文技能包，用于嵌入式 EtherCAT 伺服驱动开发和排障。

## 安装位置

将整个目录复制到以下任一位置：

```text
# 仓库级，团队共享
<your-repo>/.agents/skills/ethercat-cia402/

# 用户级，所有仓库可用
$HOME/.agents/skills/ethercat-cia402/
```

核心文件为：

```text
SKILL.md
```

## 推荐用法

显式调用：

```text
$ethercat-cia402 帮我分析 TwinCAT invalid IO data / WcState 问题
```

隐式调用：

```text
TwinCAT 上电后 0x6060=8，但 0x6061=0，NC 仍像 PP 模式，应该查哪里？
```

## 辅助脚本

```bash
python scripts/decode_cia402.py --statusword 1591 --mode 8
python scripts/decode_cia402.py --controlword 0x000F --statusword 0x0637
```

## 文件结构

```text
ethercat-cia402/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── evals/
│   └── evals.json
├── references/
│   ├── ethercat-cia402-quick-reference.md
│   ├── ethercat-web-knowledge-index.md
│   ├── ssc-et9300-notes.md
│   ├── troubleshooting-playbooks.md
│   ├── twincat-diagnostics.md
│   ├── web-cia402-mdp-multiaxis.md
│   ├── web-coe-pdo-eoe-twincat.md
│   ├── web-phy-eeprom-hardware.md
│   ├── web-ssc-sync-errors.md
│   └── source-map.md
└── scripts/
    └── decode_cia402.py
```



## 网页知识库本地化 ref

本版本已把 EtherCAT 网页文章内容拆分为 5 个本地 ref。使用时不要再让 Agent 临时访问网页，直接按问题关键词读取对应文件：

| 场景 | 读取 ref |
|---|---|
| Module/Slot、MDP、CIA402 多轴、2轴扩 8轴、TwinCAT 多生成 Axis | `references/web-cia402-mdp-multiaxis.md` |
| 0x1A/0x1B/0x2C、Sync0 watchdog、PDI/Sync 中断、SSC Tool 同步参数 | `references/web-ssc-sync-errors.md` |
| CoE、OD、SDO/PDO、动态 PDO、EoE、TwinCAT PLC 任务、输入到输出延时 | `references/web-coe-pdo-eoe-twincat.md` |
| PHY、Link、EEPROM、ESC 引脚、RUN/ERR LED、扫描不到从站、地址/别名/Explicit Device ID | `references/web-phy-eeprom-hardware.md` |
| 不确定该读哪个 | `references/ethercat-web-knowledge-index.md` |

这些 ref 是工程化转写与重组，不包含原网页品牌词、原始链接或大段原文。用于 Agent 快速理解背景、选择检查路径和给出代码/配置建议。


## 新增：EtherCAT 深度速读参考

`references/ethercat-deep-dive-agent-ref.md` 是离线深度速读 ref，用于让 Agent 在不联网的情况下快速理解 EtherCAT 的协议层级和工程排障路径。

优先读取场景：

- 用户问 EtherCAT 协议栈、帧格式、Datagram、WKC；
- 用户问 ESC、FMMU、Sync Manager、SII EEPROM、AL/ESM；
- 用户问 CoE/SDO/PDO、ESI、SM assign、动态 PDO；
- 用户问 DC、Sync0/Sync1、watchdog、WcState、invalid IO data；
- 用户问 SSC/ET9300 工程结构和 `PDO_OutputMapping()` / `PDO_InputMapping()` / `ECAT_Application()`；
- 用户要求构建 Agent Skill、离线知识库或快速排障参考。


## 新增：开源项目蒸馏与 MCP 设计

本版本新增 6 个离线 ref，用于把开源主站、从站、CiA402、LinuxCNC/ROS2 和 MCP 设计纳入本地知识库：

```text
references/
├── ethercat-master-source-map-soem-igh.md
├── ethercat-slave-source-map-ssc-soes.md
├── cia402-open-source-implementation-map.md
├── twincat-linuxcnc-ros2-diagnostics-map.md
├── ethercat-mcp-design.md
├── ethercat-project-selection-guide.md
└── ethercat-maintenance-roadmap.md
```

推荐读取逻辑：

| 场景 | 读取 ref |
|---|---|
| 主站、WKC、SDO、SOEM、IgH、Linux 实时线程 | `references/ethercat-master-source-map-soem-igh.md` |
| 从站栈、SSC/ET9300、SOES、PDI、OutputMapping/InputMapping、FoE | `references/ethercat-slave-source-map-ssc-soes.md` |
| CiA402 状态机、6040/6041、6060/6061、CSP/CSV/CST、fault reset | `references/cia402-open-source-implementation-map.md` |
| TwinCAT / LinuxCNC / ROS2 轴诊断 | `references/twincat-linuxcnc-ros2-diagnostics-map.md` |
| MCP 工具化、ESI 解析、SOEM/IgH/TwinCAT 只读诊断、抓包解析 | `references/ethercat-mcp-design.md` |
| 不确定应该参考哪个项目 | `references/ethercat-project-selection-guide.md` |
| 后续维护与版本计划 | `references/ethercat-maintenance-roadmap.md` |
```

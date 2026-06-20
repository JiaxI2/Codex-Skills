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

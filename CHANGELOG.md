# 更新日志

## 2026-06-25

### 新增

- **feat**：新增 `platform/aicoding-kit-maintenance/`，定义 Codex-Skills/AiCoding 双仓库维护流程，明确 AGENTS 边界、架构文档、config/scripts 执行入口以及 Git hooks/CI 完成门禁。
- **docs**：新增根 `AGENTS.md`、`plugins/AiCoding/AGENTS.md` 和 `docs/PLUGIN_DEVELOPMENT.md`，明确人工维护区、自动生成区、Hook 辅助边界和跨仓库发布顺序。
- 新增 `skill-creator/`，将原 Anthropic skill creator 迁移为 Codex/OpenCode Agent Skill 创建、迁移和验证工作流。
- 新增 `platform/aicoding-user-skill-creator/scripts/skill_gate.py`，用于判断是否应该创建 skill、分类四类 skill，并阻塞缺失 workflow contract、gate rules 或人工确认的标准/流程类 skill。

### 更新

- 更新 `embedded/C99/`，把 C99 编码规范补充为 `consistent-workflow`、`organization-standard` 和 `team-expertise` 类型，并要求可机器检查规则落成 CLI/Hook/Lint/CI 门禁。
- 更新 `embedded/architecture/`，把架构平台化规范补充为四类 skill，并要求架构边界、发布门禁和量产约束优先机器化为阻塞规则。
- 更新 `README.md`，加入 `platform/aicoding-user-skill-creator/` 目录说明，并改为依赖 Git 管理 user-level skill 变更，避免散落临时备份。
- **docs**：更新 `embedded/git/` 提交治理规则，要求每次提交明确 `feat/fix/docs/style/refactor/perf/test/chore/build/ci` 类型，在 CHANGELOG 记录类型和影响，并通过 lint/hook 管理提交消息与 CHANGELOG 门禁。
- **docs**：新增 `embedded/git/references/repository-initialization.md`，把 Git 仓库初始化标准化为本地同步空远程、远程优先绑定本地、克隆已有远程、本地引导、模板引导和 submodule 感知初始化，并要求通过 CLI 配置 `.githooks` 后运行 hook/lint 验证。
- **docs**：补充大厂式 Git 分支/环境映射和单次提交纪律，覆盖 `main/develop/feature/test/release/hotfix`、`DEV/FAT/UAT/PRO`、同类提交、不超过 3 个议题以及禁止默认使用破坏性 reset。
- **feat**：新增 `plugins/AiCoding/`，按 Codex 官方 plugin 结构生成扁平化 `aicoding-*` skills、Codex lifecycle hooks 和 `BUILDINFO.json`，用于新电脑安装 AiCoding 嵌入式 Codex kit。
- **refactor**：将 `embedded/git/` 迁移为 `platform/aicoding-git-governance/`，把 Git-Skill 明确归类为跨领域平台治理能力。
- **build**：新增 `config/aicoding-plugin-pack.json`、`scripts/build-plugin.ps1`、`scripts/verify-plugin.ps1`、`scripts/compare-generated.ps1` 和 `scripts/verify-skills.ps1`，支持可重复构建、生成目录校验和构建漂移检查。
- **docs**：新增 `docs/ARCHITECTURE.md`，明确人工维护目录与自动生成目录、BUILDINFO 非自引用模型、local plugin 缓存刷新方式、CodingKit 外部资产发现协议、Hook 辅助边界以及禁止 AiCoding 在 submodule 中重新构建 Plugin。
- **docs**：将 `embedded/git/` 的 skill 名称从 `embedded-git-workflow` 改为 `Git-Skill`（frontmatter `name: git-skill`），保留嵌入式路径定位，同时说明其嵌入式优先、可通用的 Git 治理边界。

### 移除

- 移除旧的 `anthropic-skill-creator/` 路径，后续统一使用 `skill-creator/`。
## 2026-06-22

### 新增

- **feat**：新增 `platform/aicoding-kit-maintenance/`，定义 Codex-Skills/AiCoding 双仓库维护流程，明确 AGENTS 边界、架构文档、config/scripts 执行入口以及 Git hooks/CI 完成门禁。
- **docs**：新增根 `AGENTS.md`、`plugins/AiCoding/AGENTS.md` 和 `docs/PLUGIN_DEVELOPMENT.md`，明确人工维护区、自动生成区、Hook 辅助边界和跨仓库发布顺序。
- 新增 `embedded/git/`，覆盖嵌入式仓库分支、提交、PR、Tag、Release、README、CHANGELOG、版本文件、固件制品、测试基线、生产基线和客户交付治理。
- 新增 EtherCAT 开源项目与 MCP 设计参考，包含 SOEM/IgH、SSC/SOES、CiA402 开源实现、TwinCAT/LinuxCNC/ROS2 诊断、项目选型和维护路线。

### 更新

- 更新 `embedded/SKILL.md`、`embedded/readme.md` 和 `embedded/agents/openai.yaml`，将 Git/发布治理纳入嵌入式 skill 路由。
- 扩展 `embedded/ethercat/SKILL.md`、`embedded/ethercat/README.md` 和评估数据，增加新增参考资料的读取规则。
- `.gitignore` 增加 `*.bak-*`，避免本地备份文件误提交。
- 从 `README.md` 移除日期型 diff 摘要，并在 `embedded/git` 规则中明确 diff 摘要应进入 CHANGELOG、Tag 或 Release Notes。
- 收紧 `embedded/git` 的 GitHub Release 规则和模板：创建 Release 时必须包含 Deprecations、Full Changelog、New Contributors 等完整章节，非适用项写 `None`。
- 调整 Release 语言策略：中文仓库默认中文，首次创建 GitHub Release 需确认语言；Release Notes 模板和校验脚本支持中文优先的中英双语标题。

## 2026-06-20

### Diff 概览

- `embedded/c99-standard-c/` 删除并迁移至 `embedded/C99/`。
- 新增 `embedded/architecture/` 及其架构审查模板和参考资料。
- 扩充 `embedded/motorcontrol/` 的算法、时序、多轴、测试和参考工程资料。
- 扩充 `embedded/ethercat/` 的 EtherCAT/CiA402、TwinCAT、SSC/ET9300、DC 和故障排查资料，并新增解码脚本与评估数据。
- 更新 `embedded/SKILL.md`、相关 `agents/openai.yaml`、仓库 README 和发布说明。

### C99 通用规范

- 将当前 C99 Skill 作为唯一通用 C 编码规范，不保留来源 Skill 的品牌或重复触发词。
- 修改前必须判断项目自研、自动生成或第三方代码。
- 自动生成和第三方代码默认保持实际编码及局部风格。
- 新项目和项目自研代码统一命名、4 空格、大括号、函数头及函数内部注释规则。
- 新增或大改函数记录作者、日期、原因以及必要的缺陷根因和修复方式。
- 项目自研代码非 GBK 时必须询问是否转换；第三方和生成代码保持实际编码。

### 嵌入式架构与电机控制

- 新增 architecture Skill，明确系统架构与控制算法的职责边界。
- 增加 Bootloader、OTA、A/B、Manifest、参数区、校准区和量产发布门禁。
- motorcontrol 增加 PWM/ADC/Encoder 同步、FOC/SVPWM、三环带宽、补偿、多轴同步及故障验证资料。
- 增加 VESC、ODrive、moteus、ODRI、PX4、ArduPilot、Betaflight 和 TI SDK 的参考边界说明。

### EtherCAT/CiA402

- 强化 EtherCAT 从站、CiA402 状态机、TwinCAT 联调、PDO/SDO/CoE 和 DC 同步规则。
- 新增 SSC/ET9300、Working Counter、WcState、AL/ESM、NC 轴 Ready 和多轴同步排查资料。
- 新增 `scripts/decode_cia402.py`、`evals/evals.json` 和专项参考索引。

### 发布

- 发布 tag：`v2026.06.20`。
- README 增加当前版本的路径级 diff 摘要。

## 2026-06-17

### 新增

- **feat**：新增 `platform/aicoding-kit-maintenance/`，定义 Codex-Skills/AiCoding 双仓库维护流程，明确 AGENTS 边界、架构文档、config/scripts 执行入口以及 Git hooks/CI 完成门禁。
- **docs**：新增根 `AGENTS.md`、`plugins/AiCoding/AGENTS.md` 和 `docs/PLUGIN_DEVELOPMENT.md`，明确人工维护区、自动生成区、Hook 辅助边界和跨仓库发布顺序。
- 建立 `Codex-Skills` 远程同步仓库结构。
- 新增中文 `README.md`，说明仓库用途、目录、排除规则和维护方式。
- 新增此 `CHANGELOG.md`，记录 skills 仓库变更。

### embedded

- `embedded` 增加独立 `SKILL.md` 作为一级 skill 入口。
- `embedded/readme.md` 改为二级 skill 分流说明，避免 `c99-standard-c`、`review` 和领域 skill 冗余调用。
- `embedded/review` 增加 MaJerle/c-code-style 中文评审参考：
  - `review/references/majerle-c-code-style-review-cn.md`
  - 明确该参考只用于风格、Doxygen、命名、格式化和头/源文件组织评审。
  - 明确兼容优先级：项目规范 > `c99-standard-c` > MaJerle 风格参考。
- `embedded/c99-standard-c` 保持 C99、安全、实时性、并发、寄存器和可移植性规则的优先级。

### 同步策略

- 排除 `.system/`、`backup/`、`*.zip` 和缓存文件。
- 使用独立 git 仓库管理 `C:\Users\24322\.codex\skills`，避免误提交上层用户目录。

# Codex-Skills

English documentation / 英文文档: [README.md](README.md).

`Codex-Skills` 是可复用 Codex Skill、AiCoding Plugin 源码、Codex lifecycle hooks 和个人 standalone skills 的源码仓库。

## 仓库定位

- 维护 `embedded/`、`platform/` 和根目录 standalone skills 的 canonical source。
- 生成 `plugins/AiCoding`，作为可安装的 AiCoding Codex Plugin 包。
- 备份个人 standalone skills，例如 `obsidian-markdown`、`drawio`、`frontend-design`、`webapp-testing` 等。
- 不应把整个仓库作为用户运行时 Skill Root 长期暴露；运行时应只暴露明确安装的 standalone skill 或已安装 plugin 中的 `aicoding-*` skill。

## 状态

- 当前仓库是 Codex skills 和 AiCoding plugin packaging 的 canonical source tree。
- 生成的 plugin 副本是构建产物，不是可手工编辑的源文件。
- Release notes、CHANGELOG 和 README 治理均以 `.github/repository-governance.toml` 为准。

## 快速开始

```powershell
git clone https://github.com/JiaxI2/Codex-Skills.git
cd Codex-Skills
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify-skills.ps1
```

## 架构

详见 [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)。

简要结构：

- `embedded/` 存放嵌入式领域 skill 源码。
- `platform/` 存放跨领域平台 workflow skill，包括 Git 治理。
- `plugins/AiCoding/skills/` 由 `config/aicoding-plugin-pack.json` 生成，不手工编辑。
- `plugins/AiCoding/hooks/` 是手工维护的 plugin hook 源码。
- `.agents/plugins/marketplace.json` 是本地 plugin 测试用 development marketplace。

## 目录说明

- `embedded/`：嵌入式固件 skill 族，包括 C99、架构、ARM、DSP、EtherCAT/CiA402、OS、电机控制和评审路由。
- `platform/aicoding-git-governance/`：Git-Skill 源码，覆盖分支、提交、CHANGELOG、Release、hook 和仓库治理。
- `platform/aicoding-kit-maintenance/`：Codex-Skills/AiCoding 架构、plugin packaging、submodule、hooks 和完成门禁维护 workflow。
- `platform/aicoding-sdd-bdd-tdd-development-flow/`：SDD、MVP、BDD、架构优先、TDD fallback、分层验证和文档同步 workflow。
- `platform/aicoding-user-skill-creator/`：User-Skill-Creator 源码，用于创建、验证、改进和迁移 AiCoding user skills。
- `plugins/AiCoding/`：生成/可安装的 Codex plugin 包，包含手工维护 manifest/hooks 和生成的 skills/BUILDINFO。
- `config/aicoding-plugin-pack.json`：AiCoding Plugin 打包清单的唯一来源。
- `scripts/build-plugin.ps1`：可复现 plugin 生成脚本。
- `scripts/verify-plugin.ps1`：plugin 包验证脚本。
- `scripts/compare-generated.ps1`：重复构建漂移检查脚本。
- 根目录 `obsidian-*` 等 standalone skill 默认不进入 AiCoding Plugin。

## 构建和验证

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/build-plugin.ps1 -Plugin AiCoding -Configuration Development -Clean -Verify
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/compare-generated.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify-skills.ps1
```

正式 release build 只应在排除生成 plugin 输出的干净 source tree 中使用 `-Configuration Release`。

## 运行时原则

- `aicoding-*` 成组能力通过 AiCoding Plugin 暴露。
- standalone skill 通过用户 Skill Root 的独立目录或链接暴露。
- 不手工编辑 `plugins/AiCoding/skills/` 或 `plugins/AiCoding/BUILDINFO.json`。
- 不直接修改 Codex plugin cache。

## Git 治理标准

所有 AiCoding 管理的 Git 仓库都应在 README 或等价治理文档中写明分支、环境、提交类型和 Release 说明规则，方便后续维护。

- 分支：`main` 或 `master` 是稳定生产分支，除批准的 release/hotfix 集成外不得直接改代码；`develop` 是 DEV 集成分支；`feature/<scope>` 从 `develop` 创建；存在共享测试环境时 `test` 对应 FAT；`release/<version>` 对应 UAT/预上线；`hotfix/<scope>` 从 `main` 创建，并回合到 `main` 和 `develop`。
- 环境：`DEV` 用于开发调试，`FAT` 用于功能验收测试，`UAT` 用于用户验收/预生产，`PRO` 用于生产。
- 提交类型：`feat` 新增功能，`fix` 修复 bug，`docs` 仅文档变更，`style` 仅格式/空白等不影响语义的变更，`refactor` 既不修 bug 也不加功能的代码重构，`perf` 性能改进，`test` 添加或修正测试，`chore` 构建、辅助工具或维护文件变更。
- 单次提交：一个 commit 只放一类变更，议题不超过 3 个，并使用 `feat(scope): summary` 这类 typed subject。
- Release：Tag 和 GitHub Release 必须按类型汇总本次包含的全部提交，说明本次 release 主类型，并写清具体影响。

## 文档和支持

- [英文文档](README.md)
- [架构说明](docs/ARCHITECTURE.md)
- [Plugin 开发说明](docs/PLUGIN_DEVELOPMENT.md)
- [贡献指南](CONTRIBUTING.md)
- [安全策略](SECURITY.md)
- [问题反馈](https://github.com/JiaxI2/Codex-Skills/issues)
- [许可证](LICENSE)

## 更新日志和发布

- [更新日志](CHANGELOG.md)
- [最新版本](https://github.com/JiaxI2/Codex-Skills/releases/latest)
- [全部 Release](https://github.com/JiaxI2/Codex-Skills/releases)

diff 摘要应放在 `CHANGELOG.md`、annotated Tag message 或 GitHub Release notes 中，不放在 README 中。

## 维护规则

- 每个 skill source 只保留一个权威位置；生成的 plugin 副本不是源码。
- 每次普通 commit 都要评估并更新 `CHANGELOG.md`，且明确 commit type。
- Codex hooks 和 Git hooks 分开维护。
- 不把 `obsidian-*` 打包进 AiCoding。
- 不在 plugin 文件、hooks、scripts 或 README 文件中硬编码个人绝对路径。
- 不在 AiCoding submodule checkout 内重建 AiCoding plugin；应在 Codex-Skills 中构建、提交，再更新 AiCoding submodule pointer。
- Kit 维护任务按 `AGENTS.md`、`platform/aicoding-kit-maintenance/SKILL.md`、`docs/ARCHITECTURE.md` 和 `docs/PLUGIN_DEVELOPMENT.md` 顺序执行。

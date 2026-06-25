# Git-Skill

嵌入式优先、可通用的 Codex Git/Release Skill。

它不是固定模仿 Linux、OpenAI、PX4、Git Flow 或某个 README 模板，而是：

1. 先识别项目问题和约束；
2. 组合选择 profile；
3. 通过 Quick Ref 快速读取和应用；
4. 使用配置、模板和脚本保持一致；
5. 对普通 commit、Tag 和 GitHub Release 做严格区分。

## 定位

`Git-Skill` 的插件内触发名是 `$aicoding-git-governance`，源码路径为 `platform/aicoding-git-governance/`，因为 Git 治理属于跨领域平台能力，但主要服务 AiCoding 嵌入式开发发布流程。

## 安装

```text
<REPO_ROOT>/.agents/skills/platform/aicoding-git-governance/
```

建议把 `assets/AGENTS_SNIPPET.md` 合并到仓库根目录 `AGENTS.md`。

## 仓库配置

复制：

```text
assets/REPOSITORY_GOVERNANCE_TEMPLATE.toml
```

到：

```text
.github/repository-governance.toml
```

这是本 Skill 使用的自定义治理配置，不是 GitHub 内置文件。

## Quick Ref

```text
$aicoding-git-governance ref readme open-source-firmware
$aicoding-git-governance ref changelog unreleased
$aicoding-git-governance ref branch environment-promotion
$aicoding-git-governance ref release firmware-minor
$aicoding-git-governance ref tag
$aicoding-git-governance ref links
```

## 自动化

生成启用的模板：

```bash
python .agents/skills/platform/aicoding-git-governance/scripts/render_governance_templates.py \
  --config .github/repository-governance.toml \
  --output-dir .
```

验证 Markdown：

```bash
python .agents/skills/platform/aicoding-git-governance/scripts/validate_markdown_links.py \
  README.md CHANGELOG.md
```

验证 Release Notes：

```bash
python .agents/skills/platform/aicoding-git-governance/scripts/validate_release_notes.py \
  --config .github/repository-governance.toml \
  RELEASE_NOTES.md
```
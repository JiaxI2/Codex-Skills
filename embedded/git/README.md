# Git-Skill

嵌入式优先、可通用的 Codex Git/Release Skill。

它不是固定模仿 Linux、OpenAI、PX4、Git Flow 或某个 README 模板，而是：

1. 先识别项目问题和约束；
2. 组合选择 profile；
3. 通过 Quick Ref 快速读取和应用；
4. 使用配置、模板和脚本保持一致；
5. 对普通 commit、Tag 和 GitHub Release 做严格区分。

## 定位

`Git-Skill` 的触发名是 `$git-skill`，物理路径仍保留在 `embedded/git/`，因为主要使用场景是嵌入式开发中的 Git、发布、基线和交付治理。

## 安装

```text
<REPO_ROOT>/.agents/skills/embedded/git/
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
$git-skill ref readme open-source-firmware
$git-skill ref changelog unreleased
$git-skill ref branch environment-promotion
$git-skill ref release firmware-minor
$git-skill ref tag
$git-skill ref links
```

## 自动化

生成启用的模板：

```bash
python .agents/skills/embedded/git/scripts/render_governance_templates.py \
  --config .github/repository-governance.toml \
  --output-dir .
```

验证 Markdown：

```bash
python .agents/skills/embedded/git/scripts/validate_markdown_links.py \
  README.md CHANGELOG.md
```

验证 Release Notes：

```bash
python .agents/skills/embedded/git/scripts/validate_release_notes.py \
  --config .github/repository-governance.toml \
  RELEASE_NOTES.md
```
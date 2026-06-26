# Codex-Skills

`Codex-Skills` 是可复用 Codex Skill、AiCoding Plugin 源码、Codex lifecycle hooks 和个人 standalone skills 的源码仓库。

## 仓库定位

- 维护 `embedded/`、`platform/` 和根目录 standalone skills 的 canonical source。
- 生成 `plugins/AiCoding`，作为可安装的 AiCoding Codex Plugin 包。
- 备份个人 standalone skills，例如 `obsidian-markdown`、`drawio`、`frontend-design`、`webapp-testing` 等。
- 不应把整个仓库作为用户运行时 Skill Root 长期暴露；运行时应只暴露明确安装的 standalone skill 或已安装 plugin 中的 `aicoding-*` skill。

## 目录说明

- `embedded/`：嵌入式固件 skill 族，包括 C99、架构、ARM、DSP、EtherCAT/CiA402、OS、电机控制和评审路由。
- `platform/`：跨领域平台 workflow skill，例如 Git 治理、Kit 维护和用户 skill 创建。
- `plugins/AiCoding/`：AiCoding Codex Plugin 包；`skills/` 和 `BUILDINFO.json` 为生成内容。
- `config/aicoding-plugin-pack.json`：唯一的 AiCoding Plugin 打包清单。
- `scripts/`：构建、验证、漂移检查和维护脚本。
- 根目录 standalone skill：个人/工具类 skill，默认不进入 AiCoding Plugin。

## 构建和验证

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/build-plugin.ps1 -Plugin AiCoding -Configuration Development -Clean -Verify
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/compare-generated.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify-skills.ps1
```

## 运行时原则

- `aicoding-*` 成组能力通过 AiCoding Plugin 暴露。
- standalone skill 通过用户 Skill Root 的独立目录或链接暴露。
- 不手工编辑 `plugins/AiCoding/skills/` 或 `plugins/AiCoding/BUILDINFO.json`。
- 不直接修改 Codex plugin cache。

## 相关文档

- [English README](README.md)
- [架构说明](docs/ARCHITECTURE.md)
- [Plugin 开发说明](docs/PLUGIN_DEVELOPMENT.md)
- [更新日志](CHANGELOG.md)
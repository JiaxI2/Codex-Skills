# Codex Skills 仓库

这是个人 Codex skills 仓库，用于同步 `C:\Users\24322\.codex\skills` 下的可复用 skill。

## 仓库用途

- 备份和版本管理个人 Codex skills。
- 在不同机器之间同步常用工作流、参考资料和领域规则。
- 记录 embedded、文档、图表、Obsidian、前端、MCP 等 skill 的演进。

## 目录说明

- `embedded/`：嵌入式一级 skill，包含 C99、architecture、review、ARM、DSP、EtherCAT/CiA402、OS、电机控制等二级 skill。
- `karpathy-guidelines/`：Karpathy 风格开发指南。
- `frontend-design/`、`webapp-testing/`、`web-artifacts-builder/`：前端设计、实现和测试相关 skill。
- `drawio/`、`json-canvas/`：图表和可视化结构化文档相关 skill。
- `obsidian-*`：Obsidian vault、Markdown、Bases 等工作流。
- `anthropic-*`、`codex-documents-anthropic-docx/`：文档、表格、幻灯片等参考或桥接 skill。
- 其他目录为不同任务领域的独立 skill。

## 不同步内容

本仓库默认不提交以下内容：

- `.system/`：Codex/OpenAI 系统内置 skill。
- `**/backup/`：本地变更备份。
- `*.zip`：临时导出包或压缩归档。
- OS、编辑器、缓存和临时文件。

## 使用方式

1. 将仓库同步到 Codex skills 目录。
2. 保持每个 skill 使用独立目录，并包含 `SKILL.md`。
3. 对需要延迟加载的长文档放入 `references/`。
4. 对 Codex App UI 元数据使用 `agents/openai.yaml`。
5. 修改 user-level skill 前先备份，再提交变更。

## embedded 分流约定

`embedded/SKILL.md` 负责二级 skill 分流：

- 实现 C 模块时必须使用 `embedded/C99`（skill 名称：`c99-standard-c`）。
- 代码审查时优先使用 `embedded/review`。
- 风格、Doxygen、格式化、命名审查使用 `embedded/review/references/majerle-c-code-style-review-cn.md`。
- 系统分层、平台抽象、Bootloader、OTA 和量产发布使用 `embedded/architecture`。
- EtherCAT 从站、CiA402、TwinCAT、PDO/SDO、DC 和 SSC/ET9300 使用 `embedded/ethercat`。
- FOC、SVPWM、三环控制、采样时序和多轴控制使用 `embedded/motorcontrol`。
- 其他领域任务按需使用 `arm`、`dsp`、`os` 和 `review`。
- 不为单一任务重复加载多个同级 skill；只选主 skill，必要时补充一个辅助 skill。

## 2026-06-20 diff 摘要

- `embedded/c99-standard-c/` 迁移为 `embedded/C99/`：统一文件归属、实际编码、固定格式、函数注释、修改记录、安全和可移植性规则；新增 `references/c-coding-rules-zh.md`。
- 新增 `embedded/architecture/`：覆盖职责分层、真实变化点、Bootloader/OTA、量产约束、参考工程矩阵及测试发布门禁。
- 扩展 `embedded/motorcontrol/`：补充 PWM/ADC/Encoder 时序、三环带宽、补偿、多轴同步、参考工程和测试模板。
- 扩展 `embedded/ethercat/`：升级为 EtherCAT/CiA402 专项 Skill，新增 TwinCAT、SSC/ET9300、PDO/SDO、DC、故障排查参考、评估数据和 CiA402 解码脚本。
- 更新 `embedded/SKILL.md`：按主问题路由 C99、architecture、EtherCAT/CiA402 和 motorcontrol，明确领域组合规则。
- 同步更新各 Skill 的 `agents/openai.yaml`，确保界面名称、触发描述和默认提示与当前内容一致。

## 维护规则

- 默认中文说明。
- 保留项目既有风格和已验证内容。
- 新增或大改 skill 后更新 `CHANGELOG.md`。
- 推送前检查 `git status`，避免提交本地备份、系统 skill 或压缩包。

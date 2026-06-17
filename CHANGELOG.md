# 更新日志

## 2026-06-17

### 新增

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

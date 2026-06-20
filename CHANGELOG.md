# 更新日志

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

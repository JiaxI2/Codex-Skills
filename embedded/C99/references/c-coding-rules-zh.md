# C 编码规则参考

## 目录

- [适用范围与文件归属](#适用范围与文件归属)
- [命名与格式](#命名与格式)
- [文件组织](#文件组织)
- [注释与修改记录](#注释与修改记录)
- [安全性与可移植性](#安全性与可移植性)
- [审查清单](#审查清单)
- [静态检查起点](#静态检查起点)

## 适用范围与文件归属

先将文件判定为项目自研、自动生成或第三方代码。

判断证据包括：

- 文件头的生成标记、许可证和版权所有者；
- STM32Cube、SysConfig、配置器或 IDL 的输入和再生脚本；
- 包管理、submodule、vendor 目录和上游仓库；
- 当前团队是否拥有接口和实现的维护责任。

自动生成和第三方代码默认保持实际编码和局部风格，只做必要逻辑修改。新项目和项目自研代码对新增或修改函数执行本参考的固定规则。

## 命名与格式

| 对象 | 规则 | 示例 |
|---|---|---|
| 文件 | `snake_case` | `motor_control.c` |
| 函数 | `snake_case` | `motor_control_init` |
| 局部变量、参数 | `lowerCamelCase` | `targetSpeed` |
| 文件级或全局可变状态 | `g_` + `lowerCamelCase` | `g_motorState` |
| 宏、枚举值、标签 | `UPPER_SNAKE_CASE` | `MOTOR_STATE_RUN` |
| `typedef` 抽象类型 | `PascalCase` | `MotorConfig` |

- 使用 4 个空格缩进，禁止 TAB；
- 行宽默认不超过 120 列；
- 一行只写一条语句；
- 函数左大括号独占一行；
- 控制语句左大括号放在语句行末；
- 所有控制语句必须使用大括号；
- `case/default` 缩进一级，并明确退出或 fallthrough；
- 优先使用函数或 `static inline`，避免具有副作用的函数式宏。

```c
static ResultCode motor_control_start(MotorContext *context)
{
    if (context == NULL) {
        return RESULT_INVALID_ARGUMENT;
    }

    return RESULT_OK;
}
```

## 文件组织

新建或大幅重写项目自研 `.c` 文件时，优先采用：

1. 项目现有文件头；
2. `#include`；
3. 宏与常量；
4. 类型定义；
5. 文件级 `static` 状态；
6. 内部声明；
7. 内部 `static` 函数；
8. 对外函数。

不要写死年份、公司、作者或版权。新文件必须复用当前项目模板；没有模板时询问用户。

## 注释与修改记录

### 函数头

项目自研代码中的所有函数必须有函数头注释。沿用项目现有 Doxygen 格式；没有格式时使用：

```c
/**
 * @brief Start motor control.
 * @param[in,out] context Motor context; must not be NULL.
 * @return RESULT_OK on success; an error code otherwise.
 * @note Callable from task context only.
 */
```

### 函数内部

每个函数内部必须包含有意义的注释，说明阶段、设计意图、边界条件、硬件时序、同步关系或非显然取舍。对简单函数可以用一条整体意图注释；复杂函数按逻辑块注释。禁止 `i++; /* i 加 1 */` 这类机械翻译。

```c
/* Validate the command before changing shared motor state. */
if (command == NULL) {
    return RESULT_INVALID_ARGUMENT;
}
```

### 新增或大幅修改函数

补充可追溯记录，作者必须来自用户、仓库配置或既有记录；无法确定时询问。

```c
/*
 * Modification History
 * Date         Author      Reason
 * YYYY-MM-DD   <author>    <why this function was added or changed>
 */
```

关键缺陷修复可补充：

```c
/*
 * Bug Fix
 * Date   : YYYY-MM-DD
 * Author : <author>
 * Issue  : <observed symptom>
 * Cause  : <root cause>
 * Fix    : <implemented correction>
 */
```

不要删除已有有效注释；代码变化时同步更新过期注释。

## 安全性与可移植性

- 函数保持单一职责；可行时控制在 50 行非空非注释代码和 4 层嵌套以内；
- 所有可能失败的 API 立即检查返回值；
- 对 API 参数、文件、报文、IPC 数据和跨信任边界的共享状态做显式校验；
- 不使用 `assert` 校验外部输入；
- 动态内存、锁、句柄、队列和信号量在所有退出路径正确释放；
- 复杂资源清理可使用单一 `cleanup:` 出口；
- 文件私有符号使用 `static`；共享状态说明互斥、原子或中断保护策略；
- 指针运算使用 `uintptr_t` 或字节指针；
- 长度和索引使用 `size_t`，缩窄前检查边界；
- 生产代码使用项目日志接口，不遗留裸 `printf` 或敏感信息；
- 调试钩子和测试代码不得无保护地进入发布路径。

## 审查清单

- 是否正确判断项目自研、自动生成或第三方代码；
- 是否保持第三方和生成代码的实际编码及局部风格；
- 项目自研新增或修改函数是否满足命名、4 空格和大括号规则；
- 每个函数是否有函数头和内部意图注释；
- 新增或大改函数是否记录作者、日期和原因；
- 是否覆盖或伪造版权、作者、年份；
- 返回值和外部输入是否校验；
- 是否存在宏副作用、指针截断或 `size_t` 未检查缩窄；
- 资源是否在所有退出路径释放；
- ISR、任务、DMA 和共享状态是否有同步说明；
- 是否产生与任务无关的格式化或重命名 diff。

## 静态检查起点

根据项目编译链调整，不直接覆盖仓库现有配置。

```yaml
# .clang-format
Language: C
BasedOnStyle: LLVM
IndentWidth: 4
TabWidth: 4
UseTab: Never
ColumnLimit: 120
IndentCaseLabels: true
BreakBeforeBraces: Custom
BraceWrapping:
  AfterFunction: true
  AfterControlStatement: false
AllowShortIfStatementsOnASingleLine: Never
AllowShortLoopsOnASingleLine: false
AllowShortBlocksOnASingleLine: Never
```

```bash
cppcheck --std=c99 --enable=warning,style,performance,portability \
  --inline-suppr --error-exitcode=1 --suppress=missingIncludeSystem -I. src/
```

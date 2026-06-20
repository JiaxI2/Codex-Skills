---
name: architecture
description: 设计、审查和重构嵌入式固件系统架构，覆盖 MCU、MPU、DSP、FPGA、SoC、裸机、RTOS 和 Linux 边缘设备。用于职责分层、真实变化点抽象、App/算法平台化、Bootloader、OTA、A/B、Manifest、参数与校准区、产线烧录、依赖注入、测试和发布门禁。仅在系统边界、目录结构、平台适配或量产交付是主问题时使用；FOC、SVPWM、PI/PID、采样时序和多轴控制算法改用 motorcontrol。参考开源或厂商工程前先确认主控、需求、许可证和复刻范围，不得默认照搬。
---

# 嵌入式架构平台化

默认使用中文输出。

## 核心边界

- 只抽象真实变化点，不为目录美观增加层次。
- 保持 App、算法核心、协议语义、升级与故障状态机不依赖具体芯片和厂商 HAL。
- 允许固定板级 GPIO、bring-up 和一次性实验保留薄实现。
- 将 FOC、SVPWM、PI/PID、采样时序和多轴控制算法交给 `motorcontrol`。
- 涉及 C 实现时同时使用 `c99-standard-c`；涉及具体 ARM 启动、中断或 cache 时同时使用 `arm`。

## 工作流

### 1. 建立上下文

先从仓库证据识别，缺失且会改变方案时再询问：

- 主控、编译器、操作系统和厂商 SDK 版本；
- 项目阶段：Demo、bring-up、产品化、平台化或量产维护；
- 强实时路径、周期、WCET、抖动和安全状态；
- 真实变化点：主控、板卡、协议、编码器、功率板或产品型号；
- Bootloader、升级、回滚、签名、参数、校准和产线追溯需求。

不要默认引入 HAL/BSP/ops、跨 RTOS、A/B 或全量 GPIO 抽象。

### 2. 按职责映射现有结构

识别以下语义，不强制采用固定目录名：

```text
App：产品意图和客户可见流程
Service：状态机、策略和协议语义
Algorithm Core：可脱离硬件测试的算法
Platform/API：稳定能力接口，可 fake/mock/stub
Impl/Board：芯片、寄存器、外设和板级实现
Vendor/SDK：厂商库、RTOS 和寄存器定义
```

需要决策矩阵时读取 `references/architecture_decision_matrix_zh.md`。

### 3. 只针对真实变化点提出方案

对每个新增边界说明：

- 它隔离了哪个已确认的变化；
- 哪些调用方依赖它；
- 如何测试或替换；
- 不增加该边界的实际代价是什么。

无法回答时，不新增抽象。

### 4. 处理量产和升级

涉及交付、现场维护或升级时，读取 `references/production_firmware_constraints_zh.md`，明确镜像验证、断电恢复、回滚、参数保护、版本追溯和调试口策略。

### 5. 使用参考项目

仅当主控、产品形态或问题相近时读取：

- `references/repository_reference_matrix_zh.md`：快速匹配参考工程；
- `references/customer_function_replicate_options_zh.md`：比较可复刻行为、代价和许可证风险；
- `references/customer_interview_checklist_zh.md`：需求信息不足时组织问题。

区分架构思想、行为重实现、代码参考和不建议照搬的部分。未经用户确认，不复制参考工程的目录或功能。

### 6. 定义验证和发布门禁

读取 `references/testing_release_gate_zh.md`，至少覆盖单元测试、依赖注入、状态迁移、故障注入、强实时测量和升级断电测试。没有证据时，不宣称架构已验证或可发布。

## 输出

按任务规模输出必要部分：

1. 当前平台、阶段和已确认假设；
2. 真实变化点与不应抽象点；
3. 建议边界、依赖方向和目录映射；
4. 参考项目的匹配理由与复刻边界；
5. 验证、发布门禁和待用户确认项。

正式审查可使用 `assets/architecture_review_template_zh.md`；需要方案签字确认时使用 `assets/customer_confirmation_template_zh.md`。

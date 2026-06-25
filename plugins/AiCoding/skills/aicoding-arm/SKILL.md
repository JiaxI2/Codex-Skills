---
name: aicoding-arm
description: ARM 嵌入式固件 skill，用于 Cortex-M/Cortex-A 启动、CMSIS、NVIC、中断、Fault、MPU/cache、链接脚本、低功耗模式、厂商 HAL 边界和寄存器级固件。涉及 C 编码细节时结合 c99-standard-c 使用。默认使用中文输出。
---

# ARM 固件

默认使用中文回答和生成说明。仅在用户明确要求英文，或项目注释/接口规范要求英文时使用英文。

使用此 skill 处理 ARM 专属固件工作。C 规则结合 `c99-standard-c`，评审任务结合 `review`。

## 工作流程

1. 确认 core 系列、厂商 SDK/HAL、编译器/链接器、启动文件、时钟树、内存映射和权限/安全模型。
2. 除非任务明确指向厂商头文件或生成代码，否则保持它们稳定。
3. 将可移植逻辑与 CMSIS/HAL/寄存器访问分离。
4. 明确中断优先级、抢占、临界区、fault 处理和内存屏障。
5. 在目标硬件上验证，或提供最接近的硬件/仿真证据。

## 检查项

- NVIC 优先级符合 RTOS 规则，高优先级 ISR 不调用不安全 API。
- Fault handler 保留足够上下文用于诊断。
- MPU/cache/DMA 代码说明 clean/invalidate、对齐和内存区域属性。
- startup/linker 变更保持向量表、栈/堆、section 布局和 bootloader handoff 合约。
- 低功耗变更保持唤醒源、时钟恢复、外设状态和调试行为。

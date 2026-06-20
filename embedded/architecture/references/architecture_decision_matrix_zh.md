# 架构决策矩阵

## 1. 不按固定层名判断，按职责判断

| 语义层 | STM32 可能命名 | TI C2000 可能命名 | 飞控/机器人可能命名 | 判断标准 |
|---|---|---|---|---|
| App | UserApp / app | app | modules / vehicle / user_app | 是否只表达产品行为 |
| Service | Robot / service | control_service / protocol | commander / estimator / controller | 是否封装状态机/协议/策略 |
| Algorithm Core | algorithm / math | control / DCL / foc | control / estimator | 是否能脱离硬件单测 |
| Platform/API | bsp_api / driver_if | hal / board_if | device / driver api | 是否可 fake/mock/stub |
| Impl/Board | Drivers / BSP | driverlib / device | boards / target | 是否允许出现寄存器/厂商 API |
| Vendor | HAL/LL/CMSIS | C2000Ware/DriverLib | NuttX/ChibiOS/vendor SDK | 是否为第三方/厂商依赖 |

## 2. 何时抽象

需要抽象：

```text
硬件或主控未来可能变化
协议语义长期稳定
算法需要跨平台复用
模块需要单元测试/仿真/故障注入
多个板卡/轴/通道复用同一能力
```

不需要复杂抽象：

```text
一次性 demo
固定 GPIO
固定板级电源使能
固定 LED/风扇/继电器
不会迁移且不影响测试的 bring-up 代码
```

## 3. 参考仓库使用方式

不要照搬目录名。先判断：

```text
参考项目解决的问题是什么？
当前项目是否有同样真实变化点？
客户是否需要同样功能？
当前主控是否匹配？
许可证、实时性、安全性是否允许复刻？
```

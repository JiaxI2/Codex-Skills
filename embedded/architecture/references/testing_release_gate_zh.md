# 测试与发布门禁

## 1. 模块化代码发布前必须测试

```text
Algorithm Core：纯函数单元测试，边界值测试，定点/浮点一致性测试。
Platform API：fake/mock/stub 注入测试。
Service 状态机：状态迁移测试、非法输入测试、故障恢复测试。
Bootloader/OTA：断电、CRC 错误、版本错误、防降级、回滚测试。
强实时路径：WCET、抖动、栈深、overrun 统计。
```

## 2. 参考飞控/机器人项目的工程化能力

可参考：

```text
PX4：modules/drivers/boards/msg/ROMFS、参数、日志、SITL/HITL。
ArduPilot：AP_HAL、libraries、vehicle 分离、日志和参数长期维护。
Betaflight：target 配置、Blackbox、CLI 参数、强实时板级裁剪。
TI SDK：Datalog、SFRA、DCL、SysConfig、官方示例回归。
```

## 3. 交付前必须给客户确认

```text
最终目录结构
模块边界
升级策略
测试门禁
参考仓库是否复刻
不能复刻或不建议复刻的原因
```

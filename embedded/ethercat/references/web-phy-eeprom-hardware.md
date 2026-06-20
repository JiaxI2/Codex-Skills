# EtherCAT 网页参考：PHY、EEPROM、ESC 引脚、地址与扫描问题

## 读取触发

当用户提到以下任一内容时读取本文件：

- 片上 ESC MCU ESC 外设、PHY、MII、MDC/MDIO、Link 信号、`0x110 ESC DL Status`。
- 主站扫描不到从站、端口顺序异常、Link 跳变、Lost Link、RX Error。
- EEPROM、Flash 模拟 EEPROM、`CREATE_EEPROM_CONTENT`、EEPROM checksum、eeprom.h。
- ESC_CTR_x、IO_CFG、NMII_LINK0/1、LINK_ACT、PHY Reset、RUN_LED、ERR_LED。
- 从站地址、地址别名、Explicit Device ID、APPL_GetDeviceID()、IdentificationReg134。

## 核心来源

1. `[EtherCAT]ESC使用PHY的注意事项`
2. `[EtherCAT]ESC配置PHY的示例`
3. `[EtherCAT]EtherCAT主站扫描不到从站的情况说明`
4. `[EtherCAT]从设备EEPROM数据说明`
5. `[EtherCAT]EEPROM数据存储与烧录，厂商解决方案！`
6. `[EtherCAT]ESC的引脚功能说明`
7. `[EtherCAT]ESC的RUN_LED和ERR_LED使用GPIO引脚`
8. `[EtherCAT]从站地址、从站地址别名与从站Explicit Device ID`

详见 `ethercat-web-knowledge-index.md`。

## PHY 与 Link 规则

网页文章强调：ESC 每个端口对应一个 PHY，ESC 依据 PHY 提供的 Link 信号自动开闭端口并形成网络拓扑。

典型问题：

| 现象 | 可能原因 | 优先检查 |
|---|---|---|
| 网线连接但扫不到下游设备 | PHY Link 被 ESC 识别为 No Link | ESC `0x110 DL Status`、PHY LED/Link 引脚、电平极性、IO_CFG |
| 连接状态跳变 | PHY Link 电平不稳或 LED Blink 被当 Link | PHY LED 模式、MDC/MDIO 配置、TwinCAT Link 状态 |
| 未接网线却被识别为 Link | 端口误开，帧转发到空端口导致环路开环/丢帧 | Link 极性、NMII_LINK 配置、Port0/Port1 连接顺序 |
| 主站顺序与物理顺序不一致 | 端口连接顺序错误 | 端口拓扑、Port0/Port1 入口出口定义 |

调试提示：使用 IDE 寄存器窗口读 ESC 寄存器前，必须先完成 `ecat_hardware_init()` 使能 ESC 时钟，否则可能总线访问挂住。

## PHY 选型/硬件建议

- 优先使用 MII，网页文章提到 ESC MII 因省略传输 FIFO，处理/传输延时更低。
- 同一 ESC 的多个 PHY 应共享同一时钟源。
- 多个 PHY 共用 MDC/MDIO 总线，应分配不同地址；建议避免地址 0，因为地址 0 常被用作广播地址。
- 典型地址建议：Port0=1，Port1=2，Port2=3。
- PHY Reset 应由 MCU/ESC 控制，ESC 未就绪前保持 PHY reset，避免上游误判 Link 后把帧发入尚未工作的 ESC。
- PHY 上电默认应能进入 100 Mbit/s 全双工，不应完全依赖 EEPROM 正确加载后再通过 MDC/MDIO 配置；否则 EEPROM 空/错时难以恢复。

## PHY Link 配置示例

网页文章给出 JL1111、YT8512、LAN8710 例子：

- JL1111：LED1 默认可能 Blink，需要切到稳定 `On for 100 Link` 一类模式。
- YT8512：LED 默认模式也可能 Blink，需要通过扩展寄存器配置。
- LAN8710：LED2 可作为 100M Link active，默认可为稳态电平，通常不需要 LED 模式配置。

工程判断：

- Link 引脚不应输出 Blink 波形给 ESC 当端口 Link 判据。
- 必须确认 Link 电平极性与 `BOARD_ECAT_PORTx_LINK_INVERT` / IO_CFG 一致。
- 新 PHY/新硬件优先查 PHY datasheet 的 LED/Link、地址复用、上拉下拉和默认自协商配置。

## EEPROM 与 Flash 模拟 EEPROM

EtherCAT 从站 EEPROM 用于存储设备配置和描述信息。ESC 上电从 EEPROM 前 8 word 读取配置并加载到对应寄存器，同时做 checksum 校验。

关注点：

- EEPROM checksum 错会导致 ESC EEPROM 未正确加载，影响部分功能。
- 网页示例的 ESC 外设某些寄存器在 IC 设计中固定，如 PDI 接口类型可能固定为 On-Chip bus，不能通过 EEPROM 第一个字节修改。
- 片上 ESC MCU 支持 Flash 模拟 EEPROM，可省外部 EEPROM 器件。
- SSC Tool 设置 `CREATE_EEPROM_CONTENT = 1` 可把 EEPROM 数据生成到 `eeprom.h`，由固件写入 EEPROM/Flash 模拟区。
- EEPROM 为空或全 `0xff` 时，只要 PHY/Port0 恢复链路正常，主站可能仍可扫描到信息全 `0xff` 的设备，再通过主站更新 EEPROM。

## 扫描不到从站 Playbook

优先顺序：

1. 确认网卡/主站本身可扫描已知正常从站。
2. 查 PHY 电路、Link 信号、Port0/Port1 接线方向。
3. 查 ESC `0x110 DL Status`，确认端口真实 Link 状态。
4. 查 NMII_LINK 的 ESC_CTR_x 二级 pinmux、IO_CFG、极性。
5. 查 EEPROM checksum 和 ESC 是否完成 EEPROM 加载。
6. 若 EEPROM 全空，利用 Port0 强制恢复端口和 PHY 默认 100M 全双工能力烧录 EEPROM。
7. 不要先修改 CiA402/CoE 代码；扫不到从站通常在 PHY/ESC/EEPROM 层。

## ESC 引脚和 LED

### 二级 pinmux

厂商 ESC 有若干功能信号通过 CTR MUX/IO_CFG 映射到 `ESC_CTR_x`：

- PHY Reset
- LED_RUN
- LED_ERR
- LINK_ACT0~3
- NMII_LINK0~3

实现链路：

```text
pinmux.c: 把具体 PAD 配成 ESC0_CTR_x
board.h: 定义 BOARD_ECAT_xxx_CTRL_INDEX = x
ecat_hardware_init(): 调用 esc_config_ctrl_signal_function() 把 ESC_CTR_x 分配为具体 ESC 功能，并设置极性
```

### RUN_LED / ERR_LED 用 GPIO

默认：`ESC_SUPPORT_ECAT_LED=1`，`UC_SET_ECAT_LED=0`，由 ESC 硬件引脚控制 LED。

如果引脚无法分配给 ESC.CTR[x]：

```text
ESC_SUPPORT_ECAT_LED = 0
UC_SET_ECAT_LED      = 1
```

此时 SSC 会调用：

```c
void HW_SetLed(UINT8 RunLed, UINT8 ErrLed)
```

由用户在目标平台 GPIO 外设中实现实际 LED 控制。

## 地址、别名与 Explicit Device ID

| 标识 | 位置/来源 | 掉电保持 | 用途 |
|---|---|---|---|
| 从站地址 | ESC `0x10`，主站配置，复位默认 0 | 否 | EtherCAT 固定地址寻址，随拓扑配置变化 |
| 从站地址别名 | ESC `0x12`，上电从 EEPROM 加载 | 是 | 固定地址寻址别名；修改 EEPROM 时要同步 checksum |
| Explicit Device ID | 应用层 `APPL_GetDeviceID()` 返回，经 `0x120` 请求、`0x134` 读取 | 取决于实现 | 主站识别设备，不参与 EtherCAT 数据帧寻址 |

注意：

- TwinCAT 扫描网络通常先用顺序寻址发现设备；别名不是替代初始扫描的机制。
- SSC Tool 开启 Explicit Device ID 后，ESI 会出现 `IdentificationReg134`，一致性测试可能期望默认返回值为 5；量产项目可改为拨码开关或非易失参数。
- 应用层若只写 ESC `0x0012`，掉电不保持；若写 EEPROM 别名区域，必须正确更新 config area checksum。

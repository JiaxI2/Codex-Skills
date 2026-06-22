# EtherCAT 深度速读参考（Agent 离线版）

> 目标：让 Agent 在不联网、不重新翻规范的情况下，快速形成对 EtherCAT 的工程级理解。本文不是 ETG/CiA 原始规范的替代品，而是面向嵌入式从站、伺服驱动、TwinCAT/IgH 主站诊断、SSC/ET9300 移植的蒸馏参考。
>
> 适用场景：EtherCAT 从站 bring-up、CoE/SDO/PDO、ESI、ESC 寄存器、FMMU/SyncManager、Distributed Clocks、AL/ESM 状态机、WKC、SSC 代码审查、CiA402 伺服轴、TwinCAT NC 轴诊断。

---

## 0. Agent 使用方式

遇到以下问题时，应先读本文件，再进入具体 ref 或代码：

| 用户问题关键词 | 先看章节 | 后续再看 |
|---|---:|---|
| EtherCAT 是什么、协议栈、帧格式、Datagram、WKC | 1、2、3 | 13 诊断矩阵 |
| ESC、寄存器、FMMU、Sync Manager、EEPROM、PDI、MII | 4、5、6 | 13.1、13.2 |
| CoE、SDO、PDO、对象字典、ESI、SM assign、动态 PDO | 7、8 | `web-coe-pdo-eoe-twincat.md` |
| DC、Sync0/Sync1、抖动、0x1A/0x1B/0x2C、Watchdog | 9、13.4 | `web-ssc-sync-errors.md` |
| SSC/ET9300、APPL_InputMapping、PDO_OutputMapping、ECAT_Application | 10 | `ssc-et9300-notes.md` |
| CiA402、0x6040/0x6041、0x6060/0x6061、CSP/CSV/CST/PP、TwinCAT NC Ready | 11、12 | `ethercat-cia402-quick-reference.md`、`twincat-diagnostics.md` |
| 扫描不到从站、Link、PHY、EEPROM、RUN/ERR LED | 4、6、13.1 | `web-phy-eeprom-hardware.md` |

---

## 1. 一句话模型：EtherCAT 的核心不是“以太网通信”，而是“帧穿越从站时被硬件加工”

EtherCAT 使用标准以太网物理层和以太网帧承载，但它的实时性并不依赖 TCP/IP，也不是传统的“主站轮询每个设备”。主站发送一个或多个 EtherCAT 帧，帧沿拓扑经过所有从站；每个从站的 ESC（EtherCAT Slave Controller）在帧经过时立即读出属于自己的数据、写入自己的反馈数据、更新 Working Counter，然后继续转发。

Agent 必须建立这个认知：

```text
传统以太网/现场总线思维：
  Master -> Slave1 请求/响应 -> Slave2 请求/响应 -> ...

EtherCAT 思维：
  Master -> 一个帧穿过所有 Slave，Slave 在硬件层 on-the-fly 处理 -> 帧返回 Master
```

因此，很多 EtherCAT 故障不是“应用层收不到包”这么简单，而是以下链路中某一层没有对齐：

```text
PHY/Link
  -> ESC 端口和帧转发
  -> ESC 寄存器/EEPROM/SII
  -> FMMU/Sync Manager
  -> AL/ESM 状态机
  -> Mailbox/CoE/SDO
  -> PDO/过程数据
  -> DC/Sync0/Sync1
  -> 应用对象/CiA402 状态机
  -> 主站 NC/PLC 绑定与周期
```

---

## 2. 协议分层：从 Agent 角度必须掌握的 6 层

| 层 | 关键实体 | Agent 需要理解的重点 |
|---|---|---|
| 物理层 | 100BASE-TX、MII/EBUS、PHY、Link | 扫描不到从站、Link 抖动、PHY 地址/MII 访问、端口状态 |
| 数据链路层 | EtherCAT Header、Datagram、WKC、寻址 | 帧怎么寻址，为什么 WKC 错，APRD/FPRD/LRW 各做什么 |
| ESC 硬件层 | FMMU、Sync Manager、DC、SII EEPROM、PDI | 主站如何把逻辑过程映像映射到从站 RAM；邮箱和 PDO 如何隔离 |
| 应用层 | AL/ESM、Mailbox、CoE/EoE/FoE/SoE | Init/PreOp/SafeOp/Op 代表什么；SDO/PDO/FoE 走哪条通道 |
| 设备行规 | CiA402、对象字典、0x6040/0x6041 | 伺服驱动如何抽象为标准对象和状态机 |
| 主站/工程层 | TwinCAT/IgH、ESI、NC/PLC | 配置、扫描、PDO 绑定、DC 诊断、NC Ready、WcState |

---

## 3. 帧结构与 Datagram

### 3.1 EtherCAT 帧的基本结构

EtherCAT 通常直接承载在以太网帧中，EtherType 为 `0x88A4`。一个以太网帧中可以串联多个 EtherCAT Datagram。每个 Datagram 可独立指定命令、地址、长度和数据，并在末尾带一个 WKC 字段。

```text
Ethernet Frame
├─ Destination MAC       6 B
├─ Source MAC            6 B
├─ EtherType             2 B = 0x88A4
├─ EtherCAT Header       2 B
│  ├─ Length             11 bit
│  ├─ Reserved           1 bit
│  └─ Type               4 bit，通常为 EtherCAT Datagram 类型
├─ Datagram #0
│  ├─ Cmd                1 B
│  ├─ Index              1 B
│  ├─ Address            4 B
│  ├─ Length + More      2 B
│  ├─ IRQ                2 B
│  ├─ Data               N B
│  └─ WKC                2 B
├─ Datagram #1
└─ FCS                   4 B，由以太网硬件/ESC 处理
```

Agent 诊断时不要把整个 EtherCAT 帧看成一个业务消息。真正需要定位的是：哪个 Datagram、哪个地址模式、哪个 SyncManager/FMMU 映射、哪个 WKC 期望值不匹配。

### 3.2 Datagram 命令族

| 命令族 | 命令 | 寻址逻辑 | 典型用途 | WKC 直觉 |
|---|---|---|---|---|
| APxx | APRD/APWR/APRW | Auto-increment，按拓扑位置逐站处理 | 扫描、发现、早期配置 | 命中的站按读/写/读写增加 |
| FPxx | FPRD/FPWR/FPRW | Configured address，按站地址匹配 | 已分配地址后的寄存器访问 | 地址匹配才增加 |
| Bxx | BRD/BWR/BRW | Broadcast，所有从站处理 | 广播读写、全网状态 | 多个从站累计增加 |
| Lxx | LRD/LWR/LRW | Logical address，经 FMMU 映射到从站物理区 | 周期过程数据 PDO | 与参与映射的从站相关 |
| xRMW | ARMW/FRMW | 读多写 | 特殊同步/锁存场景 | 读写组合增加 |
| NOP | NOP | 不操作 | 占位/测试 | 通常不影响 |

### 3.3 WKC 的工程含义

WKC（Working Counter）是 EtherCAT 诊断的核心变量。每个成功处理 Datagram 的从站会按操作类型增加 WKC。一般直觉是：

```text
读成功   -> +1
写成功   -> +2
读写成功 -> +3
```

但实际期望 WKC 与命令、寻址方式、PDO 映射、从站数量、逻辑地址覆盖范围相关。WKC 错误不等于“网线断了”，常见原因包括：

- 某个从站未进入期望 AL 状态；
- FMMU/SM 配置与 ESI 或对象字典不一致；
- 主站过程映像覆盖范围和从站实际 PDO 长度不一致；
- DC 同步或 SyncManager watchdog 导致过程数据被判无效；
- 多轴/模块化 OD 中轴数量、slot、PDO assign 不匹配；
- 应用层没有按周期更新 TxPDO 或没有及时消耗 RxPDO。

---

## 4. ESC：从站硬件的真实中心

ESC 是 EtherCAT 从站的硬件核心。MCU 应用程序通常不是直接收发以太网帧，而是通过 PDI（Process Data Interface）访问 ESC 的寄存器、邮箱、过程数据 RAM 和事件。

### 4.1 ESC 基本功能

```text
EtherCAT Port(s)
  -> Frame parser / forwarding
  -> Address match / FMMU
  -> Sync Manager
  -> Process Data RAM
  -> Mailbox RAM
  -> AL Event / IRQ
  -> PDI to MCU
  -> DC unit / latch / Sync0 / Sync1
  -> SII EEPROM interface
```

关键点：

- ESC 在帧穿越时执行地址匹配和数据搬运；
- 过程数据一般通过 FMMU + SyncManager 映射到主站逻辑过程映像；
- 邮箱数据通过 SyncManager 的 mailbox mode 进行握手；
- DC 单元提供系统时间、端口延时测量、Sync0/Sync1 输出；
- SII EEPROM 保存从站身份、邮箱配置、PDO/类别信息等可被主站扫描读取的信息。

### 4.2 常见 ESC 寄存器区：只记用途，不背全表

| 地址区 | 用途 | 诊断价值 |
|---|---|---|
| `0x0000` 附近 | ESC 类型、修订、FMMU/SM 数量、特性位 | 判断硬件是否被正确识别 |
| `0x0010`/`0x0012` | 配置站地址、别名地址 | 主站扫描、别名寻址、Explicit Device ID |
| `0x0110` | DL Status | Link、通信状态诊断入口 |
| `0x0120` | AL Control | 主站请求 AL 状态切换 |
| `0x0130` | AL Status | 当前 AL 状态 |
| `0x0134` | AL Status Code | 状态切换失败原因 |
| `0x0140` 起 | PDI 控制/配置 | MCU 和 ESC 接口配置 |
| `0x0200` 起 | ECAT/AL 事件请求和屏蔽 | 中断源定位 |
| `0x0300` 起 | 错误计数器 | 物理层、端口、PDI、丢链诊断 |
| `0x0400` 起 | Watchdog | 过程数据/PDI 超时诊断 |
| `0x0500` 起 | SII EEPROM | EEPROM 读写/重载/校验 |
| `0x0510` 起 | MII 管理 | PHY 访问、Link 诊断 |
| `0x0600` 起 | FMMU | 逻辑地址到 ESC 物理地址映射 |
| `0x0800` 起 | Sync Manager | 邮箱/PDO 缓冲区、方向、长度、状态 |
| `0x0900` 起 | Distributed Clocks | DC 时间、偏移、延时、Sync0/Sync1 |

### 4.3 错误计数器和看门狗

出现间歇掉 OP、多轴 WKC 错、Invalid IO Data 时，不要只看应用层状态字。应按顺序读：

```text
DL Status 0x0110
AL Status 0x0130
AL Status Code 0x0134
RX/Lost Link/Error counters 0x0300+
Watchdog registers 0x0400+
SM status 0x0800+
DC status 0x0900+
```

错误计数器可帮助区分：

- 物理层干扰/线缆/PHY：RX error、lost link 增加；
- PDI 接口异常：PDI error 或 PDI watchdog；
- 过程数据未按期写入：process data watchdog；
- SyncManager 配置错误：SM 长度/地址/方向或事件异常；
- DC 不同步：Sync0/Sync1 watchdog 或同步窗口错误。

---

## 5. FMMU：逻辑地址映射器

FMMU（Fieldbus Memory Management Unit）把主站的逻辑过程映像映射到从站 ESC 的物理内存区域。理解 FMMU 是理解 PDO/WKC 的关键。

### 5.1 逻辑过程映像

主站通常把全网 RxPDO/TxPDO 拼成连续的逻辑地址空间：

```text
Master logical process image
0x00000000 ─┬─ Slave1 RxPDO -> Slave1 ESC physical RAM
            ├─ Slave2 RxPDO -> Slave2 ESC physical RAM
            ├─ Slave1 TxPDO <- Slave1 ESC physical RAM
            └─ Slave2 TxPDO <- Slave2 ESC physical RAM
```

FMMU 配置告诉 ESC：当某个 LRW/LRD/LWR Datagram 访问某段逻辑地址时，应映射到本从站哪个 ESC 物理地址、哪个 bit 偏移、长度多少、方向是什么。

### 5.2 FMMU 错误的典型表现

| 现象 | 常见根因 |
|---|---|
| 主站能扫描，从站能进 PreOp，但 SafeOp/Op 失败 | SM/FMMU/PDO assign 配置不一致 |
| 单轴正常，多轴后 WKC 错 | 逻辑过程映像长度或轴偏移累加错误 |
| PDO 数据错位 | bit length、subindex、alignment、entry 顺序不一致 |
| TwinCAT 显示 invalid IO data | WKC、SM watchdog、DC sync 或 PDO 映射状态不满足 |
| ESI 改了但主站不生效 | ESI cache 未刷新、EEPROM 未更新或线上对象字典不一致 |

---

## 6. Sync Manager：邮箱和过程数据的边界

Sync Manager（SM）负责 ESC 内存区域的访问同步和一致性保护。它不是 DC 的 Sync0/Sync1，不要混淆。

### 6.1 常见 SM 分工

| SM | 常见用途 | 模式 | 方向直觉 |
|---|---|---|---|
| SM0 | Mailbox Out，主站写从站读 | Mailbox mode | Master -> Slave |
| SM1 | Mailbox In，从站写主站读 | Mailbox mode | Slave -> Master |
| SM2 | RxPDO | Buffered mode | Master -> Slave |
| SM3 | TxPDO | Buffered mode | Slave -> Master |

### 6.2 Mailbox mode 与 Buffered mode

- Mailbox mode 强调握手和完整性，适合 CoE/SDO、FoE、EoE 等非周期数据；
- Buffered mode 强调实时刷新，适合 PDO 周期过程数据，通常使用三缓冲思想，消费者读取最新有效数据。

如果邮箱大小/地址错误，PreOp 阶段的 CoE/SDO 就会失败；如果过程数据 SM 长度/方向/激活状态错误，SafeOp -> Op 或周期 WKC 会失败。

---

## 7. SII EEPROM、ESI、对象字典之间的关系

Agent 必须区分三个概念：

| 名称 | 所在位置 | 作用 | 常见误区 |
|---|---|---|---|
| SII EEPROM | 从站非易失存储/仿真 | 主站扫描时读取身份、邮箱、类别、PDO 相关信息 | 以为改 ESI 就等于改 EEPROM |
| ESI XML | 主站工程侧文件 | 描述从站能力、对象、PDO、DC、模块信息 | TwinCAT 可能使用缓存，不一定立即更新 |
| Object Dictionary | 从站运行时对象表 | CoE/SDO 访问的真实对象 | ESI 有对象但固件未实现会导致 SDO/PDO 异常 |

### 7.1 基本检查原则

```text
ESI 描述的对象/PDO
  必须与固件 OD 中实际对象一致；
ESI 中的 PDO 映射
  必须与 0x1600/0x1A00 等映射对象一致；
SM assign
  必须与 0x1C12/0x1C13 及 ESC SM 配置一致；
EEPROM/SII
  必须与主站扫描到的身份、邮箱配置一致；
TwinCAT cache
  必须在 ESI 更新后清理或重新扫描验证。
```

---

## 8. 应用层：AL/ESM 状态机

EtherCAT 从站应用层状态机通常包括：

| 状态 | Mailbox | PDO 输入 | PDO 输出 | 工程含义 |
|---|---|---|---|---|
| Init | 不可用 | 不可用 | 不可用 | ESC/应用初始化，主站可访问基础寄存器 |
| Pre-Operational | 可用 | 不可用 | 不可用 | 可通过 CoE/SDO 配置对象、PDO、参数 |
| Safe-Operational | 可用 | 可用 | 通常不生效或保持安全值 | 从站可给输入，尚未完整接收输出 |
| Operational | 可用 | 可用 | 可用 | 周期过程数据完整交换 |
| Bootstrap | 可用 | 不可用 | 不可用 | FoE 固件升级等特殊模式 |

### 8.1 状态切换的诊断逻辑

| 失败点 | 先查什么 | 常见原因 |
|---|---|---|
| Init -> PreOp 失败 | EEPROM/SII、Mailbox SM0/SM1 | EEPROM 内容错误、邮箱地址/长度错误、PDI 初始化失败 |
| PreOp -> SafeOp 失败 | PDO mapping、SM2/SM3、对象字典 | PDO 对象不存在、长度不一致、SM 配置错误 |
| SafeOp -> Op 失败 | RxPDO、Watchdog、应用是否 ready | 输出过程数据未被主站写入、应用未确认、watchdog 超时 |
| Op 运行中掉 SafeOp | WKC、DC、SM watchdog、AL status code | 周期丢失、同步错误、应用超时、物理链路干扰 |

---

## 9. Mailbox 协议：CoE、FoE、EoE、SoE、VoE

Mailbox 是非周期通信通道，常用于配置、诊断和固件升级。

| 协议 | 用途 | 常见对象/流程 |
|---|---|---|
| CoE | CANopen over EtherCAT，对象字典、SDO、PDO、Emergency | 0x1000、0x1018、0x1600、0x1A00、0x1C12、0x1C13、0x6040 等 |
| FoE | File over EtherCAT | 固件下载、Bootloader、文件传输 |
| EoE | Ethernet over EtherCAT | 以太网隧道、虚拟网卡、IP 参数 |
| SoE | Servo over EtherCAT | SERCOS 风格伺服参数访问 |
| VoE | Vendor over EtherCAT | 厂商私有扩展 |

### 9.1 CoE 对象字典视角

对象字典的核心不是“变量表”，而是主站、ESI、PDO、应用之间的契约。

| 区域 | 典型对象 | 含义 |
|---|---|---|
| `0x1000` | Device Type | 设备类型和 profile 编号 |
| `0x1008/1009/100A` | 名称/硬件版本/软件版本 | 识别信息 |
| `0x1018` | Identity Object | Vendor ID、Product Code、Revision、Serial |
| `0x1600..0x17FF` | RxPDO Mapping | 主站到从站过程输出映射 |
| `0x1A00..0x1BFF` | TxPDO Mapping | 从站到主站过程输入映射 |
| `0x1C12` | RxPDO Assign | 哪些 RxPDO 分配给过程数据 SM |
| `0x1C13` | TxPDO Assign | 哪些 TxPDO 分配给过程数据 SM |
| `0x6000..0x9FFF` | Profile/application objects | CiA402/设备应用对象 |

---

## 10. Distributed Clocks（DC）

DC 解决的是多从站、多轴、多采样点的时间一致性问题。它不是普通软件定时器，而是 ESC 硬件时间系统。

### 10.1 DC 的工程模型

```text
Master selects reference clock
  -> measures port propagation delay
  -> writes offset / delay compensation
  -> arms Sync0 / Sync1
  -> every bus cycle exchanges PDO
  -> drive application latches/updates at fixed Sync point
```

### 10.2 DC 常见错误认知

| 错误认知 | 正确理解 |
|---|---|
| 只要进入 OP 就说明同步没问题 | OP 只能说明状态机满足，Sync0 jitter/watchdog 仍可能导致 IO invalid |
| FreeRun 也能稳定多轴伺服 | 单轴或低要求可用，多轴 CSP/CSV/CST 推荐 DC 同步 |
| Sync0 周期等于应用控制周期就够了 | 还要考虑 shift time、内部计算延迟、PDO 更新时间、主站任务周期 |
| WKC 错一定是 PDO 映射 | DC watchdog、SM watchdog、主站周期抖动也可能导致 WKC/IO invalid |

### 10.3 多轴伺服的经验原则

- CSP/CSV/CST 优先使用 DC Sync0；
- 主站 NC/PLC 周期、EtherCAT bus cycle、Sync0 cycle 必须一致或明确成整数倍；
- 从站应用应在 Sync0 或 SM event 的明确时刻消耗 RxPDO 和刷新 TxPDO；
- 过程数据更新不要被低优先级后台任务阻塞；
- 多轴数量增加后，帧长度、主站任务负载、应用计算时间和 WKC 期望值都要重新核算。

---

## 11. SSC/ET9300 从站实现视角

ET9300/SSC 的核心思想是把从站拆成三层：

```text
Application
  - 对象字典
  - PDO 映射函数
  - 用户周期逻辑
  - CiA402/设备 profile

Generic EtherCAT Stack
  - ESM/AL
  - Mailbox/CoE/FoE/EoE
  - PDO handling
  - Sync handling

Hardware/PDI Abstraction
  - ESC register access
  - interrupt/timer
  - EEPROM emulation/programming
  - platform-specific PDI
```

### 11.1 过程数据三函数

很多 SSC 工程最终围绕这三个函数排故：

```text
PDO_OutputMapping()
  将 ESC RxPDO 数据复制到应用变量

ECAT_Application()
  执行业务逻辑、状态机、控制算法或对象更新

PDO_InputMapping()
  将应用变量复制到 ESC TxPDO 数据
```

如果多轴运行中 WKC 或 IO invalid，必须检查：

- 这三个函数在当前 sync mode 下的调用时刻；
- 输入/输出映射长度是否与 ESI/OD 一致；
- 应用更新 TxPDO 的周期是否低于主站 watchdog 期望；
- 临界区、共享内存、双核通信是否导致 PDO 数据不一致；
- 字节序、对齐、bit length 是否正确。

### 11.2 SSC 的常见配置点

| 配置点 | 影响 |
|---|---|
| `COE_SUPPORTED` | 是否支持 CoE/SDO/对象字典 |
| `FOE_SUPPORTED` | 是否支持 FoE 文件传输/升级 |
| `BOOTSTRAPMODE_SUPPORTED` | 是否支持 Bootstrap 固件升级状态 |
| Sync modes | 决定 PDO_OutputMapping/ECAT_Application/PDO_InputMapping 调用时机 |
| EEPROM emulation | 无外置 EEPROM 时的 SII 数据来源 |
| Object dictionary generation | 影响 ESI、SDO、PDO mapping、entry description |

---

## 12. CiA402：把伺服驱动叠加到 EtherCAT 上

CiA402 不是 EtherCAT 的数据链路协议，而是驱动器设备 profile。EtherCAT 提供通信和同步，CiA402 提供伺服驱动对象、状态机和模式语义。

### 12.1 最小对象心智模型

| 对象 | 名称 | 作用 |
|---|---|---|
| `0x6040` | Controlword | 主站控制驱动状态机：Shutdown、Switch on、Enable operation、Fault reset 等 |
| `0x6041` | Statusword | 从站反馈驱动状态、fault、operation enabled、target reached、drive follows command 等 |
| `0x6060` | Modes of operation | 主站设置模式：PP/PV/PT/HM/CSP/CSV/CST 等 |
| `0x6061` | Modes of operation display | 从站反馈当前实际模式 |
| `0x607A` | Target position | PP/CSP 常用目标位置 |
| `0x6064` | Position actual value | 实际位置反馈 |
| `0x60FF` | Target velocity | 速度模式目标速度 |
| `0x6071` | Target torque | 转矩模式目标转矩 |
| `0x6502` | Supported drive modes | 支持的驱动模式位图 |

### 12.2 CSP/CSV/CST 与 DC

周期同步模式不是“只把 0x6060 设为 8/9/10”。它隐含主站每个 bus cycle 提供新给定，从站按同步周期消耗给定并刷新反馈。对于 TwinCAT NC 轴，CSP 模式下 Statusword 的 bit12 通常被解释为 drive follows command；若 bit12 不满足，NC 可能无法 Ready，即使 0x6041 其他位看似正常。

### 12.3 模式显示值 0x6061 的意义

`0x6060` 是请求模式，`0x6061` 是实际显示模式。若上电 `0x6060=8` 但 `0x6061=0`，Agent 应优先怀疑：

- 模式切换逻辑只写了 OD 默认值，没有真正驱动内部模式状态；
- CiA402 状态机尚未进入允许模式显示更新的状态；
- 0x6061 对象未映射/未刷新/未从应用变量回写；
- TwinCAT 读取的是旧 ESI/旧对象或 PDO/SDO 通道状态异常；
- CSP 必要对象、PDO、DC 或 0x6502 支持位不完整。

---

## 13. 诊断矩阵

### 13.1 扫描不到从站

优先检查：

```text
1. Link LED / PHY 地址 / MII 访问
2. ESC 是否释放复位，PDI 是否初始化
3. SII EEPROM 是否有效，是否能被 ESC 自动加载
4. 主站网卡是否直连 EtherCAT 网络，是否被普通交换机隔离
5. 物理层是否为 100 Mbit/s full duplex
6. 端口极性、TX/RX、晶振、PHY reset、MDIO/MDC 时序
```

不要一开始看 CoE 或 CiA402。扫描不到从站通常还没到应用层。

### 13.2 能扫描，但 Init -> PreOp 失败

重点：Mailbox 和 EEPROM/SII。

```text
读取 AL Status Code 0x0134
检查 SM0/SM1 地址、长度、方向、激活
检查 SII 中 mailbox offset/size
检查 CoE/FoE/EoE mailbox protocol bit
检查 PDI 中断/AL event 是否能触发
```

### 13.3 PreOp -> SafeOp 失败

重点：PDO、SM2/SM3、对象字典。

```text
检查 0x1600/0x1A00 PDO mapping 对象是否存在
检查 0x1C12/0x1C13 assign 是否正确
检查 PDO entry 的 bit length 是否累加正确
检查 ESI 和运行时 OD 是否一致
检查 SM2/SM3 长度是否与 PDO 总长度一致
```

### 13.4 SafeOp -> Op 失败或运行后掉 OP

重点：过程数据、DC、watchdog、应用实时性。

```text
检查 WKC expected/actual
检查 Sync0/Sync1 是否启用且周期匹配
检查 SM watchdog / process data watchdog
检查 PDO_OutputMapping/PDO_InputMapping 是否按周期调用
检查应用是否阻塞或共享内存锁等待
检查多轴时每轴数据偏移是否正确
```

### 13.5 TwinCAT 显示 invalid IO data / WcState error

典型排查顺序：

```text
1. 看 EtherCAT 诊断页 expected WKC vs actual WKC
2. 看对应从站 AL state 是否短暂掉 SafeOp/PreOp
3. 看 DC Diagnostics 是否有 Sync0/Sync1 error
4. 看 SM watchdog / process data watchdog
5. 看 PDO 映射长度，尤其多轴模块化对象
6. 看主站任务周期和 NC/PLC 周期是否一致
7. 看从站应用是否每周期更新 TxPDO
8. 降低轴数或拉长周期，判断是配置错误还是实时性不足
```

### 13.6 CiA402 轴 Not Ready

```text
检查 0x6040 控制字状态转换是否完整
检查 0x6041 状态字是否达到 operation enabled
检查 0x6060 请求模式和 0x6061 显示模式是否一致
检查 0x6502 是否声明支持当前模式
CSP/CSV/CST 检查 Statusword bit12 语义
检查实际值对象 0x6064/0x606C/0x6077 是否刷新
检查 NC 轴编码器 scaling 和 PDO 变量绑定
```

---

## 14. Agent 的回答策略

### 14.1 避免泛泛解释

用户问 EtherCAT 问题时，不要停留在“EtherCAT 是实时工业以太网”。应快速落到：

```text
当前问题处在哪一层？
  PHY/Link?
  ESC/SII?
  FMMU/SM?
  AL/ESM?
  CoE/SDO?
  PDO/WKC?
  DC/Sync?
  CiA402/NC?
```

### 14.2 必须区分规范语义和工程实现

- ETG.1000 是协议层基础；
- ETG.6010/CiA402 是伺服驱动 profile 指令/约束；
- ET9300/SSC 是常见从站栈实现方式；
- TwinCAT/IgH 是主站实现和工程工具；
- 某些网页/SDK 文章是工程经验，不应覆盖规范定义。

### 14.3 回答嵌入式从站问题时的固定模板

```text
1. 判断层级：PHY / ESC / SM-FMMU / AL / CoE / PDO / DC / CiA402
2. 给出最小验证路径：读哪些寄存器、对象、主站诊断项
3. 给出可能根因排序：高概率在前
4. 给出代码检查点：映射函数、对象字典、状态机、同步中断
5. 给出隔离实验：单轴/多轴、FreeRun/DC、拉长周期、固定PDO长度
6. 明确哪些结论需要实际抓包/寄存器/日志验证
```

---

## 15. 最小术语表

| 术语 | 解释 |
|---|---|
| ESC | EtherCAT Slave Controller，从站硬件通信核心 |
| PDI | Process Data Interface，MCU 访问 ESC 的接口 |
| FMMU | 逻辑地址到 ESC 物理内存的映射单元 |
| Sync Manager | ESC 内存访问同步单元，用于邮箱和 PDO 缓冲 |
| SII | Slave Information Interface，从站 EEPROM 信息接口 |
| ESI | EtherCAT Slave Information，主站侧 XML 描述文件 |
| AL/ESM | Application Layer / EtherCAT State Machine |
| CoE | CANopen over EtherCAT，对象字典、SDO、PDO、Emergency |
| SDO | 非周期对象访问，走 mailbox |
| PDO | 周期过程数据，走 FMMU/SM 和逻辑地址 |
| WKC | Working Counter，用于判断 Datagram 被多少从站成功处理 |
| DC | Distributed Clocks，分布式时钟同步机制 |
| Sync0/Sync1 | ESC DC 单元输出的同步事件 |
| CiA402 | 驱动器和运动控制设备 profile |
| CSP/CSV/CST | 周期同步位置/速度/转矩模式 |

---

## 16. 来源校核说明

本文综合了以下材料的工程语义，并做了重写和压缩：

- ETG.1000.2：物理层服务和协议；
- ETG.1000.3：数据链路层服务；
- ETG.1000.4：数据链路层协议，帧、Datagram、FMMU、SM、DC、SII、看门狗等；
- ETG.1000.5：应用层服务，CoE、PDO/SM assign、SII、同步相关对象；
- ETG.1000.6：应用层协议，AL/ESM、CoE/SDO/EoE/FoE 编码；
- ETG.6010 / IEC 61800-7 / CiA402：EtherCAT 伺服驱动的 CiA402 实现约束；
- ET9300/SSC：从站栈工程结构、同步模式、过程数据映射、FoE/EEPROM/Bootloader 等；
- IgH EtherCAT 主站文章：用主站源码视角解释 Datagram、FMMU、SM、Mailbox、CoE、ESM 和 DC 的阅读路径。

注意：本文不包含 ETG/CiA 原始规范或网页原文的大段复制。用于 Agent 离线理解和排障路由时，应优先作为“工程索引”和“心智模型”，涉及一致性认证、对象精确定义、二进制编码细节时仍应回到正式规范或项目源代码。

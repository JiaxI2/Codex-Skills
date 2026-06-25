# EtherCAT 主站源码蒸馏：SOEM / IgH / Linux 实时主站

> 用途：让 Agent 在不联网时快速理解 EtherCAT 主站如何从“扫描从站”推进到“周期收发 PDO、检查 WKC、读写 SDO、同步 DC、驱动 CiA402 轴”。
>
> 正确性核对：本文件用 ETG.1000 数据链路/应用层文档校验协议语义，用 SOEM、IgH 官方仓库/文档校验源码角色。最后核对日期：2026-06-20。

## 1. 主站职责边界

EtherCAT 主站不是“普通 TCP/IP 客户端”，而是周期性构造 EtherCAT Datagram，通过逻辑地址/物理地址访问从站 ESC 的过程数据区、邮箱区和寄存器区。主站主要负责：

1. 发现拓扑、读取从站身份与 SII/ESI 信息。
2. 为每个从站配置地址、SM、FMMU、PDO、DC 和状态机转换。
3. 在周期任务中发送/接收 PDO，并用 Working Counter 验证每个 Datagram 被期望数量的从站处理。
4. 用 Mailbox/CoE 读写对象字典，例如 SDO 访问 `0x6041`、`0x6061`、`0x603F`。
5. 对 CiA402 驱动执行控制字状态转换，必要时执行 fault reset、mode 切换、homing 或 CSP/CSV/CST 周期控制。

## 2. 主站排障心智模型

```text
网卡/实时线程
  -> Ethernet frame / EtherCAT datagram
  -> WKC 是否符合期望
  -> FMMU/SM 映射是否正确
  -> SDO/CoE 是否成功
  -> DC/Sync0 是否稳定
  -> CiA402 状态机是否进入 Operation enabled
  -> NC/运动控制层是否接收有效反馈
```

不要跳过 WKC。EtherCAT 的很多“驱动不动”“轴 Not Ready”“invalid IO data”最终都能回到以下几类：

| 现象 | 首查层级 | 主站侧检查 |
|---|---|---|
| 从站扫描不到 | PHY/拓扑/ESC/SII | 网卡、线缆、Link、从站 EEPROM/SII、Auto Increment 读 |
| PREOP 失败 | Mailbox/ESI/InitCmd | SDO init command、邮箱大小、AL status code |
| SAFEOP 失败 | PDO/SM/FMMU | PDO 长度、SM2/SM3、FMMU logical mapping、process data size |
| OP 后掉线 | WKC/DC/Watchdog | expected WKC、actual WKC、DC drift、SM watchdog |
| SDO 能读，PDO 不更新 | PDO/周期任务 | send/receive process data 是否在实时线程、domain 是否 active |
| CiA402 不使能 | 应用层 | 0x6040/0x6041、0x6060/0x6061、0x603F、mode specific bit |

## 3. SOEM 源码阅读路线

SOEM 适合读“最小主站模型”：轻量、C 语言、示例清晰，适合嵌入式 PC、Windows/Linux 以及自研主站验证工具。

### 先看示例

| 目录/文件类型 | 看什么 | Agent 用法 |
|---|---|---|
| `samples/simple_test` | 从 `ec_init()` 到 `ec_config_init()`、状态切换、周期 PDO 收发 | 用来解释“最小 OP 流程” |
| `samples/slaveinfo` | 读取从站信息、SDO、PDO 映射、CoE 对象 | 用来写“离线诊断/对象导出”工具 |
| `samples/eepromtool` 或类似工具 | SII/EEPROM 读写思路 | 用来排查 SII/ESI/身份不匹配 |

### 再看核心模块

| 模块 | 关注点 |
|---|---|
| 初始化/配置 | 扫描从站、设置 station address、读取/推导 PDO、配置 FMMU/SM |
| CoE/SDO | expedited/segmented SDO、abort code、OD list |
| Process data | IOmap、expected WKC、send/receive processdata |
| DC | DC slave 检测、时间偏移、同步启动、漂移检查 |
| OSAL/OSHW | 平台抽象、raw socket、网卡收发、时间函数 |

### SOEM 适合做什么

- 快速写一个 `read_cia402.py/c` 工具：读 `0x6041/0x6061/0x603F/0x6064`。
- 写产线或实验室扫描工具：导出从站身份、PDO、SM/FMMU、DC 能力。
- 对比 TwinCAT 行为：如果 SOEM 能稳定 OP，TwinCAT 失败，重点查 ESI/TwinCAT 配置；如果两者都失败，查从站固件/硬件。
- 做 Agent MCP 的底层读取后端。

### SOEM 局限

- 它是库，不是完整运动控制框架。
- 不替代 TwinCAT NC、LinuxCNC 或 ROS2 控制层。
- 周期实时性取决于 OS、网卡、线程优先级、驱动和调度策略。
- 对复杂多轴/分布式时钟/冗余拓扑需要额外工程封装。

## 4. IgH / EtherLab 主站阅读路线

IgH 适合读“Linux 工业主站模型”：Linux 内核模块、用户态配置工具、domain/process data、实时周期任务、LinuxCNC 集成。

### 核心概念

| 概念 | 含义 | 排障价值 |
|---|---|---|
| Master | Linux 侧 EtherCAT 主站实例 | 判断 master 是否激活、网卡是否绑定 |
| Slave config | 某个从站的配置对象 | 判断 vendor/product/revision/PDO 是否匹配 |
| Domain | 一组过程数据逻辑映射 | 判断 PDO offset、bit position、domain state |
| SDO request | 非周期对象访问 | 读取 0x6041/0x6061/错误码 |
| DC config | 同步周期/shift/参考时钟 | 排查 OP 后抖动、丢 WKC、watchdog |

### IgH 适合做什么

- LinuxCNC、ROS2 或自研 Linux 实时控制器。
- 多轴控制、I/O 扩展、伺服驱动、编码器采集。
- 工程化运行：systemd、udev、PREEMPT_RT、网卡驱动绑定、诊断命令。

### 典型诊断命令概念

不同安装版本命令名略有差异，但 Agent 应关注这些信息：

```text
master state
slave list / slave state
sdo upload / download
pdo mapping / domain layout
reg read ESC register
wkc / domain state / AL status code
```

## 5. 主站周期任务模板

```c
// 伪代码，不绑定具体 API
init_master();
scan_slaves();
load_or_parse_esi();
config_pdo_sm_fmmu();
config_dc_if_required();
request_safeop();
request_op();

while (run) {
    wait_period();
    receive_processdata();
    check_wkc_and_domain_state();
    read_rx_feedback_snapshot();
    run_motion_or_cia402_state_machine();
    write_tx_command_snapshot();
    send_processdata();
}
```

周期任务中不要做：慢速 SDO、文件 IO、复杂日志格式化、大量动态内存分配、阻塞网络操作。SDO 读写应放低频诊断线程，必要时通过快照传给实时线程。

## 6. Agent 处理主站问题时的回答策略

1. 先判断用户是在 TwinCAT、SOEM、IgH、LinuxCNC、ROS2 还是自研主站。
2. 明确问题发生在：扫描、PREOP、SAFEOP、OP、周期运行、CiA402 使能、运动控制。
3. 给出最小观测集合：state、AL status、WKC、PDO map、DC diag、0x6041/0x6061。
4. 若用户有源码，优先让 Agent 查：配置流程、周期线程、WKC 判断、SDO 访问、PDO offset、DC 参数。
5. 不确定时用 SOEM/SOEM-like 工具做交叉验证。

## 7. 可维护蒸馏规则

- 本文件只保留主站抽象、源码入口和排障路径；具体 API 参数以项目当前源码为准。
- 每季度核对一次 SOEM/IgH README 和 release；只更新“入口路径”和“能力边界”，不要把大量源码复制进 ref。
- 所有“可执行命令”必须标注主站类型，避免把 TwinCAT/IgH/SOEM 命令混用。

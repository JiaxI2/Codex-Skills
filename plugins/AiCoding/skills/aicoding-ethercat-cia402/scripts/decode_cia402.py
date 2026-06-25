#!/usr/bin/env python3
"""解码 CiA402 Controlword/Statusword。

用法：
  python scripts/decode_cia402.py --statusword 1591 --mode 8
  python scripts/decode_cia402.py --controlword 0x000F --statusword 0x0637
"""

from __future__ import annotations

import argparse
from typing import Iterable

STATUS_BITS = [
    (0, "Ready to switch on / 准备好上电"),
    (1, "Switched on / 已上电"),
    (2, "Operation enabled / 运行使能"),
    (3, "Fault / 故障"),
    (4, "Voltage enabled / 电压已使能"),
    (5, "Quick stop：置位通常表示未触发 Quick stop"),
    (6, "Switch on disabled / 禁止上电"),
    (7, "Warning / 警告"),
    (8, "Manufacturer specific / 厂商自定义"),
    (9, "Remote / 主站远程控制"),
    (10, "Operation mode specific / 模式相关"),
    (11, "Internal limit active / 内部限幅激活"),
    (12, "Operation mode specific；CS 模式常用作 drive follows command"),
    (13, "Operation mode specific；跟随误差/回零错误等"),
    (14, "Manufacturer specific / 厂商自定义"),
    (15, "Manufacturer specific / 厂商自定义"),
]

CONTROL_BITS = [
    (0, "Switch on / 上电"),
    (1, "Enable voltage / 使能电压"),
    (2, "Quick stop：置位通常表示不执行 Quick stop"),
    (3, "Enable operation / 运行使能"),
    (4, "Operation mode specific / 模式相关"),
    (5, "Operation mode specific / 模式相关"),
    (6, "Operation mode specific / 模式相关"),
    (7, "Fault reset / 故障复位"),
    (8, "Halt / 暂停"),
    (9, "Operation mode specific / 模式相关"),
    (10, "Reserved / 保留"),
    (11, "Manufacturer specific / 厂商自定义"),
    (12, "Manufacturer specific / 厂商自定义"),
    (13, "Manufacturer specific / 厂商自定义"),
    (14, "Manufacturer specific / 厂商自定义"),
    (15, "Manufacturer specific / 厂商自定义"),
]

MODE_NAMES = {
    1: "Profile Position, PP / 位置规划",
    2: "Velocity Mode, VL / 速度模式",
    3: "Profile Velocity, PV / 速度规划",
    4: "Profile Torque, TQ / 转矩规划",
    6: "Homing, HM / 回零",
    7: "Interpolated Position, IP / 插补位置",
    8: "Cyclic Synchronous Position, CSP / 周期同步位置",
    9: "Cyclic Synchronous Velocity, CSV / 周期同步速度",
    10: "Cyclic Synchronous Torque, CST / 周期同步转矩",
}


def parse_int(text: str) -> int:
    return int(text, 0)


def print_bits(title: str, value: int, bits: Iterable[tuple[int, str]]) -> None:
    print(f"{title}: {value} dec = 0x{value:04X}")
    for bit, name in bits:
        state = "1" if value & (1 << bit) else "0"
        print(f"  bit {bit:02d} = {state}  {name}")


def infer_fsa(status: int) -> str:
    masked = status & 0x006F
    patterns = {
        0x0000: "Not ready to switch on / 未准备好上电（典型值，非唯一）",
        0x0040: "Switch on disabled / 禁止上电",
        0x0021: "Ready to switch on / 准备好上电",
        0x0023: "Switched on / 已上电",
        0x0027: "Operation enabled / 运行使能",
        0x0007: "Quick stop active / Quick stop 激活",
        0x000F: "Fault reaction active / 故障反应中（典型值，非唯一）",
        0x0008: "Fault / 故障",
    }
    return patterns.get(masked, f"未知或厂商扩展状态，masked=0x{masked:04X}")


def main() -> None:
    parser = argparse.ArgumentParser(description="解码 CiA402 Controlword/Statusword")
    parser.add_argument("--controlword", type=parse_int, help="Controlword，例如 0x000F")
    parser.add_argument("--statusword", type=parse_int, help="Statusword，例如 1591 或 0x0637")
    parser.add_argument("--mode", type=parse_int, help="CiA402 模式值，例如 8=CSP")
    args = parser.parse_args()

    if args.mode is not None:
        print(f"Mode: {args.mode} -> {MODE_NAMES.get(args.mode, '未知/厂商自定义/保留模式')}")

    if args.controlword is not None:
        print_bits("Controlword", args.controlword, CONTROL_BITS)

    if args.statusword is not None:
        print_bits("Statusword", args.statusword, STATUS_BITS)
        print(f"FSA 推断: {infer_fsa(args.statusword)}")
        if args.mode in (8, 9, 10):
            follows = bool(args.statusword & (1 << 12))
            print(f"CS 模式 bit12 drive follows command: {'1/有效' if follows else '0/未跟随或无效'}")

    if args.controlword is None and args.statusword is None and args.mode is None:
        parser.print_help()


if __name__ == "__main__":
    main()

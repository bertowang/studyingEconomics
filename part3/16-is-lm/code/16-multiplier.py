#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 16-multiplier.py | 凯恩斯乘数与 IS-LM（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
C_MPC, AUTONOMOUS = 0.8, 100.0
D_INV, K_MONEY, H_MONEY = 20.0, 0.5, 20.0
M_OVER_P = 200.0
DG = 10.0
ITERS = 40
# ---- 简单乘数：迭代求不动点 ----
y = 0.0
for _ in range(ITERS):
    y = C_MPC * y + AUTONOMOUS
y_simple = AUTONOMOUS / (1 - C_MPC)
tax_mult = -C_MPC / (1 - C_MPC)
# ---- IS-LM 联立 ----
def solve_y(a):
    return (a + D_INV * (M_OVER_P / H_MONEY)) / ((1 - C_MPC) + D_INV * K_MONEY / H_MONEY)

def solve_r(y):
    return (K_MONEY * y - M_OVER_P) / H_MONEY
y0, r0 = solve_y(AUTONOMOUS), None
r0 = solve_r(y0)
y1 = solve_y(AUTONOMOUS + DG)
r1 = solve_r(y1)
mult_islm = (y1 - y0) / DG
# ---- 数值验证：打印可手算核对的量 ----
print("迭代 Y=%.4f 解析 Y=%.4f 乘数=%.4f 税收乘数=%.4f" %
      (y, y_simple, 1 / (1 - C_MPC), tax_mult))
print("IS-LM 初始 Y=%.4f r=%.4f" % (y0, r0))
print("G 增加 %.2f 后 Y=%.4f r=%.4f" % (DG, y1, r1))
print("IS-LM 支出乘数=%.4f (简单乘数 %.4f，挤出 %.4f)" %
      (mult_islm, 1 / (1 - C_MPC), 1 / (1 - C_MPC) - mult_islm))
print("储蓄悖论: c 从 0.8 降到 0.6 时均衡 Y 由 %.2f 降到 %.2f" %
      (AUTONOMOUS / (1 - 0.8), AUTONOMOUS / (1 - 0.6)))

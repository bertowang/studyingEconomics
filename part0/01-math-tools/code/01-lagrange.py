#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""01-lagrange.py | FOC 数值求解、比较静态与影子价格"""
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
B, PX, PY, ALPHA = 100.0, 2.0, 5.0, 0.5
TOL_ITER = 80
# ---- 模型：MRS = (a/(1-a))*(y/x)，最优时 MRS = p_x/p_y ----
def y_of(x):
    return (B - PX * x) / PY

def mrs(x):
    return (ALPHA / (1 - ALPHA)) * (y_of(x) / x)

lo, hi = 1e-9, B / PX - 1e-9
for _ in range(TOL_ITER):
    mid = (lo + hi) / 2
    if mrs(mid) > PX / PY:      # x 偏小，MRS 偏高，需增大 x
        lo = mid
    else:
        hi = mid
x = (lo + hi) / 2
y = y_of(x)
u = (x ** ALPHA) * (y ** (1 - ALPHA))
lam = ALPHA * (x ** (ALPHA - 1)) * (y ** (1 - ALPHA)) / PX
# ---- 比较静态：预算增加 1 元时效用增加多少 ----
dB = 1.0
B2 = B + dB
x2 = ALPHA * B2 / PX
y2 = (1 - ALPHA) * B2 / PY
u2 = (x2 ** ALPHA) * (y2 ** (1 - ALPHA))
# ---- 数值验证：打印可手算核对的量 ----
print("FOC 数值解 x=%.6f y=%.6f MRS=%.6f p比=%.6f" % (x, y, mrs(x), PX / PY))
print("解析解     x=%.6f y=%.6f" % (ALPHA * B / PX, (1 - ALPHA) * B / PY))
print("最大效用 u=%.6f  影子价格 lambda=%.6f" % (u, lam))
print("预算+1 的效用增益=%.6f (包络定理预测=%.6f)" % (u2 - u, lam * dB))

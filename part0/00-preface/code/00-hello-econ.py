#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""00-hello-econ.py | 第一个经济程序：把「选择」写成约束最优化"""
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
BUDGET = 100.0          # 预算
PX, PY = 2.0, 5.0       # 两种商品的价格
ALPHA = 0.5             # Cobb-Douglas 效用中 x 的份额
GRID = 100              # 网格精度
# ---- 模型：u(x,y) = x^a * y^(1-a)，约束 p_x*x + p_y*y = B ----
best = (-1.0, 0.0, 0.0)
for i in range(GRID + 1):
    x = BUDGET / PX * i / GRID
    y = (BUDGET - PX * x) / PY
    u = (x ** ALPHA) * (y ** (1 - ALPHA))
    if u > best[0]:
        best = (u, x, y)
# ---- 解析解（后面第 05 章会推导）----
analytic_x = ALPHA * BUDGET / PX
analytic_y = (1 - ALPHA) * BUDGET / PY
# ---- 数值验证：打印可手算核对的量 ----
print("预算=%.2f 价格=(%.2f, %.2f) a=%.2f" % (BUDGET, PX, PY, ALPHA))
print("网格最优 x=%.2f y=%.2f u=%.4f" % (best[1], best[2], best[0]))
print("解析最优 x=%.2f y=%.2f" % (analytic_x, analytic_y))
print("支出校验=%.2f (应等于预算)" % (PX * best[1] + PY * best[2]))

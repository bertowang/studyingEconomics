#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 05-consumer.py | Cobb-Douglas 需求的对偶计算（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
B = 100.0
PX0, PY = 2.0, 5.0
PX1 = 3.0              # x 涨价
ALPHA = 0.5
# ---- 马歇尔需求与间接效用 ----
def demand(px, py, b):
    return ALPHA * b / px, (1 - ALPHA) * b / py

def utility(x, y):
    return (x ** ALPHA) * (y ** (1 - ALPHA))

# ---- 支出函数与希克斯需求（alpha=0.5 的解析式）----
def expenditure(px, py, u):
    return u * (px / ALPHA) ** ALPHA * (py / (1 - ALPHA)) ** (1 - ALPHA)

def hicks_x(px, py, u):
    return u * (py / px) ** (1 - ALPHA)

x0, y0 = demand(PX0, PY, B)
x1, y1 = demand(PX1, PY, B)
u0, u1 = utility(x0, y0), utility(x1, y1)
cv = B - expenditure(PX0, PY, u1)
ev = expenditure(PX1, PY, u0) - B
sub = hicks_x(PX1, PY, u0) - hicks_x(PX0, PY, u0)
inc = x1 - hicks_x(PX1, PY, u0)
# ---- 数值验证：打印可手算核对的量 ----
print("旧价需求 x0=%.4f y0=%.4f u0=%.4f" % (x0, y0, u0))
print("新价需求 x1=%.4f y1=%.4f u1=%.4f" % (x1, y1, u1))
print("支出函数校验 e(p0,u0)=%.4f (应=B=%.2f)" % (expenditure(PX0, PY, u0), B))
print("CV=%.4f  EV=%.4f  (涨价损失，EV>CV 因新价计价更高)" % (cv, ev))
print("总效应=%.4f = 替代效应 %.4f + 收入效应 %.4f" % (x1 - x0, sub, inc))

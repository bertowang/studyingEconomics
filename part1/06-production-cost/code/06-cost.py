#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 06-cost.py | 短期生产函数、MC=p 条件与规模报酬（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
A_PROD, K_FIXED = 2.0, 16.0     # y = A * sqrt(K) * sqrt(L)
WAGE, FIXED_COST = 4.0, 20.0
PRICE = 10.0
GRID = 1000
# ---- 模型 ----
def output(l, k=K_FIXED):
    return A_PROD * math.sqrt(k) * math.sqrt(l)

def mp_l(l, k=K_FIXED):
    return 0.5 * A_PROD * math.sqrt(k) / math.sqrt(l)

def profit(l):
    return PRICE * output(l) - WAGE * l - FIXED_COST

best_l, best_pi = 0.0, profit(0.0)
for i in range(1, GRID + 1):
    l = 200.0 * i / GRID
    if profit(l) > best_pi:
        best_l, best_pi = l, profit(l)
# p*MP_L=w 的解析解: L = (p*A*sqrt(K)/(2w))^2
analytic_l = (PRICE * A_PROD * math.sqrt(K_FIXED) / (2 * WAGE)) ** 2
q = output(best_l)
mc = WAGE / mp_l(best_l)
ac = (WAGE * best_l + FIXED_COST) / q
# ---- 数值验证：打印可手算核对的量 ----
print("网格最优 L=%.4f 产量=%.4f 利润=%.4f" % (best_l, q, best_pi))
print("解析解   L=%.4f (由 p*MP_L=w 解出)" % analytic_l)
print("最优处 MC=%.4f (应=p=%.2f)  AC=%.4f" % (mc, PRICE, ac))
print("MP_L(L=1)=%.4f, MP_L(L=100)=%.4f → 递减" % (mp_l(1.0), mp_l(100.0)))
print("规模报酬: 投入翻倍 y 由 %.2f 到 %.2f (比值 %.2f)" %
      (output(25.0, 16.0), output(50.0, 32.0), output(50.0, 32.0) / output(25.0, 16.0)))

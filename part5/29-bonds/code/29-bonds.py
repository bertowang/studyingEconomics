#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 29-bonds.py | 现金流贴现与利率敏感度（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
FACE, COUPON_RATE, MATURITY = 100.0, 0.05, 5
YTM = 0.04
SHIFT_BP, SHIFT_BIG = 0.0001, 0.01
S1, S2 = 0.03, 0.04

def price(y):
    cfs = [FACE * COUPON_RATE] * MATURITY
    cfs[-1] += FACE
    return sum(cf / (1 + y) ** t for t, cf in enumerate(cfs, 1))

p0 = price(YTM)
cash = [FACE * COUPON_RATE] * MATURITY
cash[-1] += FACE
pv = [cf / (1 + YTM) ** t for t, cf in enumerate(cash, 1)]
d_mac = sum(t * v for t, v in enumerate(pv, 1)) / p0
d_mod = d_mac / (1 + YTM)
convex = sum(t * (t + 1) * pv[t - 1] for t in range(1, MATURITY + 1)) / \
         (p0 * (1 + YTM) ** 2)
# ---- 泰勒近似 vs 精确重定价 ----
def approx(dy):
    return p0 * (1 - d_mod * dy + 0.5 * convex * dy ** 2)
p_up = price(YTM + SHIFT_BIG)
p_down = price(YTM - SHIFT_BIG)
# ---- 远期利率与期限结构 ----
f12 = (1 + S2) ** 2 / (1 + S1) - 1
# ---- 数值验证：打印可手算核对的量 ----
print("5 年期 5%% 票息、YTM=%.2f%% 价格=%.6f" % (100 * YTM, p0))
print("麦考利久期=%.6f 修正久期=%.6f 凸性=%.6f" % (d_mac, d_mod, convex))
print("+1bp: 久期预测 ΔP=%.6f 精确 ΔP=%.6f" %
      (approx(SHIFT_BP) - p0, price(YTM + SHIFT_BP) - p0))
print("+100bp: 一阶预测=%.6f 二阶预测=%.6f 精确=%.6f" %
      (p0 * (1 - d_mod * SHIFT_BIG), approx(SHIFT_BIG), p_up))
print("利率 +100bp 价格变化=%.4f, -100bp 价格变化=%.4f (不对称来自凸性)" %
      (p_up - p0, p_down - p0))
print("即期 s1=%.2f%% s2=%.2f%% => 隐含远期 f(1,2)=%.4f%%" %
      (100 * S1, 100 * S2, 100 * f12))

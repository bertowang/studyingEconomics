#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 14-ge.py | 纯交换经济的均衡相对价格（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
ALPHA_A, ALPHA_B = 0.4, 0.7       # A 禀赋 (1,0)，B 禀赋 (0,1)
LO, HI, ITERS = 0.05, 5.0, 100
# ---- 超额需求：p1=1, r=p2/p1 ----
def demands(r):
    ma, mb = 1.0, r
    xa1, xa2 = ALPHA_A * ma / 1.0, (1 - ALPHA_A) * ma / r
    xb1, xb2 = ALPHA_B * mb / 1.0, (1 - ALPHA_B) * mb / r
    return xa1 + xb1 - 1.0, xa2 + xb2 - 1.0

def z1(r):
    return demands(r)[0]
# ---- 二分法求 z1=0 ----
lo, hi = LO, HI
for _ in range(ITERS):
    mid = (lo + hi) / 2
    if z1(mid) > 0:
        hi = mid
    else:
        lo = mid
r = (lo + hi) / 2
z_1, z_2 = demands(r)
# ---- 瓦尔拉斯法则：在非均衡价格处也恒成立 ----
test_r = 0.5
w1, w2 = demands(test_r)
walras = 1.0 * w1 + test_r * w2
# ---- 福利：贸易是否让双方都改善 ----
ua_before = 0.0                     # A 初始只有商品 1，x2=0
ma, mb = 1.0, r
xa1, xa2 = ALPHA_A * ma, (1 - ALPHA_A) * ma / r
xb1, xb2 = ALPHA_B * mb, (1 - ALPHA_B) * mb / r
ua_after = (xa1 ** ALPHA_A) * (xa2 ** (1 - ALPHA_A))
ub_after = (xb1 ** ALPHA_B) * (xb2 ** (1 - ALPHA_B))
# ---- 数值验证：打印可手算核对的量 ----
print("均衡相对价格 r=p2/p1=%.8f (解析解 6/7=%.8f)" % (r, 6 / 7))
print("均衡超额需求 z1=%.2e z2=%.2e (应为 0)" % (z_1, z_2))
print("A 消费=(%.6f, %.6f)  B 消费=(%.6f, %.6f)" % (xa1, xa2, xb1, xb2))
print("市场1总量=%.6f 市场2总量=%.6f (禀赋均为 1)" % (xa1 + xb1, xa2 + xb2))
print("瓦尔拉斯法则在 r=0.5 时 p·z=%.2e (恒为 0)" % walras)
print("贸易后效用 A=%.6f (贸易前 0) B=%.6f (贸易前 0)" % (ua_after, ub_after))

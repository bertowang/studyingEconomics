#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 08-risk.py | 跨期贴现与期望效用（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
C_ANNUAL, RATE, YEARS = 100.0, 0.05, 20
BETA = 0.95
W_LOW, W_HIGH, P_HIGH = 80.0, 120.0, 0.5
N_DRAWS = 20000
# ---- 跨期：年金现值 ----
pv = C_ANNUAL * (1 - (1 + RATE) ** (-YEARS)) / RATE
perpetuity = C_ANNUAL / RATE
c_ratio = BETA * (1 + RATE)     # 对数效用下 c2/c1
# ---- 风险：解析期望效用 ----
eu = (1 - P_HIGH) * math.log(W_LOW) + P_HIGH * math.log(W_HIGH)
ce = math.exp(eu)
expected_w = (1 - P_HIGH) * W_LOW + P_HIGH * W_HIGH
rp = expected_w - ce
# ---- 蒙特卡洛核对 ----
draws = [W_HIGH if random.random() < P_HIGH else W_LOW for _ in range(N_DRAWS)]
mc_mean = statistics.fmean(draws)
mc_ce = math.exp(statistics.fmean([math.log(w) for w in draws]))
# ---- 数值验证：打印可手算核对的量 ----
print("年金现值(T=%d)=%.4f  永续现值=%.4f" % (YEARS, pv, perpetuity))
print("欧拉方程 c2/c1=beta*(1+r)=%.4f" % c_ratio)
print("EU=%.6f  CE=%.6f (=sqrt(80*120)=%.6f)" % (eu, ce, math.sqrt(W_LOW * W_HIGH)))
print("E[w]=%.4f  风险溢价 RP=%.4f" % (expected_w, rp))
print("蒙特卡洛: 平均财富=%.4f  几何平均(CE)=%.4f  与解析差=%.4f" %
      (mc_mean, mc_ce, mc_ce - ce))

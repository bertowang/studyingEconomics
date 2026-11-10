#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 30-options.py | 欧式期权三种定价方法（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
S0, K, R, SIGMA, T = 100.0, 100.0, 0.05, 0.20, 1.0
N_STEPS = 200
N_PATHS = 20000

def norm_cdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))

# ---- 1. CRR 二叉树回溯 ----
dt = T / N_STEPS
u = math.exp(SIGMA * math.sqrt(dt))
d = 1 / u
p = (math.exp(R * dt) - d) / (u - d)
disc = math.exp(-R * dt)
call = [max(S0 * (u ** j) * (d ** (N_STEPS - j)) - K, 0.0)
        for j in range(N_STEPS + 1)]
put = [max(K - S0 * (u ** j) * (d ** (N_STEPS - j)), 0.0)
       for j in range(N_STEPS + 1)]
for step in range(N_STEPS, 0, -1):
    call = [disc * (p * call[j + 1] + (1 - p) * call[j]) for j in range(step)]
    put = [disc * (p * put[j + 1] + (1 - p) * put[j]) for j in range(step)]
c_tree, p_tree = call[0], put[0]
# ---- 2. Black-Scholes 闭式解 ----
d1 = (math.log(S0 / K) + (R + 0.5 * SIGMA ** 2) * T) / (SIGMA * math.sqrt(T))
d2 = d1 - SIGMA * math.sqrt(T)
c_bs = S0 * norm_cdf(d1) - K * math.exp(-R * T) * norm_cdf(d2)
p_bs = K * math.exp(-R * T) * norm_cdf(-d2) - S0 * norm_cdf(-d1)
# ---- 3. 蒙特卡洛 ----
rng = random.Random(7)
payoffs = []
for _ in range(N_PATHS):
    z = rng.gauss(0, 1)
    st = S0 * math.exp((R - 0.5 * SIGMA ** 2) * T + SIGMA * math.sqrt(T) * z)
    payoffs.append(max(st - K, 0.0))
c_mc = math.exp(-R * T) * statistics.fmean(payoffs)
mc_se = math.exp(-R * T) * statistics.pstdev(payoffs) / math.sqrt(N_PATHS)
# ---- 4. delta 有限差分 ----
def bs_call(s):
    dd1 = (math.log(s / K) + (R + 0.5 * SIGMA ** 2) * T) / (SIGMA * math.sqrt(T))
    dd2 = dd1 - SIGMA * math.sqrt(T)
    return s * norm_cdf(dd1) - K * math.exp(-R * T) * norm_cdf(dd2)
delta = (bs_call(S0 + 0.01) - bs_call(S0 - 0.01)) / 0.02
# ---- 数值验证：打印可手算核对的量 ----
print("参数: S=K=%.0f r=%.2f sigma=%.2f T=%.0f N=%d" %
      (S0, R, SIGMA, T, N_STEPS))
print("二叉树   call=%.6f put=%.6f" % (c_tree, p_tree))
print("B-S 公式 call=%.6f put=%.6f" % (c_bs, p_bs))
print("蒙特卡洛 call=%.6f ±%.6f (1 倍标准误, %d 路径)" % (c_mc, mc_se, N_PATHS))
print("平价校验 C-P=%.6f  S-K*e^(-rT)=%.6f  差=%.2e" %
      (c_tree - p_tree, S0 - K * math.exp(-R * T),
       abs((c_tree - p_tree) - (S0 - K * math.exp(-R * T)))))
print("delta=%.6f (≈N(d1)=%.6f)" % (delta, norm_cdf(d1)))

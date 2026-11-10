#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 26-returns.py | 收益定义与几何布朗运动（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
S0, MU, SIGMA = 100.0, 0.08, 0.20
DT, STEPS = 1.0 / 12, 240       # 20 年月度
N_PATHS = 4000
# ---- 单条路径 ----
rng = random.Random(7)
prices, logrets, simple = [S0], [], []
s = S0
for _ in range(STEPS):
    z = rng.gauss(0, 1)
    r = (MU - 0.5 * SIGMA ** 2) * DT + SIGMA * math.sqrt(DT) * z
    s *= math.exp(r)
    prices.append(s)
    logrets.append(r)
    simple.append(math.exp(r) - 1)
mean_r = statistics.fmean(logrets)
mean_simple = statistics.fmean(simple)
vol_month = statistics.pstdev(logrets)
total_log = sum(logrets)
# ---- 蒙特卡洛：终点价格期望 E[S_T] = S0*exp(mu*T) ----
mc = random.Random(19)
terminals = []
for _ in range(N_PATHS):
    st = S0 * math.exp((MU - 0.5 * SIGMA ** 2) * (STEPS * DT) +
                       SIGMA * math.sqrt(STEPS * DT) * mc.gauss(0, 1))
    terminals.append(st)
# ---- 最大回撤 ----
peak, mdd = prices[0], 0.0
for p in prices:
    peak = max(peak, p)
    mdd = max(mdd, (peak - p) / peak)
# ---- 数值验证：打印可手算核对的量 ----
print("终点价格=%.4f  S0*exp(sum r)=%.4f (恒等式)" %
      (prices[-1], S0 * math.exp(total_log)))
print("月对数收益均值=%.6f 简单收益均值=%.6f 差≈sigma²*dt/2=%.6f" %
      (mean_r, mean_simple, 0.5 * SIGMA ** 2 * DT))
print("年化对数收益=%.4f%% 年化波动=%.4f%% (目标 %.2f%%)" %
      (100 * mean_r / DT, 100 * vol_month / math.sqrt(DT), 100 * SIGMA))
print("长期增长率 E[r]-0.5sigma²=%.4f%% (算术漂移 %.2f%%)" %
      (100 * (MU - 0.5 * SIGMA ** 2), 100 * MU))
print("蒙特卡洛 E[S_T]=%.4f 解析=%.4f" %
      (statistics.fmean(terminals), S0 * math.exp(MU * STEPS * DT)))
print("单路径最大回撤=%.2f%%" % (100 * mdd))

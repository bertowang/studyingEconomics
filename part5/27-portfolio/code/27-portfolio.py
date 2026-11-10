#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 27-portfolio.py | 两资产组合与切点组合（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
MU1, MU2 = 0.08, 0.12
S1, S2, RHO = 0.15, 0.25, 0.30
RF = 0.03
GRID = 1000

def stats(w):
    mu = w * MU1 + (1 - w) * MU2
    var = (w * w * S1 ** 2 + (1 - w) ** 2 * S2 ** 2 +
           2 * w * (1 - w) * RHO * S1 * S2)
    return mu, math.sqrt(var)

w_min = (S2 ** 2 - RHO * S1 * S2) / (S1 ** 2 + S2 ** 2 - 2 * RHO * S1 * S2)
mu_min, sd_min = stats(w_min)
best_w, best_sharpe = 0.0, -1e9
for i in range(GRID + 1):
    w = -0.5 + 1.5 * i / GRID      # 允许少量卖空以看清前沿形状
    mu, sd = stats(w)
    sh = (mu - RF) / sd
    if sh > best_sharpe:
        best_w, best_sharpe = w, sh
mu_t, sd_t = stats(best_w)
# ---- ρ=1 时无分散化收益的对照 ----
cov = RHO * S1 * S2
sd_equal = math.sqrt(0.25 * S1 ** 2 + 0.25 * S2 ** 2 + 0.5 * cov)
sd_equal_rho1 = math.sqrt(0.25 * S1 ** 2 + 0.25 * S2 ** 2 + 0.5 * S1 * S2)
# ---- 数值验证：打印可手算核对的量 ----
print("资产1: mu=%.2f sd=%.2f  资产2: mu=%.2f sd=%.2f  rho=%.2f" %
      (MU1, S1, MU2, S2, RHO))
print("最小方差权重 w*=%.6f 组合 sd=%.6f (低于两资产)" % (w_min, sd_min))
print("最大夏普权重 w=%.6f 夏普=%.6f mu=%.6f sd=%.6f" %
      (best_w, best_sharpe, mu_t, sd_t))
print("等权组合 sd=%.6f ; 若 rho=1 则 sd=%.6f (无分散化收益)" %
      (sd_equal, sd_equal_rho1))
print("切点组合超预期收益/风险 = %.6f = 夏普比率" % ((mu_t - RF) / sd_t))

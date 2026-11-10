#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 23-iv.py | 工具变量与两阶段最小二乘（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
N, REPS = 20000, 400
BETA1 = 2.0
PI_STRONG, PI_WEAK = 0.8, 0.05
S_U, S_E = 1.0, 1.0

def cov(a, b):
    ma, mb = statistics.fmean(a), statistics.fmean(b)
    return sum((a[i] - ma) * (b[i] - mb) for i in range(len(a))) / len(a)

def slope(xs, ys):
    return cov(xs, ys) / cov(xs, xs)

def dgp(rng, n, pi):
    z = [rng.gauss(0, 1) for _ in range(n)]
    u = [rng.gauss(0, S_U) for _ in range(n)]
    e = [rng.gauss(0, S_E) for _ in range(n)]
    x = [pi * z[i] + 0.6 * u[i] + e[i] for i in range(n)]
    y = [1.0 + BETA1 * x[i] + u[i] for i in range(n)]
    return z, x, y

def estimate(z, x, y):
    b_ols = slope(x, y)
    b_iv = cov(z, y) / cov(z, x)
    pi1 = slope(z, x)
    zbar, xbar = statistics.fmean(z), statistics.fmean(x)
    xhat = [xbar + pi1 * (zi - zbar) for zi in z]
    b_2sls = slope(xhat, y)
    return b_ols, b_iv, b_2sls, pi1

rng = random.Random(7)
z, x, y = dgp(rng, N, PI_STRONG)
b_ols, b_iv, b_2sls, pi1 = estimate(z, x, y)
# ---- 弱工具：重复抽样的 IV 分布 ----
weak_rng = random.Random(19)
weak_iv = []
for _ in range(REPS):
    zz, xx, yy = dgp(weak_rng, 500, PI_WEAK)
    weak_iv.append(cov(zz, yy) / cov(zz, xx))
# ---- 数值验证：打印可手算核对的量 ----
print("真实 beta1=%.2f" % BETA1)
print("OLS=%.6f (内生性导致上偏)  IV=%.6f  2SLS=%.6f" % (b_ols, b_iv, b_2sls))
print("IV 与 2SLS 差=%.2e (代数等价)" % abs(b_iv - b_2sls))
print("第一阶段斜率 pi1=%.6f (强工具)" % pi1)
print("弱工具 %d 次: IV 均值=%.4f 标准差=%.4f (偏回 OLS 且方差巨大)" %
      (REPS, statistics.fmean(weak_iv), statistics.pstdev(weak_iv)))

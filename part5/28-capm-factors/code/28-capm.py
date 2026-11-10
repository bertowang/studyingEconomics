#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 28-capm.py | CAPM 时间序列与横截面回归（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
T = 240                      # 20 年月度
RF_M, MU_M_M, SD_M_M = 0.03 / 12, 0.08 / 12, 0.16 / math.sqrt(12)
N_ASSETS = 12
BETAS = [0.4 + 0.12 * i for i in range(N_ASSETS)]
ALPHAS = [0.0] * N_ASSETS
IDIO_SD = 0.01

def mean(v):
    return statistics.fmean(v)

def cov(a, b):
    ma, mb = mean(a), mean(b)
    return sum((a[i] - ma) * (b[i] - mb) for i in range(len(a))) / len(a)

def ols1(xs, ys):
    b = cov(xs, ys) / cov(xs, xs)
    a = mean(ys) - b * mean(xs)
    e = [ys[i] - a - b * xs[i] for i in range(len(xs))]
    tss = sum((y - mean(ys)) ** 2 for y in ys)
    r2 = 1 - sum(v * v for v in e) / tss
    s2 = sum(v * v for v in e) / (len(xs) - 2)
    se = math.sqrt(s2 / (cov(xs, xs) * len(xs)))
    return a, b, se, r2

# ---- DGP: 市场因子 + 三个因子暴露 ----
rng = random.Random(7)
mkt = [rng.gauss(MU_M_M, SD_M_M) for _ in range(T)]
excess_m = [m - RF_M for m in mkt]
smb = [rng.gauss(0.001, 0.02) for _ in range(T)]
hml = [rng.gauss(0.001, 0.02) for _ in range(T)]
series = []
for beta, alpha in zip(BETAS, ALPHAS):
    ri_excess = [alpha + beta * excess_m[t] +
                 0.4 * smb[t] + 0.2 * hml[t] + rng.gauss(0, IDIO_SD)
                 for t in range(T)]
    series.append(ri_excess)
# ---- 第一步：时间序列 CAPM 回归 ----
est = [ols1(excess_m, s) for s in series]
# ---- 第二步：横截面回归 mean(r_i) ~ beta_i ----
xs = [e[1] for e in est]
ys = [mean(s) for s in series]
a_cs, b_cs, se_cs, r2_cs = ols1(xs, ys)
# ---- 三因子回归的 R² 增量 ----
def ols3(rows, y):
    # 用标准库做 4x4 高斯-约当求逆
    n = 4
    xtx = [[0.0] * n for _ in range(n)]
    xty = [0.0] * n
    for row, yi in zip(rows, y):
        for i in range(n):
            xty[i] += row[i] * yi
            for j in range(n):
                xtx[i][j] += row[i] * row[j]
    m = [list(xtx[i]) + [1.0 if i == j else 0.0 for j in range(n)]
         for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        m[c], m[p] = m[p], m[c]
        d = m[c][c]
        for j in range(2 * n):
            m[c][j] /= d
        for r in range(n):
            if r != c:
                f = m[r][c]
                if f:
                    for j in range(2 * n):
                        m[r][j] -= f * m[c][j]
    inv = [row[n:] for row in m]
    b = [sum(inv[i][j] * xty[j] for j in range(n)) for i in range(n)]
    e = [yi - sum(b[k] * row[k] for k in range(n))
         for row, yi in zip(rows, y)]
    tss = sum((yi - mean(y)) ** 2 for yi in y)
    return 1 - sum(v * v for v in e) / tss

rows = [[1.0, excess_m[t], smb[t], hml[t]] for t in range(T)]
r2_3f = ols3(rows, series[0])
# ---- 数值验证：打印可手算核对的量 ----
print("市场月超额收益: 样本=%.6f 理论=%.6f 年化≈%.2f%%" %
      (mean(excess_m), MU_M_M - RF_M, 1200 * mean(excess_m)))
for i in (0, 5, 11):
    a, b, bse, r2 = est[i]
    print("资产%02d beta_hat=%.4f (真 %.2f) beta_se=%.6f alpha_hat=%.6f R2=%.4f" %
          (i + 1, b, BETAS[i], bse, a, r2))
print("横截面斜率=%.6f (对照市场已实现超额收益 %.6f) 截距=%.6f R2=%.4f" %
      (b_cs, mean(excess_m), a_cs, r2_cs))
print("加入 SMB/HML 后资产1 R2: %.4f -> %.4f" % (est[0][3], r2_3f))

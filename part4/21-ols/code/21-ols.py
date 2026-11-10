#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 21-ols.py | 从零实现多元 OLS：beta / se / t / R2（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
N, REPS = 400, 500
BETA = [1.0, 2.0, -1.5]       # 截距, x1, x2 的真实系数
NOISE_SD = 1.0

def inverse(a):
    n = len(a)
    m = [list(a[i]) + [1.0 if i == j else 0.0 for j in range(n)]
          for i in range(n)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(m[r][col]))
        m[col], m[piv] = m[piv], m[col]
        p = m[col][col]
        for j in range(2 * n):
            m[col][j] /= p
        for r in range(n):
            if r != col:
                f = m[r][col]
                if f:
                    for j in range(2 * n):
                        m[r][j] -= f * m[col][j]
    return [row[n:] for row in m]

def ols(rows, ys):
    xtx = [[0.0] * 3 for _ in range(3)]
    xty = [0.0] * 3
    for row, y in zip(rows, ys):
        for i in range(3):
            xty[i] += row[i] * y
            for j in range(3):
                xtx[i][j] += row[i] * row[j]
    inv = inverse(xtx)
    beta = [sum(inv[i][j] * xty[j] for j in range(3)) for i in range(3)]
    resid = [y - sum(b * x for b, x in zip(beta, row))
             for row, y in zip(rows, ys)]
    k = 3
    s2 = sum(r * r for r in resid) / (len(ys) - k)
    se = [math.sqrt(s2 * inv[i][i]) for i in range(3)]
    my = statistics.fmean(ys)
    tss = sum((y - my) ** 2 for y in ys)
    rss = sum(r * r for r in resid)
    return beta, se, 1 - rss / tss

def sample(seed_rng):
    rows, ys = [], []
    for _ in range(N):
        x1 = seed_rng.uniform(0, 10)
        x2 = 0.5 * x1 + seed_rng.gauss(0, 1)
        u = seed_rng.gauss(0, NOISE_SD)
        rows.append([1.0, x1, x2])
        ys.append(BETA[0] + BETA[1] * x1 + BETA[2] * x2 + u)
    return rows, ys

rng = random.Random(7)
rows, ys = sample(rng)
beta, se, r2 = ols(rows, ys)
# ---- 蒙特卡洛：验证无偏与标准误 ----
mc_rng = random.Random(11)
b1s, t1s = [], []
for _ in range(REPS):
    rr, yy = sample(mc_rng)
    b, s, _ = ols(rr, yy)
    b1s.append(b[1])
    t1s.append((b[1] - BETA[1]) / s[1])
# ---- 数值验证：打印可手算核对的量 ----
print("真实 beta =", BETA)
print("估计 beta = [%.6f, %.6f, %.6f]" % tuple(beta))
print("标准误   = [%.6f, %.6f, %.6f]" % tuple(se))
print("t 值(H0:beta=0) = [%.3f, %.3f, %.3f]" %
      tuple(beta[i] / se[i] for i in range(3)))
print("R²=%.4f  残差均值=%.6f (应近 0)" %
      (r2, statistics.fmean([y - sum(b * x for b, x in zip(beta, row))
                            for row, y in zip(rows, ys)])))
print("蒙特卡洛 %d 次: beta1 均值=%.6f 标准差=%.6f 单次 se=%.6f" %
      (REPS, statistics.fmean(b1s), statistics.pstdev(b1s), se[1]))
print("|t|>1.96 比例=%.4f (名义 0.05)" %
      (sum(1 for t in t1s if abs(t) > 1.96) / REPS))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 25-timeseries.py | 平稳性与伪回归蒙特卡洛（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
T, REPS = 200, 400
PHI = 0.8
SIGMA = 1.0
BETA_COINT = 2.0

def mean(v):
    return statistics.fmean(v)

def lag1_corr(v):
    a, b = v[:-1], v[1:]
    ma, mb = mean(a), mean(b)
    num = sum((a[i] - ma) * (b[i] - mb) for i in range(len(a)))
    den = math.sqrt(sum((x - ma) ** 2 for x in a) * sum((x - mb) ** 2 for x in b))
    return num / den

def ols1(xs, ys):
    mx, my = mean(xs), mean(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    b = sum((xs[i] - mx) * (ys[i] - my) for i in range(len(xs))) / sxx
    a = my - b * mx
    e = [ys[i] - a - b * xs[i] for i in range(len(xs))]
    s2 = sum(v * v for v in e) / (len(xs) - 2)
    se = math.sqrt(s2 / sxx)
    tss = sum((y - my) ** 2 for y in ys)
    r2 = 1 - sum(v * v for v in e) / tss
    return b, b / se, r2, e

def random_walk(rng, t):
    v, out = 0.0, []
    for _ in range(t):
        v += rng.gauss(0, SIGMA)
        out.append(v)
    return out
# ---- 平稳 AR(1) ----
rng = random.Random(7)
x, ar = 0.0, []
for _ in range(10000):
    x = PHI * x + rng.gauss(0, SIGMA)
    ar.append(x)
# ---- 伪回归蒙特卡洛 ----
mc = random.Random(23)
false_pos, r2_list = 0, []
for _ in range(REPS):
    xx, yy = random_walk(mc, T), random_walk(mc, T)
    b, t, r2, e = ols1(xx, yy)
    if abs(t) > 1.96:
        false_pos += 1
    r2_list.append(r2)
# ---- 协整：y = 2x + 平稳噪声 ----
coint = random.Random(31)
xc, yc = 0.0, []
xc_path = []
for _ in range(T):
    xc += coint.gauss(0, SIGMA)
    xc_path.append(xc)
    yc.append(BETA_COINT * xc + coint.gauss(0, 0.5))
_, _, _, ec = ols1(xc_path, yc)
# ---- 数值验证：打印可手算核对的量 ----
print("AR(1): 理论方差=%.4f 样本方差=%.4f" %
      (SIGMA ** 2 / (1 - PHI ** 2), statistics.pvariance(ar)))
print("AR(1): 理论 lag1 自相关=%.4f 样本=%.4f" % (PHI, lag1_corr(ar)))
print("伪回归 %d 次(两条独立随机游走): |t|>1.96 比例=%.4f 平均 R²=%.4f" %
      (REPS, false_pos / REPS, mean(r2_list)))
print("协整回归残差 lag1 自相关=%.4f (平稳残差应远小于 1)" % lag1_corr(ec))
print("对照: 水平序列自相关≈%.4f" % lag1_corr(yc))

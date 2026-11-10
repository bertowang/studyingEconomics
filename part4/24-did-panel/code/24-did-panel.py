#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 24-did-panel.py | 三种准实验设计（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
N_UNITS, TAU = 4000, 3.0
N_FE_UNITS, T_FE = 600, 4
N_RDD = 20000
BANDWIDTH = 0.3

def mean(v):
    return statistics.fmean(v)

def linfit(xs, ys):
    mx, my = mean(xs), mean(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    b = sum((xs[i] - mx) * (ys[i] - my) for i in range(len(xs))) / sxx
    return my - b * mx, b

# ---- 1. DID：两期两组 ----
rng = random.Random(7)
cells = {(g, t): [] for g in (0, 1) for t in (0, 1)}
trend_cells_pretrend = {(g, t): [] for g in (0, 1) for t in (-1, 0, 1)}
for i in range(N_UNITS):
    a_i = rng.gauss(0, 1)
    g = 1 if i >= N_UNITS // 2 else 0
    for t in (0, 1):
        y = 10 + a_i + 0.5 * t + 1.0 * g + TAU * g * t + rng.gauss(0, 0.5)
        cells[(g, t)].append(y)
    for t in (-1, 0, 1):
        y = 10 + a_i + 0.5 * t + 1.0 * g + (TAU * g * t if t == 1 else 0) + \
            0.8 * g * t + rng.gauss(0, 0.5)
        trend_cells_pretrend[(g, t)].append(y)
m = {k: mean(v) for k, v in cells.items()}
did = (m[(1, 1)] - m[(1, 0)]) - (m[(0, 1)] - m[(0, 0)])
mt = {k: mean(v) for k, v in trend_cells_pretrend.items()}
pre_gap = (mt[(1, 0)] - mt[(1, -1)]) - (mt[(0, 0)] - mt[(0, -1)])
did_bad = (mt[(1, 1)] - mt[(1, 0)]) - (mt[(0, 1)] - mt[(0, 0)])
# ---- 2. 固定效应 ----
rng2 = random.Random(17)
pooled_x, pooled_y, dx, dy = [], [], [], []
for _ in range(N_FE_UNITS):
    a_i = rng2.gauss(0, 1)
    xs = [0.5 * a_i + rng2.gauss(0, 1) for _ in range(T_FE)]
    ys = [a_i + 2.0 * x + rng2.gauss(0, 0.5) for x in xs]
    pooled_x.extend(xs); pooled_y.extend(ys)
    mx, my = mean(xs), mean(ys)
    dx.extend([x - mx for x in xs]); dy.extend([y - my for y in ys])
_, b_pooled = linfit(pooled_x, pooled_y)
b_fe = sum(dx[i] * dy[i] for i in range(len(dx))) / sum(v * v for v in dx)
# ---- 3. RDD：局部线性 ----
rng3 = random.Random(31)
x_all, y_all, x_l, y_l, x_r, y_r = [], [], [], [], [], []
for _ in range(N_RDD):
    xv = rng3.uniform(-1, 1)
    d = 1 if xv >= 0 else 0
    yv = 0.5 * xv + TAU * d + rng3.gauss(0, 0.5)
    x_all.append(xv); y_all.append(yv)
    if abs(xv) <= BANDWIDTH:
        (x_l if xv < 0 else x_r).append(xv)
        (y_l if xv < 0 else y_r).append(yv)
naive = mean([y_all[i] for i in range(N_RDD) if x_all[i] >= 0]) - \
        mean([y_all[i] for i in range(N_RDD) if x_all[i] < 0])
a_l, b_l = linfit(x_l, y_l)
a_r, b_r = linfit(x_r, y_r)
rdd = a_r - a_l
# ---- 数值验证：打印可手算核对的量 ----
print("真实处理效应 tau=%.2f" % TAU)
print("DID(平行趋势成立)=%.4f" % did)
print("预趋势差分=%.4f (显著非 0 说明违背平行趋势)" % pre_gap)
print("DID(存在 0.8 差别趋势)=%.4f (被推离真值)" % did_bad)
print("固定效应: 混合 OLS beta=%.4f (上偏)  组内去均值 beta=%.4f (真值 2)" %
      (b_pooled, b_fe))
print("RDD: 朴素均值差=%.4f (含 0.5x 趋势) 局部线性跳跃=%.4f" % (naive, rdd))
print("带宽内样本: 左=%d 右=%d" % (len(x_l), len(x_r)))

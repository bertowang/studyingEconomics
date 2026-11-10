#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 22-diagnostics.py | 手写 HC0 与诊断量（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
N, REPS = 200, 1000
B0, B1 = 1.0, 2.0
RHO_AR = 0.7

def ols1(xs, ys):
    mx, my = statistics.fmean(xs), statistics.fmean(ys)
    dx = [x - mx for x in xs]
    sxx = sum(v * v for v in dx)
    sxy = sum(dx[i] * (ys[i] - my) for i in range(len(xs)))
    b = sxy / sxx
    a = my - b * mx
    e = [ys[i] - a - b * xs[i] for i in range(len(xs))]
    s2 = sum(v * v for v in e) / (len(xs) - 2)
    se = math.sqrt(s2 / sxx)
    se_rob = math.sqrt(sum(e[i] ** 2 * dx[i] ** 2 for i in range(len(xs))) / sxx ** 2)
    return a, b, se, se_rob, e

def one_sample(rng):
    xs = [10.0 * i / N for i in range(N)]
    # 异方差: 噪声标准差随 x 增大
    ys = [B0 + B1 * x + rng.gauss(0, 0.5 + 0.3 * x) for x in xs]
    return xs, ys

rng = random.Random(7)
xs, ys = one_sample(rng)
a, b, se, se_rob, e = ols1(xs, ys)
# ---- 蒙特卡洛：两种 se 的假阳性率 ----
mc = random.Random(23)
r_ordinary, r_robust = 0, 0
for _ in range(REPS):
    xx, yy = one_sample(mc)
    _, bb, s1, s2, _ = ols1(xx, yy)
    if abs((bb - B1) / s1) > 1.96:
        r_ordinary += 1
    if abs((bb - B1) / s2) > 1.96:
        r_robust += 1
# ---- AR(1) 残差与 DW ----
ar_rng = random.Random(31)
prev, errs = 0.0, []
for _ in range(N):
    prev = RHO_AR * prev + ar_rng.gauss(0, 1)
    errs.append(prev)
dw = sum((errs[i] - errs[i - 1]) ** 2 for i in range(1, N)) / sum(v * v for v in errs)
# ---- 共线性：VIF 与 se 膨胀 ----
vifs = [(r, 1 / (1 - r * r), math.sqrt(1 / (1 - r * r))) for r in (0.0, 0.9, 0.99)]
# ---- 数值验证：打印可手算核对的量 ----
print("单样本 beta1=%.6f (真实 %.2f) 普通 se=%.6f 稳健 se=%.6f" % (b, B1, se, se_rob))
print("蒙特卡洛 %d 次 H0 假阳性率: 普通 se=%.4f 稳健 se=%.4f (名义 0.05)" %
      (REPS, r_ordinary / REPS, r_robust / REPS))
print("DW=%.4f ≈ 2(1-rho)=%.4f" % (dw, 2 * (1 - RHO_AR)))
for r, vif, infl in vifs:
    print("  相关系数 r=%.2f  VIF=%.2f  se 膨胀=%.2f 倍" % (r, vif, infl))

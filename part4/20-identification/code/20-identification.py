#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 20-identification.py | 已知真值 ATE 的识别实验（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
N = 20000
TAU = 2.0                 # 真实 ATE
BETA_ABILITY = 0.5        # 能力对基线结果的影响
NOISE_SD = 0.5
# ---- DGP: 能力 A 决定自我选择，Y(1)=Y(0)+TAU ----
ability = [random.gauss(0, 1) for _ in range(N)]
d = [1 if a + random.gauss(0, 1) > 0 else 0 for a in ability]
y0 = [1.0 + BETA_ABILITY * a + random.gauss(0, NOISE_SD) for a in ability]
y1 = [v + TAU for v in y0]
y = [y1[i] if d[i] else y0[i] for i in range(N)]
ate_true = statistics.fmean([y1[i] - y0[i] for i in range(N)])
# ---- 估计 1: 观测组间差 ----
m1 = statistics.fmean([y[i] for i in range(N) if d[i] == 1])
m0 = statistics.fmean([y[i] for i in range(N) if d[i] == 0])
naive = m1 - m0
sel_bias = statistics.fmean([y0[i] for i in range(N) if d[i] == 1]) - \
           statistics.fmean([y0[i] for i in range(N) if d[i] == 0])
# ---- 估计 2: 随机指派（反事实实验）----
d_r = [1 if random.random() < 0.5 else 0 for _ in range(N)]
y_r = [y1[i] if d_r[i] else y0[i] for i in range(N)]
mr1 = statistics.fmean([y_r[i] for i in range(N) if d_r[i] == 1])
mr0 = statistics.fmean([y_r[i] for i in range(N) if d_r[i] == 0])
rand_est = mr1 - mr0
# ---- 估计 3: 按能力分层后加权（条件独立）----
order = sorted(range(N), key=lambda i: ability[i])
strata = [order[k * N // 4:(k + 1) * N // 4] for k in range(4)]
strat_est = 0.0
for s in strata:
    t = [i for i in s if d[i] == 1]
    c = [i for i in s if d[i] == 0]
    strat_est += (statistics.fmean([y[i] for i in t]) -
                  statistics.fmean([y[i] for i in c])) * len(s) / N
# ---- 数值验证：打印可手算核对的量 ----
print("真实 ATE=%.4f 处理组比例=%.4f" % (ate_true, sum(d) / N))
print("朴素组间差=%.4f = ATE %.4f + 选择偏误 %.4f" % (naive, ate_true, sel_bias))
print("随机指派估计=%.4f (误差 %.4f)" % (rand_est, rand_est - ate_true))
print("按能力四分层估计=%.4f (误差 %.4f)" % (strat_est, strat_est - ate_true))

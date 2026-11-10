#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 31-reproducibility.py | 多重检验的蒙特卡洛（只用标准库）
import math, random, statistics
from statistics import NormalDist
random.seed(7)
# ---- 参数区 ----
N, M_TESTS, REPS = 100, 20, 1000
ALPHA = 0.05
TRUE_EFFECT = 0.3

def norm_sf(x):
    return 0.5 * (1 - math.erf(abs(x) / math.sqrt(2)))

def p_from_t(t):
    return 2 * norm_sf(t)

def mean(v):
    return statistics.fmean(v)

def t_stat(xs, ys):
    mx, my = mean(xs), mean(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    b = sum((xs[i] - mx) * (ys[i] - my) for i in range(len(xs))) / sxx
    e = [ys[i] - my - b * (xs[i] - mx) for i in range(len(xs))]
    s2 = sum(v * v for v in e) / (len(xs) - 2)
    return b / math.sqrt(s2 / sxx)

# ---- t 分布临界值（Cornish-Fisher 一阶修正，df=N-2）----
df = N - 2
def t_crit(alpha):
    z = NormalDist().inv_cdf(1 - alpha / 2)
    return z + (z ** 3 + z) / (4 * df)
crit05 = t_crit(ALPHA)
crit_bonf = t_crit(ALPHA / M_TESTS)
# ---- 原假设为真：20 个候选解释变量都与 y 无关 ----
rng = random.Random(7)
raw, corrected, minp_sum = 0, 0, 0.0
for _ in range(REPS):
    y = [rng.gauss(0, 1) for _ in range(N)]
    ts = []
    for _ in range(M_TESTS):
        x = [rng.gauss(0, 1) for _ in range(N)]
        ts.append(abs(t_stat(x, y)))
    maxt = max(ts)
    minp_sum += p_from_t(maxt)
    if maxt > crit05:
        raw += 1
    if maxt > crit_bonf:
        corrected += 1
# ---- 真实效应下的功效 ----
power_rng = random.Random(19)
hits = 0
for _ in range(REPS):
    x = [power_rng.gauss(0, 1) for _ in range(N)]
    y = [TRUE_EFFECT * x[i] + power_rng.gauss(0, 1) for i in range(N)]
    if abs(t_stat(x, y)) > crit05:
        hits += 1
theory = 1 - (1 - ALPHA) ** M_TESTS
# ---- 数值验证：打印可手算核对的量 ----
print("临界值: t(0.975,df=%d)≈%.4f  Bonferroni 对应≈%.4f" % (df, crit05, crit_bonf))
print("单次检验 alpha=%.2f, m=%d, 独立检验至少一次假阳性理论=%.4f" %
      (ALPHA, M_TESTS, theory))
print("蒙特卡洛 %d 次: 未校正假阳性率=%.4f (最小 p 平均=%.4f)" %
      (REPS, raw / REPS, minp_sum / REPS))
print("Bonferroni 阈值=%.6f 校正后假阳性率=%.4f" %
      (ALPHA / M_TESTS, corrected / REPS))
print("真实效应 delta=%.2f, n=%d 时检出率(功效)=%.4f" %
      (TRUE_EFFECT, N, hits / REPS))
print("理论 z≈delta*sqrt(n)/sigma=%.4f" % (TRUE_EFFECT * math.sqrt(N)))

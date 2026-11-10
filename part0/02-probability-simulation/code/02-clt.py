#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""02-clt.py | 固定种子的重复抽样实验：LLN / CLT / 标准误"""
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
N = 25                 # 每个样本的观测数
REPS = 4000            # 重复抽样次数
CONF_Z = 1.96          # 正态近似 95% 临界值
# ---- DGP: Y ~ U(0,1)，mu=0.5，sigma^2=1/12 ----
mu, sigma = 0.5, math.sqrt(1.0 / 12.0)
means = []
for _ in range(REPS):
    draws = [random.random() for _ in range(N)]
    means.append(statistics.fmean(draws))
avg = statistics.fmean(means)
sd = statistics.pstdev(means)
se_theory = sigma / math.sqrt(N)
cover = sum(1 for m in means if abs(m - mu) <= CONF_Z * se_theory) / REPS
# ---- 数值验证：打印可手算核对的量 ----
rng = random.Random(7)
first3 = [rng.random() for _ in range(3)]
print("前 3 个随机数(固定种子): %.6f %.6f %.6f" % tuple(first3))
print("理论 mu=%.6f sigma=%.6f 标准误=%.6f" % (mu, sigma, se_theory))
print("重复抽样均值均值=%.6f 均值标准差=%.6f" % (avg, sd))
print("95%% 置信区间实际覆盖率=%.4f (理论约 0.95)" % cover)
print("n=25 时区间半宽=%.6f" % (CONF_Z * se_theory))

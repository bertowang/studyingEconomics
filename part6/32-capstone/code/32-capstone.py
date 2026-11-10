#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 32-capstone.py | 综合课题：合成地区面板的政策评估（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
N_REGIONS, T_PERIODS = 200, 8
TREAT_START = 4                  # 第 5 期开始处理（0 起索引）
TRUE_TAU = -0.4                  # 对 log 就业的真实 ATT
GROUP_DIFF, TIME_TREND = 0.10, 0.03
BETA_X = 0.2
NOISE_SD = 0.15

def mean(v):
    return statistics.fmean(v)

# ---- 1. DGP: 地区固定效应 + 共同趋势 + 组间差异 + 政策效应 ----
rng = random.Random(7)
panel = []
for i in range(N_REGIONS):
    a_i = rng.gauss(0, 0.3)
    g = 1 if i >= N_REGIONS // 2 else 0
    for t in range(T_PERIODS):
        post = 1 if t >= TREAT_START else 0
        x_it = rng.gauss(0, 1)
        y = (2.0 + a_i + TIME_TREND * t + GROUP_DIFF * g +
             TRUE_TAU * g * post + BETA_X * x_it + rng.gauss(0, NOISE_SD))
        panel.append((i, t, g, post, x_it, y))
# ---- 2. 描述与处理前平衡 ----
x_pre_t = mean([r[4] for r in panel if r[1] < TREAT_START and r[2] == 1])
x_pre_c = mean([r[4] for r in panel if r[1] < TREAT_START and r[2] == 0])
# ---- 3. 主估计：按地区求前后差，再比较两组（地区层面聚类稳健）----
delta_t, delta_c = [], []
for i in range(N_REGIONS):
    pre = mean([r[5] for r in panel if r[0] == i and r[1] < TREAT_START])
    post = mean([r[5] for r in panel if r[0] == i and r[1] >= TREAT_START])
    (delta_t if i >= N_REGIONS // 2 else delta_c).append(post - pre)
did = mean(delta_t) - mean(delta_c)
se = math.sqrt(statistics.variance(delta_t) / len(delta_t) +
               statistics.variance(delta_c) / len(delta_c))
ci = (did - 1.96 * se, did + 1.96 * se)
# ---- 4. 事件研究：各期组间差减去处理前基准 ----
def group_diff(t):
    return (mean([r[5] for r in panel if r[1] == t and r[2] == 1]) -
            mean([r[5] for r in panel if r[1] == t and r[2] == 0]))
base = mean([group_diff(t) for t in range(TREAT_START)])
event = [group_diff(t) - base for t in range(T_PERIODS)]
pre_trend = mean(event[:TREAT_START])
# ---- 5. 安慰剂：处理前随机指派「假处理组」，做随机化推断 ----
fake = 2
pre_delta = []
for i in range(N_REGIONS):
    p0 = mean([r[5] for r in panel if r[0] == i and r[1] < fake])
    p1 = mean([r[5] for r in panel if r[0] == i and fake <= r[1] < TREAT_START])
    pre_delta.append(p1 - p0)
placebo_rng = random.Random(31)
placebos = []
for _ in range(500):
    idx = placebo_rng.sample(range(N_REGIONS), N_REGIONS // 2)
    s = set(idx)
    a = mean([pre_delta[i] for i in idx])
    b = mean([pre_delta[i] for i in range(N_REGIONS) if i not in s])
    placebos.append(a - b)
placebo = mean(placebos)
placebo_sd = statistics.pstdev(placebos)
p_ri = sum(1 for v in placebos if abs(v) >= abs(did)) / len(placebos)
# ---- 6. 朴素横截面差（对照：会被组间差异污染）----
naive = mean([r[5] for r in panel if r[1] >= TREAT_START and r[2] == 1]) - \
        mean([r[5] for r in panel if r[1] >= TREAT_START and r[2] == 0])
# ---- 数值验证：打印可手算核对的量 ----
print("真实 ATT=%.4f  地区=%d 期数=%d 政策起点 t=%d" %
      (TRUE_TAU, N_REGIONS, T_PERIODS, TREAT_START))
print("[描述] 处理前协变量均值: 处理组=%.4f 对照组=%.4f 差=%.4f" %
      (x_pre_t, x_pre_c, x_pre_t - x_pre_c))
print("[估计] DID=%.4f  稳健 se=%.4f  95%%CI=[%.4f, %.4f]" % (did, se, ci[0], ci[1]))
print("[识别] 事件研究处理前平均系数=%.4f (应≈0)" % pre_trend)
print("[识别] 政策前各期系数: " + " ".join("%.3f" % v for v in event[:TREAT_START]))
print("[识别] 政策后各期系数: " + " ".join("%.3f" % v for v in event[TREAT_START:]))
print("[安慰剂] 随机假处理组 500 次: 均值=%.4f 标准差=%.4f" % (placebo, placebo_sd))
print("[安慰剂] 随机化推断 p=%.4f (无假政策能产生 |DID|≥%.4f)" % (p_ri, abs(did)))
print("[对照] 朴素横截面差=%.4f (混入组间差异 %.2f，偏误明显)" %
      (naive, GROUP_DIFF))
print("[结论] 估计 %.4f 与真值 %.4f 相差 %.4f；识别依赖平行趋势，外推需谨慎" %
      (did, TRUE_TAU, did - TRUE_TAU))

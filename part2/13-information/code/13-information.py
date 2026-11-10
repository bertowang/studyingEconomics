#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 13-information.py | 逆向选择的价格-质量反馈与 Spence 信号（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
Q_MAX = 100.0        # 质量上界
ALPHA = 0.8          # 卖家保留价值 = alpha * q
GAMMA = 1.2          # 买家估值 = gamma * q
P_START = 60.0
STEPS = 12
THETA_L, THETA_H = 1.0, 2.0
# ---- 柠檬市场：迭代 p <- gamma * E[q | alpha*q <= p] ----
def avg_quality(p):
    cutoff = min(Q_MAX, p / ALPHA)
    return cutoff / 2.0

p = P_START
trace = [p]
for _ in range(STEPS):
    p = GAMMA * avg_quality(p)
    trace.append(p)
ratio = GAMMA / (2 * ALPHA)
# ---- 信号：分离均衡的教育区间 ----
e_low = THETA_H - THETA_L                 # 低类型不冒充的下界
e_high = THETA_H * (THETA_H - THETA_L)   # 高类型愿意选的上界
check_low = THETA_H - e_low / THETA_L    # 冒充所得
check_high = THETA_H - e_low / THETA_H   # 选择所得
# ---- 数值验证：打印可手算核对的量 ----
print("参数: alpha=%.2f gamma=%.2f 收敛因子 gamma/(2 alpha)=%.4f" % (ALPHA, GAMMA, ratio))
print("价格迭代(前 6 步): " + " -> ".join("%.4f" % x for x in trace[:6]))
print("第 %d 步价格=%.8f (收敛因子<1 时趋于 0)" % (STEPS, trace[-1]))
print("分离均衡教育区间 e ∈ [%.2f, %.2f]" % (e_low, e_high))
print("e=1 时低类型冒充所得=%.2f (=不冒充的工资 %.2f)" % (check_low, THETA_L))
print("e=1 时高类型净所得=%.2f (>低类型工资 %.2f)" % (check_high, THETA_L))

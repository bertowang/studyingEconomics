#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 10-monopoly.py | MR=MC、弹性加价与分组定价（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
A, B, MC = 100.0, 2.0, 10.0     # 单市场反需求 p=A-B*Q
M1 = (100.0, 2.0)               # 市场 1: (a, b)
M2 = (80.0, 4.0)                # 市场 2
GRID = 20000
# ---- 单市场：竞争 / 垄断 ----
qc = (A - MC) / B
qm = (A - MC) / (2 * B)
pm = A - B * qm
profit_m = (pm - MC) * qm
cs_m = 0.5 * qm * (A - pm)
dwl = 0.5 * (pm - MC) * (qc - qm)
eps = -pm / (B * qm)
lerner = (pm - MC) / pm
# ---- 统一价格 vs 分别定价（两市场，MC 相同）----
def total_q(p):
    return sum(max(0.0, (a - p) / b) for a, b in (M1, M2))
best_p, best_pi = MC, 0.0
for i in range(GRID + 1):
    p = MC + (A - MC) * i / GRID
    pi = (p - MC) * total_q(p)
    if pi > best_pi:
        best_p, best_pi = p, pi
sep = []
for a, b in (M1, M2):
    q = (a - MC) / (2 * b)
    sep.append((q, a - b * q, (a - b * q - MC) * q))
sep_profit = sum(x[2] for x in sep)
# ---- 数值验证：打印可手算核对的量 ----
print("竞争 Q=%.4f p=%.4f" % (qc, MC))
print("垄断 Q=%.4f p=%.4f 利润=%.4f" % (qm, pm, profit_m))
print("垄断 CS=%.4f DWL=%.4f" % (cs_m, dwl))
print("需求弹性=%.4f 勒纳指数=%.4f 1/|eps|=%.4f" % (eps, lerner, 1 / abs(eps)))
print("统一价格 p=%.4f 利润=%.4f 总产量=%.4f" % (best_p, best_pi, total_q(best_p)))
for i, (q, p, pi) in enumerate(sep, 1):
    print("  市场%d 分别定价 q=%.4f p=%.4f 利润=%.4f" % (i, q, p, pi))
print("歧视总利润=%.4f 增量=%.4f" % (sep_profit, sep_profit - best_pi))

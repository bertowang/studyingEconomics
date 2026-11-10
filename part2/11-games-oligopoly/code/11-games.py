#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 11-games.py | 最优反应迭代与触发策略（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
A, B, C = 100.0, 1.0, 10.0
ITERS = 60
PD = {("C", "C"): (3, 3), ("C", "D"): (0, 5),
      ("D", "C"): (5, 0), ("D", "D"): (1, 1)}
# ---- 囚徒困境：逐个检查是否为纳什均衡 ----
acts = ["C", "D"]
nash = []
for s1 in acts:
    for s2 in acts:
        stable = all(PD[(s1, s2)][0] >= PD[(t, s2)][0] for t in acts) and \
                 all(PD[(s1, s2)][1] >= PD[(s1, t)][1] for t in acts)
        if stable:
            nash.append((s1, s2))
# ---- 古诺：最优反应迭代 ----
def br(qj):
    return max(0.0, (A - C - B * qj) / (2 * B))
q1 = q2 = 0.0
history = []
for _ in range(ITERS):
    n1, n2 = br(q2), br(q1)
    history.append((n1, n2))
    q1, q2 = n1, n2
q_star = (A - C) / (3 * B)
price = A - B * (q1 + q2)
pi_each = (price - C) * q1
# ---- 重复博弈：合作 / 背叛 / 惩罚收益 ----
q_coop = (A - C) / (2 * B) / 2          # 两家平分垄断产量
pi_c = (A - B * (2 * q_coop) - C) * q_coop
q_dev = br(q_coop)                       # 对方合作时的最优背叛
pi_d = (A - B * (q_dev + q_coop) - C) * q_dev
pi_n = pi_each
delta_min = (pi_d - pi_c) / (pi_d - pi_n)
# ---- 数值验证：打印可手算核对的量 ----
print("囚徒困境纳什均衡:", nash, " 支付=", PD[nash[0]])
print("古诺迭代第1轮=(%.4f, %.4f) 第2轮=(%.4f, %.4f)" %
      (history[0][0], history[0][1], history[1][0], history[1][1]))
print("迭代收敛 q=%.6f  解析解=%.6f  价格=%.4f  单家利润=%.4f" % (q1, q_star, price, pi_each))
print("垄断/古诺/竞争总产量=%.2f / %.2f / %.2f" %
      ((A - C) / (2 * B), 2 * q_star, (A - C) / B))
print("合作收益=%.4f 背叛收益=%.4f 惩罚收益=%.4f" % (pi_c, pi_d, pi_n))
print("触发策略可持续所需 delta >= %.4f" % delta_min)

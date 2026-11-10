#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 18-solow.py | 资本积累动力系统与条件收敛（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
A_PROD, ALPHA, DELTA = 1.0, 0.4, 0.05
SAVE = 0.2
K_POOR, K_RICH = 1.0, 8.0
PERIODS = 120
# ---- 模型 ----
def f(k):
    return A_PROD * (k ** ALPHA)

def step(k, s=SAVE):
    return (1 - DELTA) * k + s * f(k)

def steady(s):
    return (s * A_PROD / DELTA) ** (1 / (1 - ALPHA))

k_star = steady(SAVE)
k_gr = (ALPHA * A_PROD / DELTA) ** (1 / (1 - ALPHA))
s_gr = DELTA * (k_gr ** (1 - ALPHA)) / A_PROD
c_star = (1 - SAVE) * f(k_star)
c_gr = (1 - s_gr) * f(k_gr)
# ---- 条件收敛：穷国与富国从各自初始点出发 ----
kp, kr = K_POOR, K_RICH
for _ in range(PERIODS):
    kp, kr = step(kp), step(kr)
g_poor = (step(K_POOR) / K_POOR - 1)
g_rich = (step(K_RICH) / K_RICH - 1)
# ---- AK 模型 ----
g_ak = SAVE * A_PROD - DELTA
k_ak = 1.0
for _ in range(20):
    k_ak = (1 - DELTA) * k_ak + SAVE * A_PROD * k_ak
# ---- 数值验证：打印可手算核对的量 ----
print("稳态 k*=%.6f y*=%.6f c*=%.6f" % (k_star, f(k_star), c_star))
print("迭代 %d 期后 k=%.6f (应接近稳态)" % (PERIODS, kp))
print("初始增长率: 穷国(k=1)=%.4f 富国(k=8)=%.4f → 条件收敛" % (g_poor, g_rich))
print("黄金律 k_gr=%.4f s_gr=%.4f (=alpha %.2f) c_gr=%.4f" % (k_gr, s_gr, ALPHA, c_gr))
print("本例 s=%.2f < s_gr 时 c_gr=%.4f > c*=%.4f" % (SAVE, c_gr, c_star))
print("AK: 理论增长率=%.4f, 20 期实际平均=%.4f (无稳态)" %
      (g_ak, (k_ak ** (1 / 20) - 1)))

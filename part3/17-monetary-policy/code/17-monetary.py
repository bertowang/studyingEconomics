#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 17-monetary.py | 政策利率与通胀动态（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
R_STAR, PI_STAR = 2.0, 2.0
COEF_PI, COEF_Y = 0.5, 0.5       # 泰勒规则增益
RHO_IS, BETA_IS = 0.7, 0.4       # IS: 产出持续性与实际利率敏感度
KAPPA_PC, GAMMA_PC = 0.25, 0.15  # 菲利普斯曲线与预期锚定
PI_SHOCK = 5.0                   # 初始通胀（供给冲击后）
PERIODS = 10
# ---- 费雪方程与泰勒规则表 ----
def taylor(pi, y):
    return R_STAR + pi + COEF_PI * (pi - PI_STAR) + COEF_Y * y

grid = [(2.0, 0.0), (4.0, 0.0), (4.0, -2.0), (1.0, 1.0)]
# ---- 动态模拟 ----
pi, y = PI_SHOCK, 0.0
path = []
for t in range(1, PERIODS + 1):
    i = taylor(pi, y)
    y = RHO_IS * y - BETA_IS * (i - R_STAR - pi)
    pi = pi + KAPPA_PC * y - GAMMA_PC * (pi - PI_STAR)
    path.append((t, i, pi, y, i - pi))
# ---- 数值验证：打印可手算核对的量 ----
print("费雪: i=5%%, pi^e=2%% => 实际利率 r≈%.2f%%" % (5.0 - 2.0))
for p, g in grid:
    print("泰勒规则 pi=%.1f y=%.1f => i*=%.4f 实际利率=%.4f" %
          (p, g, taylor(p, g), taylor(p, g) - p))
print("通胀每高 1pp，名义利率升 %.2fpp，实际利率升 %.2fpp (泰勒原理)" %
      (1 + COEF_PI, COEF_PI))
for t, i, p, g, r in path[:6]:
    print("  t=%d i=%.3f pi=%.3f y_gap=%.3f r_real=%.3f" % (t, i, p, g, r))
print("第 %d 期通胀=%.4f (目标 %.2f)" % (PERIODS, path[-1][2], PI_STAR))

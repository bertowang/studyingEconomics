#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 19-open.py | 开放经济的核心恒等式（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
C_SPEND, I_SPEND, G_SPEND, Y_OUT = 700.0, 280.0, 300.0, 1300.0
KA_FLOW = -30.0
E_SPOT, P_HOME, P_FOREIGN = 7.0, 8.0, 1.2
I_HOME, I_FOREIGN = 0.05, 0.03
RISK_PREMIUM = 0.01
# ---- 国民账户与国际收支 ----
saving = Y_OUT - C_SPEND - G_SPEND
nx = Y_OUT - C_SPEND - I_SPEND - G_SPEND
ca = nx
reserve_change = -(ca + KA_FLOW)
# ---- 汇率与 PPP ----
real_ex = E_SPOT * P_FOREIGN / P_HOME
e_ppp = P_HOME / P_FOREIGN
misalign = (E_SPOT - e_ppp) / e_ppp
# ---- 利率平价 ----
expected_dep = I_HOME - I_FOREIGN
e_expected = E_SPOT * (1 + expected_dep)
forward = E_SPOT * (1 + I_HOME) / (1 + I_FOREIGN)
fixed_rate_i = I_FOREIGN + RISK_PREMIUM
# ---- 数值验证：打印可手算核对的量 ----
print("S=%.2f  I=%.2f  NX=S-I=%.2f  (支出法 NX=%.2f)" %
      (saving, I_SPEND, saving - I_SPEND, nx))
print("国际收支: CA=%.2f KA=%.2f ΔR=%.2f  合计=%.2f" %
      (ca, KA_FLOW, reserve_change, ca + KA_FLOW + reserve_change))
print("实际汇率 eps=%.4f  PPP 隐含 e=%.4f  名义偏离=%.2f%%" %
      (real_ex, e_ppp, 100 * misalign))
print("UIP 预期贬值=%.4f 预期即期 e=%.4f  CIP 远期 F=%.4f" %
      (expected_dep, e_expected, forward))
print("固定汇率+资本自由流动: 本国 i 必须≈%.4f (含风险溢价)，无法独立设为 %.2f" %
      (fixed_rate_i, I_HOME))

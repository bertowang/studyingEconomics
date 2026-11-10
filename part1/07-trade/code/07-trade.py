#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 07-trade.py | 李嘉图模型的贸易收益（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
L = 100.0
A_AF, A_AC = 2.0, 2.0      # A 国: 食品/布 单位工时
A_BF, A_BC = 1.0, 4.0      # B 国
WORLD_PF = 0.5             # 世界相对价格 p_F/p_C，p_C=1
SHARE = 0.5                # 收入中用于食品的份额（Cobb-Douglas）
# ---- 机会成本与比较优势 ----
oc_a = A_AF / A_AC
oc_b = A_BF / A_BC
# ---- 自给自足：收入一半买食品、一半买布 ----
fa = SHARE * L / A_AF
ca = SHARE * L / A_AC
fb = SHARE * L / A_BF
cb = SHARE * L / A_BC
# ---- 专业化 + 贸易 ----
# A 生产布，B 生产食品；世界价格必须落在两国机会成本之间
q_c_world = L / A_AC
q_f_world = L / A_BF
value_a = q_c_world * 1.0
value_b = q_f_world * WORLD_PF
f_a = SHARE * value_a / WORLD_PF
c_a = SHARE * value_a / 1.0
f_b = SHARE * value_b / WORLD_PF
c_b = SHARE * value_b / 1.0
# ---- 数值验证：打印可手算核对的量 ----
def u(f, c):
    return math.sqrt(f * c)
print("机会成本: A=%.4f  B=%.4f  世界价=%.4f 在区间内=%s" %
      (oc_a, oc_b, WORLD_PF, min(oc_a, oc_b) <= WORLD_PF <= max(oc_a, oc_b)))
print("自给自足 A=(%.2f, %.2f) u=%.4f ; B=(%.2f, %.2f) u=%.4f" %
      (fa, ca, u(fa, ca), fb, cb, u(fb, cb)))
print("贸易后   A=(%.2f, %.2f) u=%.4f ; B=(%.2f, %.2f) u=%.4f" %
      (f_a, c_a, u(f_a, c_a), f_b, c_b, u(f_b, c_b)))
print("市场出清: 食品需求=%.2f 供给=%.2f ; 布需求=%.2f 供给=%.2f" %
      (f_a + f_b, q_f_world, c_a + c_b, q_c_world))
print("A 出口布=%.2f 进口食品=%.2f" % (q_c_world - c_a, f_a))

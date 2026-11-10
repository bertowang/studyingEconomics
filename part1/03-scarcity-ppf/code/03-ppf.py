#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""03-ppf.py | 从劳动与技术参数计算 PPF 与边际转换率"""
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
L = 100.0              # 总劳动
A_F, A_C = 2.0, 4.0   # 单位产品耗用工时
POINTS = 5
# ---- 模型 1: 线性技术，机会成本为常数 ----
def linear_c(f):
    return (L - A_F * f) / A_C

# ---- 模型 2: 边际报酬递减 F=sqrt(L_f), C=sqrt(L-L_f) ----
def bowed_c(f):
    used = f * f
    return math.sqrt(max(0.0, L - used))

def mrt(f, h=1e-4):
    return (bowed_c(f) - bowed_c(f + h)) / h
# ---- 数值验证：打印可手算核对的量 ----
print("线性 PPF: F=0 时 C=%.2f；F=%.2f 时 C=0" % (linear_c(0.0), L / A_F))
print("线性机会成本 dC/dF = -a_F/a_C = %.4f (常数)" % (-A_F / A_C))
print("外凸 PPF: F=0 时 C=%.2f；F=%.2f 时 C=0" % (bowed_c(0.0), math.sqrt(L)))
for i in range(POINTS):
    f = 2.0 * i + 1.0
    print("  F=%4.1f  C=%7.4f  MRT=%8.4f" % (f, bowed_c(f), mrt(f)))
print("检验预算约束: 2*10+4*20 = %.1f (应等于 L)" % (A_F * 10 + A_C * 20))

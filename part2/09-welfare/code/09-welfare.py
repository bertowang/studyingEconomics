#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 09-welfare.py | 从反供需曲线积分计算福利（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
A, B, C, D = 100.0, 2.0, 10.0, 3.0    # Qd=A-B*p, Qs=C+D*p
CEILING = 14.0                         # 价格上限
# ---- 反需求 / 反供给及其原函数 ----
def pd(q):
    return (A - q) / B

def ps(q):
    return (q - C) / D

def int_pd(q):
    return (A * q - q * q / 2) / B

def int_ps(q):
    return (q * q / 2 - C * q) / D

def ts(q):
    return int_pd(q) - int_ps(q)

p0 = (A - C) / (B + D)
q0 = A - B * p0
cs0 = int_pd(q0) - p0 * q0
psi0 = p0 * q0 - int_ps(q0)
# ---- 价格上限：成交取短边 ----
qs = C + D * CEILING
qd = A - B * CEILING
qt = min(qd, qs)
cs_t = int_pd(qt) - CEILING * qt
ps_t = CEILING * qt - int_ps(qt)
dwl = ts(q0) - ts(qt)
# ---- 数值验证：打印可手算核对的量 ----
print("均衡 p*=%.4f Q*=%.4f" % (p0, q0))
print("均衡 CS=%.4f PS=%.4f TS=%.4f" % (cs0, psi0, ts(q0)))
print("上限 p=%.2f: Qs=%.2f Qd=%.2f 短缺=%.2f 成交=%.2f" % (CEILING, qs, qd, qd - qs, qt))
print("管制后 CS=%.4f PS=%.4f TS=%.4f" % (cs_t, ps_t, ts(qt)))
print("无谓损失=%.4f  三角公式=%.4f" %
      (dwl, 0.5 * (pd(qt) - ps(qt)) * (q0 - qt)))
print("检验: 上限处反供给=%.4f (应等于上限)" % ps(qs))

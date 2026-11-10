#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""04-supply-demand.py | 线性供需的均衡与税收归宿全量核算"""
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
A, B, C, D = 100.0, 2.0, 10.0, 3.0    # Qd=A-B*p, Qs=C+D*p
TAX = 6.0                              # 单位税
# ---- 模型：无税均衡 ----
p0 = (A - C) / (B + D)
q0 = A - B * p0
ed = -B * p0 / q0
es = D * p0 / q0
# ---- 比较静态：征税后 ----
ps = (A - C - B * TAX) / (B + D)
pc = ps + TAX
qt = A - B * pc
revenue = TAX * qt
dwl = 0.5 * TAX * (q0 - qt)
consumer_share = (pc - p0) / TAX
producer_share = (p0 - ps) / TAX
# ---- 数值验证：打印可手算核对的量 ----
print("无税: p*=%.4f Q*=%.4f 需求弹性=%.4f 供给弹性=%.4f" % (p0, q0, ed, es))
print("征税: 买方价=%.4f 卖方价=%.4f 楔子=%.4f Q=%.4f" % (pc, ps, pc - ps, qt))
print("消费者承担=%.4f 生产者承担=%.4f (理论 %.4f / %.4f)" %
      (consumer_share, producer_share, D / (B + D), B / (B + D)))
print("税收收入=%.4f 无谓损失=%.4f 总剩余损失=%.4f" % (revenue, dwl, revenue + dwl))
print("校验: 无税 Qs=%.4f, 征税 Qs=%.4f, 征税 Qd=%.4f" % (C + D * p0, C + D * ps, qt))

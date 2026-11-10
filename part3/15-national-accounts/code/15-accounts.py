#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 15-accounts.py | 国民账户与价格指数（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
P0, Q0 = (1.0, 2.0), (100.0, 50.0)      # 基期价格与数量（两种商品）
P1, Q1 = (1.2, 2.1), (130.0, 60.0)      # 当期
C_SPEND, I_SPEND, G_SPEND = 156.0, 60.0, 40.0
WAGE, PROFIT, DEPREC, TAX = 180.0, 60.0, 20.0, 22.0
# ---- 支出法 / 收入法 ----
nominal0 = sum(p * q for p, q in zip(P0, Q0))
nominal1 = sum(p * q for p, q in zip(P1, Q1))
real1 = sum(p * q for p, q in zip(P0, Q1))
nx = nominal1 - C_SPEND - I_SPEND - G_SPEND
income = WAGE + PROFIT + DEPREC + TAX
value_added = sum(p * q for p, q in zip(P1, Q1)) - 0.0   # 无中间投入
# ---- 价格指数 ----
deflator = nominal1 / real1
laspeyres = sum(p * q for p, q in zip(P1, Q0)) / nominal0
paasche = nominal1 / real1
fisher = math.sqrt(laspeyres * paasche)
real_growth = real1 / nominal0 - 1
nominal_growth = nominal1 / nominal0 - 1
# ---- 数值验证：打印可手算核对的量 ----
print("基期名义 GDP=%.2f 当期名义 GDP=%.2f" % (nominal0, nominal1))
print("支出法 C+I+G+NX=%.2f+%.2f+%.2f+%.2f=%.2f" %
      (C_SPEND, I_SPEND, G_SPEND, nx, C_SPEND + I_SPEND + G_SPEND + nx))
print("收入法 工资+利润+折旧+税=%.2f  生产法增加值=%.2f" % (income, value_added))
print("实际 GDP(基期价)=%.2f 实际增长=%.2f%% 名义增长=%.2f%%" %
      (real1, 100 * real_growth, 100 * nominal_growth))
print("平减指数=%.4f  CPI(拉氏)=%.4f  帕氏=%.4f  费雪=%.4f" %
      (deflator, laspeyres, paasche, fisher))
print("拉氏−帕氏=%.4f (本例为负：数量结构移向涨价更多的商品)" % (laspeyres - paasche))

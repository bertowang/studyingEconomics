#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 12-externality.py | 外部性内部化与公共品搭便车（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
A, B, C_PRIV, DAMAGE = 100.0, 2.0, 10.0, 12.0
TRANSACTION_COST = 2.0       # 科斯谈判的单位组织成本
N_PERSONS = 3                # 公共品人数
PG_INTERCEPT, PG_COST = 20.0, 12.0
# ---- 竞争均衡与社会最优 ----
q0 = (A - C_PRIV) / B
q_opt = (A - C_PRIV - DAMAGE) / B
ext_loss = DAMAGE ** 2 / (2 * B)
tax_revenue = DAMAGE * q_opt
q_taxed = (A - C_PRIV - DAMAGE) / B
# ---- 科斯：谈判净收益与交易成本 ----
gross_gain = DAMAGE * (q0 - q_opt) - 0.5 * B * (q0 - q_opt) ** 2
net_gain = gross_gain - TRANSACTION_COST * (q0 - q_opt)
# ---- 公共品：私人自愿 vs 萨缪尔森条件 ----
# 每人 MRS_i = 20 - G, 边际成本 = 12
g_private = PG_INTERCEPT - PG_COST                    # 20 - G = 12
g_social = (N_PERSONS * PG_INTERCEPT - PG_COST) / N_PERSONS / 1.0  # n*(20-G)=12
# ---- 数值验证：打印可手算核对的量 ----
print("私人 MC=%.2f 社会 MC=%.2f (含损害 %.2f)" % (C_PRIV, C_PRIV + DAMAGE, DAMAGE))
print("竞争 Q0=%.4f 社会最优 Q*=%.4f 超额=%.4f" % (q0, q_opt, q0 - q_opt))
print("外部性福利损失=%.4f (=e^2/2b)" % ext_loss)
print("庇古税 t=%.2f 后产量=%.4f (应=Q*) 税收=%.4f" % (DAMAGE, q_taxed, tax_revenue))
print("科斯谈判总增益=%.4f 扣交易成本后净增益=%.4f" % (gross_gain, net_gain))
print("公共品自愿总量=%.4f 社会最优总量=%.4f 缺口=%.4f" %
      (g_private, g_social, g_social - g_private))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""宏观篇 15-19：国民账户、短期波动、货币政策、增长与开放经济。"""
from book_schema import C, demo, eq, table

CH = [

C("15", "p3", "part3/15-national-accounts", "国民账户与价格指数：如何度量总量",
  "宏观的第一件事是把无数微观交易压成几个可加总、且相互钩稽的数字；三套核算恒等式是后面所有模型的坐标系。",
  hours="2 学时",
  goals=["能用支出法、收入法、生产法三种方式算出同一个 GDP",
         "会计算名义 GDP、实际 GDP、GDP 平减指数与 CPI 并说明差别",
         "理解替代偏差与链式加权，知道增长率该怎么读"],
  points=["GDP 与国民账户恒等式", "支出法/收入法/生产法", "名义与实际", "GDP 平减指数", "CPI 与拉氏指数", "帕氏指数与费雪指数", "替代偏差", "存量与流量"],
  bridge="承接 {{ch:14}} 的加总问题：一般均衡给出「所有市场同时出清」，国民账户给出「这些交易如何记账」。{{ch:16}} 在这个坐标系里研究短期波动。",
  analogy="三套核算方法是对同一份交易日志的三种 group-by：按买方、按收款方、按增加值分组，总和必须相等；名义与实际的区别是「按当期价格还是按固定基准价格聚合」。",
  sections=[
      ("15.1", "三套恒等式", """<p>GDP 是一国境内一定时期生产的最终产品市场价值。三种算法从不同角度切入：</p>"""
       + eq("支出法: Y = C + I + G + NX")
       + eq("收入法: Y = 工资 + 利息 + 租金 + 利润 + 折旧 + 间接税净额")
       + eq("生产法: Y = Σ 各部门增加值 = Σ(产值 − 中间投入)")
       + """<p>三者理论上恒等，因为<strong>每一笔支出都是另一方的收入</strong>；实际统计里出现的差额叫统计误差。由此可推出储蓄-投资恒等式：</p>"""
       + eq("S = Y − C − G = I + NX   ⇒   NX = S − I   ({{ch:19}} 开放经济的起点)")
       + """<p>恒等式不是行为方程：它永远成立，而「S 随利率上升」是需要另加假设的行为关系。混淆两者会让后面的模型推导全盘错位。</p>"""),
      ("15.2", "名义、实际与价格指数", """<p>名义 GDP 用当期价格，实际 GDP 用基期价格。两者之比是 <strong>GDP 平减指数</strong>（帕氏形式）：</p>"""
       + eq("平减指数 = Σp_t q_t / Σp_0 q_t  ;  实际增长率 ≈ 名义增长率 − 通胀率")
       + """<p>CPI 用<strong>固定基期篮子</strong>（拉氏形式）：<code>CPI = Σp_t q_0 / Σp_0 q_0</code>。篮子固定意味着消费者不会用变便宜的商品替代变贵的商品，因此 CPI 系统性<strong>高估</strong>生活成本涨幅（替代偏差）；此外还有新品引入偏差与质量变化偏差。</p>
<p>费雪理想指数取拉氏与帕氏的几何平均；链式加权则逐年更换基期再连乘，避免长期比较时基期过旧。这是各国统计机构的标准做法。</p>"""),
      ("15.3", "读宏观数据时的三个坑", """<table><thead><tr><th style="width:26%">坑</th><th>说明</th><th>正确做法</th></tr></thead><tbody>
<tr><td>存量与流量混用</td><td>债务是存量、赤字是流量；财富与收入不可直接比</td><td>先统一单位与时期</td></tr>
<tr><td>人均与总量</td><td>总量增长可能只来自人口增长</td><td>用人均实际 GDP 讨论生活水平</td></tr>
<tr><td>名义当实际</td><td>高通胀期名义工资上涨不等于购买力上涨</td><td>用 CPI 或平减指数折算</td></tr>
</tbody></table>
<p>本章扩展学习里给出 FRED、BEA、BLS、World Bank 等官方数据源。做实证前先把「单位、频率、季节调整、基期」四项写进数据字典，这一步省掉的调试时间最多。</p>"""),
  ],
  demos=[
      demo("code/15-accounts.py", "三种核算口径与四种价格指数", r"""#!/usr/bin/env python3
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
""",
            "把 <code>Q1</code> 改成 (100, 50)（产量不变），观察名义增长是否全部来自价格。",
            "基期 200、当期名义 282；三套口径都等于 282；实际 GDP 250、实际增长 25%、名义增长 41%；平减指数 1.128、CPI 1.125、费雪≈1.1265。本例数量结构向涨价更多的商品移动，因此拉氏指数反而略低；若消费者转向相对便宜的商品，才会出现教科书里 CPI 高于平减指数的替代偏差。",
            params="P1 改变量价拆分；Q1 的结构决定拉氏与帕氏谁更大；加入中间投入可验证生产法恒等式。"),
  ],
  highlights=[("gdp", "GDP 定义与边界案例"), ("national-accounts", "三套恒等式"),
              ("bea", "官方国民账户数据"), ("fred", "下载真实时间序列做对照")],
  pitfalls=["把恒等式当行为方程：<code>S=I+NX</code> 恒成立，不说明利率如何影响储蓄。",
            "把 CPI 当平减指数：篮子不同、覆盖范围不同（CPI 含进口、不含投资品）。",
            "把名义增长当实际增长：高通胀期两者可以差出一个数量级。"],
  exercises=["加入 30 单位中间投入，重新用生产法计算增加值并核对恒等式。",
             "构造一个「便宜商品被大量替代」的例子，使 CPI 明显高于平减指数。",
             "用 FRED 下载名义与实际 GDP，验证脚本里的近似式 <code>实际增长≈名义增长−通胀</code> 的误差量级。"],
  further=["{{ch:16}}　用 Y 的分解研究短期波动", "{{ch:17}}　通胀与价格水平", "{{ch:19}}　NX = S − I 的开放经济推论"]),

C("16", "p3", "part3/16-is-lm", "短期波动：乘数、IS-LM 与 AD-AS",
  "把 {{ch:14}} 的合成谬误具体化：人人同时多储蓄会压低总需求；乘数、挤出效应与总供给约束是宏观短期分析的三个齿轮。",
  hours="3 学时",
  goals=["能推导简单凯恩斯乘数并用迭代法验证收敛",
         "会联立 IS 与 LM 求出均衡产出与利率，量化挤出效应",
         "区分总需求冲击与总供给冲击，说明菲利普斯曲线的斜率来源"],
  points=["凯恩斯交叉与乘数", "边际消费倾向", "储蓄悖论", "IS 曲线", "LM 曲线与货币需求", "挤出效应", "AD-AS 与价格黏性", "菲利普斯曲线"],
  bridge="把 {{ch:15}} 的核算恒等式升级为行为方程；{{ch:17}} 把 LM 一侧替换成央行的政策规则，{{ch:18}} 把视野从短期拉到长期增长。",
  analogy="乘数是带反馈的迭代：<code>Y ← c·Y + A</code> 收敛到 <code>A/(1−c)</code>，收敛速度由谱半径 c 决定；IS-LM 是两条约束的联立求解，挤出效应来自利率这条额外反馈通道。",
  sections=[
      ("16.1", "乘数：一个一阶线性反馈", """<p>简单凯恩斯模型：消费 <code>C = c₀ + c(Y−T)</code>，计划支出 <code>E = C + I + G + NX</code>，均衡 <code>Y = E</code>：</p>"""
       + eq("Y = [c₀ − cT + I + G + NX] / (1−c)  ;  支出乘数 = 1/(1−c)")
       + """<p><code>c=0.8</code> 时乘数为 5。数值上它就是迭代 <code>Y_{t+1}=cY_t+A</code> 的不动点，收敛速度由 <code>|c|</code> 决定。<strong>储蓄悖论</strong>：每家想多存钱（c 下降）使总需求与总收入下降，最终总储蓄未必增加——{{ch:14}} 合成谬误的最经典案例。</p>
<p>政府税收乘数是 <code>−c/(1−c)</code>，平衡预算乘数为 1（政府支出与税收等额增加时）。这些结论都依赖「有闲置产能、价格不立刻调整」的短期假设。</p>"""),
      ("16.2", "IS-LM：加入利率与货币市场", """<p>让投资对利率敏感 <code>I = I₀ − d·r</code>，货币需求 <code>L = kY − h·r = M/P</code>。两式联立：</p>"""
       + eq("IS: Y(1−c) = A − d·r   ;   LM: r = (kY − M/P)/h")
       + eq("Y* = [A + d(M/P)/h] / [(1−c) + dk/h]")
       + """<p>分母多出 <code>dk/h</code>，使政府支出乘数从 <code>1/(1−c)</code> 降到 <code>1/[(1−c)+dk/h]</code>：财政扩张推高利率，私人投资被<strong>挤出</strong>。流动性陷阱（h 很大）或投资利率不敏感（d 很小）时挤出很弱，乘数接近简单模型。</p>"""),
      ("16.3", "AD-AS 与菲利普斯曲线", """<table><thead><tr><th style="width:22%">框架</th><th>价格假设</th><th>主要结论</th></tr></thead><tbody>
<tr><td>凯恩斯交叉 / IS-LM</td><td>价格水平固定</td><td>产出由总需求决定</td></tr>
<tr><td>AD-AS 短期</td><td>价格/工资黏性</td><td>需求冲击同时影响产出与价格</td></tr>
<tr><td>AD-AS 长期</td><td>价格完全灵活</td><td>产出回到潜在水平，需求只影响价格</td></tr>
</tbody></table>
<p>短期总供给曲线向上倾斜，对应<strong>菲利普斯曲线</strong> <code>π = πᵉ + κ·产出缺口 + 供给冲击</code>：需求过热推高通胀；但 <code>πᵉ</code> 会随经验调整，因此不存在可长期利用的「通胀换就业」稳定替代关系。{{ch:17}} 的泰勒规则正是把这条关系写进政策反应函数。</p>"""),
  ],
  demos=[
      demo("code/16-multiplier.py", "乘数迭代、IS-LM 联立与挤出效应", r"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 16-multiplier.py | 凯恩斯乘数与 IS-LM（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
C_MPC, AUTONOMOUS = 0.8, 100.0
D_INV, K_MONEY, H_MONEY = 20.0, 0.5, 20.0
M_OVER_P = 200.0
DG = 10.0
ITERS = 40
# ---- 简单乘数：迭代求不动点 ----
y = 0.0
for _ in range(ITERS):
    y = C_MPC * y + AUTONOMOUS
y_simple = AUTONOMOUS / (1 - C_MPC)
tax_mult = -C_MPC / (1 - C_MPC)
# ---- IS-LM 联立 ----
def solve_y(a):
    return (a + D_INV * (M_OVER_P / H_MONEY)) / ((1 - C_MPC) + D_INV * K_MONEY / H_MONEY)

def solve_r(y):
    return (K_MONEY * y - M_OVER_P) / H_MONEY
y0, r0 = solve_y(AUTONOMOUS), None
r0 = solve_r(y0)
y1 = solve_y(AUTONOMOUS + DG)
r1 = solve_r(y1)
mult_islm = (y1 - y0) / DG
# ---- 数值验证：打印可手算核对的量 ----
print("迭代 Y=%.4f 解析 Y=%.4f 乘数=%.4f 税收乘数=%.4f" %
      (y, y_simple, 1 / (1 - C_MPC), tax_mult))
print("IS-LM 初始 Y=%.4f r=%.4f" % (y0, r0))
print("G 增加 %.2f 后 Y=%.4f r=%.4f" % (DG, y1, r1))
print("IS-LM 支出乘数=%.4f (简单乘数 %.4f，挤出 %.4f)" %
      (mult_islm, 1 / (1 - C_MPC), 1 / (1 - C_MPC) - mult_islm))
print("储蓄悖论: c 从 0.8 降到 0.6 时均衡 Y 由 %.2f 降到 %.2f" %
      (AUTONOMOUS / (1 - 0.8), AUTONOMOUS / (1 - 0.6)))
""",
            "把 <code>D_INV</code> 改成 0（投资对利率不敏感），观察 IS-LM 乘数是否回到 5。",
            "迭代收敛到 Y≈500（解析 500），乘数 5、税收乘数 −4；IS-LM 初始 Y≈428.57、r≈0.71；G 增加 10 后 Y≈442.86、r≈1.07，乘数≈1.43；c 降到 0.6 时 Y 从 500 降到 250。",
            params="D_INV 或 H_MONEY 上升使挤出减弱；C_MPC 上升提高乘数；M_OVER_P 上升通过 LM 右移提高产出。"),
  ],
  highlights=[("multiplier", "乘数的推导与前提"), ("is-lm", "产品与货币市场同时均衡"),
              ("ad-as", "总需求总供给框架"), ("fred", "用真实 GDP 与利率做对照")],
  pitfalls=["把恒等式 S=I 当成「储蓄增加会带来投资增加」的因果链：短期由收入调整实现相等。",
            "忽略价格黏性前提：长期价格灵活时需求冲击只影响价格水平。",
            "把菲利普斯曲线当作稳定的政策菜单：预期调整会使替代关系消失。"],
  exercises=["把 <code>H_MONEY</code> 设为 1e6 模拟流动性陷阱，观察乘数是否回到简单模型。",
             "推导平衡预算乘数并用脚本数值验证等于 1。",
             "用 {{ch:18}} 的语言说明：短期波动模型与长期增长模型分别固定了什么、放松了什么。"],
  further=["{{ch:15}}　总量核算恒等式", "{{ch:17}}　泰勒规则与通胀动态", "{{ch:18}}　长期增长与稳态"]),

C("17", "p3", "part3/17-monetary-policy", "货币政策、通胀与利率：费雪方程与泰勒规则",
  "名义利率、实际利率与预期通胀由费雪方程相连；央行用一个可写的反应函数把通胀与产出缺口反馈到政策利率。",
  hours="3 学时",
  goals=["会用费雪方程区分名义与实际利率",
         "能写出泰勒规则并计算给定通胀/产出缺口下的政策利率",
         "会跑一个小型动态模拟，解释加息如何经产出缺口传导到通胀"],
  points=["费雪方程", "实际利率与名义利率", "央行目标与工具", "泰勒规则", "泰勒原理", "通胀预期", "菲利普斯曲线", "传导机制与滞后"],
  bridge="把 {{ch:16}} 的 LM 曲线替换成内生政策规则，把 {{ch:08}} 的贴现率与 {{ch:29}} 的债券利率统一到同一个 r。",
  analogy="央行是一个反馈控制器：输入是通胀缺口与产出缺口，输出是政策利率；泰勒原理要求控制器对通胀的增益大于 1，否则闭环不稳定。",
  sections=[
      ("17.1", "费雪方程：三个利率一个关系", """<p>投资者关心的是购买力，因此名义利率要补偿预期通胀：</p>"""
       + eq("i ≈ r + πᵉ   ;   r ≈ i − πᵉ   ;   精确式 1+i = (1+r)(1+πᵉ)")
       + """<p><code>r</code> 是 {{ch:08}} 欧拉方程里决定跨期消费的实际利率，也是 {{ch:29}} 债券定价与 {{ch:27}} 组合选择的贴现基准。<strong>名义利率低不等于货币宽松</strong>：若通胀预期更低，实际利率可能很高。这是读历史数据时最容易踩的坑。</p>
<p>长期中货币中性（货币量变化主要影响价格水平），但短期因价格黏性，实际利率变化会影响产出——这正是 {{ch:16}} AD-AS 的传导通道。</p>"""),
      ("17.2", "泰勒规则与泰勒原理", """<p>标准泰勒规则：</p>"""
       + eq("i* = r* + π + 0.5(π − π*) + 0.5·y_gap")
       + """<p>通胀高于目标 1 个百分点，名义利率应上升 1.5 个百分点，于是<strong>实际利率上升 0.5 个百分点</strong>，需求降温。这个「名义利率对通胀的响应大于 1」称为<strong>泰勒原理</strong>：若响应小于 1，通胀上升反而压低实际利率，形成自我强化的不稳定闭环。程序员的读法：闭环增益必须落在稳定区间。</p>"""),
      ("17.3", "一次供给冲击的动态路径", """<p>把 IS 曲线 <code>y_t = ρy_{t−1} − β(i_t − r* − π_t)</code>、菲利普斯曲线 <code>π_t = π_{t−1} + κy_t − γ(π_{t−1} − π*)</code> 与泰勒规则联立，就能迭代出「油价冲击 → 加息 → 负产出缺口 → 通胀回落」的路径。注意<strong>滞后</strong>：本期利率影响下一期产出，再影响后续通胀，因此政策存在「打得过猛/过晚」的风险。</p>
<div class="card warn"><p style="margin-bottom:0">这类小型模型用于<strong>讲清机制</strong>，不是预测工具：参数是校准出来的、预期是适应性的、没有微观基础。真实政策分析用 DSGE 或 VAR，见 {{ch:25}} 时间序列；用历史数据拟合后做反事实还要面对 {{ch:20}} 的卢卡斯批判。</p></div>"""),
  ],
  demos=[
      demo("code/17-monetary.py", "费雪方程、泰勒规则与冲击传导模拟", r"""#!/usr/bin/env python3
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
""",
            "把 <code>COEF_PI</code> 改成 0（违反泰勒原理），观察通胀路径是否不再回落。",
            "费雪 i=5%、πᵉ=2% ⇒ r≈3%；π=4、缺口 0 时 i*=7、实际利率 3；通胀每高 1pp 名义升 1.5pp、实际升 0.5pp；供给冲击后通胀从 5 逐步向 2 回落并伴随负产出缺口。",
            params="COEF_PI&lt;0 或过小会破坏稳定性；BETA_IS 越大加息对产出的压制越强；GAMMA_PC 越大通胀预期锚定越强。"),
  ],
  highlights=[("taylor-rule", "规则与泰勒原理"), ("fisher", "费雪方程"),
              ("monetary-policy", "政策工具与传导机制"), ("fed", "官方政策声明与利率数据")],
  pitfalls=["用名义利率判断松紧：必须减去预期通胀得到实际利率。",
            "把央行反应函数当结构不变：政策规则本身会变，历史拟合不能直接做反事实。",
            "忽略传导滞后：本期加息主要影响后续若干期的产出与通胀。"],
  exercises=["把 <code>COEF_PI</code> 从 0 扫到 1.5，画出 10 期后通胀，找出稳定边界。",
             "加入零利率下限 <code>i≥0</code>，说明通缩冲击下政策为何失效。",
             "用 {{ch:29}} 的久期公式说明政策利率上升 1pp 对债券价格的影响。"],
  further=["{{ch:08}}　实际利率与跨期选择", "{{ch:16}}　IS-LM 中的货币市场", "{{ch:29}}　利率与债券定价"]),

C("18", "p3", "part3/18-growth", "长期增长：索洛稳态、条件收敛与内生增长",
  "把视野从需求侧波动移到供给侧能力：资本积累受边际报酬递减约束，长期人均增长只能来自技术进步。",
  hours="3 学时",
  goals=["会推导并数值求解索洛稳态 k*，验证资本边际报酬递减导致的收敛",
         "理解黄金律储蓄率与「储蓄率不决定长期增长率」",
         "比较索洛外生增长与 AK 内生增长模型的可检验含义"],
  points=["总量生产函数", "资本积累方程", "稳态与不动点", "条件收敛", "储蓄率与黄金律", "技术进步与外生增长", "AK 内生增长", "跨国增长实证"],
  bridge="把 {{ch:06}} 的微观生产函数加总并加上资本积累动态；{{ch:16}} 讨论短期为何偏离潜在产出，本章决定潜在产出本身的路径。",
  analogy="稳态是迭代 <code>k ← (1−δ)k + s·f(k)</code> 的不动点；收敛速度由 <code>f'(k*)</code> 决定，与 {{ch:16}} 乘数迭代的谱半径是同一个概念。",
  sections=[
      ("18.1", "索洛模型：一个一维动力系统", """<p>人均生产函数 <code>y = A·k^α</code>（<code>0&lt;α&lt;1</code>，来自 {{ch:06}} 的规模报酬不变技术），资本积累：</p>"""
       + eq("k_{t+1} = (1−δ)k_t + s·A·k_t^α   ;   稳态 s·A·k*^α = δ·k*")
       + eq("k* = (sA/δ)^{1/(1−α)} ,  y* = (sA/δ)^{α/(1−α)}")
       + """<p>因为 <code>α&lt;1</code>，<code>k^α</code> 的增长慢于 <code>k</code>，投资终将被折旧追上。<strong>储蓄率 s 提高只能把经济抬到更高的稳态水平，不能维持长期增长率</strong>；人均长期增长必须靠 A 的持续提高（外生的技术进步）。</p>"""),
      ("18.2", "条件收敛与黄金律", """<p>离自身稳态越远，增长速度越快，这解释了<strong>条件收敛</strong>：在储蓄率、人口增长、制度与技术相近的国家之间，穷国增长更快；无条件对比所有国家则不成立。跨国实证常用 {{ch:21}} 的回归检验「初始人均 GDP 的系数显著为负，且控制住 s、n、人力资本」。</p>
<p>稳态消费 <code>c* = (1−s)f(k*)</code> 关于 s 先升后降。令 <code>dc*/ds=0</code> 得<strong>黄金律</strong> <code>f'(k_gr)=δ</code>，Cobb-Douglas 下 <code>s_gr=α</code>：把过多产出用于积累反而降低长期消费（动态无效率）。</p>"""),
      ("18.3", "内生增长：把 A 变成变量", """<p>AK 模型令 <code>y = A·k</code>（资本边际报酬不递减，把人力资本、知识溢出都算进广义资本）：</p>"""
       + eq("Δk/k = sA − δ = g   ⇒   增长率由 s 与 A 永久决定，无稳态")
       + """<p>两模型给出完全不同的可检验含义：索洛预测储蓄率变化只带来水平效应、且存在条件收敛；AK 预测增长效应持续、贫富差距不自动缩小。研发驱动的增长模型（Romer）、创造性破坏（Aghion–Howitt）与人力资本模型则进一步解释 A 从何而来，把 {{ch:10}} 的垄断租金与 {{ch:12}} 的知识外部性接进增长框架。</p>"""),
  ],
  demos=[
      demo("code/18-solow.py", "索洛稳态、收敛速度与黄金律", r"""#!/usr/bin/env python3
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
""",
            "把 <code>SAVE</code> 从 0.1 扫到 0.6，画出稳态消费曲线并验证最大值在 s=α=0.4。",
            "s=0.2 时 k*≈10.079、y*≈2.520、c*≈2.016；穷国(k=1)初始增长率 15%、富国(k=8)约 0.74%；120 期后 k≈9.75（因 α=0.4 收敛较慢）；黄金律 s=0.4、k=32、c≈2.4；AK 模型增长率恒为 0.15。",
            params="SAVE 上升提高稳态水平但不改变长期增长率；ALPHA 越大收敛越慢；DELTA 上升压低稳态资本。"),
  ],
  highlights=[("solow", "索洛模型标准推导"), ("convergence", "条件收敛与跨国实证"),
              ("worldbank", "跨国人均 GDP 与储蓄率数据"), ("owid", "长周期增长数据")],
  pitfalls=["把「储蓄率提高」说成「长期增长率提高」：索洛里只有水平效应和过渡期增长。",
            "把条件收敛说成「穷国一定追上富国」：前提是稳态决定因素相近。",
            "忽略人口增长与折旧：稳态条件是 s·f(k) = (n+δ)k，本例为简化设 n=0。"],
  exercises=["在脚本里加入人口增长率 n=0.02，重新推导并核对稳态 k*。",
             "把 <code>SAVE</code> 从 0.1 扫到 0.6 打印 c*，验证峰值在 α=0.4 附近。",
             "用 {{ch:21}} 的 OLS 思路设计一个条件收敛回归：被解释变量、核心解释变量与控制变量各是什么。"],
  further=["{{ch:06}}　生产函数与规模报酬", "{{ch:16}}　短期波动与潜在产出", "{{ch:21}}　增长回归的估计"]),

C("19", "p3", "part3/19-open-economy", "开放经济：国际收支、汇率与三元悖论",
  "把 {{ch:15}} 的 NX = S − I 展开到跨境：经常账户、资本账户与官方储备必须钩稽；汇率把两国价格与利率连起来。",
  hours="3 学时",
  goals=["会用国际收支恒等式核算经常账户、资本账户与储备变动",
         "能计算名义/实际汇率、PPP 隐含汇率与高估/低估幅度",
         "说明利率平价与三元悖论，并解释固定汇率下货币政策为何不独立"],
  points=["国际收支恒等式", "NX = S − I", "名义与实际汇率", "购买力平价", "利率平价与远期汇率", "三元悖论", "资本流动与风险溢价", "汇率制度"],
  bridge="把 {{ch:07}} 的实物贸易加上货币与资产维度；{{ch:17}} 的利率、{{ch:30}} 的远期/期权定价都在这里第一次跨出国界。",
  analogy="国际收支是一张复式记账表：每笔跨境交易都有借贷两侧，总和恒为零；汇率与利率是两张表之间的换算率，三元悖论说明三个约束不能同时满足（类似分布式系统里的一致性/可用性/分区容忍取舍）。",
  sections=[
      ("19.1", "国际收支：一张必须配平的表", """<p>国民收入恒等式给出</p>"""
       + eq("NX = S − I  ;  CA ≈ NX + 净要素收入 + 经常转移")
       + eq("CA + KA + ΔR ≡ 0   (经常账户 + 资本与金融账户 + 官方储备变动)")
       + """<p>含义：经常账户顺差必然对应资本净流出（或储备增加）。把顺差说成「赚了钱」而不说明对应资产变化，是漏掉半张表。浮动汇率下 ΔR≈0，汇率调整使 CA+KA≈0；固定汇率下央行必须被动买卖外汇，储备随之变动。</p>"""),
      ("19.2", "汇率、PPP 与实际汇率", """<p>定义 <code>e</code> 为本币/外币（数值上升=本币贬值），<code>P</code> 为本国价格水平、<code>P*</code> 为外国价格水平：</p>"""
       + eq("实际汇率 ε = e·P*/P ;  PPP 隐含名义汇率 e_PPP = P/P* ;  ε=1 时购买力平价成立")
       + """<p><code>ε>1</code> 表示本国商品相对便宜（实际贬值），有利于净出口。PPP 是长期锚而非短期定价公式：可贸易品套利、运输成本、非贸易品（服务、房租）与生产率差异（巴拉萨–萨缪尔森效应）都会造成系统性偏离。</p>"""),
      ("19.3", "利率平价与三元悖论", """<p>无抛补利率平价（UIP）与抛补利率平价（CIP）：</p>"""
       + eq("UIP: i ≈ i* + E[Δe]/e  ;  CIP: F = S·(1+i)/(1+i*)")
       + """<p>若资本自由流动且汇率固定（预期贬值≈0），则必须有 <code>i=i*</code>：本国央行无法独立设定利率。<strong>三元悖论</strong>说，汇率稳定、资本自由流动、货币政策独立三者只能取二。小国选固定汇率往往要接受他国货币政策；要独立政策则需浮动汇率或资本管制。</p>
<div class="card tip"><p style="margin-bottom:0"><strong>接口</strong>：CIP 是 {{ch:30}} 无套利定价的直接前身——远期价格不是预测，而是由即期价格与两国利率「算」出来的；风险溢价、交易成本与危机时的信用利差会让 CIP 出现偏离。</p></div>"""),
  ],
  demos=[
      demo("code/19-open.py", "国际收支、PPP、利率平价与三元悖论", r"""#!/usr/bin/env python3
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
""",
            "把 <code>E_SPOT</code> 改成 6.0，观察实际汇率与 PPP 偏离的符号；把 <code>I_FOREIGN</code> 改成 0.05 看利差与远期如何变化。",
            "S=300、I=280、NX=20；CA=20、KA=−30、ΔR=10，合计为 0；ε=1.05、PPP 隐含 e≈6.6667，即期汇率比 PPP 隐含值高 5%（本币实际低估）；UIP 预期贬值 2%、预期 e=7.14、CIP 远期≈7.1359；固定汇率下 i≈4%。",
            params="E_SPOT 上升（本币贬值）抬高 ε；两国利差决定远期升贴水；RISK_PREMIUM 上升使固定汇率下本国利率更高。"),
  ],
  highlights=[("bop", "国际收支账户结构"), ("ppp", "购买力平价与偏离"),
              ("trilemma", "三元悖论"), ("imf", "跨国宏观与国际收支数据")],
  pitfalls=["把 CA 顺差当成「净赚的钱」而不看对应的资本流出与储备变化。",
            "把 PPP 当短期汇率预测：它是长期锚，短期由利率、预期与风险偏好主导。",
            "把远期汇率当市场对未来即期的预测：CIP 下它由利差机械决定。"],
  exercises=["推导加入净要素收入后 CA 与 NX 的差额，并说明为什么两者常被混用。",
             "在脚本里加入 1% 的交易成本，计算无套利区间（联系 {{ch:30}} 的买卖价差）。",
             "用三元悖论解释 {{ch:17}} 中「央行加息」在固定汇率与浮动汇率下的不同效果。"],
  further=["{{ch:15}}　NX = S − I 的来源", "{{ch:17}}　政策利率与利差", "{{ch:30}}　远期与无套利定价"]),
]

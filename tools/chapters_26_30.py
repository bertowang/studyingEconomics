#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""投资篇 26-30：收益、组合、因子、债券与期权定价。"""
from book_schema import C, demo, eq, table

CH = [

C("26", "p5", "part5/26-returns", "收益、复利与波动：把价格变成可建模的序列",
  "资产价格是 {{ch:25}} 的随机游走，收益才近似平稳；对数收益可跨期相加，是建模与计量的标准输入。",
  hours="2 学时",
  goals=["会计算简单收益、对数收益、年化收益与年化波动",
         "解释算术平均与几何平均的差别（波动拖累）",
         "能用固定种子模拟几何布朗运动并核对复利恒等式"],
  points=["简单收益与对数收益", "复利与年化", "算术平均与几何平均", "波动拖累", "几何布朗运动", "对数正态分布", "最大回撤", "收益的平稳性"],
  bridge="把 {{ch:02}} 的分布、{{ch:08}} 的贴现与 {{ch:25}} 的随机游走合流；{{ch:27}}～{{ch:30}} 都把收益序列当作输入。",
  analogy="价格像累加器（积分），收益像增量（差分）；对数收益把乘法累积变成加法累积，等价于把乘性过程取对数变成加性过程，便于做统计。",
  sections=[
      ("26.1", "三种收益与两个恒等式", """<p>简单收益 <code>R_t = P_t/P_{t−1} − 1</code>，对数收益 <code>r_t = ln(P_t/P_{t−1}) = ln(1+R_t)</code>。多期总收益：</p>"""
       + eq("1 + R_total = Π(1+R_t) ;  r_total = Σ r_t = ln(1+R_total)")
       + """<p>简单收益可跨资产加总（组合收益是加权平均），对数收益可跨时间加总。<strong>两者不能混用</strong>：把对数收益当权重算组合收益是常见 bug。年化时 <code>μ_ann = 12·μ_month</code>、<code>σ_ann = √12·σ_month</code>（方差可加、标准差不可加）。</p>"""),
      ("26.2", "波动拖累", """<p>对数效用或连续复利下，长期增长率是<strong>几何平均</strong>而非算术平均：</p>"""
       + eq("g = E[r] − ½σ²   （GBM 下精确成立，一般情形下为二阶近似）")
       + """<p>因此「平均收益 10%、波动 30%」的资产长期增长率不是 10%，而约 5.5%。{{ch:08}} 的确定性等价、{{ch:27}} 的均值-方差目标函数都在这里得到同一个结论：<strong>波动本身要付出复利代价</strong>。</p>"""),
      ("26.3", "几何布朗运动与路径模拟", """<p>标准价格模型 <code>dS = μS dt + σS dW</code> 的离散解：</p>"""
       + eq("S_{t+Δt} = S_t·exp[(μ − ½σ²)Δt + σ√Δt·Z] ,  Z~N(0,1)")
       + """<p><code>S_T</code> 服从对数正态分布，价格水平是 I(1) 而收益近似 I(0)——这正是 {{ch:25}} 的结论。脚本会验证「终点价格 = 初始价 × exp(对数收益之和)」，并用蒙特卡洛均值与解析漂移对照。真实市场还有厚尾、波动聚集与跳跃，GBM 是<strong>基准模型而非事实</strong>。</p>"""),
  ],
  demos=[
      demo("code/26-returns.py", "复利、波动拖累与 GBM 路径模拟", r"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 26-returns.py | 收益定义与几何布朗运动（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
S0, MU, SIGMA = 100.0, 0.08, 0.20
DT, STEPS = 1.0 / 12, 240       # 20 年月度
N_PATHS = 4000
# ---- 单条路径 ----
rng = random.Random(7)
prices, logrets, simple = [S0], [], []
s = S0
for _ in range(STEPS):
    z = rng.gauss(0, 1)
    r = (MU - 0.5 * SIGMA ** 2) * DT + SIGMA * math.sqrt(DT) * z
    s *= math.exp(r)
    prices.append(s)
    logrets.append(r)
    simple.append(math.exp(r) - 1)
mean_r = statistics.fmean(logrets)
mean_simple = statistics.fmean(simple)
vol_month = statistics.pstdev(logrets)
total_log = sum(logrets)
# ---- 蒙特卡洛：终点价格期望 E[S_T] = S0*exp(mu*T) ----
mc = random.Random(19)
terminals = []
for _ in range(N_PATHS):
    st = S0 * math.exp((MU - 0.5 * SIGMA ** 2) * (STEPS * DT) +
                       SIGMA * math.sqrt(STEPS * DT) * mc.gauss(0, 1))
    terminals.append(st)
# ---- 最大回撤 ----
peak, mdd = prices[0], 0.0
for p in prices:
    peak = max(peak, p)
    mdd = max(mdd, (peak - p) / peak)
# ---- 数值验证：打印可手算核对的量 ----
print("终点价格=%.4f  S0*exp(sum r)=%.4f (恒等式)" %
      (prices[-1], S0 * math.exp(total_log)))
print("月对数收益均值=%.6f 简单收益均值=%.6f 差≈sigma²*dt/2=%.6f" %
      (mean_r, mean_simple, 0.5 * SIGMA ** 2 * DT))
print("年化对数收益=%.4f%% 年化波动=%.4f%% (目标 %.2f%%)" %
      (100 * mean_r / DT, 100 * vol_month / math.sqrt(DT), 100 * SIGMA))
print("长期增长率 E[r]-0.5sigma²=%.4f%% (算术漂移 %.2f%%)" %
      (100 * (MU - 0.5 * SIGMA ** 2), 100 * MU))
print("蒙特卡洛 E[S_T]=%.4f 解析=%.4f" %
      (statistics.fmean(terminals), S0 * math.exp(MU * STEPS * DT)))
print("单路径最大回撤=%.2f%%" % (100 * mdd))
""",
            "把 <code>SIGMA</code> 改成 0.4，观察长期增长率下降与最大回撤上升；把 <code>STEPS</code> 改成 12 看年化估计的噪声。",
            "终点价格与 S0·exp(Σr) 完全一致；简单收益均值比对数收益均值高约 σ²Δt/2；年化波动≈20%；长期增长率≈6% 而算术漂移 8%；蒙特卡洛 E[S_T] 接近 S0·e^(μT)。",
            params="SIGMA 上升同时压低长期增长率、放大回撤；N_PATHS 控制蒙特卡洛误差；DT 改变年化换算系数。"),
  ],
  highlights=[("rate-of-return", "收益定义与年化"), ("lognormal", "对数正态分布"),
              ("compound-interest", "复利与长期增长"), ("fred", "用真实指数序列核对")],
  pitfalls=["把对数收益当简单收益做组合加权：跨时间可加与跨资产可加是两种不同性质。",
            "把算术平均当长期增长率：忽略波动拖累会系统性高估终值。",
            "把 GBM 当真实市场：厚尾、波动聚集与跳跃都不在模型里。"],
  exercises=["推导 <code>Var(R_total)</code> 与期数的关系，说明为什么年化波动用 √12。",
             "在脚本里把收益改成 t 分布（用 <code>random.gauss</code> 混合方差），观察回撤分布的变化。",
             "用 {{ch:25}} 的 ADF 思路检验价格与收益的平稳性差异。"],
  further=["{{ch:08}}　贴现与确定性等价", "{{ch:27}}　组合方差与分散化", "{{ch:30}}　GBM 与期权定价"]),

C("27", "p5", "part5/27-portfolio", "均值-方差组合：分散化与有效前沿",
  "把 {{ch:01}} 的约束最优化用于资产权重：给定风险求最高期望收益，或给定收益求最低方差。",
  hours="3 学时",
  goals=["能计算两资产组合的期望收益与方差，并求最小方差权重",
         "会用网格搜索求含无风险资产时的最大夏普组合",
         "解释分散化为何在相关系数小于 1 时有效、以及系统性风险不可分散"],
  points=["组合收益与方差", "相关系数与分散化", "最小方差组合", "有效前沿", "夏普比率", "切点组合与两基金分离", "系统性风险", "均值-方差与期望效用"],
  bridge="把 {{ch:01}} 的 FOC、{{ch:08}} 的凹效用与 {{ch:26}} 的收益分布接成第一个定价决策模型；{{ch:28}} 追问「风险为何应该被补偿」。",
  analogy="组合优化是一个二次型目标函数加线性约束：方差矩阵是协方差，权重是决策变量；低相关资产相当于「 diversify 依赖」，降低共同失效的概率。",
  sections=[
      ("27.1", "组合方差：协方差才是关键", """<p>两资产权重 <code>w</code> 与 <code>1−w</code>：</p>"""
       + eq("μ_p = wμ₁+(1−w)μ₂ ;  σ_p² = w²σ₁²+(1−w)²σ₂²+2w(1−w)ρσ₁σ₂")
       + """<p>令导数为零得最小方差权重 <code>w* = (σ₂²−ρσ₁σ₂)/(σ₁²+σ₂²−2ρσ₁σ₂)</code>。只要 <code>ρ&lt;1</code>，最小方差组合的风险就低于两种资产各自的风险；<code>ρ=−1</code> 时理论上可构造零方差组合。分散化收益来自<strong>协方差项</strong>，不是「资产数量多」。</p>"""),
      ("27.2", "有效前沿与切点组合", """<p>把 <code>(σ_p, μ_p)</code> 对所有权重连成曲线，其上「给定风险收益最高」的半支是<strong>有效前沿</strong>。加入无风险利率 <code>r_f</code> 后，最大化夏普比率：</p>"""
       + eq("Sharpe = (μ_p − r_f)/σ_p  ;  最优解 = 从 r_f 出发与前沿相切的切点组合")
       + """<p><strong>两基金分离定理</strong>：所有投资者的风险资产部分都持有同一个切点组合，差别只在「无风险资产 + 切点组合」的配比，由风险偏好决定。这是 {{ch:08}} 期望效用与 {{ch:05}} 对偶结构在金融里的对应：偏好只影响一个标量。</p>"""),
      ("27.3", "模型边界", """<table><thead><tr><th style="width:28%">假设</th><th>现实问题</th><th>改进方向</th></tr></thead><tbody>
<tr><td>收益正态 / 效用二次</td><td>厚尾、偏度、下行风险</td><td>CVaR、期望效用数值解</td></tr>
<tr><td>μ、Σ 已知</td><td>期望收益估计误差极大，权重对输入敏感</td><td>收缩估计、Black-Litterman、最小方差/风险平价</td></tr>
<tr><td>单期、无摩擦</td><td>交易成本、税负、约束</td><td>多期与带约束优化</td></tr>
</tbody></table>
<p>实践中「估计误差比模型误差更致命」：{{ch:21}} 的标准误在这里被放大成权重的不稳定，因此工业界常放弃估计 μ、只用协方差做最小方差或风险平价。</p>"""),
  ],
  demos=[
      demo("code/27-portfolio.py", "最小方差、有效前沿与最大夏普组合", r"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 27-portfolio.py | 两资产组合与切点组合（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
MU1, MU2 = 0.08, 0.12
S1, S2, RHO = 0.15, 0.25, 0.30
RF = 0.03
GRID = 1000

def stats(w):
    mu = w * MU1 + (1 - w) * MU2
    var = (w * w * S1 ** 2 + (1 - w) ** 2 * S2 ** 2 +
           2 * w * (1 - w) * RHO * S1 * S2)
    return mu, math.sqrt(var)

w_min = (S2 ** 2 - RHO * S1 * S2) / (S1 ** 2 + S2 ** 2 - 2 * RHO * S1 * S2)
mu_min, sd_min = stats(w_min)
best_w, best_sharpe = 0.0, -1e9
for i in range(GRID + 1):
    w = -0.5 + 1.5 * i / GRID      # 允许少量卖空以看清前沿形状
    mu, sd = stats(w)
    sh = (mu - RF) / sd
    if sh > best_sharpe:
        best_w, best_sharpe = w, sh
mu_t, sd_t = stats(best_w)
# ---- ρ=1 时无分散化收益的对照 ----
cov = RHO * S1 * S2
sd_equal = math.sqrt(0.25 * S1 ** 2 + 0.25 * S2 ** 2 + 0.5 * cov)
sd_equal_rho1 = math.sqrt(0.25 * S1 ** 2 + 0.25 * S2 ** 2 + 0.5 * S1 * S2)
# ---- 数值验证：打印可手算核对的量 ----
print("资产1: mu=%.2f sd=%.2f  资产2: mu=%.2f sd=%.2f  rho=%.2f" %
      (MU1, S1, MU2, S2, RHO))
print("最小方差权重 w*=%.6f 组合 sd=%.6f (低于两资产)" % (w_min, sd_min))
print("最大夏普权重 w=%.6f 夏普=%.6f mu=%.6f sd=%.6f" %
      (best_w, best_sharpe, mu_t, sd_t))
print("等权组合 sd=%.6f ; 若 rho=1 则 sd=%.6f (无分散化收益)" %
      (sd_equal, sd_equal_rho1))
print("切点组合超预期收益/风险 = %.6f = 夏普比率" % ((mu_t - RF) / sd_t))
""",
            "把 <code>RHO</code> 改成 −0.5 或 1.0，观察最小方差权重与等权组合风险如何变化。",
            "ρ=0.3 时最小方差权重=0.82、组合波动≈0.1431（低于资产 1 的 0.15）；最大夏普权重≈0.5905、夏普≈0.4306；等权组合波动≈0.1639，ρ=1 时为 0.20，无分散化收益。",
            params="RHO 下降降低组合风险；MU2 上升把切点组合推向资产 2；RF 上升改变切点位置。"),
  ],
  highlights=[("mpt", "均值-方差框架"), ("efficient-frontier", "有效前沿与两基金分离"),
              ("sharpe", "夏普比率定义"), ("numpy", "工业版矩阵运算")],
  pitfalls=["用资产数量衡量分散化：真正起作用的是相关性与协方差。",
            "把估计出的期望收益当已知参数：μ 的估计误差会主导权重。",
            "把夏普比率当唯一目标：它忽略偏度、厚尾与流动性风险。"],
  exercises=["解析推导最大夏普权重并和网格解对比（提示：对 <code>(μ_p−r_f)/σ_p</code> 求导）。",
             "把 <code>RHO</code> 从 −1 扫到 1，画最小方差组合波动曲线。",
             "用 {{ch:08}} 的 <code>E[r]−(A/2)σ²</code> 重解切点组合，说明风险厌恶系数 A 落在哪里。"],
  further=["{{ch:08}}　期望效用与风险厌恶", "{{ch:26}}　收益与波动输入", "{{ch:28}}　CAPM 与因子"]),

C("28", "p5", "part5/28-capm-factors", "CAPM 与因子模型：什么风险该有补偿",
  "把 {{ch:27}} 的结论推到市场均衡：只有无法分散的系统性风险（beta）才该获得风险溢价。",
  hours="3 学时",
  goals=["会估计个股 beta、alpha 与 R²，并写出证券市场线",
         "用横截面回归检验「平均收益与 beta 线性相关」",
         "理解因子模型、有效市场假说与实证异象的关系"],
  points=["市场组合与两基金分离", "beta 与系统性风险", "证券市场线 SML", "Jensen alpha", "CAPM 时间序列回归", "横截面检验", "Fama-French 因子", "有效市场假说", "因子投资"],
  bridge="给 {{ch:27}} 的组合优化加上市场均衡条件；{{ch:31}} 会讨论因子挖掘中的多重检验问题，{{ch:23}} 的估计误差在这里再次出现。",
  analogy="beta 就是资产收益对市场因子的回归斜率；CAPM 声称「alpha 应该为零」，即不存在无法用系统性暴露解释的超额收益。检验 CAPM 本质上是在跑一组回归并检验截距。",
  sections=[
      ("28.1", "从组合优化到市场均衡", """<p>若所有人都按 {{ch:27}} 持有同一切点组合，该组合就是<strong>市场组合</strong>。均衡条件给出：</p>"""
       + eq("E[r_i] − r_f = β_i·(E[r_m] − r_f) ,  β_i = Cov(r_i, r_m)/Var(r_m)")
       + """<p>证券市场线（SML）说：期望超额收益只与 beta 线性相关，<strong>特有风险不被定价</strong>（因为它可分散）。这与 {{ch:12}} 的「只内部化边际社会成本」在结构上很像：只给不可消除的部分定价。</p>
<p>实证形式是时间序列回归 <code>r_i − r_f = α_i + β_i(r_m − r_f) + ε_i</code>；CAPM 预言所有 <code>α_i=0</code>。<code>α_i</code> 显著不为零即 Jensen's alpha，可能来自定价错误，也可能来自模型设定错误（<strong>联合检验问题</strong>）。</p>"""),
      ("28.2", "横截面检验与因子扩展", """<p>两步法：先估每只股票的 β̂，再用平均超额收益对 β̂ 做横截面回归，斜率应约等于市场风险溢价。实证中斜率往往偏平、截距偏高，小市值与高账面市值比股票收益系统性偏高，于是有 Fama–French 三因子：</p>"""
       + eq("r_i − r_f = α + β_m MKT + β_s SMB + β_h HML + ε")
       + """<p>后续又加入动量、盈利、投资等因子，形成「因子动物园」。这里要带着 {{ch:31}} 的警觉：从大量候选因子里挑显著的，本身就是多重检验问题；样本外表现与经济学解释同样重要。</p>"""),
      ("28.3", "有效市场与行为金融的张力", """<table><thead><tr><th style="width:26%">命题</th><th>含义</th><th>可检验推论</th></tr></thead><tbody>
<tr><td>弱式有效</td><td>价格已含历史价格信息</td><td>收益不可由自身滞后预测</td></tr>
<tr><td>半强式有效</td><td>价格已含公开信息</td><td>事件公告后无持续漂移（实际有 PEAD）</td></tr>
<tr><td>行为金融</td><td>存在系统性认知偏差</td><td>动量、反转、处置效应、泡沫</td></tr>
</tbody></table>
<p>Grossman–Stiglitz 的洞见：若市场完全有效，收集信息就没有回报，于是没人收集信息，价格又不会反映信息。<strong>均衡只能是「近似有效」</strong>，留出刚好补偿信息成本的价格偏差。</p>"""),
  ],
  demos=[
      demo("code/28-capm.py", "估计 beta/alpha、横截面检验与因子增量 R²", r"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 28-capm.py | CAPM 时间序列与横截面回归（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
T = 240                      # 20 年月度
RF_M, MU_M_M, SD_M_M = 0.03 / 12, 0.08 / 12, 0.16 / math.sqrt(12)
N_ASSETS = 12
BETAS = [0.4 + 0.12 * i for i in range(N_ASSETS)]
ALPHAS = [0.0] * N_ASSETS
IDIO_SD = 0.01

def mean(v):
    return statistics.fmean(v)

def cov(a, b):
    ma, mb = mean(a), mean(b)
    return sum((a[i] - ma) * (b[i] - mb) for i in range(len(a))) / len(a)

def ols1(xs, ys):
    b = cov(xs, ys) / cov(xs, xs)
    a = mean(ys) - b * mean(xs)
    e = [ys[i] - a - b * xs[i] for i in range(len(xs))]
    tss = sum((y - mean(ys)) ** 2 for y in ys)
    r2 = 1 - sum(v * v for v in e) / tss
    s2 = sum(v * v for v in e) / (len(xs) - 2)
    se = math.sqrt(s2 / (cov(xs, xs) * len(xs)))
    return a, b, se, r2

# ---- DGP: 市场因子 + 三个因子暴露 ----
rng = random.Random(7)
mkt = [rng.gauss(MU_M_M, SD_M_M) for _ in range(T)]
excess_m = [m - RF_M for m in mkt]
smb = [rng.gauss(0.001, 0.02) for _ in range(T)]
hml = [rng.gauss(0.001, 0.02) for _ in range(T)]
series = []
for beta, alpha in zip(BETAS, ALPHAS):
    ri_excess = [alpha + beta * excess_m[t] +
                 0.4 * smb[t] + 0.2 * hml[t] + rng.gauss(0, IDIO_SD)
                 for t in range(T)]
    series.append(ri_excess)
# ---- 第一步：时间序列 CAPM 回归 ----
est = [ols1(excess_m, s) for s in series]
# ---- 第二步：横截面回归 mean(r_i) ~ beta_i ----
xs = [e[1] for e in est]
ys = [mean(s) for s in series]
a_cs, b_cs, se_cs, r2_cs = ols1(xs, ys)
# ---- 三因子回归的 R² 增量 ----
def ols3(rows, y):
    # 用标准库做 4x4 高斯-约当求逆
    n = 4
    xtx = [[0.0] * n for _ in range(n)]
    xty = [0.0] * n
    for row, yi in zip(rows, y):
        for i in range(n):
            xty[i] += row[i] * yi
            for j in range(n):
                xtx[i][j] += row[i] * row[j]
    m = [list(xtx[i]) + [1.0 if i == j else 0.0 for j in range(n)]
         for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        m[c], m[p] = m[p], m[c]
        d = m[c][c]
        for j in range(2 * n):
            m[c][j] /= d
        for r in range(n):
            if r != c:
                f = m[r][c]
                if f:
                    for j in range(2 * n):
                        m[r][j] -= f * m[c][j]
    inv = [row[n:] for row in m]
    b = [sum(inv[i][j] * xty[j] for j in range(n)) for i in range(n)]
    e = [yi - sum(b[k] * row[k] for k in range(n))
         for row, yi in zip(rows, y)]
    tss = sum((yi - mean(y)) ** 2 for yi in y)
    return 1 - sum(v * v for v in e) / tss

rows = [[1.0, excess_m[t], smb[t], hml[t]] for t in range(T)]
r2_3f = ols3(rows, series[0])
# ---- 数值验证：打印可手算核对的量 ----
print("市场月超额收益: 样本=%.6f 理论=%.6f 年化≈%.2f%%" %
      (mean(excess_m), MU_M_M - RF_M, 1200 * mean(excess_m)))
for i in (0, 5, 11):
    a, b, bse, r2 = est[i]
    print("资产%02d beta_hat=%.4f (真 %.2f) beta_se=%.6f alpha_hat=%.6f R2=%.4f" %
          (i + 1, b, BETAS[i], bse, a, r2))
print("横截面斜率=%.6f (对照市场已实现超额收益 %.6f) 截距=%.6f R2=%.4f" %
      (b_cs, mean(excess_m), a_cs, r2_cs))
print("加入 SMB/HML 后资产1 R2: %.4f -> %.4f" % (est[0][3], r2_3f))
""",
            "把 <code>IDIO_SD</code> 改成 0.03，观察 beta 的 se 与 R² 如何变化；把 <code>T</code> 改成 60 看横截面斜率的噪声。",
            "12 个资产的 β̂ 都接近各自真值（0.4～1.72），α̂ 在 0 附近；横截面斜率接近本次样本的市场已实现月超额收益（理论约 0.0042，20 年样本会有抽样波动）；加入 SMB/HML 后资产 1 的 R² 明显上升。",
            params="IDIO_SD 越大 R² 越低、beta 越不精确；T 越小横截面斜率越不稳定；因子载荷系数决定 R² 增量。"),
  ],
  highlights=[("capm", "CAPM 与证券市场线"), ("fama-french", "三因子模型"),
              ("french", "Ken French 公开因子数据"), ("emh", "有效市场假说")],
  pitfalls=["把 alpha 显著直接解读为「基金经理能力」：它是相对某个因子模型的残差，模型错则 alpha 也错。",
            "用估计出的 β̂ 做横截面回归却忽略测量误差：会产生变量误差偏误（见 {{ch:23}}）。",
            "把样本内显著的因子当成可交易收益：需考虑多重检验、交易成本与样本外表现。"],
  exercises=["把 <code>smb/hml</code> 的载荷设为 0，观察三因子 R² 增量是否消失。",
             "用 {{ch:22}} 的稳健标准误重算 alpha 的 t 值。",
             "用 Ken French 数据复现一次三因子回归，对照本章手写输出。"],
  further=["{{ch:27}}　切点组合与市场组合", "{{ch:31}}　因子动物园与多重检验", "{{ch:30}}　因子与期权定价的共同基础"]),

C("29", "p5", "part5/29-bonds", "债券、久期与期限结构：利率风险的一阶与二阶",
  "债券价格是未来现金流的贴现值；久期是价格对收益率的一阶敏感度，凸性补上二阶项。",
  hours="3 学时",
  goals=["能从即期利率曲线给附息债券定价",
         "会计算麦考利久期、修正久期与凸性，并用泰勒展开预测价格变化",
         "理解远期利率、期限结构形状与预期假说"],
  points=["现值定价", "到期收益率 YTM", "麦考利久期", "修正久期", "凸性", "价格近似与误差", "即期利率与远期利率", "期限结构形状"],
  bridge="把 {{ch:08}} 的现值、{{ch:17}} 的政策利率、{{ch:19}} 的利差统一到一条收益率曲线；{{ch:30}} 的无套利定价延续同一逻辑。",
  analogy="久期是价格函数对利率的导数（一阶敏感度），凸性是二阶导数；用泰勒展开近似价格等价于用低阶多项式做局部近似，利率变动越大误差越明显。",
  sections=[
      ("29.1", "定价与久期", """<p>附息债券价格 <code>P = Σ CF_t/(1+y)^t</code>。由 <code>dP/P = −D_mod·dy + ½C·dy²</code> 定义：</p>"""
       + eq("D_mac = Σ t·PV(CF_t)/P ;  D_mod = D_mac/(1+y) ;  C = Σ t(t+1)PV(CF_t)/[P(1+y)²]")
       + """<p>久期也是「现金流的加权平均回收时间」，还是{{ch:01}} 包络定理意义下的敏感度：<code>D_mod = −(1/P)·∂P/∂y</code>。零息债券的麦考利久期恰好等于期限；票息越高、期限越短，久期越短、利率风险越小。</p>"""),
      ("29.2", "即期、远期与期限结构", """<p>即期利率 <code>s_t</code> 用于贴现第 t 期现金流；由无套利可推出隐含远期利率：</p>"""
       + eq("f(1,2) = (1+s₂)²/(1+s₁) − 1  ;  一般 f(t,t+1) = (1+s_{t+1})^{t+1}/(1+s_t)^t − 1")
       + """<p><strong>预期假说</strong>认为长期利率是未来短期利率的平均（加期限溢价后为流动性偏好理论）；收益率曲线向上倾斜通常反映预期加息或正的期限溢价，倒挂常被视为衰退信号（实证关联，不是因果定律）。{{ch:17}} 的政策利率通过短端传导到整条曲线。</p>"""),
      ("29.3", "利率风险管理的边界", """<table><thead><tr><th style="width:26%">度量</th><th>回答什么</th><th>局限</th></tr></thead><tbody>
<tr><td>久期</td><td>收益率平行移动 1bp 的价格变化</td><td>只适用小幅、平行移动</td></tr>
<tr><td>凸性</td><td>修正二阶误差，解释「涨多跌少」</td><td>仍是局部近似</td></tr>
<tr><td>关键利率久期</td><td>曲线非平行形变（陡峭化/扭曲）</td><td>需要分段曲线数据</td></tr>
</tbody></table>
<p>脚本会同时给出泰勒近似与精确重定价的误差，直观展示「一阶近似何时够用」。</p>"""),
  ],
  demos=[
      demo("code/29-bonds.py", "债券定价、久期/凸性与远期利率", r"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 29-bonds.py | 现金流贴现与利率敏感度（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
FACE, COUPON_RATE, MATURITY = 100.0, 0.05, 5
YTM = 0.04
SHIFT_BP, SHIFT_BIG = 0.0001, 0.01
S1, S2 = 0.03, 0.04

def price(y):
    cfs = [FACE * COUPON_RATE] * MATURITY
    cfs[-1] += FACE
    return sum(cf / (1 + y) ** t for t, cf in enumerate(cfs, 1))

p0 = price(YTM)
cash = [FACE * COUPON_RATE] * MATURITY
cash[-1] += FACE
pv = [cf / (1 + YTM) ** t for t, cf in enumerate(cash, 1)]
d_mac = sum(t * v for t, v in enumerate(pv, 1)) / p0
d_mod = d_mac / (1 + YTM)
convex = sum(t * (t + 1) * pv[t - 1] for t in range(1, MATURITY + 1)) / \
         (p0 * (1 + YTM) ** 2)
# ---- 泰勒近似 vs 精确重定价 ----
def approx(dy):
    return p0 * (1 - d_mod * dy + 0.5 * convex * dy ** 2)
p_up = price(YTM + SHIFT_BIG)
p_down = price(YTM - SHIFT_BIG)
# ---- 远期利率与期限结构 ----
f12 = (1 + S2) ** 2 / (1 + S1) - 1
# ---- 数值验证：打印可手算核对的量 ----
print("5 年期 5%% 票息、YTM=%.2f%% 价格=%.6f" % (100 * YTM, p0))
print("麦考利久期=%.6f 修正久期=%.6f 凸性=%.6f" % (d_mac, d_mod, convex))
print("+1bp: 久期预测 ΔP=%.6f 精确 ΔP=%.6f" %
      (approx(SHIFT_BP) - p0, price(YTM + SHIFT_BP) - p0))
print("+100bp: 一阶预测=%.6f 二阶预测=%.6f 精确=%.6f" %
      (p0 * (1 - d_mod * SHIFT_BIG), approx(SHIFT_BIG), p_up))
print("利率 +100bp 价格变化=%.4f, -100bp 价格变化=%.4f (不对称来自凸性)" %
      (p_up - p0, p_down - p0))
print("即期 s1=%.2f%% s2=%.2f%% => 隐含远期 f(1,2)=%.4f%%" %
      (100 * S1, 100 * S2, 100 * f12))
""",
            "把 <code>COUPON_RATE</code> 改成 0（零息债券），验证麦考利久期是否等于 5；把 <code>SHIFT_BIG</code> 改成 0.05 观察二阶近似误差。",
            "5 年期 5% 票息、YTM=4% 时价格≈104.45；麦考利久期≈4.557、修正久期≈4.382、凸性≈24.48；+1bp 时久期预测与精确值几乎一致；+100bp 时一阶预测 99.87、二阶预测 100.003、精确 100.000；零息债券久期=期限。",
            params="COUPON_RATE 越低久期越长；MATURITY 越长久期与凸性越大；SHIFT_BIG 越大越能看出凸性价值。"),
  ],
  highlights=[("bond-duration", "久期与凸性"), ("yield-curve", "期限结构形状"),
              ("present-value", "贴现基础"), ("fed", "政策利率与曲线短端")],
  pitfalls=["把久期当成熟期限：只有零息债券两者才相等。",
            "用久期预测大幅利率变动：需加凸性或直接精确重定价。",
            "把倒挂曲线当确定性衰退信号：它是预期与期限溢价共同作用的结果。"],
  exercises=["把 <code>MATURITY</code> 从 1 扫到 20，画出久期与凸性曲线。",
             "加入非平行移动（短端 +50bp、长端不变），说明久期为何失效。",
             "用 {{ch:17}} 的费雪方程说明通胀预期如何进入名义曲线。"],
  further=["{{ch:08}}　现值与贴现", "{{ch:17}}　政策利率传导", "{{ch:30}}　无套利定价"]),

C("30", "p5", "part5/30-options", "期权、二叉树与蒙特卡洛：无套利定价的闭环",
  "把「复制组合 + 无套利」写成可回溯的二叉树，再与 Black-Scholes 闭式解和蒙特卡洛模拟三方对照。",
  hours="4 学时",
  goals=["能实现 CRR 二叉树并回溯欧式看涨/看跌期权价格",
         "会用 math.erf 写 Black-Scholes 公式并验证平价关系",
         "理解风险中性概率、蒙特卡洛误差与 delta 对冲"],
  points=["或有权益与 payoff", "无套利与复制组合", "风险中性概率", "CRR 二叉树回溯", "Black-Scholes 公式", "平价关系", "蒙特卡洛定价", "delta 与对冲"],
  bridge="把 {{ch:26}} 的 GBM、{{ch:19}} 的远期无套利与 {{ch:08}} 的贴现合流；{{ch:31}}、{{ch:32}} 会回到「模型可信度」这一主线。",
  analogy="二叉树是动态规划：从叶子节点的 payoff 往回递推期望；风险中性概率不是真实概率，而是让贴现期望等于无套利价格的「等价测度」，相当于换了一套计价单位。",
  sections=[
      ("30.1", "无套利与风险中性", """<p>期权是或有权益，到期 payoff 为 <code>max(S_T−K,0)</code>（看涨）或 <code>max(K−S_T,0)</code>（看跌）。若能用标的与无风险借贷构造复制组合，则价格由无套利唯一确定，与投资者风险偏好无关：</p>"""
       + eq("p = (e^{rΔt} − d)/(u − d) ;  C₀ = e^{−rΔt}[p·C_u + (1−p)·C_d]")
       + """<p>这里 <code>p</code> 是<strong>风险中性概率</strong>，不是真实上涨概率；真实漂移 μ 被无套利条件替换成 r。这是 {{ch:08}} 期望效用之后最重要的一次视角转换：<strong>定价用等价测度，决策用真实测度</strong>。</p>"""),
      ("30.2", "Black-Scholes 与平价关系", """<p>当二叉树步数趋于无穷，得到连续时间闭式解：</p>"""
       + eq("d₁=[ln(S/K)+(r+½σ²)T]/(σ√T) , d₂=d₁−σ√T")
       + eq("C = S·N(d₁) − K·e^{−rT}N(d₂) ;  P = K·e^{−rT}N(−d₂) − S·N(−d₁)")
       + """<p><code>N(·)</code> 用标准库 <code>math.erf</code> 实现：<code>N(x)=½[1+erf(x/√2)]</code>。看涨看跌平价 <code>C − P = S − K·e^{−rT}</code> 是检验实现是否正确的最快单元测试。</p>"""),
      ("30.3", "蒙特卡洛与对冲", """<p>高维或路径依赖 payoff 没有闭式解时，用 <code>S_T = S₀exp[(r−½σ²)T + σ√T Z]</code> 抽样、取贴现平均：</p>"""
       + eq("Ĉ = e^{−rT}·(1/N)Σ max(S_T^{(n)}−K,0) ;  标准误 ≈ σ_payoff/√N")
       + """<p>误差按 <code>1/√N</code> 下降，与 {{ch:02}} 的中心极限定理完全一致；降低方差可用对偶变量、控制变量与准随机序列。<code>Δ=∂C/∂S</code> 给出复制组合里需要持有的标的份额，动态再平衡就是 delta 对冲；现实中的离散对冲、交易成本与跳跃风险是模型误差的主要来源。</p>"""),
  ],
  demos=[
      demo("code/30-options.py", "二叉树、Black-Scholes、蒙特卡洛与平价校验", r"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 30-options.py | 欧式期权三种定价方法（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
S0, K, R, SIGMA, T = 100.0, 100.0, 0.05, 0.20, 1.0
N_STEPS = 200
N_PATHS = 20000

def norm_cdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))

# ---- 1. CRR 二叉树回溯 ----
dt = T / N_STEPS
u = math.exp(SIGMA * math.sqrt(dt))
d = 1 / u
p = (math.exp(R * dt) - d) / (u - d)
disc = math.exp(-R * dt)
call = [max(S0 * (u ** j) * (d ** (N_STEPS - j)) - K, 0.0)
        for j in range(N_STEPS + 1)]
put = [max(K - S0 * (u ** j) * (d ** (N_STEPS - j)), 0.0)
       for j in range(N_STEPS + 1)]
for step in range(N_STEPS, 0, -1):
    call = [disc * (p * call[j + 1] + (1 - p) * call[j]) for j in range(step)]
    put = [disc * (p * put[j + 1] + (1 - p) * put[j]) for j in range(step)]
c_tree, p_tree = call[0], put[0]
# ---- 2. Black-Scholes 闭式解 ----
d1 = (math.log(S0 / K) + (R + 0.5 * SIGMA ** 2) * T) / (SIGMA * math.sqrt(T))
d2 = d1 - SIGMA * math.sqrt(T)
c_bs = S0 * norm_cdf(d1) - K * math.exp(-R * T) * norm_cdf(d2)
p_bs = K * math.exp(-R * T) * norm_cdf(-d2) - S0 * norm_cdf(-d1)
# ---- 3. 蒙特卡洛 ----
rng = random.Random(7)
payoffs = []
for _ in range(N_PATHS):
    z = rng.gauss(0, 1)
    st = S0 * math.exp((R - 0.5 * SIGMA ** 2) * T + SIGMA * math.sqrt(T) * z)
    payoffs.append(max(st - K, 0.0))
c_mc = math.exp(-R * T) * statistics.fmean(payoffs)
mc_se = math.exp(-R * T) * statistics.pstdev(payoffs) / math.sqrt(N_PATHS)
# ---- 4. delta 有限差分 ----
def bs_call(s):
    dd1 = (math.log(s / K) + (R + 0.5 * SIGMA ** 2) * T) / (SIGMA * math.sqrt(T))
    dd2 = dd1 - SIGMA * math.sqrt(T)
    return s * norm_cdf(dd1) - K * math.exp(-R * T) * norm_cdf(dd2)
delta = (bs_call(S0 + 0.01) - bs_call(S0 - 0.01)) / 0.02
# ---- 数值验证：打印可手算核对的量 ----
print("参数: S=K=%.0f r=%.2f sigma=%.2f T=%.0f N=%d" %
      (S0, R, SIGMA, T, N_STEPS))
print("二叉树   call=%.6f put=%.6f" % (c_tree, p_tree))
print("B-S 公式 call=%.6f put=%.6f" % (c_bs, p_bs))
print("蒙特卡洛 call=%.6f ±%.6f (1 倍标准误, %d 路径)" % (c_mc, mc_se, N_PATHS))
print("平价校验 C-P=%.6f  S-K*e^(-rT)=%.6f  差=%.2e" %
      (c_tree - p_tree, S0 - K * math.exp(-R * T),
       abs((c_tree - p_tree) - (S0 - K * math.exp(-R * T)))))
print("delta=%.6f (≈N(d1)=%.6f)" % (delta, norm_cdf(d1)))
""",
            "把 <code>N_STEPS</code> 改成 10、50、200，观察二叉树价格如何收敛到 B-S；把 <code>N_PATHS</code> 改成 2000 看蒙特卡洛标准误是否按 1/√N 放大。",
            "S=K=100、r=5%、σ=20%、T=1 时二叉树 call≈10.4406/put≈5.5635，B-S call≈10.4506/put≈5.5735（200 步离散误差约 0.01）；蒙特卡洛 call≈10.47 ±0.10；C−P 与 S−K·e^(−rT)≈4.8771 一致；delta≈0.6368。",
            params="N_STEPS 控制离散化误差；N_PATHS 控制蒙特卡洛误差；SIGMA 上升同时提高 call 与 put 价格。"),
  ],
  highlights=[("binomial-option", "CRR 二叉树"), ("black-scholes", "闭式解与假设"),
              ("monte-carlo", "蒙特卡洛方法"), ("risk-neutral", "等价鞅测度")],
  pitfalls=["把风险中性概率当真实上涨概率：它只是便于贴现的等价权重。",
            "忽略平价关系校验：它是发现实现 bug 最便宜的手段。",
            "把 BS 的常数波动假设当事实：隐含波动率微笑正是它的系统性偏离。"],
  exercises=["把二叉树改成美式看跌期权（每节点比较提前行权价值），观察价格何时高于欧式。",
             "用对偶变量法（同时取 Z 与 −Z）重跑蒙特卡洛，比较标准误。",
             "用 {{ch:26}} 的 GBM 路径实现亚式期权定价，说明为何没有闭式解。"],
  further=["{{ch:26}}　GBM 与对数收益", "{{ch:19}}　远期与利率平价", "{{ch:32}}　端到端综合课题"]),
]

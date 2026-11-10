#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""计量篇 20-25：识别、OLS、诊断、工具变量、面板因果与时间序列。"""
from book_schema import C, demo, eq, table

CH = [

C("20", "p4", "part4/20-identification", "识别：从数据生成过程到因果参数",
  "在估计之前先问：这个参数能否由观测数据的分布唯一确定？本章用潜在结果框架把「相关不等于因果」写成可计算的偏误公式。",
  hours="3 学时",
  goals=["能写出潜在结果、ATE 与选择偏误的代数分解",
         "会构造一个已知真值的 DGP，并对比选择样本与随机实验的估计",
         "理解「先识别、后估计」的研究顺序与卢卡斯批判"],
  points=["数据生成过程 DGP", "潜在结果与 ATE", "选择偏误", "随机化与可忽略性", "条件独立与分层", "反事实与识别", "卢卡斯批判", "内部/外部效度"],
  bridge="把 {{ch:02}} 的 DGP 升级为研究对象：前四篇都在已知参数下正推均衡，从这里开始要从观测数据反推参数。{{ch:21}}～{{ch:25}} 逐一给出估计量与诊断。",
  analogy="DGP 是「带已知答案的测试夹具」；识别是检查「从可观测日志里能不能反解出参数」，估计是「样本有限时解得准不准」，推断是「误差有多大」。三者是不同的失败模式。",
  sections=[
      ("20.1", "潜在结果与 ATE", """<p>对每个个体 i 定义两个潜在结果 <code>Y_i(1)</code>（接受处理）与 <code>Y_i(0)</code>（未接受），个体处理效应 <code>τ_i = Y_i(1) − Y_i(0)</code>，目标参数通常是 <code>ATE = E[τ_i]</code>。观测到的只有 <code>Y_i = D_i Y_i(1) + (1−D_i)Y_i(0)</code>：<strong>每个个体都缺一半数据</strong>，这就是因果推断的根本问题。</p>"""),
      ("20.2", "朴素差异的偏误分解", """<p>把组间均值差拆开：</p>"""
       + eq("E[Y|D=1] − E[Y|D=0] = ATT + { E[Y(0)|D=1] − E[Y(0)|D=0] }")
       + """<p>第二项是<strong>选择偏误</strong>：处理组即使不处理，本来结果也不同。随机化使 <code>D ⟂ (Y(1),Y(0))</code>，第二项归零；观察性研究里则要靠「依可观测变量条件独立」（<code>D ⟂ Y(0) | X</code>）或 {{ch:23}}、{{ch:24}} 的设计型识别策略。</p>
<div class="card warn"><p style="margin-bottom:0"><strong>顺序不能倒过来</strong>：控制更多变量不等于识别更好；若控制的是处理之后的变量（对撞变量 / 中介），反而会引入新偏误。先画因果图（DAG）写清 DGP，再决定回归里放什么，这是程序员最容易凭直觉跳错的一步。</p></div>"""),
      ("20.3", "模拟：把识别假设做成实验", """<p>本章脚本构造「能力高者更可能参加培训」的 DGP，真实 ATE 已知为 2。三种估计对比：直接用观测组间差（偏）、随机指派（无偏）、按能力分层后加权（分层越细越接近无偏，本例只分四层会残留少量偏误）。这是全书后续所有计量脚本的模板：<strong>已知真值 → 生成数据 → 估计 → 比较</strong>。</p>
<p>最后提醒<strong>卢卡斯批判</strong>：若政策本身改变了行为方程（例如培训补贴改变了谁去培训），历史数据估计出的参数就不能直接用于反事实预测。这与「训练分布与部署分布不一致」是同一个问题。</p>"""),
  ],
  demos=[
      demo("code/20-identification.py", "潜在结果、选择偏误与随机化", r"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 20-identification.py | 已知真值 ATE 的识别实验（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
N = 20000
TAU = 2.0                 # 真实 ATE
BETA_ABILITY = 0.5        # 能力对基线结果的影响
NOISE_SD = 0.5
# ---- DGP: 能力 A 决定自我选择，Y(1)=Y(0)+TAU ----
ability = [random.gauss(0, 1) for _ in range(N)]
d = [1 if a + random.gauss(0, 1) > 0 else 0 for a in ability]
y0 = [1.0 + BETA_ABILITY * a + random.gauss(0, NOISE_SD) for a in ability]
y1 = [v + TAU for v in y0]
y = [y1[i] if d[i] else y0[i] for i in range(N)]
ate_true = statistics.fmean([y1[i] - y0[i] for i in range(N)])
# ---- 估计 1: 观测组间差 ----
m1 = statistics.fmean([y[i] for i in range(N) if d[i] == 1])
m0 = statistics.fmean([y[i] for i in range(N) if d[i] == 0])
naive = m1 - m0
sel_bias = statistics.fmean([y0[i] for i in range(N) if d[i] == 1]) - \
           statistics.fmean([y0[i] for i in range(N) if d[i] == 0])
# ---- 估计 2: 随机指派（反事实实验）----
d_r = [1 if random.random() < 0.5 else 0 for _ in range(N)]
y_r = [y1[i] if d_r[i] else y0[i] for i in range(N)]
mr1 = statistics.fmean([y_r[i] for i in range(N) if d_r[i] == 1])
mr0 = statistics.fmean([y_r[i] for i in range(N) if d_r[i] == 0])
rand_est = mr1 - mr0
# ---- 估计 3: 按能力分层后加权（条件独立）----
order = sorted(range(N), key=lambda i: ability[i])
strata = [order[k * N // 4:(k + 1) * N // 4] for k in range(4)]
strat_est = 0.0
for s in strata:
    t = [i for i in s if d[i] == 1]
    c = [i for i in s if d[i] == 0]
    strat_est += (statistics.fmean([y[i] for i in t]) -
                  statistics.fmean([y[i] for i in c])) * len(s) / N
# ---- 数值验证：打印可手算核对的量 ----
print("真实 ATE=%.4f 处理组比例=%.4f" % (ate_true, sum(d) / N))
print("朴素组间差=%.4f = ATE %.4f + 选择偏误 %.4f" % (naive, ate_true, sel_bias))
print("随机指派估计=%.4f (误差 %.4f)" % (rand_est, rand_est - ate_true))
print("按能力四分层估计=%.4f (误差 %.4f)" % (strat_est, strat_est - ate_true))
""",
            "把 <code>BETA_ABILITY</code> 改成 0（能力不影响结果），观察选择偏误是否消失。",
            "真实 ATE=2；朴素组间差≈2.55 = 2 + 选择偏误≈0.55；随机指派≈2.00；按能力四分层≈2.08（分层过粗残留约 0.08 偏误，把分层数加到 20 会明显减小）。",
            params="BETA_ABILITY 越大选择偏误越大；NOISE_SD 越大估计方差越大；N 越大随机误差越小。"),
  ],
  highlights=[("rubin", "潜在结果框架"), ("identification", "识别的严格定义"),
              ("causal-book", "用 Python 讲因果推断的开放教材"), ("dgp", "DGP 概念")],
  pitfalls=["把「控制了更多变量」当成识别改善：控制对撞变量或中介会引入偏误。",
            "把相关系数的显著性当成因果证据：显著性只回答抽样误差，不回答识别。",
            "忽略外部效度：样本上的 ATE 未必能外推到另一个人群或政策规模。"],
  exercises=["在脚本里加入一个「处理后变量」作为控制，观察估计为何变坏。",
             "把处理效应改成异质 <code>τ_i = 2 + A_i</code>，分别计算 ATE 与 ATT 并比较。",
             "用 {{ch:02}} 的语言说明：为什么随机指派相当于消除了 D 与 u 的相关。"],
  further=["{{ch:21}}　OLS 与条件期望", "{{ch:23}}　工具变量识别", "{{ch:24}}　DID 与平行趋势"]),

C("21", "p4", "part4/21-ols", "最小二乘：手写 OLS、标准误与高斯-马尔可夫",
  "把 <code>(XᵀX)⁻¹Xᵀy</code> 完全展开成可读的循环，看清无偏性究竟依赖哪些假设，以及标准误从哪来。",
  hours="4 学时",
  goals=["能用标准库实现多元 OLS 与矩阵求逆，输出 β̂、标准误、t 值与 R²",
         "说明 OLS 无偏所需的假设，并用蒙特卡洛验证抽样分布",
         "解释 R² 与因果解释力无关、共线性如何放大标准误"],
  points=["条件期望函数", "最小二乘目标", "正规方程与矩阵求逆", "高斯-马尔可夫定理", "残差与方差估计", "标准误与 t 检验", "R² 的误用", "蒙特卡洛抽样分布"],
  bridge="把 {{ch:20}} 的识别问题先放在「D 与误差无关」的理想条件下，得到最基础的估计量；{{ch:22}}、{{ch:23}} 逐条放松假设。",
  analogy="OLS 是把 y 正交投影到 X 的列空间：<code>β̂ = (XᵀX)⁻¹Xᵀy</code> 就是正规方程的解；标准误来自残差方差乘以 <code>(XᵀX)⁻¹</code> 的对角元——数据越「各方向都有变化」，矩阵越良态，估计越稳。",
  sections=[
      ("21.1", "投影与正规方程", """<p>最小化 <code>SSR(β)=Σ(y_i−x_i'β)²</code>，令梯度为零得正规方程 <code>X'X·β̂ = X'y</code>：</p>"""
       + eq("β̂ = (XᵀX)⁻¹Xᵀy  ;  残差 e = y − Xβ̂ 满足 Xᵀe = 0（正交性）")
       + """<p>若 <code>E[u|X]=0</code>（外生性），则 <code>E[β̂|X]=β</code>；在同方差且无自相关时 <code>Var(β̂|X)=σ²(XᵀX)⁻¹</code>，<strong>高斯-马尔可夫定理</strong>说它是线性无偏估计量中方差最小的（BLUE）。注意无偏性不依赖正态假设，正态只用于小样本精确推断。</p>"""),
      ("21.2", "标准误、t 值与 R²", """<p>用 <code>s² = e'e/(n−k)</code> 估计 σ²，标准误 <code>se(β̂_j)=√(s²·[(XᵀX)⁻¹]_{jj})</code>，<code>t=(β̂_j−β_{j,0})/se</code> 在 <code>H₀</code> 下近似 t(n−k)。R² 衡量样本内拟合：</p>"""
       + eq("R² = 1 − RSS/TSS ;  加变量永远不会降低 R²（调整 R² 才惩罚自由度）")
       + """<p><strong>R² 高不代表模型可用于因果解释</strong>：{{ch:25}} 的伪回归能给出很高的 R²；反过来 {{ch:20}} 里随机实验的 R² 可能很低但 ATE 估计完全可信。判断因果靠识别假设，不靠拟合优度。</p>"""),
      ("21.3", "手写的价值与边界", """<table><thead><tr><th style="width:30%">脚本里手写</th><th>工业实现</th><th>为什么先手写</th></tr></thead><tbody>
<tr><td>高斯-约当求逆</td><td><code>numpy.linalg</code> / LAPACK</td><td>看清奇异与近共线性如何发生</td></tr>
<tr><td>XᵀX 累加循环</td><td>向量化矩阵乘</td><td>理解正规方程每一项的含义</td></tr>
<tr><td>t 值与 R²</td><td><code>statsmodels.OLS.fit().summary()</code></td><td>知道输出每一列对应哪个公式</td></tr>
</tbody></table>
<p>现实数据请直接换成 <code>statsmodels</code>：数值稳定性（QR 分解）、缺失值、稳健标准误、面板与时间序列都更可靠。附录 A.5 给出对照表。</p>"""),
  ],
  demos=[
      demo("code/21-ols.py", "手写矩阵求逆、OLS 全量输出与蒙特卡洛", r"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 21-ols.py | 从零实现多元 OLS：beta / se / t / R2（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
N, REPS = 400, 500
BETA = [1.0, 2.0, -1.5]       # 截距, x1, x2 的真实系数
NOISE_SD = 1.0

def inverse(a):
    n = len(a)
    m = [list(a[i]) + [1.0 if i == j else 0.0 for j in range(n)]
          for i in range(n)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(m[r][col]))
        m[col], m[piv] = m[piv], m[col]
        p = m[col][col]
        for j in range(2 * n):
            m[col][j] /= p
        for r in range(n):
            if r != col:
                f = m[r][col]
                if f:
                    for j in range(2 * n):
                        m[r][j] -= f * m[col][j]
    return [row[n:] for row in m]

def ols(rows, ys):
    xtx = [[0.0] * 3 for _ in range(3)]
    xty = [0.0] * 3
    for row, y in zip(rows, ys):
        for i in range(3):
            xty[i] += row[i] * y
            for j in range(3):
                xtx[i][j] += row[i] * row[j]
    inv = inverse(xtx)
    beta = [sum(inv[i][j] * xty[j] for j in range(3)) for i in range(3)]
    resid = [y - sum(b * x for b, x in zip(beta, row))
             for row, y in zip(rows, ys)]
    k = 3
    s2 = sum(r * r for r in resid) / (len(ys) - k)
    se = [math.sqrt(s2 * inv[i][i]) for i in range(3)]
    my = statistics.fmean(ys)
    tss = sum((y - my) ** 2 for y in ys)
    rss = sum(r * r for r in resid)
    return beta, se, 1 - rss / tss

def sample(seed_rng):
    rows, ys = [], []
    for _ in range(N):
        x1 = seed_rng.uniform(0, 10)
        x2 = 0.5 * x1 + seed_rng.gauss(0, 1)
        u = seed_rng.gauss(0, NOISE_SD)
        rows.append([1.0, x1, x2])
        ys.append(BETA[0] + BETA[1] * x1 + BETA[2] * x2 + u)
    return rows, ys

rng = random.Random(7)
rows, ys = sample(rng)
beta, se, r2 = ols(rows, ys)
# ---- 蒙特卡洛：验证无偏与标准误 ----
mc_rng = random.Random(11)
b1s, t1s = [], []
for _ in range(REPS):
    rr, yy = sample(mc_rng)
    b, s, _ = ols(rr, yy)
    b1s.append(b[1])
    t1s.append((b[1] - BETA[1]) / s[1])
# ---- 数值验证：打印可手算核对的量 ----
print("真实 beta =", BETA)
print("估计 beta = [%.6f, %.6f, %.6f]" % tuple(beta))
print("标准误   = [%.6f, %.6f, %.6f]" % tuple(se))
print("t 值(H0:beta=0) = [%.3f, %.3f, %.3f]" %
      tuple(beta[i] / se[i] for i in range(3)))
print("R²=%.4f  残差均值=%.6f (应近 0)" %
      (r2, statistics.fmean([y - sum(b * x for b, x in zip(beta, row))
                            for row, y in zip(rows, ys)])))
print("蒙特卡洛 %d 次: beta1 均值=%.6f 标准差=%.6f 单次 se=%.6f" %
      (REPS, statistics.fmean(b1s), statistics.pstdev(b1s), se[1]))
print("|t|>1.96 比例=%.4f (名义 0.05)" %
      (sum(1 for t in t1s if abs(t) > 1.96) / REPS))
""",
            "把 <code>NOISE_SD</code> 改成 3，观察标准误与 t 值是否按 σ 放大；把 <code>N</code> 改成 100 看 se 是否约翻倍。",
            "β̂≈(1.14, 2.01, −1.56)，与真值 (1, 2, −1.5) 在标准误范围内一致，残差均值≈0，R²≈0.94；500 次重复中 β̂₁ 均值≈2.000、标准差≈0.029 与单次 se≈0.030 接近，|t|>1.96 的比例≈0.034（有限样本略低于名义 0.05）。",
            params="NOISE_SD 越大 se 越大；N 越大 se 按 1/√N 缩小；x2 与 x1 相关性越高，se 膨胀越明显。"),
  ],
  highlights=[("ols", "最小二乘的推导与几何"), ("gauss-markov", "BLUE 的假设清单"),
              ("statsmodels-ols", "对照工业实现的输出"), ("python-docs", "标准库语法参考")],
  pitfalls=["把 R² 当作因果可信度：伪回归、遗漏变量都可能给出高 R²。",
            "把无偏性当成「一次估计必然接近真值」：无偏是重复抽样性质，见 {{ch:02}}。",
            "忽略近共线性：XᵀX 接近奇异时求逆数值不稳、标准误暴涨。"],
  exercises=["把 <code>x2</code> 的相关系数提到 0.99，观察 se₂ 与 t 值如何变化。",
             "在 DGP 里加入异方差，观察本章普通 se 是否还准确（预告 {{ch:22}}）。",
             "用 <code>statsmodels</code> 跑同一份数据，逐项对照 β̂、se、t、R²。"],
  further=["{{ch:20}}　识别先于估计", "{{ch:22}}　异方差与稳健标准误", "{{ch:23}}　内生性与 IV"]),

C("22", "p4", "part4/22-diagnostics", "诊断与修正：异方差、自相关与共线性",
  "OLS 的点估计在这些假设被破坏时往往仍无偏，但标准误失效；本章手写稳健标准误并用蒙特卡洛验证覆盖率。",
  hours="3 学时",
  goals=["会推导并实现 White 稳健标准误（HC0）",
         "通过重复抽样比较普通 se 与稳健 se 的假阳性率",
         "用 DW 统计量与 VIF 诊断自相关和共线性"],
  points=["异方差的后果", "普通标准误为何失效", "White HC0 稳健标准误", "蒙特卡洛覆盖率", "自相关与 DW 统计量", "多重共线性与 VIF", "可行广义最小二乘思路"],
  bridge="放松 {{ch:21}} 的「同方差、无自相关、无共线性」；{{ch:23}} 继续放松最关键的「外生性」。",
  analogy="普通 se 假设每个样本的噪声水平相同；稳健 se 允许每个观测有自己的噪声尺度，相当于给每个残差单独加权再重估协方差矩阵，是「不对误差分布做强假设」的防御式实现。",
  sections=[
      ("22.1", "异方差：点估计无偏，推断失真", """<p>若 <code>Var(u_i|X)=σ_i²</code> 非常数，<code>β̂</code> 仍无偏（只要 <code>E[u|X]=0</code>），但 <code>Var(β̂)</code> 不再是 <code>σ²(XᵀX)⁻¹</code>。一致估计量（以一元回归为例）：</p>"""
       + eq("Var_HC0(β̂₁) = Σ e_i²(x_i−x̄)² / [Σ(x_i−x̄)²]²   (White / Eicker–Huber–White)")
       + """<p>矩阵形式是三明治 <code>(XᵀX)⁻¹ (Σ e_i² x_i x_iᵀ) (XᵀX)⁻¹</code>。小样本下 HC0 偏乐观，实际常用 HC1/HC3 做自由度修正。若已知异方差结构，FGLS/WLS 可以提高效率，但错误设定权重反而更糟。</p>"""),
      ("22.2", "自相关与共线性的诊断量", """<p>时间序列残差若满足 AR(1) <code>e_t=ρe_{t−1}+v_t</code>，Durbin–Watson 统计量近似 <code>DW≈2(1−ρ)</code>：接近 2 表示无自相关，接近 0 表示强正相关。多重共线性用方差膨胀因子度量：</p>"""
       + eq("VIF_j = 1/(1−R_j²)  ;  se 膨胀倍数 = √VIF_j")
       + """<p>共线性不是「模型错了」，而是<strong>数据里缺少识别该系数所需的变化</strong>：r=0.99 时 se 膨胀约 7 倍。解法是增加信息（更多样本、实验设计）或正则化/降维，而不是删掉「不显著」的变量了事。</p>"""),
      ("22.3", "诊断不是猎巫", """<table><thead><tr><th style="width:28%">症状</th><th>可能原因</th><th>先做什么</th></tr></thead><tbody>
<tr><td>残差漏斗形</td><td>异方差 / 函数形式错</td><td>画残差-拟合图；改用稳健 se</td></tr>
<tr><td>DW 明显小于 2</td><td>遗漏时间趋势 / 序列相关</td><td>加趋势或滞后，见 {{ch:25}}</td></tr>
<tr><td>系数符号反常且不显著</td><td>共线性 / 度量误差</td><td>看相关矩阵与 VIF</td></tr>
</tbody></table>
<p>重要边界：诊断检验本身也有多重检验问题（{{ch:31}}），在报告结果前反复试 specification 会抬高假阳性率。预注册分析计划、报告全部设定，是更可靠的做法。</p>"""),
  ],
  demos=[
      demo("code/22-diagnostics.py", "异方差稳健标准误、DW 与 VIF", r"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 22-diagnostics.py | 手写 HC0 与诊断量（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
N, REPS = 200, 1000
B0, B1 = 1.0, 2.0
RHO_AR = 0.7

def ols1(xs, ys):
    mx, my = statistics.fmean(xs), statistics.fmean(ys)
    dx = [x - mx for x in xs]
    sxx = sum(v * v for v in dx)
    sxy = sum(dx[i] * (ys[i] - my) for i in range(len(xs)))
    b = sxy / sxx
    a = my - b * mx
    e = [ys[i] - a - b * xs[i] for i in range(len(xs))]
    s2 = sum(v * v for v in e) / (len(xs) - 2)
    se = math.sqrt(s2 / sxx)
    se_rob = math.sqrt(sum(e[i] ** 2 * dx[i] ** 2 for i in range(len(xs))) / sxx ** 2)
    return a, b, se, se_rob, e

def one_sample(rng):
    xs = [10.0 * i / N for i in range(N)]
    # 异方差: 噪声标准差随 x 增大
    ys = [B0 + B1 * x + rng.gauss(0, 0.5 + 0.3 * x) for x in xs]
    return xs, ys

rng = random.Random(7)
xs, ys = one_sample(rng)
a, b, se, se_rob, e = ols1(xs, ys)
# ---- 蒙特卡洛：两种 se 的假阳性率 ----
mc = random.Random(23)
r_ordinary, r_robust = 0, 0
for _ in range(REPS):
    xx, yy = one_sample(mc)
    _, bb, s1, s2, _ = ols1(xx, yy)
    if abs((bb - B1) / s1) > 1.96:
        r_ordinary += 1
    if abs((bb - B1) / s2) > 1.96:
        r_robust += 1
# ---- AR(1) 残差与 DW ----
ar_rng = random.Random(31)
prev, errs = 0.0, []
for _ in range(N):
    prev = RHO_AR * prev + ar_rng.gauss(0, 1)
    errs.append(prev)
dw = sum((errs[i] - errs[i - 1]) ** 2 for i in range(1, N)) / sum(v * v for v in errs)
# ---- 共线性：VIF 与 se 膨胀 ----
vifs = [(r, 1 / (1 - r * r), math.sqrt(1 / (1 - r * r))) for r in (0.0, 0.9, 0.99)]
# ---- 数值验证：打印可手算核对的量 ----
print("单样本 beta1=%.6f (真实 %.2f) 普通 se=%.6f 稳健 se=%.6f" % (b, B1, se, se_rob))
print("蒙特卡洛 %d 次 H0 假阳性率: 普通 se=%.4f 稳健 se=%.4f (名义 0.05)" %
      (REPS, r_ordinary / REPS, r_robust / REPS))
print("DW=%.4f ≈ 2(1-rho)=%.4f" % (dw, 2 * (1 - RHO_AR)))
for r, vif, infl in vifs:
    print("  相关系数 r=%.2f  VIF=%.2f  se 膨胀=%.2f 倍" % (r, vif, infl))
""",
            "把 DGP 里的 <code>0.3*x</code> 改成 0（同方差），观察普通 se 与稳健 se 是否接近、假阳性率是否都回到 0.05。",
            "β̂₁≈2.02，普通 se≈0.056、稳健 se≈0.062；1000 次重复中普通 se 的假阳性率≈0.074，HC0 稳健 se≈0.063（明显改善但小样本仍偏高）；DW≈0.72，与 2(1−ρ)=0.6 同一量级；r=0.99 时 se 膨胀约 7.09 倍。",
            params="RHO_AR 越接近 1，DW 越接近 0；N 变小会放大 HC0 的小样本偏差。"),
  ],
  highlights=[("heteroscedasticity", "异方差的定义与后果"), ("robust-se", "HC0/HC1/HC3 系列"),
              ("autocorrelation", "序列相关与 DW"), ("statsmodels", "工业实现对照")],
  pitfalls=["以为异方差使 β̂ 有偏：它破坏的是推断效率与标准误，不是无偏性。",
            "把稳健标准误当成万能药：存在内生性或聚类相关时仍不够。",
            "靠反复删变量解决共线性：这会引入设定搜索偏误，见 {{ch:31}}。"],
  exercises=["推导 HC1 = n/(n−k)·HC0 的自由度修正，并在脚本里实现。",
             "把误差改成聚类结构（同一组内相关），观察 HC0 是否仍失效。",
             "用 {{ch:21}} 的矩阵版 OLS 实现完整三明治协方差矩阵。"],
  further=["{{ch:21}}　OLS 与经典假设", "{{ch:23}}　内生性：连无偏性都不保", "{{ch:31}}　设定搜索与多重检验"]),

C("23", "p4", "part4/23-iv", "内生性与工具变量：2SLS 的手写实现",
  "当解释变量与误差相关，OLS 连无偏性都失去；工具变量用「只通过 x 影响 y 的外生变动」隔离出因果通道。",
  hours="4 学时",
  goals=["能写出内生性偏误公式并判断方向",
         "实现 IV 估计量与两阶段最小二乘，验证两者代数等价",
         "解释相关性、排他性、单调性与弱工具变量问题"],
  points=["内生性来源", "遗漏变量偏误公式", "工具变量相关性", "排他性约束", "IV 估计量", "两阶段最小二乘", "弱工具变量", "局部平均处理效应 LATE"],
  bridge="放松 {{ch:21}} 最关键的外生性假设；{{ch:24}} 用面板与断点设计提供另一类识别策略，{{ch:20}} 的选择偏误在这里得到结构性表达。",
  analogy="工具变量是一次「天然 A/B 实验的外生分流器」：z 随机改变 x，但不直接改 y；2SLS 就是先只用 z 预测 x（去掉与误差相关的部分），再用预测值回归 y。",
  sections=[
      ("23.1", "内生性偏误", """<p>设真模型 <code>y = β₀ + β₁x + β₂w + u</code>，但回归里漏掉 <code>w</code>：</p>"""
       + eq("plim β̂₁(OLS) = β₁ + β₂·Cov(x,w)/Var(x)   (遗漏变量偏误)")
       + """<p>三种常见来源：遗漏变量、 simultaneity（y 反过来影响 x）、度量误差（衰减偏误）。{{ch:20}} 的自我选择就是遗漏「能力」这一特例。<strong>加大样本不会消除偏误</strong>，只会把错误的数估得更精确——这是程序员常犯的「堆数据」直觉错误。</p>"""),
      ("23.2", "IV 与 2SLS", """<p>工具 z 需满足：<strong>相关性</strong> <code>Cov(z,x)≠0</code>、<strong>排他性</strong> <code>Cov(z,u)=0</code>（z 只通过 x 影响 y）。恰识别时：</p>"""
       + eq("β̂_IV = Cov(z,y)/Cov(z,x) = β₁ + Cov(z,u)/Cov(z,x)")
       + """<p>2SLS：第一阶段 <code>x = π₀ + π₁z + v</code> 得 <code>x̂</code>；第二阶段用 <code>x̂</code> 回归 y。由于 <code>x̂</code> 只由 z 构成，与 u 无关，估计一致；且恰识别时与 IV 公式代数等价。第一阶段 F 统计量小于 10 常被视为<strong>弱工具</strong>警戒线：此时 IV 偏误向 OLS 靠拢、且标准误失真。</p>"""),
      ("23.3", "IV 估的是什么", """<p>处理效应异质时，IV 识别的是<strong>局部平均处理效应 LATE</strong>：被工具「推动」而改变行为的那一群人（compliers）的平均效应，而不是全体 ATE。条件包括无关性、单调性（无 defiers）与排他性。</p>
<div class="card warn"><p style="margin-bottom:0">排他性<strong>不能由数据检验</strong>（只能在不恰好识别时做过识别检验，且检验力有限）。它必须靠制度背景、研究设计与因果图来论证。把「找到显著的第一阶段」当成 IV 有效，是最常见的误用。</p></div>"""),
  ],
  demos=[
      demo("code/23-iv.py", "内生性偏误、IV/2SLS 等价与弱工具变量", r"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 23-iv.py | 工具变量与两阶段最小二乘（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
N, REPS = 20000, 400
BETA1 = 2.0
PI_STRONG, PI_WEAK = 0.8, 0.05
S_U, S_E = 1.0, 1.0

def cov(a, b):
    ma, mb = statistics.fmean(a), statistics.fmean(b)
    return sum((a[i] - ma) * (b[i] - mb) for i in range(len(a))) / len(a)

def slope(xs, ys):
    return cov(xs, ys) / cov(xs, xs)

def dgp(rng, n, pi):
    z = [rng.gauss(0, 1) for _ in range(n)]
    u = [rng.gauss(0, S_U) for _ in range(n)]
    e = [rng.gauss(0, S_E) for _ in range(n)]
    x = [pi * z[i] + 0.6 * u[i] + e[i] for i in range(n)]
    y = [1.0 + BETA1 * x[i] + u[i] for i in range(n)]
    return z, x, y

def estimate(z, x, y):
    b_ols = slope(x, y)
    b_iv = cov(z, y) / cov(z, x)
    pi1 = slope(z, x)
    zbar, xbar = statistics.fmean(z), statistics.fmean(x)
    xhat = [xbar + pi1 * (zi - zbar) for zi in z]
    b_2sls = slope(xhat, y)
    return b_ols, b_iv, b_2sls, pi1

rng = random.Random(7)
z, x, y = dgp(rng, N, PI_STRONG)
b_ols, b_iv, b_2sls, pi1 = estimate(z, x, y)
# ---- 弱工具：重复抽样的 IV 分布 ----
weak_rng = random.Random(19)
weak_iv = []
for _ in range(REPS):
    zz, xx, yy = dgp(weak_rng, 500, PI_WEAK)
    weak_iv.append(cov(zz, yy) / cov(zz, xx))
# ---- 数值验证：打印可手算核对的量 ----
print("真实 beta1=%.2f" % BETA1)
print("OLS=%.6f (内生性导致上偏)  IV=%.6f  2SLS=%.6f" % (b_ols, b_iv, b_2sls))
print("IV 与 2SLS 差=%.2e (代数等价)" % abs(b_iv - b_2sls))
print("第一阶段斜率 pi1=%.6f (强工具)" % pi1)
print("弱工具 %d 次: IV 均值=%.4f 标准差=%.4f (偏回 OLS 且方差巨大)" %
      (REPS, statistics.fmean(weak_iv), statistics.pstdev(weak_iv)))
""",
            "把 <code>PI_STRONG</code> 改成 0.05，观察 IV 是否向 OLS 靠拢；把 <code>0.6*u</code> 改成 0（无内生性）看 OLS 是否回到 2。",
            "OLS≈2.29 明显上偏；IV 与 2SLS 都≈1.99 且差在 1e−16 量级；强工具第一阶段斜率≈0.80；弱工具重复抽样下 IV 均值≈2.28 偏向 OLS、标准差≈9.3，方差爆炸。",
            params="0.6 这个系数控制内生性强度；PI 越小工具越弱；N 越大 IV 越接近真值。"),
  ],
  highlights=[("endogeneity", "内生性来源综述"), ("iv", "工具变量条件"),
              ("2sls", "两阶段实现"), ("mixtape", "DID / IV / RDD 的直观教材")],
  pitfalls=["以为样本量能解决内生性：偏误不随 N 消失。",
            "只报告第一阶段显著就宣称 IV 有效：排他性需制度性论证。",
            "忽略弱工具：会使估计偏向 OLS 并让 t 检验失真。"],
  exercises=["推导 <code>plim β̂_OLS − β₁ = Cov(x,u)/Var(x)</code> 并用脚本数值验证。",
             "加入第二个工具做过识别，说明为什么此时能检验（而非证明）排他性。",
             "用 {{ch:20}} 的语言解释 LATE 与 ATE 的差别。"],
  further=["{{ch:20}}　识别与选择偏误", "{{ch:22}}　异方差下的稳健推断", "{{ch:24}}　DID 与固定效应"]),

C("24", "p4", "part4/24-did-panel", "面板与准实验：DID、固定效应与断点回归",
  "没有随机实验时，用时间与个体两个维度的变异构造反事实；每种设计都对应一条可以被检验或反驳的关键假设。",
  hours="4 学时",
  goals=["会计算双重差分估计量并检验平行趋势",
         "实现个体固定效应的组内去均值估计",
         "实现局部线性断点回归并与朴素均值差比较"],
  points=["双重差分", "平行趋势假设", "事件研究与预趋势", "面板数据", "个体固定效应", "组内去均值", "断点回归", "局部随机化与带宽"],
  bridge="把 {{ch:20}} 的识别策略落到三类常用设计；{{ch:25}} 处理时间维度的另一类依赖结构，{{ch:31}} 讨论这些设计的规范报告。",
  analogy="DID 是「差分再差分」，等价于用对照组的变化估计处理组若不处理会怎样；固定效应是给每个个体减去自身均值，把不随时间变化的混杂变量整体消掉；RDD 是只看阈值附近的局部 A/B。",
  sections=[
      ("24.1", "DID：两次差分消掉两类混杂", """<p>两期两组面板：<code>Y_it = α_i + γ_t + τ·(G_i×Post_t) + ε_it</code>。估计量</p>"""
       + eq("τ̂_DID = [Ȳ_{处理,后} − Ȳ_{处理,前}] − [Ȳ_{对照,后} − Ȳ_{对照,前}]")
       + """<p>第一次差分去掉不随时间变的组间差异 <code>α_i</code>，第二次去掉共同时间冲击 <code>γ_t</code>。<strong>关键假设是平行趋势</strong>：若无处理，两组的趋势应相同。它本身不可直接检验（反事实），但可以用处理前的多期数据做<strong>预趋势检验</strong>，或用事件研究图展示各期系数。</p>"""),
      ("24.2", "固定效应：吸收不随时间变的异质性", """<p>设 <code>y_it = α_i + βx_it + u_it</code>，<code>α_i</code> 与 <code>x_it</code> 相关（如企业能力与投入）。对每个个体取组内均值再相减：</p>"""
       + eq("(y_it − ȳ_i) = β(x_it − x̄_i) + (u_it − ū_i)   ⇒ α_i 被消去")
       + """<p>代价：所有不随时间变化的变量（性别、地理）都被吸收，无法估计其系数；且要求 <code>x</code> 在组内<strong>有时间变异</strong>。随机效应模型假设 <code>α_i ⟂ x_it</code>，效率更高但假设更强，Hausman 检验用于在两者间选择。</p>"""),
      ("24.3", "断点回归：阈值附近的局部实验", """<p>处理由连续变量是否越过阈值决定：<code>D=1{X≥c}</code>。若个体无法精确操纵 <code>X</code>，则 <code>c</code> 附近可视为局部随机化。局部线性估计：</p>"""
       + eq("Y = a + b·(X−c) + τ·D + error ,  仅用 |X−c| ≤ h 的样本")
       + """<p><code>b</code> 控制平滑趋势，<code>τ</code> 就是阈值处的跳跃。与朴素均值差相比，它剔除了 <code>X</code> 本身带来的趋势。带宽 <code>h</code> 是偏差-方差权衡：太大引入趋势偏差、太小方差暴涨；需报告带宽敏感性并做操纵检验（密度连续性）。</p>"""),
  ],
  demos=[
      demo("code/24-did-panel.py", "DID、固定效应与局部线性 RDD", r"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 24-did-panel.py | 三种准实验设计（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
N_UNITS, TAU = 4000, 3.0
N_FE_UNITS, T_FE = 600, 4
N_RDD = 20000
BANDWIDTH = 0.3

def mean(v):
    return statistics.fmean(v)

def linfit(xs, ys):
    mx, my = mean(xs), mean(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    b = sum((xs[i] - mx) * (ys[i] - my) for i in range(len(xs))) / sxx
    return my - b * mx, b

# ---- 1. DID：两期两组 ----
rng = random.Random(7)
cells = {(g, t): [] for g in (0, 1) for t in (0, 1)}
trend_cells_pretrend = {(g, t): [] for g in (0, 1) for t in (-1, 0, 1)}
for i in range(N_UNITS):
    a_i = rng.gauss(0, 1)
    g = 1 if i >= N_UNITS // 2 else 0
    for t in (0, 1):
        y = 10 + a_i + 0.5 * t + 1.0 * g + TAU * g * t + rng.gauss(0, 0.5)
        cells[(g, t)].append(y)
    for t in (-1, 0, 1):
        y = 10 + a_i + 0.5 * t + 1.0 * g + (TAU * g * t if t == 1 else 0) + \
            0.8 * g * t + rng.gauss(0, 0.5)
        trend_cells_pretrend[(g, t)].append(y)
m = {k: mean(v) for k, v in cells.items()}
did = (m[(1, 1)] - m[(1, 0)]) - (m[(0, 1)] - m[(0, 0)])
mt = {k: mean(v) for k, v in trend_cells_pretrend.items()}
pre_gap = (mt[(1, 0)] - mt[(1, -1)]) - (mt[(0, 0)] - mt[(0, -1)])
did_bad = (mt[(1, 1)] - mt[(1, 0)]) - (mt[(0, 1)] - mt[(0, 0)])
# ---- 2. 固定效应 ----
rng2 = random.Random(17)
pooled_x, pooled_y, dx, dy = [], [], [], []
for _ in range(N_FE_UNITS):
    a_i = rng2.gauss(0, 1)
    xs = [0.5 * a_i + rng2.gauss(0, 1) for _ in range(T_FE)]
    ys = [a_i + 2.0 * x + rng2.gauss(0, 0.5) for x in xs]
    pooled_x.extend(xs); pooled_y.extend(ys)
    mx, my = mean(xs), mean(ys)
    dx.extend([x - mx for x in xs]); dy.extend([y - my for y in ys])
_, b_pooled = linfit(pooled_x, pooled_y)
b_fe = sum(dx[i] * dy[i] for i in range(len(dx))) / sum(v * v for v in dx)
# ---- 3. RDD：局部线性 ----
rng3 = random.Random(31)
x_all, y_all, x_l, y_l, x_r, y_r = [], [], [], [], [], []
for _ in range(N_RDD):
    xv = rng3.uniform(-1, 1)
    d = 1 if xv >= 0 else 0
    yv = 0.5 * xv + TAU * d + rng3.gauss(0, 0.5)
    x_all.append(xv); y_all.append(yv)
    if abs(xv) <= BANDWIDTH:
        (x_l if xv < 0 else x_r).append(xv)
        (y_l if xv < 0 else y_r).append(yv)
naive = mean([y_all[i] for i in range(N_RDD) if x_all[i] >= 0]) - \
        mean([y_all[i] for i in range(N_RDD) if x_all[i] < 0])
a_l, b_l = linfit(x_l, y_l)
a_r, b_r = linfit(x_r, y_r)
rdd = a_r - a_l
# ---- 数值验证：打印可手算核对的量 ----
print("真实处理效应 tau=%.2f" % TAU)
print("DID(平行趋势成立)=%.4f" % did)
print("预趋势差分=%.4f (显著非 0 说明违背平行趋势)" % pre_gap)
print("DID(存在 0.8 差别趋势)=%.4f (被推离真值)" % did_bad)
print("固定效应: 混合 OLS beta=%.4f (上偏)  组内去均值 beta=%.4f (真值 2)" %
      (b_pooled, b_fe))
print("RDD: 朴素均值差=%.4f (含 0.5x 趋势) 局部线性跳跃=%.4f" % (naive, rdd))
print("带宽内样本: 左=%d 右=%d" % (len(x_l), len(x_r)))
""",
            "把 <code>0.8*g*t</code> 改成 0，观察预趋势差分是否归零、DID 是否回到 3；把 <code>BANDWIDTH</code> 改成 0.05 看 RDD 方差如何变化。",
            "DID≈3.0；加入差别趋势后预趋势差分≈0.8 且 DID≈3.8；混合 OLS 系数明显大于 2，组内去均值≈2；RDD 朴素均值差≈3.5（混入趋势），局部线性跳跃≈3.0。",
            params="N_UNITS/N_RDD 控制抽样误差；BANDWIDTH 是 RDD 的偏差-方差权衡；差别趋势系数直接决定 DID 偏误。"),
  ],
  highlights=[("did", "双重差分的标准设定"), ("parallel-trends", "关键识别假设"),
              ("fixed-effects", "固定效应与随机效应"), ("rdd", "断点回归设计")],
  pitfalls=["只报告 DID 点估计不报告预趋势：平行趋势才是识别的核心。",
            "把固定效应理解为「控制了所有变量」：它只吸收不随时间变化的成分。",
            "RDD 用全样本做均值差：阈值外的趋势会伪装成处理效应。"],
  exercises=["把 DID 扩展成多期事件研究，画出各期系数并解释领先项。",
             "在固定效应 DGP 里加入随时间变化的遗漏变量，观察 FE 是否仍一致。",
             "扫描 RDD 带宽 0.05～0.8，画 τ̂ 与标准误的权衡曲线。"],
  further=["{{ch:20}}　反事实与识别假设", "{{ch:23}}　IV 作为另一类设计", "{{ch:31}}　预注册与稳健性报告"]),

C("25", "p4", "part4/25-time-series", "时间序列：平稳性、单位根与伪回归",
  "时间观测不独立：均值方差是否随时间漂移、序列之间是否共享趋势，决定回归推断是否有效。",
  hours="3 学时",
  goals=["能区分平稳 AR(1) 与随机游走，并计算理论方差与自相关",
         "用蒙特卡洛复现伪回归：两个独立随机 walk 也会「显著相关」",
         "理解差分、协整与误差修正模型的关系"],
  points=["平稳性", "AR(1) 与自相关", "随机游走与单位根", "伪回归", "差分与去趋势", "协整", "误差修正模型", "ADF 检验思想"],
  bridge="把 {{ch:22}} 的序列相关诊断升级成建模对象；{{ch:26}} 的收益序列、{{ch:18}} 的增长收敛回归都依赖本章的平稳性判断。",
  analogy="平稳序列像有界噪声，统计量收敛；随机游走像积分器，方差随时间线性增长，任何固定窗口的均值都没有稳定含义。两条独立随机游走都带趋势，回归会把共同趋势误读成关系。",
  sections=[
      ("25.1", "平稳、AR(1) 与单位根", """<p>AR(1)：<code>x_t = φx_{t−1} + ε_t</code>。当 <code>|φ|&lt;1</code> 时平稳，</p>"""
       + eq("E[x]=0 , Var(x)=σ²/(1−φ²) , ρ_k = φ^k  ;  φ=1 即随机游走，Var(x_t)=tσ²")
       + """<p>单位根过程差分后平稳（I(1)→I(0)）；ADF 检验本质是检验差分方程里 <code>x_{t−1}</code> 的系数是否为 0，但其临界值非标准，不能直接套 t 分布。<strong>把趋势当成水平、或把水平当趋势</strong>，是宏观实证最常见的错误。</p>"""),
      ("25.2", "伪回归：共同趋势制造的虚假显著", """<p>Granger–Newbold 的经典结果：两条<strong>相互独立</strong>的随机游走做回归，R² 与 t 值往往很大，且 t 值随样本量增大而发散，因为残差本身非平稳，通常的 t 检验前提被破坏。判断办法：</p>"""
       + table(["检查", "期望结果", "若不满足"], [
           ["残差是否平稳", "ADF 拒绝单位根 / DW 不接近 0", "可能是伪回归"],
           ["加趋势项后系数", "仍稳定", "系数由共同趋势驱动"],
           ["差分后再回归", "关系应消失", "说明原关系是伪的"],
       ], ["28%", "34%", "38%"])
       + """<p>脚本用数百次重复抽样把「假阳性率远超 5%」量化出来，比任何一句「相关不等于因果」都更有说服力。</p>"""),
      ("25.3", "协整：非平稳但存在长期均衡", """<p>若 <code>y_t</code> 与 <code>x_t</code> 都是 I(1)，但存在 β 使 <code>y_t − βx_t</code> 平稳，则称二者<strong>协整</strong>。此时水平回归不是伪回归，且可用<strong>误差修正模型</strong>同时刻画长期均衡与短期调整：</p>"""
       + eq("Δy_t = α(y_{t−1} − βx_{t−1}) + γΔx_t + ε_t ,  α<0 表示向均衡回调")
       + """<p>这是 {{ch:19}} 的 PPP、{{ch:17}} 的利率期限关系与 {{ch:28}} 因子回归在实证中的标准处理流程：先判单整阶数 → 再判协整 → 最后定动态模型。</p>"""),
  ],
  demos=[
      demo("code/25-timeseries.py", "AR(1)、随机游走、伪回归与协整残差", r"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 25-timeseries.py | 平稳性与伪回归蒙特卡洛（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
T, REPS = 200, 400
PHI = 0.8
SIGMA = 1.0
BETA_COINT = 2.0

def mean(v):
    return statistics.fmean(v)

def lag1_corr(v):
    a, b = v[:-1], v[1:]
    ma, mb = mean(a), mean(b)
    num = sum((a[i] - ma) * (b[i] - mb) for i in range(len(a)))
    den = math.sqrt(sum((x - ma) ** 2 for x in a) * sum((x - mb) ** 2 for x in b))
    return num / den

def ols1(xs, ys):
    mx, my = mean(xs), mean(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    b = sum((xs[i] - mx) * (ys[i] - my) for i in range(len(xs))) / sxx
    a = my - b * mx
    e = [ys[i] - a - b * xs[i] for i in range(len(xs))]
    s2 = sum(v * v for v in e) / (len(xs) - 2)
    se = math.sqrt(s2 / sxx)
    tss = sum((y - my) ** 2 for y in ys)
    r2 = 1 - sum(v * v for v in e) / tss
    return b, b / se, r2, e

def random_walk(rng, t):
    v, out = 0.0, []
    for _ in range(t):
        v += rng.gauss(0, SIGMA)
        out.append(v)
    return out
# ---- 平稳 AR(1) ----
rng = random.Random(7)
x, ar = 0.0, []
for _ in range(10000):
    x = PHI * x + rng.gauss(0, SIGMA)
    ar.append(x)
# ---- 伪回归蒙特卡洛 ----
mc = random.Random(23)
false_pos, r2_list = 0, []
for _ in range(REPS):
    xx, yy = random_walk(mc, T), random_walk(mc, T)
    b, t, r2, e = ols1(xx, yy)
    if abs(t) > 1.96:
        false_pos += 1
    r2_list.append(r2)
# ---- 协整：y = 2x + 平稳噪声 ----
coint = random.Random(31)
xc, yc = 0.0, []
xc_path = []
for _ in range(T):
    xc += coint.gauss(0, SIGMA)
    xc_path.append(xc)
    yc.append(BETA_COINT * xc + coint.gauss(0, 0.5))
_, _, _, ec = ols1(xc_path, yc)
# ---- 数值验证：打印可手算核对的量 ----
print("AR(1): 理论方差=%.4f 样本方差=%.4f" %
      (SIGMA ** 2 / (1 - PHI ** 2), statistics.pvariance(ar)))
print("AR(1): 理论 lag1 自相关=%.4f 样本=%.4f" % (PHI, lag1_corr(ar)))
print("伪回归 %d 次(两条独立随机游走): |t|>1.96 比例=%.4f 平均 R²=%.4f" %
      (REPS, false_pos / REPS, mean(r2_list)))
print("协整回归残差 lag1 自相关=%.4f (平稳残差应远小于 1)" % lag1_corr(ec))
print("对照: 水平序列自相关≈%.4f" % lag1_corr(yc))
""",
            "把回归改成对两条序列先做一阶差分再 OLS，观察伪回归的假阳性率是否回到 0.05 附近。",
            "AR(1) 理论方差≈2.778、样本≈2.67，lag1 自相关≈0.79；400 次伪回归的 |t|>1.96 比例≈0.825、平均 R²≈0.225（两条序列其实完全独立）；协整回归残差 lag1 自相关≈−0.01，而原水平序列≈0.99。",
            params="PHI 越接近 1，AR(1) 方差越大；T 越大伪回归假阳性越严重；REPS 控制蒙特卡洛精度。"),
  ],
  highlights=[("stationarity", "平稳性的定义"), ("unit-root", "单位根与检验"),
              ("spurious", "伪回归的经典结果"), ("cointegration", "协整与误差修正")],
  pitfalls=["对非平稳水平序列直接套 t 检验：残差非平稳时标准 t 分布失效。",
            "把高 R² 当成关系存在的证据：伪回归能给出很高 R²。",
            "见到两条序列同向就断言协整：需检验残差是否平稳。"],
  exercises=["对两条随机游走先差分再回归，验证假阳性率回到约 0.05。",
             "实现 ADF 检验的回归部分，说明为什么临界值不能用标准 t 表。",
             "用 {{ch:19}} 的 PPP 数据设计一个协整检验流程。"],
  further=["{{ch:18}}　增长收敛回归中的平稳性", "{{ch:22}}　序列相关诊断", "{{ch:26}}　收益序列的平稳建模"]),
]

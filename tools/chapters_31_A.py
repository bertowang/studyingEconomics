#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""方法论篇 31-32 与附录 A：复现规范、端到端课题、速查表。"""
from book_schema import C, demo, eq, table

CH = [

C("31", "p6", "part6/31-reproducibility", "复现、多重检验与研究规范",
  "把「显著性」放回抽样分布的语境：反复试设定、反复看数据、只汇报成功的一次，都会让假阳性率远远超过 5%。",
  hours="3 学时",
  goals=["会用蒙特卡洛量化 p-hacking 与多重检验造成的假阳性膨胀",
         "理解 Bonferroni / FDR 校正与预注册的作用",
         "能列出一份可复现研究的最小清单"],
  points=["p 值的正确含义", "多重检验与假阳性", "p-hacking 与花园分叉路径", "Bonferroni 校正", "FDR 与 BH 过程", "预注册与分析计划", "功效分析", "可复现清单"],
  bridge="把 {{ch:02}} 的覆盖率、{{ch:22}} 的设定搜索、{{ch:28}} 的因子动物园收口成一套研究规范；{{ch:32}} 用它来约束一个完整课题。",
  analogy="每次额外尝试都是一次新的单元测试，但如果你只在失败后改断言、并且只汇报最后一次通过的结果，测试套件就失去了意义；预注册相当于把断言在跑之前先写死。",
  sections=[
      ("31.1", "p 值不是结论为真的概率", """<p><code>p = P(观测到当前或更极端结果 | H₀ 为真)</code>。它不回答「H₀ 为真的概率」，也不回答「效应有多大」。在 5% 阈值下重复 20 次独立检验，至少一次假阳性的概率是</p>"""
       + eq("P(至少一次假阳性) = 1 − (1−0.05)^20 ≈ 0.6415")
       + """<p>「花园分叉路径」更隐蔽：不同控制变量、样本窗口、变量变换、剔除规则都算一次尝试，即使研究者没有恶意，最终汇报的那条路径也是被结果选出来的。</p>"""),
      ("31.2", "校正、功效与预注册", """<p><strong>Bonferroni</strong> 把阈值改为 <code>α/m</code>，控制家族错误率（FWER），但保守、降低功效。<strong>Benjamini–Hochberg</strong> 控制错误发现率（FDR），在高维因子筛选中更常用。另一条路是<strong>预注册</strong>：先固定假设、主设定、样本与排除规则，再跑数据，把探索性分析与验证性分析明确分开。</p>
<p>还要做<strong>功效分析</strong>：真实效应 δ、样本量 n、噪声 σ 决定 <code>z ≈ δ√n/σ</code>；低功效研究即使显著，效应量也常被高估（赢家诅咒）。这与 {{ch:21}} 的标准误、{{ch:23}} 的弱工具在数学上是同一件事：<strong>信息量不足时，条件在「显著」上的估计必然偏大</strong>。</p>"""),
      ("31.3", "最小可复现清单", """<table><thead><tr><th style="width:26%">项目</th><th>具体要求</th><th>本书对应</th></tr></thead><tbody>
<tr><td>数据与 DGP</td><td>数据来源、单位、清洗规则；合成数据固定种子</td><td>全书 <code>random.seed(7)</code></td></tr>
<tr><td>代码</td><td>版本、依赖、一键运行脚本、输出可核对数值</td><td><code>tools/run_python.sh</code></td></tr>
<tr><td>设定</td><td>主设定与全部稳健性设定都报告</td><td>{{ch:32}} 研究日志</td></tr>
<tr><td>推断</td><td>标准误类型、多重检验处理、置信区间</td><td>{{ch:22}}、本章</td></tr>
<tr><td>边界</td><td>外部效度、识别假设、卢卡斯批判</td><td>{{ch:20}}</td></tr>
</tbody></table>"""),
  ],
  demos=[
      demo("code/31-reproducibility.py", "p-hacking、Bonferroni 与功效分析", r"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 31-reproducibility.py | 多重检验的蒙特卡洛（只用标准库）
import math, random, statistics
from statistics import NormalDist
random.seed(7)
# ---- 参数区 ----
N, M_TESTS, REPS = 100, 20, 1000
ALPHA = 0.05
TRUE_EFFECT = 0.3

def norm_sf(x):
    return 0.5 * (1 - math.erf(abs(x) / math.sqrt(2)))

def p_from_t(t):
    return 2 * norm_sf(t)

def mean(v):
    return statistics.fmean(v)

def t_stat(xs, ys):
    mx, my = mean(xs), mean(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    b = sum((xs[i] - mx) * (ys[i] - my) for i in range(len(xs))) / sxx
    e = [ys[i] - my - b * (xs[i] - mx) for i in range(len(xs))]
    s2 = sum(v * v for v in e) / (len(xs) - 2)
    return b / math.sqrt(s2 / sxx)

# ---- t 分布临界值（Cornish-Fisher 一阶修正，df=N-2）----
df = N - 2
def t_crit(alpha):
    z = NormalDist().inv_cdf(1 - alpha / 2)
    return z + (z ** 3 + z) / (4 * df)
crit05 = t_crit(ALPHA)
crit_bonf = t_crit(ALPHA / M_TESTS)
# ---- 原假设为真：20 个候选解释变量都与 y 无关 ----
rng = random.Random(7)
raw, corrected, minp_sum = 0, 0, 0.0
for _ in range(REPS):
    y = [rng.gauss(0, 1) for _ in range(N)]
    ts = []
    for _ in range(M_TESTS):
        x = [rng.gauss(0, 1) for _ in range(N)]
        ts.append(abs(t_stat(x, y)))
    maxt = max(ts)
    minp_sum += p_from_t(maxt)
    if maxt > crit05:
        raw += 1
    if maxt > crit_bonf:
        corrected += 1
# ---- 真实效应下的功效 ----
power_rng = random.Random(19)
hits = 0
for _ in range(REPS):
    x = [power_rng.gauss(0, 1) for _ in range(N)]
    y = [TRUE_EFFECT * x[i] + power_rng.gauss(0, 1) for i in range(N)]
    if abs(t_stat(x, y)) > crit05:
        hits += 1
theory = 1 - (1 - ALPHA) ** M_TESTS
# ---- 数值验证：打印可手算核对的量 ----
print("临界值: t(0.975,df=%d)≈%.4f  Bonferroni 对应≈%.4f" % (df, crit05, crit_bonf))
print("单次检验 alpha=%.2f, m=%d, 独立检验至少一次假阳性理论=%.4f" %
      (ALPHA, M_TESTS, theory))
print("蒙特卡洛 %d 次: 未校正假阳性率=%.4f (最小 p 平均=%.4f)" %
      (REPS, raw / REPS, minp_sum / REPS))
print("Bonferroni 阈值=%.6f 校正后假阳性率=%.4f" %
      (ALPHA / M_TESTS, corrected / REPS))
print("真实效应 delta=%.2f, n=%d 时检出率(功效)=%.4f" %
      (TRUE_EFFECT, N, hits / REPS))
print("理论 z≈delta*sqrt(n)/sigma=%.4f" % (TRUE_EFFECT * math.sqrt(N)))
""",
            "把 <code>M_TESTS</code> 改成 1、5、20，观察假阳性率如何随尝试次数上升；把 <code>TRUE_EFFECT</code> 改成 0.1 看功效下降。",
            "df=98 时 t 临界值≈1.984；m=20 的理论假阳性率≈0.6415，未校正模拟≈0.68（多次检验共享同一 y，略有相关）；Bonferroni 阈值 0.0025 后≈0.034（略保守）；δ=0.3、n=100 时功效≈0.83（理论 z≈3）。",
            params="M_TESTS 越大假阳性越严重；TRUE_EFFECT 或 N 越小功效越低；ALPHA 决定整条曲线。"),
  ],
  highlights=[("phacking", "p-hacking 与数据疏浚"), ("multiple-testing", "多重比较问题"),
              ("replication", "复现危机与研究规范"), ("repec", "检索已发表研究与复现材料")],
  pitfalls=["把 p&lt;0.05 当成「效应为真」的概率：它只描述原假设下的尾部概率。",
            "只汇报最终设定：探索过程中的每一次尝试都应披露或预注册。",
            "忽略功效：低功效研究的显著效应量往往被严重高估。"],
  exercises=["实现 Benjamini–Hochberg 过程并与 Bonferroni 的拒绝数比较。",
             "模拟「边收数据边看 p 值」的 optional stopping，量化假阳性膨胀。",
             "为 {{ch:28}} 的因子筛选写一份预注册分析计划。"],
  further=["{{ch:02}}　覆盖率的频率学含义", "{{ch:22}}　设定搜索与诊断", "{{ch:32}}　端到端研究日志"]),

C("32", "p6", "part6/32-capstone", "综合课题：一项政策评估从数据到结论",
  "把全书环节拼成一条流水线：DGP → 描述与平衡 → 识别策略 → 估计 → 稳健性 → 边界 → 可复现报告。",
  hours="4 学时",
  goals=["能独立写出一个合成面板的 DGP 与数据字典",
         "会依次完成 DID、预趋势、安慰剂、稳健标准误与敏感性分析",
         "能把识别假设、卢卡斯批判与外部效度写进结论"],
  points=["研究问题与 estimand", "数据字典与 DGP", "描述统计与平衡检验", "DID 识别", "事件研究与预趋势", "安慰剂检验", "稳健标准误", "敏感性分析", "外部效度与卢卡斯批判"],
  bridge="收口全书：{{ch:20}} 的识别、{{ch:21}}～{{ch:25}} 的估计与诊断、{{ch:31}} 的规范，在一次完整的政策评估里同时出场。",
  analogy="这是一份端到端的「可复现实验报告」：数据生成是测试夹具，主估计是主断言，稳健性与安慰剂是对照实验，结论部分是适用范围与已知限制。",
  sections=[
      ("32.1", "研究问题与 estimand", """<p>问题：某地区在第 5 期提高最低工资，是否影响就业？目标参数 <code>ATT</code>：受政策影响地区在政策后的平均处理效应。先明确<strong>处理单位、时间、结果变量与反事实</strong>，再谈用什么估计量；把「显著/不显著」当研究目标是最常见的本末倒置。</p>
<p>反事实由未受影响地区构造，识别假设是<strong>平行趋势</strong>（{{ch:24}}）：若无政策，两组就业趋势应相同。这个假设不能直接检验，但可以用处理前多期数据、安慰剂与敏感性分析来「证伪」。</p>"""),
      ("32.2", "端到端流水线", """<table><thead><tr><th style="width:18%">步骤</th><th>输出物</th><th>对应章节</th></tr></thead><tbody>
<tr><td>1 数据字典</td><td>单位、频率、变量定义、缺失与排除规则</td><td>{{ch:15}}</td></tr>
<tr><td>2 描述与平衡</td><td>分组均值、处理前协变量差异</td><td>{{ch:02}}</td></tr>
<tr><td>3 主估计</td><td>DID 点估计 + 置信区间</td><td>{{ch:24}}</td></tr>
<tr><td>4 识别检验</td><td>事件研究图、预趋势、安慰剂</td><td>{{ch:24}}、{{ch:31}}</td></tr>
<tr><td>5 推断</td><td>地区层面聚类的稳健标准误</td><td>{{ch:22}}</td></tr>
<tr><td>6 稳健性</td><td>换对照组、换窗口、加控制变量</td><td>{{ch:31}}</td></tr>
<tr><td>7 结论</td><td>效应量、识别假设、外部效度、卢卡斯批判</td><td>{{ch:20}}</td></tr>
</tbody></table>"""),
      ("32.3", "结论该怎么写", """<p>一份合格的结论至少包含四句话：<strong>估计量是什么</strong>（ATT 而非「相关」）、<strong>点估计与区间是多少</strong>、<strong>识别假设及其证据有多强</strong>、<strong>结论能外推到哪里</strong>。还要主动说明：政策可能改变企业行为方式（卢卡斯批判）、处理效应可能异质、合成数据只用于验证流水线而非回答真实政策问题。</p>
<div class="card tip"><p style="margin-bottom:0"><strong>给程序员的最后一条建议</strong>：把「模型 → 数据 → 估计 → 检验 → 报告」写成一条可重跑的 pipeline，把每次改动的参数、种子、输出都留在日志里。这样当结论变化时，你能定位到是假设变了、数据变了，还是代码变了——这正是全书反复强调的<strong>可复现性</strong>。</p></div>"""),
  ],
  demos=[
      demo("code/32-capstone.py", "端到端政策评估：DID、预趋势、安慰剂与稳健推断", r"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 32-capstone.py | 综合课题：合成地区面板的政策评估（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
N_REGIONS, T_PERIODS = 200, 8
TREAT_START = 4                  # 第 5 期开始处理（0 起索引）
TRUE_TAU = -0.4                  # 对 log 就业的真实 ATT
GROUP_DIFF, TIME_TREND = 0.10, 0.03
BETA_X = 0.2
NOISE_SD = 0.15

def mean(v):
    return statistics.fmean(v)

# ---- 1. DGP: 地区固定效应 + 共同趋势 + 组间差异 + 政策效应 ----
rng = random.Random(7)
panel = []
for i in range(N_REGIONS):
    a_i = rng.gauss(0, 0.3)
    g = 1 if i >= N_REGIONS // 2 else 0
    for t in range(T_PERIODS):
        post = 1 if t >= TREAT_START else 0
        x_it = rng.gauss(0, 1)
        y = (2.0 + a_i + TIME_TREND * t + GROUP_DIFF * g +
             TRUE_TAU * g * post + BETA_X * x_it + rng.gauss(0, NOISE_SD))
        panel.append((i, t, g, post, x_it, y))
# ---- 2. 描述与处理前平衡 ----
x_pre_t = mean([r[4] for r in panel if r[1] < TREAT_START and r[2] == 1])
x_pre_c = mean([r[4] for r in panel if r[1] < TREAT_START and r[2] == 0])
# ---- 3. 主估计：按地区求前后差，再比较两组（地区层面聚类稳健）----
delta_t, delta_c = [], []
for i in range(N_REGIONS):
    pre = mean([r[5] for r in panel if r[0] == i and r[1] < TREAT_START])
    post = mean([r[5] for r in panel if r[0] == i and r[1] >= TREAT_START])
    (delta_t if i >= N_REGIONS // 2 else delta_c).append(post - pre)
did = mean(delta_t) - mean(delta_c)
se = math.sqrt(statistics.variance(delta_t) / len(delta_t) +
               statistics.variance(delta_c) / len(delta_c))
ci = (did - 1.96 * se, did + 1.96 * se)
# ---- 4. 事件研究：各期组间差减去处理前基准 ----
def group_diff(t):
    return (mean([r[5] for r in panel if r[1] == t and r[2] == 1]) -
            mean([r[5] for r in panel if r[1] == t and r[2] == 0]))
base = mean([group_diff(t) for t in range(TREAT_START)])
event = [group_diff(t) - base for t in range(T_PERIODS)]
pre_trend = mean(event[:TREAT_START])
# ---- 5. 安慰剂：处理前随机指派「假处理组」，做随机化推断 ----
fake = 2
pre_delta = []
for i in range(N_REGIONS):
    p0 = mean([r[5] for r in panel if r[0] == i and r[1] < fake])
    p1 = mean([r[5] for r in panel if r[0] == i and fake <= r[1] < TREAT_START])
    pre_delta.append(p1 - p0)
placebo_rng = random.Random(31)
placebos = []
for _ in range(500):
    idx = placebo_rng.sample(range(N_REGIONS), N_REGIONS // 2)
    s = set(idx)
    a = mean([pre_delta[i] for i in idx])
    b = mean([pre_delta[i] for i in range(N_REGIONS) if i not in s])
    placebos.append(a - b)
placebo = mean(placebos)
placebo_sd = statistics.pstdev(placebos)
p_ri = sum(1 for v in placebos if abs(v) >= abs(did)) / len(placebos)
# ---- 6. 朴素横截面差（对照：会被组间差异污染）----
naive = mean([r[5] for r in panel if r[1] >= TREAT_START and r[2] == 1]) - \
        mean([r[5] for r in panel if r[1] >= TREAT_START and r[2] == 0])
# ---- 数值验证：打印可手算核对的量 ----
print("真实 ATT=%.4f  地区=%d 期数=%d 政策起点 t=%d" %
      (TRUE_TAU, N_REGIONS, T_PERIODS, TREAT_START))
print("[描述] 处理前协变量均值: 处理组=%.4f 对照组=%.4f 差=%.4f" %
      (x_pre_t, x_pre_c, x_pre_t - x_pre_c))
print("[估计] DID=%.4f  稳健 se=%.4f  95%%CI=[%.4f, %.4f]" % (did, se, ci[0], ci[1]))
print("[识别] 事件研究处理前平均系数=%.4f (应≈0)" % pre_trend)
print("[识别] 政策前各期系数: " + " ".join("%.3f" % v for v in event[:TREAT_START]))
print("[识别] 政策后各期系数: " + " ".join("%.3f" % v for v in event[TREAT_START:]))
print("[安慰剂] 随机假处理组 500 次: 均值=%.4f 标准差=%.4f" % (placebo, placebo_sd))
print("[安慰剂] 随机化推断 p=%.4f (无假政策能产生 |DID|≥%.4f)" % (p_ri, abs(did)))
print("[对照] 朴素横截面差=%.4f (混入组间差异 %.2f，偏误明显)" %
      (naive, GROUP_DIFF))
print("[结论] 估计 %.4f 与真值 %.4f 相差 %.4f；识别依赖平行趋势，外推需谨慎" %
      (did, TRUE_TAU, did - TRUE_TAU))
""",
            "把 <code>GROUP_DIFF</code> 改成 0.5，观察朴素横截面差如何被污染而 DID 仍接近真值；把 <code>TRUE_TAU</code> 改成 0 看安慰剂与功效。",
            "真实 ATT=−0.4；处理前协变量近似平衡；DID≈−0.4、稳健 se≈0.026，95% 区间覆盖真值；事件研究处理前系数≈0、政策后≈−0.4；随机假处理组安慰剂均值≈0 且随机化推断 p≈0；朴素横截面差混入 0.10 的组间差异而明显偏离。",
            params="N_REGIONS 越大 se 越小；NOISE_SD 越大区间越宽；TRUE_TAU=0 时可检验假阳性率。"),
  ],
  highlights=[("causal-book", "完整的因果推断实战教材"), ("statsmodels", "把流水线换成工业实现"),
              ("fred", "真实宏观/地区面板数据"), ("core-econ", "全书系统视角的起点")],
  pitfalls=["先跑回归再想 estimand：不知道估计什么参数，显著性没有意义。",
            "把合成数据的结论当真实政策结论：合成数据只验证流水线是否可靠。",
            "只报告主估计：没有预趋势、安慰剂与稳健性，识别假设就无从判断。"],
  exercises=["把地区固定效应改成与协变量相关的形式，观察 DID 是否仍一致。",
             "加入处理效应异质性，讨论 ATT 与 ATE 的差别（联系 {{ch:20}}）。",
             "把全部设定写成命令行参数，实现一条一键重跑的 pipeline。"],
  further=["{{ch:20}}　识别与反事实", "{{ch:24}}　DID 与事件研究", "{{ch:31}}　预注册与稳健性报告", "{{home#toc}}　全书目录"]),

C("A", "pa", "appendix", "速查与资源总表",
  "符号、公式、脚本索引、常见坑、术语对照与全部扩展学习链接，供随时查阅。",
  hours="随查随用",
  goals=["能快速查到某个公式、符号或脚本的位置",
         "知道手写实现与工业库的对应关系",
         "能按主题找到该读的教材、课程、数据与工具"],
  points=["符号与约定", "公式速查", "章节脚本索引", "手写实现与工业库对照", "常见坑清单", "数据字典模板", "扩展学习链接总表", "中英术语对照"],
  bridge="全书查表入口：任何一章遇到符号、公式或参考链接，都回到这里。",
  analogy="附录是项目的 README + API reference：A.3 是公式索引，A.5 是代码索引，A.7 是外部依赖清单。",
  sections=[
      ("A.1", "符号与阅读约定", """<p>价格 <code>p</code>、数量 <code>q</code>、效用 <code>u</code>、成本 <code>C</code>、产出 <code>Y</code>；随机变量大写、实现值小写；<code>β</code> 为真实参数、<code>β̂</code> 为估计量；<code>ln</code> 为自然对数；<code>E[·]</code>、<code>Var(·)</code>、<code>Cov(·,·)</code> 为期望、方差与协方差。</p>
<p>公式一律写成纯文本 Unicode（如 <code>α</code>、<code>σ²</code>、<code>Σ</code>），不依赖 MathJax，断网也能读；代码块右上角可一键复制，磁盘上的 <code>code/*.py</code> 与页面由 <code>tools/extract_code.py</code> 自动同步。</p>"""),
      ("A.2", "学习路线与最短路径", """<ol class="roadmap">
<li><strong>打底</strong>（00～02）：主线、约束最优化、概率与模拟。</li>
<li><strong>微观</strong>（03～14）：选择 → 均衡 → 福利 → 失灵 → 一般均衡。</li>
<li><strong>宏观</strong>（15～19）：核算 → 短期波动 → 政策 → 增长 → 开放。</li>
<li><strong>计量</strong>（20～25）：识别 → OLS → 诊断 → IV → DID → 时间序列。</li>
<li><strong>投资</strong>（26～30）：收益 → 组合 → 因子 → 债券 → 期权。</li>
<li><strong>综合</strong>（31～32）：研究规范与端到端课题。</li>
</ol>
<p>时间有限的最短路径：{{ch:01}} → {{ch:04}} → {{ch:09}} → {{ch:20}} → {{ch:21}} → {{ch:24}} → {{ch:27}} → {{ch:30}} → {{ch:32}}。</p>"""),
      ("A.3", "核心公式速查", """<table><thead><tr><th style="width:22%">主题</th><th>公式</th><th>章节</th></tr></thead><tbody>
<tr><td>约束最优</td><td>∂f/∂x = λ·∂g/∂x；λ 为影子价格</td><td>01</td></tr>
<tr><td>供需均衡</td><td>p*=(a−c)/(b+d)；ε=(dQ/dp)(p/Q)</td><td>04</td></tr>
<tr><td>税负归宿</td><td>消费者份额 = d/(b+d)；DWL=½·t·ΔQ</td><td>04</td></tr>
<tr><td>消费者需求</td><td>x*=αB/pₓ；e(p,u)=u·(pₓ/α)^α(pᵧ/(1−α))^(1−α)</td><td>05</td></tr>
<tr><td>利润最大</td><td>p·MP_L=w ⇔ p=MC；MR=a−2bQ</td><td>06、10</td></tr>
<tr><td>现值 / 欧拉</td><td>PV=ΣC_t/(1+r)^t；u'(c₁)=β(1+r)u'(c₂)</td><td>08、29</td></tr>
<tr><td>风险</td><td>CE=u⁻¹(E[u(w)])；RP=E[w]−CE；勒纳=(p−MC)/p=−1/ε</td><td>08、10</td></tr>
<tr><td>福利</td><td>TS=∫[p_d(q)−p_s(q)]dq；ΣMRS=MRT（公共品）</td><td>09、12</td></tr>
<tr><td>古诺</td><td>q*=(a−c)/(3b)；Q_垄断 &lt; Q_古诺 &lt; Q_竞争</td><td>11</td></tr>
<tr><td>一般均衡</td><td>p·z(p)≡0；只解 n−1 个市场</td><td>14</td></tr>
<tr><td>核算</td><td>Y=C+I+G+NX；NX=S−I；平减指数=名义/实际</td><td>15、19</td></tr>
<tr><td>乘数 / IS-LM</td><td>1/(1−c)；Y=[A+d(M/P)/h]/[(1−c)+dk/h]</td><td>16</td></tr>
<tr><td>政策 / 增长</td><td>i≈r+πᵉ；i*=r*+π+0.5(π−π*)+0.5y；k*=(sA/δ)^(1/(1−α))</td><td>17、18</td></tr>
<tr><td>利率平价</td><td>F=S(1+i)/(1+i*)；ε=e·P*/P</td><td>19</td></tr>
<tr><td>识别</td><td>组间差 = ATT + 选择偏误；β̂_IV=Cov(z,y)/Cov(z,x)</td><td>20、23</td></tr>
<tr><td>OLS</td><td>β̂=(XᵀX)⁻¹Xᵀy；Var(β̂)=σ²(XᵀX)⁻¹；HC0 三明治</td><td>21、22</td></tr>
<tr><td>DID / FE</td><td>τ̂=Δ处理−Δ对照；组内去均值消掉 α_i</td><td>24</td></tr>
<tr><td>时间序列</td><td>Var(x)=σ²/(1−φ²)；ρ_k=φ^k；DW≈2(1−ρ)</td><td>25</td></tr>
<tr><td>收益 / 组合</td><td>g=E[r]−½σ²；σ_p²=w²σ₁²+(1−w)²σ₂²+2w(1−w)ρσ₁σ₂</td><td>26、27</td></tr>
<tr><td>CAPM / 久期</td><td>E[r_i]−r_f=β_i(E[r_m]−r_f)；D_mod=−(1/P)∂P/∂y</td><td>28、29</td></tr>
<tr><td>期权</td><td>p=(e^{rΔt}−d)/(u−d)；C=S·N(d₁)−K·e^{−rT}N(d₂)；C−P=S−K·e^{−rT}</td><td>30</td></tr>
</tbody></table>"""),
      ("A.4", "常见坑清单", """<div class="card warn"><ul style="margin-bottom:0">
<li>把恒等式当行为方程（{{ch:15}}）、把相关当因果（{{ch:20}}）、把拟合优度当识别（{{ch:21}}）。</li>
<li>用名义利率判断货币松紧（{{ch:17}}）、用 CPI 当平减指数（{{ch:15}}）、用算术平均当长期增长率（{{ch:26}}）。</li>
<li>把 R² 高的伪回归当发现（{{ch:25}}）、把 α 显著当能力（{{ch:28}}）、把未校正的 p 值当证据（{{ch:31}}）。</li>
<li>把风险中性概率当真实概率（{{ch:30}}）、把模型内的反事实直接外推到政策变化后（{{ch:20}} 卢卡斯批判）。</li>
</ul></div>"""),
      ("A.6", "数据字典与复现清单模板", """<table><thead><tr><th style="width:24%">字段</th><th>填写内容</th></tr></thead><tbody>
<tr><td>数据来源</td><td>URL、下载日期、版本号、许可证</td></tr>
<tr><td>观测单位</td><td>个体/企业/地区 × 时间频率</td></tr>
<tr><td>变量定义</td><td>名称、单位、是否季节调整、名义/实际、基期</td></tr>
<tr><td>清洗规则</td><td>缺失、异常值、缩尾、排除条件（<strong>事前固定</strong>）</td></tr>
<tr><td>随机性</td><td><code>random.seed(7)</code>、重复次数、并行是否影响顺序</td></tr>
<tr><td>环境</td><td>Python 版本、依赖清单、一键运行命令</td></tr>
<tr><td>输出</td><td>可手算核对的数值、主表与全部稳健性表</td></tr>
</tbody></table>
<p>把这张表随项目一起提交，比事后回忆「当时是不是删过几个异常值」可靠得多。</p>"""),
      ("A.8", "中英术语对照", """<table><thead><tr><th style="width:34%">中文</th><th>英文</th><th style="width:34%">中文</th><th>英文</th></tr></thead><tbody>
<tr><td>机会成本</td><td>opportunity cost</td><td>一般均衡</td><td>general equilibrium</td></tr>
<tr><td>边际替代率</td><td>marginal rate of substitution</td><td>帕累托效率</td><td>Pareto efficiency</td></tr>
<tr><td>无谓损失</td><td>deadweight loss</td><td>外部性</td><td>externality</td></tr>
<tr><td>纳什均衡</td><td>Nash equilibrium</td><td>逆向选择</td><td>adverse selection</td></tr>
<tr><td>国内生产总值</td><td>gross domestic product</td><td>菲利普斯曲线</td><td>Phillips curve</td></tr>
<tr><td>条件收敛</td><td>conditional convergence</td><td>购买力平价</td><td>purchasing power parity</td></tr>
<tr><td>潜在结果</td><td>potential outcomes</td><td>工具变量</td><td>instrumental variable</td></tr>
<tr><td>双重差分</td><td>difference-in-differences</td><td>固定效应</td><td>fixed effects</td></tr>
<tr><td>伪回归</td><td>spurious regression</td><td>协整</td><td>cointegration</td></tr>
<tr><td>夏普比率</td><td>Sharpe ratio</td><td>有效前沿</td><td>efficient frontier</td></tr>
<tr><td>修正久期</td><td>modified duration</td><td>风险中性测度</td><td>risk-neutral measure</td></tr>
<tr><td>多重检验</td><td>multiple testing</td><td>预注册</td><td>pre-registration</td></tr>
</tbody></table>"""),
  ],
  highlights=[("core-econ", "系统视角的开放教材"), ("statsmodels", "工业计量实现"),
              ("mit-ocw", "配套课程"), ("jupyter", "把公式、代码、结果放在同一份笔记里")],
  pitfalls=["直接编辑章节 HTML：下次重建会被覆盖，应改 <code>tools/chapters_*.py</code>。",
            "改了代码却忘了同步：先重建、再抽取、最后自检。",
            "把附录里的公式当定义使用：正文里有前提与推导，查表时留意适用条件。"],
  exercises=["用 A.5 的脚本索引挑一个模型，改成 <code>numpy</code> 实现并对照数值。",
             "用 A.7 的资源清单为一门 16 周课程排一份阅读计划。",
             "把 A.6 的模板复制到 {{ch:32}} 的课题里，逐项填满。"],
  further=["{{home}}　全书总目录", "{{ch:00}}　主线与学习闭环", "{{ch:32}}　端到端综合课题"]),
]

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""原理篇 05-08 与微观篇 09：消费者、生产者、贸易、风险与福利。"""
from book_schema import C, demo, eq, table

CH = [

C("05", "p1", "part1/05-consumer-choice", "消费者理论：偏好、需求与希克斯分解",
  "把偏好写成效用函数，把预算写成约束，需求就是 01 章一阶条件的直接产物；价格变化的影响可分解为替代效应与收入效应。",
  hours="3 学时",
  goals=["能由 Cobb-Douglas 效用推出马歇尔需求与希克斯需求",
         "会用支出函数计算补偿变化 CV 与等价变化 EV",
         "能数值验证斯勒茨基分解，并说明其符号"],
  points=["效用与偏好", "预算约束与马歇尔需求", "边际替代率", "支出函数与希克斯需求", "替代效应与收入效应", "CV 与 EV", "显示偏好"],
  bridge="把 {{ch:01}} 的 FOC 应用到消费选择；需求曲线由此成为 {{ch:04}} 里「给定」的那条曲线，{{ch:09}} 再用它算福利。",
  analogy="马歇尔需求是「给定预算的最优参数」，希克斯需求是「给定目标效用/服务等级的最小成本配置」；CV/EV 就是两次配置之间换算成钱的差价，相当于用统一的度量单位比较两个版本的性能。",
  sections=[
      ("5.1", "偏好 → 效用 → 需求", """<p>偏好若满足完备性、传递性与连续性，就能用效用函数 <code>u(x,y)</code> 表示；<strong>效用只保序，基数大小没有意义</strong>。最常用的 Cobb-Douglas 形式：</p>"""
       + eq("u(x,y) = x^α · y^(1−α) ,  0<α<1 ;  MRS = MU_x/MU_y = (α/(1−α))·(y/x)")
       + """<p>在预算 <code>pₓx + pᵧy = B</code> 下令 MRS 等于价格比，得到<strong>马歇尔需求</strong>：</p>"""
       + eq("x* = αB/pₓ ,  y* = (1−α)B/pᵧ ,  v(p,B) = B·(α/pₓ)^α·((1−α)/pᵧ)^(1−α)")
       + """<p>注意 <code>x*</code> 只花掉固定比例 <code>α</code> 的收入——这是 Cobb-Douglas 的特殊性质，不是一般规律。它使需求的价格弹性恰为 −1，收入弹性恰为 1，便于手算核对。</p>"""),
      ("5.2", "对偶问题：支出最小化", """<p>把同一个最优问题反过来问：达到给定效用 <code>u</code> 最少要花多少钱？这就是支出最小化，其解 <code>h(p,u)</code> 称为<strong>希克斯需求（补偿需求）</strong>：</p>"""
       + eq("e(p,u) = min p·x  s.t. u(x) ≥ u ;  h_i(p,u) = ∂e(p,u)/∂p_i  (谢泼德引理)")
       + """<p>对 α=1/2，可解析求出 <code>e(p,u)=2u√(pₓpᵧ)</code>、<code>hₓ=u√(pᵧ/pₓ)</code>。由包络定理还能得到 <code>∂v/∂pᵢ = −λ·xᵢ</code> 与 <code>∂v/∂B = λ</code>，相除即<strong>罗伊恒等式</strong>。这些对偶关系让「从需求反推偏好」成为可能，也是 {{ch:29}} 久期、{{ch:27}} 前沿中「敏感度即导数」的同构。</p>"""),
      ("5.3", "价格变化：斯勒茨基分解与货币化福利", """<p>价格上升对需求的总影响可以拆成两部分：</p>"""
       + eq("Δx = [h(p₁,u₀) − h(p₀,u₀)]  +  [x(p₁,B) − h(p₁,u₀)] = 替代效应 + 收入效应")
       + """<p>替代效应沿同一条无差异曲线移动，<strong>必为负</strong>（相对变贵的商品少买）；收入效应反映实际购买力下降，方向取决于商品是正常品还是劣等品。吉芬品即收入效应强到压过替代效应的极端情形。</p>
<p>把效用变化折算成钱，有两种约定：</p>"""
       + eq("CV = B − e(p₀,u₁)   (按旧价格补偿) ;  EV = e(p₁,u₀) − B   (按新价格等价)")
       + """<p>二者一般不等，因为计价的「汇率」（价格向量）不同；对拟线性偏好才恒等。政策评估里选哪个取决于要回答「涨价为补偿需要补多少钱」还是「涨价相当于收入减少多少」。</p>"""),
  ],
  demos=[
      demo("code/05-consumer.py", "需求、支出函数、CV/EV 与斯勒茨基分解", r"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 05-consumer.py | Cobb-Douglas 需求的对偶计算（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
B = 100.0
PX0, PY = 2.0, 5.0
PX1 = 3.0              # x 涨价
ALPHA = 0.5
# ---- 马歇尔需求与间接效用 ----
def demand(px, py, b):
    return ALPHA * b / px, (1 - ALPHA) * b / py

def utility(x, y):
    return (x ** ALPHA) * (y ** (1 - ALPHA))

# ---- 支出函数与希克斯需求（alpha=0.5 的解析式）----
def expenditure(px, py, u):
    return u * (px / ALPHA) ** ALPHA * (py / (1 - ALPHA)) ** (1 - ALPHA)

def hicks_x(px, py, u):
    return u * (py / px) ** (1 - ALPHA)

x0, y0 = demand(PX0, PY, B)
x1, y1 = demand(PX1, PY, B)
u0, u1 = utility(x0, y0), utility(x1, y1)
cv = B - expenditure(PX0, PY, u1)
ev = expenditure(PX1, PY, u0) - B
sub = hicks_x(PX1, PY, u0) - hicks_x(PX0, PY, u0)
inc = x1 - hicks_x(PX1, PY, u0)
# ---- 数值验证：打印可手算核对的量 ----
print("旧价需求 x0=%.4f y0=%.4f u0=%.4f" % (x0, y0, u0))
print("新价需求 x1=%.4f y1=%.4f u1=%.4f" % (x1, y1, u1))
print("支出函数校验 e(p0,u0)=%.4f (应=B=%.2f)" % (expenditure(PX0, PY, u0), B))
print("CV=%.4f  EV=%.4f  (涨价损失，EV>CV 因新价计价更高)" % (cv, ev))
print("总效应=%.4f = 替代效应 %.4f + 收入效应 %.4f" % (x1 - x0, sub, inc))
""",
            "把 <code>ALPHA</code> 改成 0.3，观察 CV/EV 与替代效应如何变化；把 <code>PX1</code> 改成 2.5 观察分解是否仍成立。",
            "x0=25、y0=10、u0≈15.8114；x1≈16.6667、u1≈12.9099；e(p0,u0)=100；CV≈18.3503、EV≈22.4745；总效应 −8.3333 = 替代 −4.5876 + 收入 −3.7457。",
            params="PX1 越接近 PX0，CV 与 EV 越接近；ALPHA 越大，涨价带来的福利损失越大。"),
  ],
  highlights=[("utility", "偏好表示的完备条目"), ("indifference", "无差异曲线与 MRS"),
              ("cobb-douglas", "弹性为 1 的可解析需求")],
  pitfalls=["把效用当作可人际比较的基数：它只表示排序，单调变换不改变需求。",
            "把 CV 与 EV 混用：两者计价价格不同，只有拟线性偏好才相等。",
            "以为替代效应可能为正：希克斯需求对自身价格单调不增，符号由对偶性保证。"],
  exercises=["推导一般 α 下的 <code>e(p,u)=u·(pₓ/α)^α·(pᵧ/(1−α))^(1−α)</code>，并验证脚本中的 α=0.5 情形。",
             "把 <code>x</code> 设为劣等品（例如线性支出系统），思考收入效应何时能压过替代效应。",
             "用 {{ch:01}} 的包络定理证明谢泼德引理 <code>hᵢ=∂e/∂pᵢ</code>。"],
  further=["{{ch:06}}　生产侧的对偶问题：成本函数", "{{ch:09}}　用补偿变化衡量政策福利", "{{ch:14}}　一般均衡中的需求加总"]),

C("06", "p1", "part1/06-production-cost", "生产者理论、成本曲线与供给",
  "企业的技术与消费者的偏好是同一套最优化的对偶镜像：利润最大化给出供给，成本最小化给出条件要素需求。",
  hours="3 学时",
  goals=["能从生产函数推导边际产量、边际成本与要素需求",
         "说明短期供给曲线为什么是 MC 在 AVC 之上的一段",
         "会验证规模报酬与利润最大化条件 p·MP_L = w"],
  points=["生产函数与边际产量", "规模报酬", "成本最小化", "边际成本与平均成本", "利润最大化与供给", "零利润条件"],
  bridge="承接 {{ch:05}} 的对偶结构，把效用换成产量、把支出最小化换成成本最小化，产出 {{ch:04}} 里「给定」的供给曲线。",
  analogy="生产函数是「吞吐模型」，成本函数是「给定 QoS 下的最小资源开销」；边际成本是新增一个请求带来的增量开销，最优并发量由「边际收益等于边际开销」决定。",
  sections=[
      ("6.1", "技术与边际产量", """<p>设 <code>y = A·K^α·L^(1−α)</code>。短期 <code>K</code> 固定，劳动的边际产量递减：</p>"""
       + eq("MP_L = ∂y/∂L = (1−α)·A·K^α·L^(−α) ,  ∂MP_L/∂L < 0")
       + """<p>若所有投入同乘 <code>t</code>，产出乘 <code>t^(α+1−α)=t</code>，即<strong>规模报酬不变</strong>；指数之和大于 1 为递增、小于 1 为递减。这一条指数和直接决定 {{ch:18}} 索洛模型能否有稳态，也决定长期平均成本是否 U 形。</p>"""),
      ("6.2", "成本最小化与成本曲线", """<p>成本最小化 <code>min wL + rK  s.t. f(K,L) ≥ y</code> 的一阶条件是技术替代率等于要素价格比：</p>"""
       + eq("MP_L/MP_K = w/r  ;  MC(y) = ∂C(y)/∂y = w/MP_L  (短期 K 固定)")
       + """<p>因为 MP_L 递减，MC 递增；MC 穿过 AVC 与 ATC 的最低点（「平均值被边际值拉动」的算术事实）。固定成本不影响 MC，因此<strong>短期产量决策与固定成本无关</strong>——这是容易被会计直觉带偏的一点。</p>"""),
      ("6.3", "利润最大化与供给", """<p>价格接受型企业解 <code>max_L p·f(K,L) − wL − rK</code>，一阶条件：</p>"""
       + eq("p·MP_L = w    ⇔    p = MC(y)")
       + """<p>所以<strong>短期供给曲线就是 MC 曲线在 AVC 最低点之上的部分</strong>；低于 AVC 时停业更划算。长期自由进入退出使价格压到 ATC 最低点，经济利润为零——与 {{ch:03}} 的机会成本定义闭环。把个体供给横向加总，就得到 {{ch:04}} 的市场供给。</p>
<div class="card note"><p style="margin-bottom:0">研究生视角：利润函数 <code>π(p,w,r)=max py−C(y)</code> 对 <code>p</code> 求导即供给（霍特林引理），对 <code>w</code> 求导的负数是要素需求（谢泼德引理的对偶版本）。{{ch:29}} 久期、{{ch:05}} 希克斯需求与此完全同构：<strong>值函数对价格的导数就是净需求</strong>。</p></div>"""),
  ],
  demos=[
      demo("code/06-cost.py", "生产、成本曲线与利润最大化的数值验证", r"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 06-cost.py | 短期生产函数、MC=p 条件与规模报酬（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
A_PROD, K_FIXED = 2.0, 16.0     # y = A * sqrt(K) * sqrt(L)
WAGE, FIXED_COST = 4.0, 20.0
PRICE = 10.0
GRID = 1000
# ---- 模型 ----
def output(l, k=K_FIXED):
    return A_PROD * math.sqrt(k) * math.sqrt(l)

def mp_l(l, k=K_FIXED):
    return 0.5 * A_PROD * math.sqrt(k) / math.sqrt(l)

def profit(l):
    return PRICE * output(l) - WAGE * l - FIXED_COST

best_l, best_pi = 0.0, profit(0.0)
for i in range(1, GRID + 1):
    l = 200.0 * i / GRID
    if profit(l) > best_pi:
        best_l, best_pi = l, profit(l)
# p*MP_L=w 的解析解: L = (p*A*sqrt(K)/(2w))^2
analytic_l = (PRICE * A_PROD * math.sqrt(K_FIXED) / (2 * WAGE)) ** 2
q = output(best_l)
mc = WAGE / mp_l(best_l)
ac = (WAGE * best_l + FIXED_COST) / q
# ---- 数值验证：打印可手算核对的量 ----
print("网格最优 L=%.4f 产量=%.4f 利润=%.4f" % (best_l, q, best_pi))
print("解析解   L=%.4f (由 p*MP_L=w 解出)" % analytic_l)
print("最优处 MC=%.4f (应=p=%.2f)  AC=%.4f" % (mc, PRICE, ac))
print("MP_L(L=1)=%.4f, MP_L(L=100)=%.4f → 递减" % (mp_l(1.0), mp_l(100.0)))
print("规模报酬: 投入翻倍 y 由 %.2f 到 %.2f (比值 %.2f)" %
      (output(25.0, 16.0), output(50.0, 32.0), output(50.0, 32.0) / output(25.0, 16.0)))
""",
            "把 <code>PRICE</code> 改成 5，观察最优 L 是否按 p² 缩小；把 <code>FIXED_COST</code> 改成 200，观察产量是否不变。",
            "L*=100、y=80、利润=380；MC=10=p；AC=5.25；MP_L 从 4.0 降到 0.4；投入翻倍产量恰好翻倍（规模报酬不变）。",
            params="PRICE 上升 → L* 按 p² 增长；FIXED_COST 只影响利润不影响产量；WAGE 上升压缩利润并提高 MC。"),
  ],
  highlights=[("production", "生产函数与规模报酬"), ("marginal-cost", "MC 与供给的关系"),
              ("perfect-competition", "价格接受与长期零利润")],
  pitfalls=["把固定成本算进边际决策：停业点由 AVC 决定，与已沉没的固定成本无关。",
            "把会计利润当经济利润：后者要扣除资本与自有劳动的机会成本。",
            "把规模报酬与边际报酬递减混为一谈：前者是所有投入一起变，后者是单一投入变、其他固定。"],
  exercises=["在脚本里加入 <code>p</code> 从 2 到 14 的扫描，打印供给表并核对它等于 MC 反函数。",
             "令 <code>α+β=1.2</code>，说明长期平均成本为何递减，并联系 {{ch:10}} 的自然垄断。",
             "用霍特林引理说明 <code>∂π/∂p = y*</code>，并在脚本里用有限差分验证。"],
  further=["{{ch:05}}　消费者侧的对偶结构", "{{ch:10}}　垄断定价与边际收益", "{{ch:18}}　总量生产函数与索洛稳态"]),

C("07", "p1", "part1/07-trade", "比较优势、专业化与贸易收益",
  "贸易收益来自机会成本的差异，而不是绝对生产率的高低；世界价格落在两国机会成本之间时，双方都能消费到超出本国 PPF 的组合。",
  hours="2 学时",
  goals=["能由单位劳动投入计算两国机会成本并判定比较优势",
         "会构造世界价格并验证进出口与市场出清",
         "解释为什么贸易收益是「消费可能性外移」而不是「多生产了所有商品」"],
  points=["绝对优势与比较优势", "机会成本", "专业化", "世界价格区间", "贸易收益", "市场出清", "贸易分配的代价"],
  bridge="把 {{ch:03}} 的机会成本推广到两个经济体；{{ch:14}} 会把两国两商品模型升级成多市场一般均衡，{{ch:19}} 加入汇率与资本流动。",
  analogy="比较优势就是「按相对吞吐率分配任务」：即使一台机器样样都快，也该把稀缺资源投到它相对优势最大的任务上；调度依据是相对成本比，不是绝对耗时。",
  sections=[
      ("7.1", "绝对优势不是贸易的理由", """<p>李嘉图模型里，两国各有一种固定技术 <code>aᵢⱼ</code>（生产一单位商品 j 所需工时），劳动总量 <code>L</code>。自给自足的相对价格就是本国 PPF 斜率：</p>"""
       + eq("(p_F/p_C)_A = a_AF/a_AC ,  (p_F/p_C)_B = a_BF/a_BC")
       + """<p>只要这两个比值不同，就存在比较优势。<strong>即使 A 国两种商品都更省工（绝对优势全占），贸易仍对双方有利</strong>，因为资源配置看的是「放弃什么」，不是「干得多快」。</p>"""),
      ("7.2", "世界价格与贸易收益", """<p>设 A 国食品机会成本为 1、B 国为 0.25。开放后世界相对价格 <code>p_F/p_C</code> 必落在 <code>[0.25, 1]</code> 之间；在此区间内 A 专业化生产布、B 专业化生产食品。用出口收入按世界价格买回另一种商品，两国消费组合都<strong>落在各自 PPF 之外</strong>：</p>"""
       + eq("消费可能性: p_F·F + p_C·C ≤ p_C·(L/a_AC)   (A 国专业化生产布时的预算线)")
       + """<p>这是全书第一个「<strong>约束被交换放宽</strong>」的例子：不是技术进步，而是允许交换使可行集外移。{{ch:09}} 的福利定理会说清它在什么条件下成立，{{ch:12}}、{{ch:13}} 则说明市场缺失或信息不对称时收益会打折。</p>"""),
      ("7.3", "收益不等于人人受益", """<table><thead><tr><th style="width:24%">层次</th><th>结论</th><th>前提 / 限制</th></tr></thead><tbody>
<tr><td>两国总量</td><td>贸易使双方总消费可能性扩大</td><td>技术差异、无运输成本、完全竞争</td></tr>
<tr><td>国内分配</td><td>相对价格变化使稀缺要素受益、密集使用该要素的部门收缩</td><td>要素可流动需要时间，短期有调整成本</td></tr>
<tr><td>长期增长</td><td>贸易可能通过技术扩散影响增长率</td><td>超出李嘉图静态模型，见 {{ch:18}}</td></tr>
</tbody></table>
<p>把「总量收益」直接说成「每个人都变好」是常见逻辑跳跃；补偿原则说的是<strong>赢家理论上足以补偿输家</strong>，不等于补偿真的发生。</p>"""),
  ],
  demos=[
      demo("code/07-trade.py", "两国两商品：机会成本、专业化与市场出清", r"""#!/usr/bin/env python3
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
""",
            "把 <code>WORLD_PF</code> 改成 0.9（更靠近 A 国机会成本），观察收益如何在两国之间重新分配。",
            "A 国机会成本 1、B 国 0.25，世界价 0.5 落在区间内；自给自足 A=(25,25)、B=(50,12.5)，效用均 25；贸易后两国均为 (50,25)，效用≈35.36；两个市场都恰好出清。",
            params="WORLD_PF 越接近某国自给自足价格，该国贸易收益越小；A_BC 下降会缩小两国技术差异与收益。"),
  ],
  highlights=[("comparative-advantage", "李嘉图模型的标准表述"),
              ("worldbank", "用跨国数据观察专业化与收入"),
              ("general-equilibrium", "两商品模型如何推广到多市场")],
  pitfalls=["把绝对优势当成贸易原因：关键是比较机会成本，不是绝对生产率。",
            "以为世界价格可以任意设定：必须落在两国机会成本之间，否则至少一国不愿专业化。",
            "把总量收益说成人人受益：部门间要素再配置会产生受损者。"],
  exercises=["把 <code>WORLD_PF</code> 从 0.26 扫到 0.99，画出两国效用曲线并解释为何单调性相反。",
             "加入每单位 0.1 的运输成本（楔子），说明贸易收益如何被侵蚀，联系 {{ch:04}} 的税收楔子。",
             "用 {{ch:14}} 的语言说明本例其实是一个 2 国 × 2 商品的一般均衡。"],
  further=["{{ch:03}}　机会成本与 PPF", "{{ch:14}}　一般均衡与瓦尔拉斯法则", "{{ch:19}}　开放经济与汇率"]),

C("08", "p1", "part1/08-risk-time", "跨期选择与不确定下的决策",
  "把时间贴现与风险偏好写进同一个最优化框架：欧拉方程决定今天与明天的消费比例，凹效用决定愿意为规避风险付多少钱。",
  hours="3 学时",
  goals=["会计算现值、年金与跨期欧拉方程",
         "能由期望效用计算确定性等价与风险溢价",
         "理解风险厌恶来自效用函数的凹性而非「不喜欢波动」的心理描述"],
  points=["贴现与现值", "跨期预算与欧拉方程", "期望效用", "确定性等价", "风险溢价", "风险厌恶系数", "蒙特卡洛验证"],
  bridge="把 {{ch:02}} 的分布与 {{ch:05}} 的效用合流；这是通向 {{ch:26}} 收益建模、{{ch:27}} 组合选择与 {{ch:30}} 期权定价的桥。",
  analogy="贴现因子就是异步任务里的折扣率；确定性等价是把一个随机 payoff 压缩成「确定给多少我才愿意换」，类似把延迟分布换成等价的固定 SLA。",
  sections=[
      ("8.1", "跨期：现值、年金与欧拉方程", """<p>一笔未来现金流 <code>C_t</code> 的现值是 <code>C_t/(1+r)^t</code>；等额年金可求和为闭式：</p>"""
       + eq("PV = C·[1 − (1+r)^(−T)] / r  ;  永续 PV = C/r")
       + """<p>两期消费者最大化 <code>u(c₁) + β·u(c₂)</code>，预算 <code>c₁ + c₂/(1+r) ≤ y₁ + y₂/(1+r)</code>，一阶条件即<strong>欧拉方程</strong>：</p>"""
       + eq("u'(c₁) = β(1+r)·u'(c₂)  ;  对数效用下 c₂/c₁ = β(1+r)")
       + """<p>读法：<code>β(1+r)</code> 大于 1 时把消费推到明天（耐心或高利率），小于 1 时提前消费。宏观的 {{ch:16}} 消费函数、{{ch:17}} 实际利率、{{ch:18}} 储蓄率与增长都由这条式子在不同约束下推出；{{ch:29}} 债券定价则是它的直接应用。</p>"""),
      ("8.2", "风险：期望效用与确定性等价", """<p>不确定下不最大化期望财富，而最大化<strong>期望效用</strong>（冯·诺依曼–摩根斯坦公理）：</p>"""
       + eq("EU = Σ p_s·u(w_s) ;  CE 满足 u(CE) = EU ;  风险溢价 RP = E[w] − CE")
       + """<p>由 Jensen 不等式，<code>u</code> 凹 ⇒ <code>E[u(w)] ≤ u(E[w])</code> ⇒ <code>CE ≤ E[w]</code> ⇒ 风险溢价非负。风险厌恶的局部度量是 <code>A(w)=−u''/u'</code>（阿罗–普拉特）；对数效用 <code>A=1/w</code>，财富越高越不怕小赌。</p>
<div class="card tip"><p style="margin-bottom:0"><strong>与 {{ch:27}} 的接口</strong>：均值-方差准则等价于「效用二次 或 收益正态」下的期望效用近似，因此 <code>E[r] − (A/2)Var(r)</code> 里的风险系数不是随手加的惩罚项，而是凹效用的二阶展开。</p></div>"""),
      ("8.3", "用蒙特卡洛核对解析结果", """<p>脚本同时用解析式与固定种子的随机抽样计算确定性等价：<code>ln</code> 效用下 <code>CE = exp(E[ln w])</code>，即财富的几何平均。这给出了本书第一次「模拟估计一个已知量」的闭环，{{ch:30}} 会把它放大成期权定价的主力方法。</p>"""),
  ],
  demos=[
      demo("code/08-risk.py", "现值、欧拉方程、确定性等价与蒙特卡洛", r"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 08-risk.py | 跨期贴现与期望效用（只用标准库）
import math, random, statistics
random.seed(7)
# ---- 参数区 ----
C_ANNUAL, RATE, YEARS = 100.0, 0.05, 20
BETA = 0.95
W_LOW, W_HIGH, P_HIGH = 80.0, 120.0, 0.5
N_DRAWS = 20000
# ---- 跨期：年金现值 ----
pv = C_ANNUAL * (1 - (1 + RATE) ** (-YEARS)) / RATE
perpetuity = C_ANNUAL / RATE
c_ratio = BETA * (1 + RATE)     # 对数效用下 c2/c1
# ---- 风险：解析期望效用 ----
eu = (1 - P_HIGH) * math.log(W_LOW) + P_HIGH * math.log(W_HIGH)
ce = math.exp(eu)
expected_w = (1 - P_HIGH) * W_LOW + P_HIGH * W_HIGH
rp = expected_w - ce
# ---- 蒙特卡洛核对 ----
draws = [W_HIGH if random.random() < P_HIGH else W_LOW for _ in range(N_DRAWS)]
mc_mean = statistics.fmean(draws)
mc_ce = math.exp(statistics.fmean([math.log(w) for w in draws]))
# ---- 数值验证：打印可手算核对的量 ----
print("年金现值(T=%d)=%.4f  永续现值=%.4f" % (YEARS, pv, perpetuity))
print("欧拉方程 c2/c1=beta*(1+r)=%.4f" % c_ratio)
print("EU=%.6f  CE=%.6f (=sqrt(80*120)=%.6f)" % (eu, ce, math.sqrt(W_LOW * W_HIGH)))
print("E[w]=%.4f  风险溢价 RP=%.4f" % (expected_w, rp))
print("蒙特卡洛: 平均财富=%.4f  几何平均(CE)=%.4f  与解析差=%.4f" %
      (mc_mean, mc_ce, mc_ce - ce))
""",
            "把 <code>W_LOW/W_HIGH</code> 的价差拉大（如 40/160），观察 RP 如何上升；把 <code>BETA</code> 改成 1.0 看 c₂/c₁。",
            "20 年年金现值≈1246.22、永续=2000；c₂/c₁=0.9975；CE=√9600≈97.9796、RP≈2.0204；蒙特卡洛几何平均≈98 左右，与解析值一致。",
            params="价差越大 RP 越大；P_HIGH 偏离 0.5 会改变 CE；BETA 上升使消费后移。"),
  ],
  highlights=[("present-value", "贴现与现值公式"), ("expected-utility", "期望效用公理"),
              ("risk-aversion", "阿罗-普拉特度量与 Jensen 不等式")],
  pitfalls=["把期望财富最大化当决策准则：凹效用下应最大化期望效用。",
            "把风险溢价当成「不理性的恐惧」：它来自边际效用递减，是可计算的价格。",
            "把名义利率当实际利率做跨期决策：需扣除预期通胀，见 {{ch:17}} 费雪方程。"],
  exercises=["推导指数效用 <code>u(w)=−e^(−aw)</code> 下 CE 与 RP，并说明为什么与财富水平无关。",
             "把 <code>RATE</code> 从 0 到 0.2 扫描，画年金现值曲线并解释凸性。",
             "在脚本里令 <code>BETA=1.0, RATE=0</code>，说明欧拉方程给出的平滑消费结论。"],
  further=["{{ch:26}}　收益、对数收益与复利", "{{ch:27}}　均值-方差与期望效用的关系", "{{ch:30}}　蒙特卡洛定价"]),

C("09", "p2", "part2/09-welfare", "福利经济学：剩余、效率与两条福利定理",
  "把供需曲线下的面积翻译成福利，给「市场好不好」一个可计算的答案；两条福利定理说明竞争均衡与帕累托效率在什么条件下互为表里。",
  hours="3 学时",
  goals=["能由反需求/反供给曲线计算消费者剩余、生产者剩余与总剩余",
         "会量化价格管制造成的短缺与无谓损失",
         "说清福利第一/第二定理的前提与常见误用"],
  points=["消费者剩余与生产者剩余", "总剩余最大化", "帕累托效率", "价格上限与短缺", "无谓损失", "福利第一定理", "福利第二定理"],
  bridge="用 {{ch:04}} 的供需模型加上 {{ch:05}} 的偏好基础，第一次给「效率」下定义；{{ch:10}}～{{ch:13}} 逐条打破福利定理的前提。",
  analogy="总剩余是系统的目标函数，竞争均衡是无约束一阶条件的解，价格管制是强行加一条不等式约束；DWL 就是约束造成的 objective gap。",
  sections=[
      ("9.1", "剩余是可计算的福利", """<p>把需求曲线理解为边际支付意愿、供给曲线理解为边际成本，则交易第 <code>q</code> 单位带来的净剩余是 <code>p_d(q) − p_s(q)</code>：</p>"""
       + eq("CS = ∫₀^Q [p_d(q) − p] dq ;  PS = ∫₀^Q [p − p_s(q)] dq ;  TS = ∫₀^Q [p_d(q) − p_s(q)] dq")
       + """<p>价格只是 CS 与 PS 之间的<strong>转移</strong>，不改变 TS；改变交易量才改变 TS。因此无谓损失总可以写成「被挤掉的那段交易上边际支付意愿与边际成本之差的积分」——{{ch:04}} 的三角形公式是线性曲线下的特例。</p>"""),
      ("9.2", "价格管制：短缺、配置与 DWL", """<p>设上限 <code>p̄ &lt; p*</code>，则 <code>Q_s(p̄) &lt; Q_d(p̄)</code>，实际成交量是<strong>短边</strong> <code>Q̄ = min(Q_d, Q_s)</code>。此时「谁买到」变得关键：</p>"""
       + table(["配给方式", "实际成交", "福利结果"], [
           ["有效配给（支付意愿最高者买到）", "Q_s(p̄)", "DWL = TS(Q*) − TS(Q̄)"],
           ["随机配给 / 排队", "Q_s(p̄)", "额外损失：错配 + 排队耗散的租"],
           ["黑市 / 变相收费", "可能接近 Q*", "名义价格失效，租转移给中间人"],
       ], ["34%", "20%", "46%"])
       + """<p>这解释了为什么单看「价格低了」判断不了政策好坏：必须说明成交量、配置规则与租的归属。{{ch:12}} 的庇古税同样是插楔子，但那个楔子把原本未被计入的成本内部化，方向恰好相反。</p>"""),
      ("9.3", "两条福利定理及其前提", """<p><strong>第一定理</strong>：在完全竞争、完备市场、无外部性、无信息不对称、凸技术下，竞争均衡是帕累托有效的。<strong>第二定理</strong>：在上述条件加凸偏好下，任一帕累托有效分配都可通过对初始禀赋的一次性再分配 + 竞争市场实现。</p>
<div class="card warn"><p style="margin-bottom:0">两个定理都不是「市场万能」的证明，而是<strong>一份前提清单</strong>：{{ch:10}} 打破价格接受，{{ch:11}} 引入策略互动，{{ch:12}} 引入外部性与公共品，{{ch:13}} 引入私有信息。第二定理还常被误读：它说的是<em>一次性 lump-sum 再分配</em>，现实中的所得税会扭曲边际激励（回到 {{ch:04}} 的楔子）。效率与公平是可分离的问题，但只在极强假设下可分离。</p></div>"""),
  ],
  demos=[
      demo("code/09-welfare.py", "剩余积分、价格上限与无谓损失", r"""#!/usr/bin/env python3
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
""",
            "把 <code>CEILING</code> 改成 18（等于均衡价），观察 DWL 是否归零；改成 10 观察短缺与 DWL 如何放大。",
            "p*=18、Q*=64；CS=1024、PS=682.6667、TS=1706.6667；上限 14 时 Qs=52、Qd=72、短缺 20，CS=1196、PS=450.6667、DWL=60，与三角公式一致。",
            params="CEILING 越低于均衡价，短缺按 (B+D)·(p*−p̄) 增大，DWL 按缺口平方增长。"),
  ],
  highlights=[("surplus", "剩余概念与几何"), ("welfare-theorems", "两条定理的严格前提"),
              ("pareto", "帕累托效率的定义")],
  pitfalls=["把价格管制下的需求量当成交量：市场按短边成交，出现的是短缺而非超额供给。",
            "忽略配给规则：随机配给会在 DWL 之外再叠加错配与排队成本。",
            "引用福利第二定理时忽略 lump-sum 假设：现实再分配工具本身会制造楔子。"],
  exercises=["推导价格下限（支持价）下的福利变化，并说明政府收购成本该记在哪一项。",
             "在脚本里加入「配额随机分配」的模拟，估计错配带来的额外损失。",
             "用 {{ch:12}} 的语言说明：若存在负外部性，TS 的积分该改成哪条曲线。"],
  further=["{{ch:04}}　供需与税收楔子", "{{ch:10}}　垄断造成的效率损失", "{{ch:12}}　外部性与庇古税"]),
]

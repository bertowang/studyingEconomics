#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全书参考文献与扩展学习链接库（唯一数据源）。

R                 : key -> (显示名, URL, 一句话说明, 分类)
TOPIC_RULES        : 知识点关键词 -> 资源 key，用于「知识点地图」逐条挂链接
CHAPTER_RESOURCES : 章节 id -> 该章「扩展学习」精读清单与检索词

说明：本开发环境无法访问 en.wikipedia.org，百科条目按标准英文条目 URL 收录；
check_book.py --urls 会把这类超时归为「本环境不可达」而非链接失效。
"""
from __future__ import annotations

import html as html_mod
from urllib.parse import quote

R = {
    # ---------- 教材与开放课程 ----------
    "core-econ": ("CORE Econ 开放教材", "https://www.core-econ.org/", "免费开源的本科经济学教材，以实证与数据贯穿全书，与本书的系统视角最接近", "教材"),
    "openstax": ("OpenStax Principles of Economics", "https://openstax.org/details/books/principles-economics", "免费、可下载的本科原理教材，适合查公式与习题", "教材"),
    "mit-ocw": ("MIT OpenCourseWare 经济学课程", "https://ocw.mit.edu/search/?q=economics", "检索 14.01 微观、14.02 宏观、14.32 计量等完整课程材料", "课程"),
    "mru": ("Marginal Revolution University", "https://marginalrevolutionuniversity.com/", "免费短视频课程，按主题讲清直觉", "课程"),
    "khan": ("Khan Academy 经济与金融", "https://www.khanacademy.org/economics-finance-domain", "交互式入门讲解与练习，适合补齐基础", "课程"),
    "aea": ("American Economic Association", "https://www.aeaweb.org/", "学会资源、JEL 分类与教学资料", "机构"),
    "nber": ("NBER", "https://www.nber.org/", "工作论文与数据集，追踪前沿实证研究的入口", "机构"),
    "repec": ("IDEAS / RePEc", "https://ideas.repec.org/", "免费的经济学论文与引文检索", "机构"),
    "arxiv-econ": ("arXiv econ", "https://arxiv.org/archive/econ", "经济学预印本，含计算与计量方法新进展", "机构"),
    "ssrn": ("SSRN", "https://www.ssrn.com/", "金融与会计领域工作论文库", "机构"),
    "econlib": ("Econlib", "https://www.econlib.org/", "经济学文库与经典文本导读", "教材"),
    "cfa": ("CFA Institute", "https://www.cfainstitute.org/", "投资学职业知识体系与伦理准则", "机构"),
    "damodaran": ("Aswath Damodaran（NYU Stern）", "https://pages.stern.nyu.edu/~adamodar/", "估值、风险溢价与行业数据的公开教学资料", "课程"),
    "cochrane": ("John H. Cochrane 资产定价资料", "https://www.johnhcochrane.com/", "资产定价课程讲义与论文，研究生进阶", "课程"),

    # ---------- Python / 数据工具 ----------
    "python-docs": ("Python 官方文档", "https://docs.python.org/3/", "语言与标准库权威参考", "工具"),
    "python-math": ("Python math 模块", "https://docs.python.org/3/library/math.html", "指数、对数、误差函数等定价与效用计算所需函数", "工具"),
    "python-random": ("Python random 模块", "https://docs.python.org/3/library/random.html", "随机数与固定种子，保证模拟可复现", "工具"),
    "python-statistics": ("Python statistics 模块", "https://docs.python.org/3/library/statistics.html", "均值、方差、相关等基础统计量", "工具"),
    "numpy": ("NumPy", "https://numpy.org/doc/stable/", "向量化与线性代数；本书手写实现的工业版", "工具"),
    "scipy": ("SciPy", "https://docs.scipy.org/doc/scipy/", "最优化、积分与统计分布", "工具"),
    "pandas": ("pandas", "https://pandas.pydata.org/docs/", "表格数据与时间序列处理", "工具"),
    "statsmodels": ("statsmodels", "https://www.statsmodels.org/stable/index.html", "OLS / IV / 面板 / 时间序列的成熟实现", "工具"),
    "statsmodels-ols": ("statsmodels OLS 文档", "https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.OLS.html", "对照本书手写 OLS 的输出与检验", "工具"),
    "matplotlib": ("Matplotlib", "https://matplotlib.org/stable/contents.html", "把曲线与模拟结果画出来", "工具"),
    "jupyter": ("Project Jupyter", "https://jupyter.org/", "把公式、代码与结果放在同一份可复现笔记里", "工具"),
    "causal-book": ("Causal Inference for the Brave and True", "https://matheusfacure.github.io/python-causality-handbook/landing-page.html", "用 Python 讲因果推断的开放教材，含可运行代码", "教材"),
    "mixtape": ("Causal Inference: The Mixtape", "https://mixtape.scunning.com/", "因果推断开放教材，DID / IV / RDD 讲得直观", "教材"),

    # ---------- 公开数据 ----------
    "fred": ("FRED 经济数据", "https://fred.stlouisfed.org/", "美联储圣路易斯分行的宏观与金融时间序列，免费可下载", "数据"),
    "worldbank": ("World Bank Data", "https://data.worldbank.org/", "跨国发展指标，适合增长与制度研究", "数据"),
    "oecd": ("OECD Data", "https://data.oecd.org/", "成员国可比宏观与劳动力数据", "数据"),
    "owid": ("Our World in Data", "https://ourworldindata.org/", "带图表与数据下载的长周期发展数据", "数据"),
    "bea": ("U.S. Bureau of Economic Analysis", "https://www.bea.gov/", "GDP 与国民账户的官方来源", "数据"),
    "bls": ("U.S. Bureau of Labor Statistics", "https://www.bls.gov/", "CPI、失业率与工资数据", "数据"),
    "fed": ("Federal Reserve", "https://www.federalreserve.gov/", "货币政策声明、利率与政策规则资料", "数据"),
    "ecb": ("European Central Bank", "https://www.ecb.europa.eu/", "欧元区货币政策与统计数据", "数据"),
    "imf": ("IMF Data", "https://www.imf.org/en/Data", "国际收支、汇率与跨国宏观数据", "数据"),
    "bis": ("Bank for International Settlements", "https://www.bis.org/", "利率、汇率与金融稳定统计", "数据"),
    "french": ("Ken French Data Library", "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html", "Fama-French 因子与组合收益，复现资产定价实证的标准数据", "数据"),
    "cbo": ("Congressional Budget Office", "https://www.cbo.gov/", "政策评估与财政预测报告，学习政策分析的范本", "数据"),
    "wrds": ("WRDS", "https://wrds-www.wharton.upenn.edu/", "CRSP / Compustat 等金融库（多需机构订阅）", "数据"),

    # ---------- 经济学百科条目 ----------
    "scarcity": ("Scarcity", "https://en.wikipedia.org/wiki/Scarcity", "经济学问题的起点：资源有限而欲望无限", "百科"),
    "opp-cost": ("Opportunity cost", "https://en.wikipedia.org/wiki/Opportunity_cost", "被放弃的最优替代用途，决策的真正成本", "百科"),
    "marginalism": ("Marginalism", "https://en.wikipedia.org/wiki/Marginalism", "边际量而非总量决定最优选择", "百科"),
    "ppf": ("Production-possibility frontier", "https://en.wikipedia.org/wiki/Production-possibility_frontier", "稀缺、取舍与机会成本的几何表示", "百科"),
    "supply-demand": ("Supply and demand", "https://en.wikipedia.org/wiki/Supply_and_demand", "局部均衡最基本的模型", "百科"),
    "equilibrium": ("Economic equilibrium", "https://en.wikipedia.org/wiki/Economic_equilibrium", "均衡作为不动点的一般概念", "百科"),
    "elasticity": ("Elasticity (economics)", "https://en.wikipedia.org/wiki/Elasticity_(economics)", "相对变化的响应程度，量纲无关", "百科"),
    "tax-incidence": ("Tax incidence", "https://en.wikipedia.org/wiki/Tax_incidence", "税负归宿由弹性决定，与法定纳税人无关", "百科"),
    "deadweight-loss": ("Deadweight loss", "https://en.wikipedia.org/wiki/Deadweight_loss", "扭曲造成的净福利损失", "百科"),
    "surplus": ("Economic surplus", "https://en.wikipedia.org/wiki/Economic_surplus", "消费者剩余与生产者剩余", "百科"),
    "utility": ("Utility", "https://en.wikipedia.org/wiki/Utility", "偏好表示与效用函数", "百科"),
    "indifference": ("Indifference curve", "https://en.wikipedia.org/wiki/Indifference_curve", "无差异曲线与边际替代率", "百科"),
    "budget": ("Budget constraint", "https://en.wikipedia.org/wiki/Budget_constraint", "可行集与相对价格", "百科"),
    "lagrange": ("Lagrange multiplier", "https://en.wikipedia.org/wiki/Lagrange_multiplier", "约束最优的一阶条件与影子价格", "百科"),
    "production": ("Production function", "https://en.wikipedia.org/wiki/Production_function", "投入产出技术与规模报酬", "百科"),
    "marginal-cost": ("Marginal cost", "https://en.wikipedia.org/wiki/Marginal_cost", "多生产一单位的增量成本", "百科"),
    "cobb-douglas": ("Cobb-Douglas production function", "https://en.wikipedia.org/wiki/Cobb%E2%80%93Douglas_production_function", "最常用的可解析生产/效用函数", "百科"),
    "comparative-advantage": ("Comparative advantage", "https://en.wikipedia.org/wiki/Comparative_advantage", "按机会成本分工使双方受益", "百科"),
    "present-value": ("Present value", "https://en.wikipedia.org/wiki/Present_value", "跨期选择的贴现基础", "百科"),
    "discounting": ("Discounted utility", "https://en.wikipedia.org/wiki/Discounted_utility", "跨期效用与贴现因子", "百科"),
    "expected-utility": ("Expected utility hypothesis", "https://en.wikipedia.org/wiki/Expected_utility_hypothesis", "不确定下的偏好表示", "百科"),
    "risk-aversion": ("Risk aversion", "https://en.wikipedia.org/wiki/Risk_aversion", "凹效用、风险溢价与确定性等价", "百科"),
    "perfect-competition": ("Perfect competition", "https://en.wikipedia.org/wiki/Perfect_competition", "价格接受者、零利润与效率", "百科"),
    "welfare-theorems": ("Fundamental theorems of welfare economics", "https://en.wikipedia.org/wiki/Fundamental_theorems_of_welfare_economics", "竞争均衡与帕累托效率的两条定理", "百科"),
    "pareto": ("Pareto efficiency", "https://en.wikipedia.org/wiki/Pareto_efficiency", "无人可在不损人时获益", "百科"),
    "monopoly": ("Monopoly", "https://en.wikipedia.org/wiki/Monopoly", "边际收益等于边际成本的定价", "百科"),
    "price-discrimination": ("Price discrimination", "https://en.wikipedia.org/wiki/Price_discrimination", "按支付意愿分段榨取剩余", "百科"),
    "game-theory": ("Game theory", "https://en.wikipedia.org/wiki/Game_theory", "策略互动的一般框架", "百科"),
    "nash": ("Nash equilibrium", "https://en.wikipedia.org/wiki/Nash_equilibrium", "互为最优反应的策略组合", "百科"),
    "prisoners-dilemma": ("Prisoner's dilemma", "https://en.wikipedia.org/wiki/Prisoner%27s_dilemma", "个体理性导致集体低效", "百科"),
    "oligopoly": ("Oligopoly", "https://en.wikipedia.org/wiki/Oligopoly", "古诺/伯特兰/斯塔克尔伯格竞争", "百科"),
    "externality": ("Externality", "https://en.wikipedia.org/wiki/Externality", "私人成本与社会成本分离", "百科"),
    "public-good": ("Public good", "https://en.wikipedia.org/wiki/Public_good", "非排他与非竞争性导致搭便车", "百科"),
    "coase": ("Coase theorem", "https://en.wikipedia.org/wiki/Coase_theorem", "产权清晰且交易成本为零时的谈判效率", "百科"),
    "pigouvian": ("Pigouvian tax", "https://en.wikipedia.org/wiki/Pigouvian_tax", "把外部性内部化的单位税", "百科"),
    "adverse-selection": ("Adverse selection", "https://en.wikipedia.org/wiki/Adverse_selection", "签约前隐藏信息导致的市场失灵", "百科"),
    "moral-hazard": ("Moral hazard", "https://en.wikipedia.org/wiki/Moral_hazard", "签约后隐藏行动导致的风险扭曲", "百科"),
    "signaling": ("Signalling (economics)", "https://en.wikipedia.org/wiki/Signalling_(economics)", "通过可观测成本传递私有信息", "百科"),
    "general-equilibrium": ("General equilibrium theory", "https://en.wikipedia.org/wiki/General_equilibrium_theory", "所有市场同时出清的联立系统", "百科"),
    "walras": ("Walras' law", "https://en.wikipedia.org/wiki/Walras%27_law", "超额需求总和恒为零，价格只需解 n−1 个方程", "百科"),
    "fallacy-of-composition": ("Fallacy of composition", "https://en.wikipedia.org/wiki/Fallacy_of_composition", "个体成立不等于总量成立（微观到宏观的陷阱）", "百科"),
    "gdp": ("Gross domestic product", "https://en.wikipedia.org/wiki/Gross_domestic_product", "国民核算的核心总量", "百科"),
    "national-accounts": ("National accounts", "https://en.wikipedia.org/wiki/National_accounts", "支出法/收入法/生产法三套恒等式", "百科"),
    "inflation": ("Inflation", "https://en.wikipedia.org/wiki/Inflation", "一般价格水平持续上涨", "百科"),
    "cpi": ("Consumer price index", "https://en.wikipedia.org/wiki/Consumer_price_index", "价格指数编制与替代偏差", "百科"),
    "unemployment": ("Unemployment", "https://en.wikipedia.org/wiki/Unemployment", "失业率度量与结构性/摩擦性失业", "百科"),
    "is-lm": ("IS–LM model", "https://en.wikipedia.org/wiki/IS%E2%80%93LM_model", "产品市场与货币市场同时均衡", "百科"),
    "ad-as": ("AD–AS model", "https://en.wikipedia.org/wiki/AD%E2%80%93AS_model", "总需求总供给与短期波动", "百科"),
    "multiplier": ("Multiplier (economics)", "https://en.wikipedia.org/wiki/Multiplier_(economics)", "边际消费倾向决定的支出乘数", "百科"),
    "monetary-policy": ("Monetary policy", "https://en.wikipedia.org/wiki/Monetary_policy", "政策目标、工具与传导机制", "百科"),
    "central-bank": ("Central bank", "https://en.wikipedia.org/wiki/Central_bank", "央行职能与独立性", "百科"),
    "taylor-rule": ("Taylor rule", "https://en.wikipedia.org/wiki/Taylor_rule", "以通胀与产出缺口设定政策利率的简单规则", "百科"),
    "fisher": ("Fisher hypothesis", "https://en.wikipedia.org/wiki/Fisher_hypothesis", "名义利率 ≈ 实际利率 + 预期通胀", "百科"),
    "solow": ("Solow–Swan model", "https://en.wikipedia.org/wiki/Solow%E2%80%93Swan_model", "资本积累、折旧与稳态增长", "百科"),
    "endogenous-growth": ("Endogenous growth theory", "https://en.wikipedia.org/wiki/Endogenous_growth_theory", "把技术进步内生化的增长模型", "百科"),
    "convergence": ("Convergence (economics)", "https://en.wikipedia.org/wiki/Convergence_(economics)", "条件收敛与跨国增长实证", "百科"),
    "exchange-rate": ("Exchange rate", "https://en.wikipedia.org/wiki/Exchange_rate", "名义/实际汇率与标价方式", "百科"),
    "bop": ("Balance of payments", "https://en.wikipedia.org/wiki/Balance_of_payments", "经常账户与资本账户恒等关系", "百科"),
    "ppp": ("Purchasing power parity", "https://en.wikipedia.org/wiki/Purchasing_power_parity", "长期汇率的一价定律版本", "百科"),
    "trilemma": ("Impossible trinity", "https://en.wikipedia.org/wiki/Impossible_trinity", "汇率稳定、资本自由流动与独立货币政策不可兼得", "百科"),

    # ---------- 计量与因果 ----------
    "dgp": ("Data-generating process", "https://en.wikipedia.org/wiki/Data-generating_process", "把「数据从哪来」写成可模拟的概率模型", "百科"),
    "identification": ("Identification (economics)", "https://en.wikipedia.org/wiki/Identification_(economics)", "参数能否由观测分布唯一确定", "百科"),
    "ols": ("Ordinary least squares", "https://en.wikipedia.org/wiki/Ordinary_least_squares", "最小化残差平方和的线性估计", "百科"),
    "gauss-markov": ("Gauss–Markov theorem", "https://en.wikipedia.org/wiki/Gauss%E2%80%93Markov_theorem", "经典假设下 OLS 为 BLUE", "百科"),
    "clt": ("Central limit theorem", "https://en.wikipedia.org/wiki/Central_limit_theorem", "估计量渐近正态的理论基础", "百科"),
    "lln": ("Law of large numbers", "https://en.wikipedia.org/wiki/Law_of_large_numbers", "样本均值收敛到期望", "百科"),
    "expected-value": ("Expected value", "https://en.wikipedia.org/wiki/Expected_value", "概率加权平均与线性性质", "百科"),
    "variance": ("Variance", "https://en.wikipedia.org/wiki/Variance", "离散程度与方差分解", "百科"),
    "p-value": ("p-value", "https://en.wikipedia.org/wiki/P-value", "原假设下观测到当前或更极端结果的概率", "百科"),
    "confidence-interval": ("Confidence interval", "https://en.wikipedia.org/wiki/Confidence_interval", "重复抽样意义下的覆盖概率", "百科"),
    "r-squared": ("Coefficient of determination", "https://en.wikipedia.org/wiki/Coefficient_of_determination", "拟合优度及其误导性", "百科"),
    "heteroscedasticity": ("Heteroscedasticity", "https://en.wikipedia.org/wiki/Heteroscedasticity", "误差方差非常数使标准误失效", "百科"),
    "robust-se": ("Heteroscedasticity-consistent standard errors", "https://en.wikipedia.org/wiki/Heteroscedasticity-consistent_standard_errors", "不假设同方差的稳健推断", "百科"),
    "autocorrelation": ("Autocorrelation", "https://en.wikipedia.org/wiki/Autocorrelation", "序列相关与时间序列推断", "百科"),
    "multicollinearity": ("Multicollinearity", "https://en.wikipedia.org/wiki/Multicollinearity", "解释变量高度相关导致估计不稳", "百科"),
    "endogeneity": ("Endogeneity (economics)", "https://en.wikipedia.org/wiki/Endogeneity_(economics)", "解释变量与误差相关造成偏误", "百科"),
    "omitted-variable": ("Omitted-variable bias", "https://en.wikipedia.org/wiki/Omitted-variable_bias", "遗漏变量的偏误方向与大小", "百科"),
    "iv": ("Instrumental variable", "https://en.wikipedia.org/wiki/Instrumental_variable", "用外生变动隔离出因果通道", "百科"),
    "2sls": ("Two-stage least squares", "https://en.wikipedia.org/wiki/Two-stage_least_squares", "IV 的两阶段实现", "百科"),
    "did": ("Difference in differences", "https://en.wikipedia.org/wiki/Difference_in_differences", "处理组与对照组的前后差分之差", "百科"),
    "panel": ("Panel data", "https://en.wikipedia.org/wiki/Panel_data", "同一主体多期观测的数据结构", "百科"),
    "fixed-effects": ("Fixed effects model", "https://en.wikipedia.org/wiki/Fixed_effects_model", "吸收不随时间变化的个体异质性", "百科"),
    "parallel-trends": ("Parallel trends assumption", "https://en.wikipedia.org/wiki/Difference_in_differences", "DID 成立的关键识别假设", "百科"),
    "rdd": ("Regression discontinuity design", "https://en.wikipedia.org/wiki/Regression_discontinuity_design", "利用阈值附近局部随机性识别因果", "百科"),
    "stationarity": ("Stationary process", "https://en.wikipedia.org/wiki/Stationary_process", "均值方差不随时间漂移", "百科"),
    "unit-root": ("Unit root", "https://en.wikipedia.org/wiki/Unit_root", "非平稳与随机游走", "百科"),
    "arma": ("ARMA model", "https://en.wikipedia.org/wiki/Autoregressive%E2%80%93moving-average_model", "自回归与移动平均的组合", "百科"),
    "cointegration": ("Cointegration", "https://en.wikipedia.org/wiki/Cointegration", "非平稳序列的长期均衡关系", "百科"),
    "spurious": ("Spurious relationship", "https://en.wikipedia.org/wiki/Spurious_relationship", "共同趋势造成的伪相关", "百科"),
    "phacking": ("Data dredging / p-hacking", "https://en.wikipedia.org/wiki/Data_dredging", "多重尝试后挑显著结果的偏误", "百科"),
    "multiple-testing": ("Multiple comparisons problem", "https://en.wikipedia.org/wiki/Multiple_comparisons_problem", "多次检验抬高假阳性率", "百科"),
    "replication": ("Replication crisis", "https://en.wikipedia.org/wiki/Replication_crisis", "可复现性与研究规范", "百科"),
    "causality": ("Causality (economics)", "https://en.wikipedia.org/wiki/Causality_(economics)", "相关不等于因果的经济学表述", "百科"),
    "rubin": ("Rubin causal model", "https://en.wikipedia.org/wiki/Rubin_causal_model", "潜在结果框架与平均处理效应", "百科"),

    # ---------- 投资学 ----------
    "compound-interest": ("Compound interest", "https://en.wikipedia.org/wiki/Compound_interest", "复利与长期增长的非线性", "百科"),
    "rate-of-return": ("Rate of return", "https://en.wikipedia.org/wiki/Rate_of_return", "简单收益、对数收益与年化", "百科"),
    "lognormal": ("Log-normal distribution", "https://en.wikipedia.org/wiki/Log-normal_distribution", "资产价格建模的常用分布", "百科"),
    "mpt": ("Modern portfolio theory", "https://en.wikipedia.org/wiki/Modern_portfolio_theory", "均值-方差框架与分散化", "百科"),
    "efficient-frontier": ("Efficient frontier", "https://en.wikipedia.org/wiki/Efficient_frontier", "给定风险下最高期望收益的组合集合", "百科"),
    "sharpe": ("Sharpe ratio", "https://en.wikipedia.org/wiki/Sharpe_ratio", "单位总风险的超额收益", "百科"),
    "diversification": ("Diversification (finance)", "https://en.wikipedia.org/wiki/Diversification_(finance)", "相关性低于 1 时可降低组合波动", "百科"),
    "capm": ("Capital asset pricing model", "https://en.wikipedia.org/wiki/Capital_asset_pricing_model", "beta 与期望收益的线性关系", "百科"),
    "beta": ("Beta (finance)", "https://en.wikipedia.org/wiki/Beta_(finance)", "资产对市场因子的暴露", "百科"),
    "fama-french": ("Fama–French three-factor model", "https://en.wikipedia.org/wiki/Fama%E2%80%93French_three-factor_model", "规模与价值因子对 CAPM 的扩展", "百科"),
    "emh": ("Efficient-market hypothesis", "https://en.wikipedia.org/wiki/Efficient-market_hypothesis", "价格是否反映全部可用信息", "百科"),
    "var-risk": ("Value at risk", "https://en.wikipedia.org/wiki/Value_at_risk", "分位数意义下的潜在损失", "百科"),
    "bond-duration": ("Bond duration", "https://en.wikipedia.org/wiki/Bond_duration", "价格对利率的一阶敏感度", "百科"),
    "yield-curve": ("Yield curve", "https://en.wikipedia.org/wiki/Yield_curve", "不同期限利率的结构", "百科"),
    "no-arbitrage": ("Arbitrage", "https://en.wikipedia.org/wiki/Arbitrage", "无套利是定价模型的共同约束", "百科"),
    "option": ("Option (finance)", "https://en.wikipedia.org/wiki/Option_(finance)", "或有权益与非线性 payoff", "百科"),
    "binomial-option": ("Binomial options pricing model", "https://en.wikipedia.org/wiki/Binomial_options_pricing_model", "离散时间风险中性定价与回溯", "百科"),
    "black-scholes": ("Black–Scholes model", "https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model", "连续时间无套利定价的闭式解", "百科"),
    "monte-carlo": ("Monte Carlo method", "https://en.wikipedia.org/wiki/Monte_Carlo_method", "用模拟逼近期望与积分", "百科"),
    "gbm": ("Geometric Brownian motion", "https://en.wikipedia.org/wiki/Geometric_Brownian_motion", "股票价格的经典随机过程", "百科"),
    "risk-neutral": ("Risk-neutral measure", "https://en.wikipedia.org/wiki/Risk-neutral_measure", "贴现期望等于无套利价格", "百科"),
    "behavioral-finance": ("Behavioral finance", "https://en.wikipedia.org/wiki/Behavioral_finance", "偏离完全理性的系统性行为偏差", "百科"),
    "prospect-theory": ("Prospect theory", "https://en.wikipedia.org/wiki/Prospect_theory", "参照点依赖与损失厌恶", "百科"),
    "risk-premium": ("Risk premium", "https://en.wikipedia.org/wiki/Risk_premium", "承担风险所要求的额外期望收益", "百科"),
    "factor-investing": ("Factor investing", "https://en.wikipedia.org/wiki/Factor_investing", "把实证因子转成可交易策略", "百科"),
}

# 关键词 -> 资源 key；用于知识点地图逐条挂 1～2 个扩展链接
TOPIC_RULES = [
    ("稀缺", ["scarcity", "core-econ"]), ("机会成本", ["opp-cost", "ppf"]),
    ("生产可能性", ["ppf", "opp-cost"]), ("边际", ["marginalism", "core-econ"]),
    ("最优化", ["lagrange", "marginalism"]), ("拉格朗日", ["lagrange", "budget"]),
    ("影子价格", ["lagrange", "general-equilibrium"]), ("均衡", ["equilibrium", "supply-demand"]),
    ("不动点", ["equilibrium", "general-equilibrium"]), ("比较静态", ["marginalism", "elasticity"]),
    ("需求", ["supply-demand", "elasticity"]), ("供给", ["supply-demand", "marginal-cost"]),
    ("弹性", ["elasticity", "tax-incidence"]), ("税收归宿", ["tax-incidence", "deadweight-loss"]),
    ("剩余", ["surplus", "deadweight-loss"]), ("无谓损失", ["deadweight-loss", "tax-incidence"]),
    ("效用", ["utility", "indifference"]), ("偏好", ["utility", "indifference"]),
    ("无差异", ["indifference", "budget"]), ("预算约束", ["budget", "lagrange"]),
    ("边际替代率", ["indifference", "utility"]), ("Cobb", ["cobb-douglas", "production"]),
    ("生产函数", ["production", "cobb-douglas"]), ("成本", ["marginal-cost", "production"]),
    ("规模报酬", ["production", "cobb-douglas"]), ("利润最大", ["marginal-cost", "perfect-competition"]),
    ("比较优势", ["comparative-advantage", "opp-cost"]), ("贸易", ["comparative-advantage", "general-equilibrium"]),
    ("贴现", ["present-value", "discounting"]), ("跨期", ["present-value", "discounting"]),
    ("期望效用", ["expected-utility", "risk-aversion"]), ("风险厌恶", ["risk-aversion", "expected-utility"]),
    ("风险溢价", ["risk-premium", "risk-aversion"]), ("确定性等价", ["expected-utility", "risk-aversion"]),
    ("完全竞争", ["perfect-competition", "welfare-theorems"]), ("帕累托", ["pareto", "welfare-theorems"]),
    ("福利定理", ["welfare-theorems", "pareto"]), ("价格管制", ["deadweight-loss", "supply-demand"]),
    ("垄断", ["monopoly", "price-discrimination"]), ("价格歧视", ["price-discrimination", "monopoly"]),
    ("博弈", ["game-theory", "nash"]), ("纳什", ["nash", "game-theory"]),
    ("囚徒困境", ["prisoners-dilemma", "nash"]), ("寡头", ["oligopoly", "nash"]),
    ("重复博弈", ["prisoners-dilemma", "game-theory"]),
    ("外部性", ["externality", "pigouvian"]), ("庇古", ["pigouvian", "externality"]),
    ("公共品", ["public-good", "externality"]), ("科斯", ["coase", "externality"]),
    ("逆向选择", ["adverse-selection", "signaling"]), ("道德风险", ["moral-hazard", "adverse-selection"]),
    ("信号", ["signaling", "adverse-selection"]), ("信息不对称", ["adverse-selection", "moral-hazard"]),
    ("一般均衡", ["general-equilibrium", "walras"]), ("瓦尔拉斯", ["walras", "general-equilibrium"]),
    ("加总", ["fallacy-of-composition", "gdp"]), ("合成谬误", ["fallacy-of-composition", "is-lm"]),
    ("GDP", ["gdp", "national-accounts"]), ("国民账户", ["national-accounts", "gdp"]),
    ("CPI", ["cpi", "inflation"]), ("通胀", ["inflation", "cpi"]),
    ("失业", ["unemployment", "inflation"]), ("IS-LM", ["is-lm", "ad-as"]),
    ("AD-AS", ["ad-as", "is-lm"]), ("乘数", ["multiplier", "is-lm"]),
    ("货币政策", ["monetary-policy", "central-bank"]), ("央行", ["central-bank", "monetary-policy"]),
    ("泰勒规则", ["taylor-rule", "monetary-policy"]), ("费雪", ["fisher", "inflation"]),
    ("利率", ["fisher", "monetary-policy"]), ("索洛", ["solow", "convergence"]),
    ("稳态", ["solow", "convergence"]), ("增长", ["solow", "endogenous-growth"]),
    ("内生增长", ["endogenous-growth", "solow"]), ("收敛", ["convergence", "solow"]),
    ("汇率", ["exchange-rate", "ppp"]), ("国际收支", ["bop", "exchange-rate"]),
    ("购买力平价", ["ppp", "exchange-rate"]), ("三元悖论", ["trilemma", "exchange-rate"]),
    ("数据生成", ["dgp", "identification"]), ("识别", ["identification", "causality"]),
    ("因果", ["causality", "rubin"]), ("潜在结果", ["rubin", "causality"]),
    ("大数定律", ["lln", "clt"]), ("中心极限", ["clt", "lln"]),
    ("期望", ["expected-value", "variance"]), ("方差", ["variance", "expected-value"]),
    ("OLS", ["ols", "gauss-markov"]), ("最小二乘", ["ols", "statsmodels-ols"]),
    ("高斯马尔可夫", ["gauss-markov", "ols"]), ("标准误", ["confidence-interval", "robust-se"]),
    ("p 值", ["p-value", "multiple-testing"]), ("置信区间", ["confidence-interval", "p-value"]),
    ("拟合优度", ["r-squared", "ols"]), ("R²", ["r-squared", "ols"]),
    ("异方差", ["heteroscedasticity", "robust-se"]), ("稳健标准误", ["robust-se", "heteroscedasticity"]),
    ("自相关", ["autocorrelation", "stationarity"]), ("多重共线", ["multicollinearity", "ols"]),
    ("内生", ["endogeneity", "omitted-variable"]), ("遗漏变量", ["omitted-variable", "endogeneity"]),
    ("工具变量", ["iv", "2sls"]), ("两阶段", ["2sls", "iv"]),
    ("双重差分", ["did", "parallel-trends"]), ("DID", ["did", "parallel-trends"]),
    ("平行趋势", ["parallel-trends", "did"]), ("面板", ["panel", "fixed-effects"]),
    ("固定效应", ["fixed-effects", "panel"]), ("断点回归", ["rdd", "causality"]),
    ("平稳", ["stationarity", "unit-root"]), ("单位根", ["unit-root", "stationarity"]),
    ("ARMA", ["arma", "stationarity"]), ("协整", ["cointegration", "unit-root"]),
    ("伪回归", ["spurious", "cointegration"]), ("p-hacking", ["phacking", "multiple-testing"]),
    ("多重检验", ["multiple-testing", "phacking"]), ("复现", ["replication", "phacking"]),
    ("复利", ["compound-interest", "rate-of-return"]), ("收益率", ["rate-of-return", "compound-interest"]),
    ("对数收益", ["rate-of-return", "lognormal"]), ("对数正态", ["lognormal", "gbm"]),
    ("组合", ["mpt", "diversification"]), ("均值-方差", ["mpt", "efficient-frontier"]),
    ("有效前沿", ["efficient-frontier", "mpt"]), ("分散化", ["diversification", "mpt"]),
    ("夏普", ["sharpe", "efficient-frontier"]), ("最小方差", ["efficient-frontier", "mpt"]),
    ("CAPM", ["capm", "beta"]), ("beta", ["beta", "capm"]),
    ("因子", ["fama-french", "factor-investing"]), ("Fama", ["fama-french", "french"]),
    ("有效市场", ["emh", "behavioral-finance"]), ("VaR", ["var-risk", "monte-carlo"]),
    ("风险价值", ["var-risk", "monte-carlo"]), ("久期", ["bond-duration", "yield-curve"]),
    ("期限结构", ["yield-curve", "bond-duration"]), ("无套利", ["no-arbitrage", "binomial-option"]),
    ("套利", ["no-arbitrage", "emh"]), ("期权", ["option", "binomial-option"]),
    ("二叉树", ["binomial-option", "no-arbitrage"]), ("Black-Scholes", ["black-scholes", "gbm"]),
    ("蒙特卡洛", ["monte-carlo", "gbm"]), ("几何布朗", ["gbm", "black-scholes"]),
    ("风险中性", ["risk-neutral", "no-arbitrage"]), ("行为金融", ["behavioral-finance", "prospect-theory"]),
    ("前景理论", ["prospect-theory", "behavioral-finance"]),
    ("Python", ["python-docs", "python-math"]), ("标准库", ["python-docs", "python-statistics"]),
    ("随机种子", ["python-random", "replication"]), ("模拟", ["monte-carlo", "python-random"]),
    ("向量化", ["numpy", "python-docs"]), ("statsmodels", ["statsmodels", "statsmodels-ols"]),
    ("FRED", ["fred", "bea"]), ("World Bank", ["worldbank", "owid"]),
    ("Ken French", ["french", "fama-french"]), ("数据泄漏", ["replication", "dgp"]),
]

CHAPTER_RESOURCES = {
    "00": (["core-econ", "openstax", "mit-ocw", "aea", "nber"], "economics curriculum principles microeconometrics investment"),
    "01": (["lagrange", "equilibrium", "python-docs", "python-math"], "constrained optimization comparative statics economics"),
    "02": (["lln", "clt", "expected-value", "python-statistics", "python-random"], "probability statistics for econometrics simulation"),
    "03": (["scarcity", "opp-cost", "ppf", "marginalism", "core-econ"], "opportunity cost production possibility frontier"),
    "04": (["supply-demand", "elasticity", "tax-incidence", "deadweight-loss", "fred"], "supply demand equilibrium tax incidence"),
    "05": (["utility", "indifference", "budget", "lagrange", "cobb-douglas"], "utility maximization budget constraint Cobb Douglas"),
    "06": (["production", "marginal-cost", "perfect-competition", "cobb-douglas"], "cost curves profit maximization supply"),
    "07": (["comparative-advantage", "opp-cost", "general-equilibrium", "worldbank"], "comparative advantage gains from trade"),
    "08": (["present-value", "expected-utility", "risk-aversion", "compound-interest"], "expected utility risk aversion intertemporal choice"),
    "09": (["perfect-competition", "welfare-theorems", "pareto", "surplus"], "welfare economics deadweight loss price ceiling"),
    "10": (["monopoly", "price-discrimination", "deadweight-loss", "cbo"], "monopoly pricing price discrimination regulation"),
    "11": (["game-theory", "nash", "prisoners-dilemma", "oligopoly"], "game theory Nash equilibrium repeated games"),
    "12": (["externality", "pigouvian", "public-good", "coase"], "Pigouvian tax Coase theorem externality"),
    "13": (["adverse-selection", "moral-hazard", "signaling", "causal-book"], "adverse selection moral hazard signaling"),
    "14": (["general-equilibrium", "walras", "welfare-theorems", "fallacy-of-composition"], "general equilibrium Walras law computable equilibrium"),
    "15": (["gdp", "national-accounts", "cpi", "unemployment", "bea", "bls", "fred"], "national accounts GDP CPI unemployment"),
    "16": (["is-lm", "ad-as", "multiplier", "fred"], "IS LM aggregate demand multiplier"),
    "17": (["monetary-policy", "central-bank", "taylor-rule", "fisher", "fed"], "monetary policy Taylor rule Fisher equation"),
    "18": (["solow", "endogenous-growth", "convergence", "worldbank", "owid"], "Solow model steady state convergence empirics"),
    "19": (["exchange-rate", "bop", "ppp", "trilemma", "imf"], "open economy exchange rate impossible trinity"),
    "20": (["dgp", "identification", "causality", "rubin", "causal-book"], "identification data generating process causal inference"),
    "21": (["ols", "gauss-markov", "statsmodels-ols", "r-squared", "python-docs"], "OLS from scratch standard errors Gauss Markov"),
    "22": (["heteroscedasticity", "robust-se", "autocorrelation", "multicollinearity", "statsmodels"], "heteroskedasticity robust standard errors diagnostics"),
    "23": (["endogeneity", "omitted-variable", "iv", "2sls", "mixtape"], "instrumental variables two stage least squares endogeneity"),
    "24": (["did", "parallel-trends", "panel", "fixed-effects", "causal-book"], "difference in differences fixed effects panel data"),
    "25": (["stationarity", "unit-root", "arma", "cointegration", "spurious"], "stationarity ARMA spurious regression cointegration"),
    "26": (["compound-interest", "rate-of-return", "lognormal", "fred"], "log returns compounding annualized volatility"),
    "27": (["mpt", "efficient-frontier", "sharpe", "diversification", "numpy"], "mean variance efficient frontier portfolio optimization"),
    "28": (["capm", "beta", "fama-french", "french", "emh"], "CAPM empirical test Fama French factors"),
    "29": (["bond-duration", "yield-curve", "present-value", "fed"], "bond duration yield curve interest rate risk"),
    "30": (["option", "binomial-option", "black-scholes", "monte-carlo", "risk-neutral"], "binomial option pricing Black Scholes Monte Carlo"),
    "31": (["phacking", "multiple-testing", "replication", "repec", "cbo"], "p hacking multiple testing replication crisis economics"),
    "32": (["core-econ", "statsmodels", "fred", "french", "jupyter"], "applied economics project theory simulation estimation policy"),
    "A": (["core-econ", "openstax", "mit-ocw", "statsmodels", "fred", "french"], "economics formulas cheat sheet terminology"),
}

DEFAULT_KEYS = ["core-econ", "openstax", "aea"]


def anchor(key, label=None):
    name, url, _desc, _cat = R[key]
    return ('<a href="' + html_mod.escape(url, quote=True) + '" target="_blank" rel="noopener">'
            + html_mod.escape(label or name) + "</a>")


def links_for_point(chapter_id, point, max_links=2):
    hits = []
    for kw, keys in TOPIC_RULES:
        if kw.lower() in point.lower():
            for k in keys:
                if k not in hits:
                    hits.append(k)
            if len(hits) >= max_links:
                break
    if not hits:
        hits = list(CHAPTER_RESOURCES.get(chapter_id, (DEFAULT_KEYS, ""))[0])[:max_links]
    return " · ".join(anchor(k) for k in hits[:max_links])


def resource_card(key, why=""):
    """章节「本章参考资料」卡片。"""
    name, url, desc, cat = R[key]
    out = ['<div class="repo-card">', "<h3>" + anchor(key, name) + "</h3>",
           '<span class="tag">' + html_mod.escape(cat) + " · 参考资料</span>",
           "<p>" + html_mod.escape(desc) + "</p>"]
    if why:
        out.append('<span class="why"><strong>怎么用</strong>：' + html_mod.escape(why) + "</span>")
    out.append('<p style="margin:0"><code>' + html_mod.escape(url) + "</code></p></div>")
    return "\n".join(out)


def search_url(query, site="web"):
    if site == "repec":
        return "https://ideas.repec.org/cgi-bin/short.cgi?q=" + quote(query)
    if site == "ocw":
        return "https://ocw.mit.edu/search/?q=" + quote(query)
    return "https://www.google.com/search?q=" + quote(query)


def chapter_links_html(chapter_id, root="../../"):
    keys, query = CHAPTER_RESOURCES.get(chapter_id, (DEFAULT_KEYS, "economics"))
    out = ["<p>以下资料按本章知识点挑选，可直接精读或对照数据；知识点地图里每一条也挂了 1～2 个直达链接。</p>", "<ul>"]
    for k in keys:
        name, _url, desc, cat = R[k]
        out.append("<li><strong>" + html_mod.escape(name) + "</strong>（" + html_mod.escape(cat) + "）："
                   + html_mod.escape(desc) + "<br>" + anchor(k) + "</li>")
    out.append("</ul>")
    out.append('<p class="code-hint">继续扩展：'
               '<a href="' + search_url(query, "repec") + '" target="_blank" rel="noopener">在 RePEc 检索本章相关论文</a> · '
               '<a href="' + search_url(query, "ocw") + '" target="_blank" rel="noopener">在 MIT OCW 检索配套课程</a> · '
               '<a href="' + search_url(query) + '" target="_blank" rel="noopener">按本章主题检索资料</a> · '
               '<a href="' + root + 'index.html#resources">全书参考资源总表</a> · '
               '<a href="' + root + 'appendix/index.html">附录 A 速查与链接总表</a></p>')
    return "\n".join(out)


def all_resources_html():
    cats = {}
    for key, (name, url, desc, cat) in R.items():
        cats.setdefault(cat, []).append((key, name, desc))
    order = ["教材", "课程", "百科", "数据", "工具", "机构"]
    out = ["<p>本书全部外部链接的唯一来源，按用途分组；各章的「知识点地图」「本章参考资料」「扩展学习」都指向这里。</p>"]
    for cat in order:
        if cat not in cats:
            continue
        out.append("<h3>" + cat + "（" + str(len(cats[cat])) + "）</h3>")
        out.append('<table><thead><tr><th style="width:28%">名称</th><th>说明</th></tr></thead><tbody>')
        for key, name, desc in cats[cat]:
            out.append("<tr><td>" + anchor(key, name) + "</td><td>" + html_mod.escape(desc) + "</td></tr>")
        out.append("</tbody></table>")
    return "\n".join(out)

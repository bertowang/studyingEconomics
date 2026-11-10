# 经济学：从稀缺到证据

> 一本写给爱好经济学的计算机专业学生、覆盖本科到研究生的教材。全书不按课程拼盘，而沿 **稀缺 → 选择 → 均衡 → 效率 → 失灵 → 动态 → 不确定 → 证据 → 决策** 一条主线，把原理、微观、宏观、计量与投资串成同一个问题；每章配一个只用 Python 3 标准库、可实跑并打印可核对数值的建模脚本。

[![Static HTML](https://img.shields.io/badge/format-static%20HTML-orange)](./index.html)
[![Chapters](https://img.shields.io/badge/chapters-33%20%2B%20appendix-blue)](#内容结构)
[![Python 3](https://img.shields.io/badge/Python%203-33%20demos-3776AB)](#快速开始)
[![Stdlib only](https://img.shields.io/badge/dependencies-stdlib%20only-2ea44f)](#约定与边界)
[![License](https://img.shields.io/badge/license-not%20specified-lightgrey)](#许可证)

**仓库**：[github.com/bertowang/studyingEconomics](https://github.com/bertowang/studyingEconomics) · **阅读入口**：[index.html](./index.html) · **版本**：v0.1 · 2026-11

---

## 目录

- [一眼看懂](#一眼看懂)
- [这本书的写法](#这本书的写法)
- [快速开始](#快速开始)
- [内容结构](#内容结构)
- [仓库结构](#仓库结构)
- [每章包含什么](#每章包含什么)
- [工具链与维护](#工具链与维护)
- [质量保障](#质量保障)
- [约定与边界](#约定与边界)
- [同系列教材](#同系列教材)
- [作者与 AI 使用说明](#作者与-ai-使用说明)
- [许可证](#许可证)

## 一眼看懂

| 项目 | 内容 |
| --- | --- |
| 读者定位 | 爱好经济学的计算机专业学生，本科到研究生；需要一定的微积分、线性代数与编程基础 |
| 规模 | 33 章（00–32）+ 附录 A · 5 个学习阶段 · 35 个 HTML 页面 · 33 个 Python 脚本 |
| 内容形态 | 纯静态 HTML5 + CSS + 原生 JS；无外部依赖，离线 / `file://` 可读 |
| 建模脚本 | Python 3 **只用标准库**（`math` / `random` / `statistics`），固定 `random.seed(7)`，自包含合成数据 |
| 扩展资源 | 159 条外部链接（CORE Econ、OpenStax、MIT OCW、FRED、Ken French、statsmodels 等） |
| 维护工具 | Python 3 生成器 / 抽取器 / 自检器 + `run_python.sh` 批量实跑 |
| 状态 | 33 章全部完稿；静态自检 0 错误 0 提示，33/33 脚本实跑通过 |

## 这本书的写法

五门课其实是**同一个计算问题**的逐层放大：给定资源、技术与信息，求可行的最优选择，再研究许多人同时选择时是否自洽。四种数学骨架反复出现——**约束最优化**（消费者、企业、组合）、**不动点**（均衡、纳什、稳态）、**条件期望**（回归、资产定价）、**反事实**（因果推断、政策评估、期权 payoff）。认出骨架，五门课就变成五种应用配置。

- **有机组合**：先写「本章位置」说明承接与引出，再给「给程序员的翻译」把概念映射到计算概念。
- **可复现实验**：计量与投资章节都先写出已知真值的数据生成过程（DGP），再由它生成数据、估计参数、打印真值与估计值对照——相当于带答案的单元测试。
- **手写而非调包**：矩阵求逆、OLS、稳健标准误、IV/2SLS、二叉树定价全部展开成可读的循环；附录 A.5 给出与 `numpy` / `statsmodels` / `linearmodels` 的对照表。
- **高屋建瓴且诚实**：每章写明模型前提、常见误区与边界，明确区分「解释 / 预测 / 反事实」三种用法，并提示卢卡斯批判与多重检验问题。

**不适合**：只想查公式背结论、或期待真实宏观 / 市场数据集的读者；本书脚本使用合成数据讲解机制，真实数据入口集中在附录 A.7。

## 快速开始

### 1. 阅读（无需构建、无需服务器）

```bash
git clone git@github.com:bertowang/studyingEconomics.git
cd studyingEconomics
open index.html          # macOS；Linux 用 xdg-open，Windows 双击即可
```

也可以直接在本仓库点开 [index.html](./index.html) 查看源码，或启用 GitHub Pages 后以 `index.html` 为入口发布成站点。侧栏目录、面包屑与上下章导航共用 [assets/toc.js](./assets/toc.js) 这一份数据。

### 2. 跑一个建模脚本（约 30 秒）

```bash
# 需要 Python 3.8+，不需要安装任何第三方包
python3 part1/04-supply-demand/code/04-supply-demand.py
# 无税: p*=18.0000 Q*=64.0000 需求弹性=-0.5625 供给弹性=0.8438
# 征税: 买方价=21.6000 卖方价=15.6000 ... 无谓损失=21.6000
```

- 任意章节的「Python 建模实例」代码块右上角可一键复制；仓库里的 `code/*.py` 由 `tools/extract_code.py` 从 HTML 自动抽取，页面与脚本永远一致。
- 脚本开头的 `# ---- 参数区 ----` 集中所有可调量，先改这里；结尾 `print` 打印可手算核对的量，页面给出预期数值与判读逻辑。
- 页面另给「改参数看趋势」说明，例如把 `D` 改成 8 观察税负归宿如何转移。

### 3. 批量实跑与自检

```bash
./tools/run_python.sh               # 共 33 个脚本：通过 33，失败 0
python3 tools/check_book.py --run   # 实跑：33/33；自检：35 个页面，0 条错误，0 条提示
```

## 内容结构

五个学习阶段把原理、微观、宏观、计量与投资串起来：

| 分部 | 章节 | 主要内容 |
| --- | --- | --- |
| 卷首 · 共同语言 | 00–02 | 全书主线与学习闭环、约束最优化与比较静态、概率统计与蒙特卡洛（LLN / CLT / 标准误） |
| 第一篇 · 原理与个体决策 | 03–08 | 稀缺与 PPF、供需弹性与税收归宿、消费者理论（CV / EV / 斯勒茨基）、生产者与成本、比较优势与贸易、跨期选择与期望效用 |
| 第二篇 · 市场结构、策略与失灵 | 09–14 | 剩余与两条福利定理、垄断与价格歧视、博弈与古诺、外部性/公共品/科斯、信息不对称与信号、一般均衡与瓦尔拉斯法则 |
| 第三篇 · 宏观、货币与增长 | 15–19 | 国民账户与价格指数、乘数与 IS-LM、费雪方程与泰勒规则、索洛稳态与内生增长、国际收支与汇率 |
| 第四篇 · 计量经济学与因果推断 | 20–25 | 潜在结果与识别、手写 OLS、异方差稳健标准误、IV/2SLS、DID/固定效应/RDD、平稳性与伪回归 |
| 第五篇 · 投资学、资产定价与风险管理 | 26–30 | 收益/复利/GBM、均值-方差有效前沿、CAPM 与因子、债券久期与期限结构、二叉树 / Black-Scholes / 蒙特卡洛 |
| 第六篇 · 方法论与综合课题 | 31–32 | p-hacking 与复现规范、端到端政策评估流水线（DID + 预趋势 + 安慰剂 + 稳健推断） |
| 附录 | A | 公式速查、示例脚本索引、手写实现与工业库对照、常见坑、数据字典模板、159 条资源总表 |

时间有限时的最短路径：`01 → 04 → 09 → 20 → 21 → 24 → 27 → 30 → 32`。完整目录与各章知识点见 [index.html](./index.html)。

## 仓库结构

```text
studyingEconomics/
├── index.html                     # 总目录：主线、代码契约、学习路线、参考资源、维护约定
├── appendix/index.html            # 附录 A：公式/脚本/资源速查（A.5、A.7 动态生成）
├── part0/ … part6/                # 每章一个文件夹
│   └── NN-slug/
│       ├── index.html             # 正文：目标、知识点地图、§x.y、Python 实例、误区、习题
│       └── code/*.py              # 该章的可运行建模脚本
├── assets/
│   ├── style.css                  # 统一排版（含深色主题、打印样式、公式块）
│   ├── app.js                     # 侧栏、复制代码块、导航填充
│   └── toc.js                     # 目录唯一数据源：BOOK_TOC / BOOK_FLAT
├── tools/
│   ├── book_schema.py             # 书名、五个学习阶段、分部与章节数据结构
│   ├── book_data.py               # 章节汇总入口与数据校验
│   ├── book_resources.py          # 外部参考资源唯一数据源
│   ├── chapters_00_04.py … chapters_31_A.py   # 正文与 Python 示例（7 个分文件）
│   ├── build_book.py              # 生成全部 HTML 与 assets/toc.js
│   ├── extract_code.py            # 从 HTML 代码块同步 code/*.py
│   ├── check_book.py              # 全书静态自检（可选 --run / --urls）
│   └── run_python.sh              # 批量实跑全部 .py
└── .gitignore                     # 忽略缓存与本地验证输出
```

## 每章包含什么

| 栏目 | 作用 |
| --- | --- |
| 本章位置 / 给程序员的翻译 | 说明承接什么、引出什么，并把概念映射到计算概念 |
| 学习目标 | 学完应能做什么，用可检验的动词描述 |
| 知识点地图 | 逐条列出知识点，每条挂 1–2 个扩展学习链接 |
| 原理小节 §x.y | 概念、直觉、公式推导与对照表；公式用 Unicode 纯文本，不依赖 MathJax |
| Python 建模实例 | 完整可运行脚本 + 操作步骤 + 预期数值与判读 + 改参数看趋势 |
| 本章参考资料 | 按知识点挑选的教材、课程、数据与工具卡片 |
| 常见误区 / 习题 | 典型错误与可动手验证的思考题 |
| 扩展学习 / 延伸阅读 | 精读清单、检索入口与全书内链 |

## 工具链与维护

**单一数据源**：章节正文、Python 示例与链接库都写在 `tools/` 的 Python 数据里，HTML 由生成器产出。**不要直接编辑章节 HTML**，否则下次重建会被覆盖。

| 想改什么 | 编辑哪里 |
| --- | --- |
| 某章正文或建模脚本 | `tools/chapters_*.py` 中对应的 `C(...)` / `demo(...)` |
| 参考资料链接 | `tools/book_resources.py` 的 `R`、`TOPIC_RULES`、`CHAPTER_RESOURCES`，以及章节的 `highlights` |
| 页面结构与总目录 | `tools/build_book.py` 的 `render()` / `render_index()` |
| 样式与交互 | `assets/style.css`、`assets/app.js` |
| 新增章节 / 分部 | `tools/book_schema.py` 的 `PARTS` + 对应 `chapters_*.py`，再重建（`toc.js` 自动同步） |

| 命令 | 作用 |
| --- | --- |
| `python3 tools/book_data.py` | 打印章节 / 实例 / 资源统计并做数据一致性校验 |
| `python3 tools/build_book.py` | 只生成缺失的章节页（不覆盖已有文件） |
| `python3 tools/build_book.py --force` | 全量重建（会丢失对章节页的手工修改） |
| `python3 tools/build_book.py --list` | 列出章节 id / 路径 / 标题 |
| `python3 tools/extract_code.py` | 从 HTML 代码块同步写出 `code/*.py` |
| `python3 tools/extract_code.py --check` | 只检查页面与脚本是否一致 |
| `python3 tools/extract_code.py --clean` | 同步并删除无对应代码块的旧 `.py` |
| `python3 tools/check_book.py` | 全文静态自检，退出码非 0 时逐条报错 |
| `python3 tools/check_book.py --run` | 静态自检 + 实跑全部脚本 |
| `python3 tools/check_book.py --urls` | 额外联网探测 159 条外部链接（需网络） |
| `./tools/run_python.sh` | 批量实跑；也可在后面接单个 `.py` 路径，或用 `PYTHON=...` 指定解释器 |

推荐改动顺序：

```bash
python3 tools/build_book.py --force      # 1. 重建页面
python3 tools/extract_code.py            # 2. 同步脚本
python3 tools/check_book.py --run        # 3. 自检 + 实跑
```

## 质量保障

`tools/check_book.py` 覆盖：目录与 `toc.js` 一致性、内部链接、HTML 标签配对、页面代码块与 `.py` 同步、Python 代码契约（shebang、`random.seed(7)`、参数区、数值打印、禁用第三方依赖）、语法编译、外部链接探测（可选）。

当前本地运行结果：

- `python3 tools/check_book.py --run` → **实跑 33 / 33 通过；35 个 HTML 页面 / 34 个章节 / 33 个 Python 脚本，0 条错误，0 条提示**
- `./tools/run_python.sh` → **33 / 33 脚本通过**
- `assets/app.js` / `assets/toc.js` 通过 JavaScriptCore 语法检查；`tools/run_python.sh` 通过 `bash -n`

> 说明：合成数据用于讲清机制与验证流水线，**不构成真实政策或市场结论**；反事实外推还需面对识别假设与卢卡斯批判。

## 约定与边界

- 示例脚本只用 Python 3 标准库、不读外部文件、固定 `random.seed(7)`；真实数据分析请改用 `numpy` / `statsmodels` / `linearmodels`（对照见附录 A.5）。
- 公式一律写成纯文本 Unicode（`α`、`σ²`、`Σ`），不依赖 MathJax，断网也能读。
- `code/*.py` 是源脚本，纳入版本控制；`__pycache__/`、`*.pyc` 与本地验证输出由 `.gitignore` 排除。
- 外部参考资料与工具的版权归各自维护者所有；本书与这些机构、项目无从属关系。

## 同系列教材

三本教材共用同一套静态站点骨架与「单一数据源 + 自检」维护方式：

| 仓库 | 主题 | 示例形态 |
| --- | --- | --- |
| [analogCircuits](https://github.com/bertowang/analogCircuits) | 模拟电路（本科） | LTspice `.cir` 网表 |
| [imageProcessing](https://github.com/bertowang/imageProcessing) | 数字图像处理（本科到研究生） | GNU Octave `.m` + 开源工程链接 |
| **studyingEconomics**（本仓库） | 经济学（本科到研究生） | Python 3 标准库 `.py` 建模脚本 |

## 作者与 AI 使用说明

- **作者**：汪亮（bertonwang） · [47608843@qq.com](mailto:47608843@qq.com)
- **AI 使用说明**：本教材的知识框架、正文、Python 建模示例与参考资料清单在 AI 辅助下整理生成，并经人工校订、实际运行与静态自检；公式、数值与运行结果请以 Python 3 实际输出及权威教材、官方文档为准。发现错漏欢迎通过上方邮箱勘误。

## 许可证

本仓库目前**未附带 `LICENSE` 文件**，尚未声明开源许可证。个人学习与课堂教学可直接阅读、使用页面内容；转载、二次分发或商业使用前请先联系作者。外部参考资料与工具的版权归各自维护者所有。

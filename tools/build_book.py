#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""静态教材生成器：从结构化章节数据生成全部 HTML 与 assets/toc.js。

单一数据源：
  tools/book_data.py        -> CHAPTERS（正文与 Python 实例，分散在 chapters_*.py）
  tools/book_schema.py      -> PARTS（分部与五个学习阶段）
  tools/book_resources.py   -> R / TOPIC_RULES / CHAPTER_RESOURCES（链接库）

用法:
  python3 tools/build_book.py            # 生成缺失的章节页（总目录与 toc.js 总是重建）
  python3 tools/build_book.py --force    # 全部重建（会覆盖手工修改的章节页）
  python3 tools/build_book.py --list     # 列出章节清单
"""
from __future__ import annotations

import argparse
import html as html_mod
import json
import pathlib
import posixpath
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from book_schema import (BOOK_TITLE, SUBTITLE, VERSION, PARTS, PART_BY_ID,  # noqa: E402
                         STAGE_CLASS, STAGE_SHORT, DEMO_CONTRACT)
from book_data import (CHAPTERS, BY_ID, chapters_of, demo_count,  # noqa: E402
                       link_count)
from book_resources import (R, anchor, links_for_point, chapter_links_html,  # noqa: E402
                            all_resources_html, resource_card)

STATUS_LABEL = {"done": "已完稿", "skeleton": "框架待补", "todo": "待建"}

CREDITS_HTML = (
    '<p class="credits"><strong>作者</strong>：汪亮（bertonwang）　'
    '<strong>联系邮箱</strong>：<a href="mailto:47608843@qq.com">47608843@qq.com</a></p>\n'
    '<p class="ai-note"><strong>AI 使用说明</strong>：本教材的知识框架、正文、Python 建模示例与'
    '参考资料清单在 AI 辅助下整理生成，并经人工校订、实际运行与静态自检。公式、数值与运行结果请以'
    'Python 3 实际输出及权威教材、官方文档为准；发现错漏欢迎通过上方邮箱勘误。</p>'
)

RESOURCE_KEYS = [
    "core-econ", "openstax", "mit-ocw", "causal-book", "mixtape",
    "statsmodels", "fred", "worldbank", "french", "numpy",
    "jupyter", "nber",
]

STAGE_NOTES = {
    "第一阶段 · 个体、市场与效率": "第 00～14 章。把「选择」写成可解的约束最优化，再研究多人同时选择时的均衡、效率与失灵。",
    "第二阶段 · 总量、货币与增长": "第 15～19 章。把加总当作新问题：核算恒等式、短期波动、政策规则、长期增长与开放经济。",
    "第三阶段 · 数据与因果识别": "第 20～25 章。从已知真值的 DGP 出发，手写 OLS、稳健推断、IV、DID 与时间序列。",
    "第四阶段 · 不确定性与资产定价": "第 26～30 章。收益建模、组合优化、因子定价、债券久期与无套利期权定价。",
    "第五阶段 · 综合与方法论": "第 31～32 章与附录。多重检验、复现规范，以及一次端到端的政策评估流水线。",
}

REF_RE = re.compile(r"\{\{ch:([0-9]{2}|A)\}\}")


def esc(s):
    return html_mod.escape(str(s), quote=False)


def li(items):
    return "\n".join("<li>" + x + "</li>" for x in items)


def lih(items):
    """含 <code> 等行内标记的列表项：直接输出 HTML。"""
    return "\n".join("<li>" + x + "</li>" for x in items)


def head(title, root, index=False):
    title_text = (BOOK_TITLE + " · 总目录") if index else (esc(title) + " | " + BOOK_TITLE)
    return [
        "<!DOCTYPE html>", '<html lang="zh-CN">', "<head>", '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>" + title_text + "</title>",
        '<link rel="stylesheet" href="' + root + 'assets/style.css">',
        '<script src="' + root + 'assets/toc.js" defer></script>',
        '<script src="' + root + 'assets/app.js" defer></script>',
        "</head>",
    ]


def footer(root="../../"):
    out = []
    if root != "./":
        out.append('<footer class="pager" data-autofill></footer>')
    out += ['<footer class="site-foot">', CREDITS_HTML,
            '<p class="imprint">' + BOOK_TITLE +
            ' · 每章一个 <code>code/*.py</code> 建模脚本（由 <code>tools/extract_code.py</code> 从 HTML 同步）'
            ' · 只用 Python 3 标准库 · 外部参考资料均为各维护者的项目，本书与之无从属关系。</p>',
            "</footer>", "</main>", "</body>", "</html>"]
    return out


def resolve_refs(text, root="./", start=""):
    """把 {{ch:NN}} / {{home}} / {{home#anchor}} 占位符解析成正确的相对链接。"""
    def repl(m):
        cid = m.group(1)
        target = BY_ID.get(cid)
        if target is None:
            raise KeyError("章节内链指向不存在的章节: " + cid)
        rel = posixpath.relpath(target["folder"] + "/index.html", start=start or ".")
        label = ("附录 A · " + target["title"]) if cid == "A" else (
            "第 " + cid + " 章 · " + target["title"])
        return "<a href='" + rel + "'>" + esc(label) + "</a>"
    text = REF_RE.sub(repl, text)
    for token, href, label in (
        ("{{home#roadmap}}", root + "index.html#roadmap", "全书学习路线"),
        ("{{home#toc}}", root + "index.html#toc", "全书目录"),
        ("{{home#howto}}", root + "index.html#howto", "使用说明"),
        ("{{home#contribute}}", root + "index.html#contribute", "维护约定"),
        ("{{home#resources}}", root + "index.html#resources", "参考资源"),
        ("{{home}}", root + "index.html", "总目录"),
    ):
        text = text.replace(token, "<a href='" + href + "'>" + label + "</a>")
    return text


# ---------------------------------------------------------------- 目录数据
def toc_js_text():
    parts = []
    for p in PARTS:
        parts.append({
            "id": p["id"], "title": p["title"], "stage": p["stage"],
            "chapters": [
                {"id": c["id"], "title": c["title"],
                 "path": c["folder"] + "/index.html", "status": c["status"]}
                for c in chapters_of(p["id"])
            ],
        })
    data = {"title": BOOK_TITLE, "subtitle": SUBTITLE, "parts": parts}
    flat = (
        "window.BOOK_FLAT = (function () {\n"
        "  const out = [];\n"
        "  (window.BOOK_TOC.parts || []).forEach(function (part) {\n"
        "    (part.chapters || []).forEach(function (ch) {\n"
        "      out.push(Object.assign({ partId: part.id, partTitle: part.title }, ch));\n"
        "    });\n"
        "  });\n"
        "  return out;\n"
        "})();\n"
    )
    return ("/* 由 tools/build_book.py 生成，请勿手工编辑。\n"
            "   目录、侧栏、面包屑、上下章导航共用这一份数据。 */\n"
            "window.BOOK_TOC = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n\n" + flat)


def toc_entry(c):
    path = c["folder"] + "/index.html"
    out = ["<li>", '<div class="toc-head"><span class="num">' + c["id"] + "</span>"
           '<a class="toc-title" href="' + path + '">' + esc(c["title"]) + "</a> "
           '<a class="toc-extra" href="' + path + '#extra-links">扩展阅读 →</a>'
           '<span class="badge ' + c["status"] + '">' + STATUS_LABEL[c["status"]] + "</span></div>",
           '<p class="toc-desc">' + c["lede"] + "</p>",
           '<ul class="toc-points">' + "".join("<li>" + esc(p) + "</li>" for p in c["points"]) + "</ul>",
           "</li>"]
    return "\n".join(out)


def toc_html():
    out = []
    last_stage = ""
    for p in PARTS:
        stage = p["stage"]
        if stage != last_stage:
            later = "" if stage.startswith(("第一", "第二")) else " later"
            out.append('<div class="stage-banner' + later + '"><h2>' + esc(stage) + "</h2>"
                       "<p>" + esc(STAGE_NOTES.get(stage, "")) + "</p></div>")
            last_stage = stage
        pid = "卷首" if p["key"] == "pre" else ("附录" if p["key"] == "appendix"
                                             else p["title"].split(" · ")[0])
        out.append('<section class="toc-part"><h2><span class="part-id">' + pid + "</span>" +
                   esc(p["title"].split(" · ", 1)[-1]) + "</h2>")
        out.append('<ul class="toc-list">')
        out.extend(toc_entry(c) for c in chapters_of(p["id"]))
        out.append("</ul></section>")
    return "\n".join(out)


def resource_cards():
    out = ['<div class="repo-grid">']
    for k in RESOURCE_KEYS:
        name, url, desc, cat = R[k]
        out.append('<div class="repo-card"><h3>' + anchor(k, name) + "</h3>"
                   '<span class="tag">' + esc(cat) + "</span>"
                   "<p>" + esc(desc) + "</p>"
                   '<p style="margin:0"><code>' + esc(url) + "</code></p></div>")
    out.append("</div>")
    return "\n".join(out)


def render_index():
    out = head("", "./", index=True)
    out.append('<body data-root="./" data-page="index">')
    out.append('<aside id="sidebar"></aside>')
    out.append('<main class="book-page">')
    out.append('<nav class="breadcrumb" data-autofill>总目录</nav>')
    out.append('<header class="chapter-head">')
    out.append('<span class="kicker">Undergraduate → Graduate · Principles / Micro / Macro / Metrics / Finance</span>')
    out.append("<h1>" + BOOK_TITLE + "</h1>")
    out.append('<p class="lede">一本面向计算机专业背景、面向本科到研究生的经济学教材。'
               '全书不按课程拼盘，而沿<strong>稀缺 → 选择 → 均衡 → 效率 → 失灵 → 动态 → 不确定 → 证据 → 决策</strong>'
               '一条主线展开：原理、微观、宏观、计量与投资是同一个问题在不同约束下的放大。'
               '每章给出原理、公式、可运行的 Python 建模脚本与可核对的数值输出。</p>')
    out.append('<div class="meta">')
    out.append('<span class="badge done">全部 ' + str(len(CHAPTERS) - 1) + ' 章已完稿</span>')
    out.append('<span class="badge done">每章配可运行 Python 实例</span>')
    out.append("<span>共 " + str(len(CHAPTERS) - 1) + " 章 · 5 个学习阶段 · 1 附录 · " +
               str(demo_count()) + " 个 Python 实例 · " + str(link_count()) + " 条参考链接</span>")
    out.append("<span>版本 " + VERSION + "</span>")
    out.append("</div></header>")

    out.append('<div class="card note"><span class="card-label">本书的主张</span>'
               '<p><strong>四种数学骨架反复出现</strong>：约束最优化（消费者、企业、组合）、'
               '不动点（均衡、纳什、稳态）、条件期望（回归、资产定价）、反事实（因果推断、政策评估、期权 payoff）。'
               '认出骨架，五门课就变成五种应用配置。</p>'
               '<p style="margin-bottom:0">每章学习闭环固定为四步：'
               '<strong>读模型 → 跑代码 → 改参数 → 写结论</strong>；'
               '每个脚本都用已知真值的数据生成过程，把估计结果和真值并列打印，相当于带答案的单元测试。</p></div>')

    out.append('<h2 id="howto">如何使用这本教材</h2>')
    out.append('<table><thead><tr><th style="width:24%">栏目</th><th>作用</th></tr></thead><tbody>'
               '<tr><td>本章位置 / 给程序员的翻译</td><td>说明承接什么、引出什么，并把概念映射到计算概念</td></tr>'
               '<tr><td>学习目标</td><td>学完应能做什么，用可检验的动词描述</td></tr>'
               '<tr><td>知识点地图</td><td>逐条列出知识点，每条挂 1～2 个扩展学习链接</td></tr>'
               '<tr><td>原理小节 §x.y</td><td>概念、直觉、公式推导、对照表与常见边界</td></tr>'
               '<tr><td>Python 建模实例</td><td>完整可运行脚本 + 操作步骤 + 预期数值与判读逻辑</td></tr>'
               '<tr><td>本章参考资料</td><td>按本章知识点挑选的教材、课程、数据与工具卡片</td></tr>'
               '<tr><td>常见误区 / 习题</td><td>典型错误与可动手验证的思考题</td></tr>'
               '<tr><td>扩展学习</td><td>精读清单、论文/课程检索入口与全书资源总表</td></tr>'
               '</tbody></table>')

    out.append('<h2 id="python">运行 Python 示例（30 秒）</h2>')
    out.append('<ol>'
               '<li>需要 Python 3.8+，<strong>不需要安装任何第三方包</strong>：'
               '示例只用 <code>math</code>、<code>random</code>、<code>statistics</code> 等标准库。</li>'
               '<li>直接运行某一章脚本：<code>python3 part1/04-supply-demand/code/04-supply-demand.py</code>；'
               '或从页面代码块右上角「复制」。</li>'
               '<li>批量验证全部示例：<code>./tools/run_python.sh</code>；'
               '只跑某几个：<code>./tools/run_python.sh part4/21-ols/code/21-ols.py</code>。</li>'
               '<li>页面里的代码块与磁盘上的 <code>code/*.py</code> 由 '
               '<code>tools/extract_code.py</code> 自动同步，永远一致。</li>'
               '</ol>')
    out.append('<div class="card contract"><span class="card-label">给程序员的代码契约</span>'
               '<ul style="margin-bottom:0">'
               '<li><strong>零依赖</strong>：矩阵求逆、OLS、稳健标准误、二叉树定价全部手写展开，方便对照公式。</li>'
               '<li><strong>自包含</strong>：数据由脚本里的「数据生成过程」合成，不下载、不读外部文件。</li>'
               '<li><strong>可复现</strong>：固定 <code>random.seed(7)</code>；参数集中在 <code># ---- 参数区 ----</code>。</li>'
               '<li><strong>数值可核对</strong>：结尾 <code>print</code> 打印可手算的量，页面给出预期值与判读。</li>'
               '<li><strong>可批量验证</strong>：<code>./tools/run_python.sh</code> 跑完全部脚本；'
               '<code>python3 tools/check_book.py --run</code> 把实跑纳入自检。</li>'
               '</ul></div>')
    out.append('<p class="code-hint">为什么不用 <code>numpy</code> / <code>statsmodels</code>？'
               '因为教材要展示的是算法本身。附录 A.5 给出手写实现与工业库的对照表，'
               '学完之后应能无缝切换到成熟工具。</p>')

    out.append('<h2 id="roadmap">学习路线（建议两个学期）</h2>')
    out.append('<ol class="roadmap">'
               '<li><strong>第一阶段 · 个体、市场与效率</strong>（00～14）：约束最优化、供需与弹性、'
               '消费者/生产者、贸易与风险、福利定理、垄断与博弈、外部性与信息、一般均衡。</li>'
               '<li><strong>第二阶段 · 总量、货币与增长</strong>（15～19）：国民账户、乘数与 IS-LM、'
               '泰勒规则、索洛稳态、国际收支与汇率。</li>'
               '<li><strong>第三阶段 · 数据与因果识别</strong>（20～25）：潜在结果 → 手写 OLS → '
               '稳健标准误 → IV/2SLS → DID 与固定效应 → 平稳性与伪回归。</li>'
               '<li><strong>第四阶段 · 不确定性与资产定价</strong>（26～30）：收益与复利 → 有效前沿 → '
               'CAPM 与因子 → 久期与期限结构 → 二叉树 / Black-Scholes / 蒙特卡洛。</li>'
               '<li><strong>第五阶段 · 综合与方法论</strong>（31～32、附录）：多重检验与复现规范，'
               '最后用一个端到端政策评估课题把全部环节跑通。</li>'
               '</ol>')
    out.append('<p>时间有限时的最短路径：<a href="part0/01-math-tools/index.html">01</a> → '
               '<a href="part1/04-supply-demand/index.html">04</a> → '
               '<a href="part2/09-welfare/index.html">09</a> → '
               '<a href="part4/20-identification/index.html">20</a> → '
               '<a href="part4/21-ols/index.html">21</a> → '
               '<a href="part4/24-did-panel/index.html">24</a> → '
               '<a href="part5/27-portfolio/index.html">27</a> → '
               '<a href="part5/30-options/index.html">30</a> → '
               '<a href="part6/32-capstone/index.html">32</a>。</p>')

    out.append('<h2 id="toc">全书目录</h2>')
    out.append('<p class="lede">每一章一个文件夹，内含 <code>index.html</code>（知识讲解）与 '
               '<code>code/*.py</code>（可直接运行的建模脚本）。状态徽章：<span class="badge done">已完稿</span> '
               '表示正文、知识点地图、参考链接与实例齐备。</p>')
    out.append(toc_html())

    out.append('<h2 id="resources">参考资源</h2>')
    out.append('<p class="lede">以下为全书高频引用的开放教材、课程、数据与工具；'
               '完整清单（含百科条目与机构链接）见<a href="appendix/index.html">附录 A.7 扩展学习链接总表</a>。</p>')
    out.append(resource_cards())

    out.append('<h2 id="contribute">维护约定</h2>')
    out.append('<p>全书由结构化数据生成，<strong>不要直接编辑章节 HTML</strong>，'
               '否则下次重建会被覆盖。改完数据后依次运行：'
               '<code>python3 tools/build_book.py --force</code> → '
               '<code>python3 tools/extract_code.py</code> → '
               '<code>python3 tools/check_book.py --run</code>。</p>')
    out.append('<table><thead><tr><th style="width:28%">想改什么</th><th>编辑哪里</th></tr></thead><tbody>'
               '<tr><td>细化某章正文或 Python 示例</td><td><code>tools/chapters_*.py</code> 中对应的 <code>C(...)</code></td></tr>'
               '<tr><td>加参考资料链接</td><td><code>tools/book_resources.py</code> 的 '
               '<code>R</code>、<code>TOPIC_RULES</code>、<code>CHAPTER_RESOURCES</code>，以及章节的 <code>highlights</code></td></tr>'
               '<tr><td>调整页面结构与总目录</td><td><code>tools/build_book.py</code> 的 <code>render()</code> / <code>render_index()</code></td></tr>'
               '<tr><td>样式与交互</td><td><code>assets/style.css</code>、<code>assets/app.js</code></td></tr>'
               '<tr><td>新增章节或分篇</td><td><code>tools/book_schema.py</code> 的 <code>PARTS</code> + 对应 '
               '<code>chapters_*.py</code>，再重建（<code>toc.js</code> 会自动同步）</td></tr>'
               '<tr><td>验证全部示例</td><td><code>./tools/run_python.sh</code> 或 <code>python3 tools/check_book.py --run</code></td></tr>'
               '</tbody></table>')

    out.extend(footer("./"))
    return resolve_refs("\n".join(out) + "\n", root="./", start="")


# ---------------------------------------------------------------- 章节页
def appendix_sections(ch):
    """附录 A.5 / A.7 由全书数据动态生成，保证与其它章节永远一致。"""
    rows = []
    for c in CHAPTERS:
        for d in c["demos"]:
            rel = "../" + c["folder"] + "/" + d["file"]
            label = "附录 A" if c["id"] == "A" else ("第 " + c["id"] + " 章")
            rows.append("<tr><td>" + label + " · " + esc(c["title"]) +
                        "</td><td><a href='" + rel + "'><code>" + esc(d["file"]) + "</code></a></td><td>" +
                        esc(d["title"]) + "</td></tr>")
    a5 = ("<p>全书 " + str(demo_count()) + " 个建模脚本，全部只用 Python 3 标准库、固定 "
          "<code>random.seed(7)</code>，参数集中在「参数区」，结尾打印可核对的数值。"
          "点击文件名可直接查看源码。</p>"
          '<table><thead><tr><th style="width:34%">章节</th><th style="width:30%">脚本</th>'
          '<th>演示内容</th></tr></thead><tbody>' + "\n".join(rows) + "</tbody></table>" +
          "<h3>手写实现 → 工业库对照</h3>" +
          '<table><thead><tr><th style="width:34%">本书手写</th><th>工业实现</th><th>对应章节</th></tr></thead><tbody>'
          '<tr><td>高斯-约当求逆 / XᵀX 累加</td><td><code>numpy.linalg.solve</code>、<code>numpy.dot</code></td><td>21、28</td></tr>'
          '<tr><td>OLS / 标准误 / t 值</td><td><code>statsmodels.OLS(...).fit()</code></td><td>21、28</td></tr>'
          '<tr><td>三明治稳健协方差</td><td><code>fit(cov_type="HC0")</code> / <code>cluster</code></td><td>22、32</td></tr>'
          '<tr><td>IV / 2SLS 两阶段</td><td><code>linearmodels.IV2SLS</code></td><td>23</td></tr>'
          '<tr><td>面板组内去均值 / DID</td><td><code>linearmodels.PanelOLS</code></td><td>24、32</td></tr>'
          '<tr><td>ADF / 协整</td><td><code>statsmodels.tsa.stattools</code></td><td>25</td></tr>'
          '<tr><td>组合前沿 / 协方差矩阵</td><td><code>numpy</code> + <code>scipy.optimize</code></td><td>27</td></tr>'
          '<tr><td>二项树 / 蒙特卡洛</td><td><code>numpy</code> 向量化、<code>QuantLib</code></td><td>30</td></tr>'
          "</tbody></table>")
    sections = list(ch["sections"])
    sections.append(("A.5", "Python 示例索引与工业库对照", a5))
    sections.append(("A.7", "扩展学习链接总表", all_resources_html()))
    return sorted(sections, key=lambda x: x[0])


def render(ch):
    folder = pathlib.PurePosixPath(ch["folder"])
    depth = len(folder.parts)
    root = "../" * depth
    part = PART_BY_ID[ch["part"]]
    is_appendix = ch["id"] == "A"
    chapter_attr = ' data-chapter="' + ch["id"] + '"'
    if is_appendix:
        chapter_attr += ' data-page="appendix"'
    head_title = ("附录 A · " + ch["title"]) if is_appendix else ("第 " + ch["id"] + " 章 · " + ch["title"])

    out = head(head_title, root)
    out.append('<body data-root="' + root + '"' + chapter_attr + ">")
    out.append('<aside id="sidebar"></aside>')
    out.append('<main class="book-page">')
    if is_appendix:
        out.append('<nav class="breadcrumb"><a href="' + root + 'index.html">总目录</a> / 附录</nav>')
    else:
        out.append('<nav class="breadcrumb" data-autofill>总目录</nav>')

    out.append('<header class="chapter-head">')
    out.append('<span class="kicker">' + esc(part["title"]) + " · " + esc(part["stage"]) + "</span>")
    label = "附录 A" if is_appendix else ("第 " + ch["id"] + " 章")
    out.append('<h1><span class="ch-num">' + label + "</span>" + esc(ch["title"]) + "</h1>")
    out.append('<p class="lede">' + ch["lede"] + "</p>")
    out.append('<div class="meta">')
    out.append('<span class="badge ' + ch["status"] + '">' + STATUS_LABEL[ch["status"]] + "</span>")
    out.append('<span class="badge ' + STAGE_CLASS[ch["part"]] + '">' +
               esc(STAGE_SHORT[ch["part"]]) + "</span>")
    out.append("<span>建议 " + esc(ch["hours"]) + "</span>")
    if is_appendix:
        out.append("<span>全书速查入口</span>")
    else:
        out.append("<span>" + str(len(ch["demos"])) + " 个 Python 实例</span>")
    out.append("<span>" + BOOK_TITLE + "</span>")
    out.append("</div></header>")

    out.append('<p class="bridge"><strong>本章位置：</strong>' + ch["bridge"] + "</p>")
    out.append('<div class="analogy"><span class="card-label">给程序员的翻译</span>'
               '<p style="margin-bottom:0">' + ch["analogy"] + "</p></div>")

    if ch["goals"]:
        out.append('<div class="card objectives"><span class="card-label">学习目标</span><ul>')
        out.append(lih(ch["goals"]))
        out.append("</ul></div>")

    out.append('<section id="map"><h2><span class="sec-num">§</span>知识点地图</h2>')
    out.append('<p class="code-hint">每个知识点都配了 1～2 个扩展学习链接；'
               '本章完整资源清单见 <a href="#extra-links">扩展学习</a>。</p>')
    out.append('<table><thead><tr><th style="width:44px">#</th><th style="width:26%">知识点</th>'
               '<th>扩展学习</th><th style="width:100px">状态</th></tr></thead><tbody>')
    for i, p in enumerate(ch["points"], 1):
        out.append("<tr><td>" + str(i) + "</td><td>" + esc(p) + "</td><td>" +
                   links_for_point(ch["id"], p) + "</td><td>正文已覆盖</td></tr>")
    out.append("</tbody></table></section>")

    sections = appendix_sections(ch) if is_appendix else ch["sections"]
    for num, title, body in sections:
        out.append('<section id="s' + num.replace(".", "-") + '"><h2><span class="sec-num">§' +
                   num + "</span>" + esc(title) + "</h2>")
        out.append(body)
        out.append("</section>")

    if is_appendix:
        out.append('<section id="lab"><h2><span class="sec-num">§</span>全书实例与工具</h2>'
                   '<div class="card note"><p style="margin-bottom:0">附录不新增示例脚本；'
                   '全部可运行实例见 <a href="#sA-5">A.5 示例索引</a>。'
                   '生成、抽取、批量运行与自检命令见 {{home#contribute}}。</p></div></section>')
    else:
        out.append('<section id="lab"><h2><span class="sec-num">§</span>Python 建模实例</h2>')
        for s in ch["demos"]:
            out.append("<h3>" + esc(s["title"]) + "</h3>")
            out.append('<pre class="code" data-file="' + s["file"] +
                       '" data-lang="Python 3 · 标准库"><code>' + esc(s["code"]) + "</code></pre>")
            out.append('<p class="code-hint"><strong>操作：</strong>' + s["steps"] +
                       "　<strong>预期与判读：</strong>" + s["expect"] + "</p>")
            out.append('<p class="code-hint"><strong>改参数看趋势：</strong>' + s["params"] +
                       "　文件位置：<code>" + esc(ch["folder"] + "/" + s["file"]) + "</code></p>")
        out.append('<div class="card note"><p style="margin-bottom:0">代码块右上角可一键复制；'
                   '仓库里的 <code>code/*.py</code> 由 <code>tools/extract_code.py</code> 从这些代码块自动抽取。'
                   '脚本只用标准库、固定 <code>random.seed(7)</code>，'
                   '批量运行用 <code>./tools/run_python.sh</code>。</p></div>')
        out.append("</section>")

    if ch["highlights"]:
        out.append('<section id="highlights"><h2><span class="sec-num">§</span>本章参考资料</h2>'
                   '<p>按本章知识点挑选的精读资料；更多检索入口见 '
                   '<a href="#extra-links">扩展学习</a>。</p><div class="repo-grid">')
        out.extend(resource_card(k, why) for k, why in ch["highlights"])
        out.append("</div></section>")

    if ch["pitfalls"]:
        out.append('<section id="pitfalls"><h2><span class="sec-num">§</span>常见误区</h2>'
                   '<div class="card warn"><ul>' + lih(ch["pitfalls"]) + "</ul></div></section>")
    if ch["exercises"]:
        out.append('<section id="exercises"><h2><span class="sec-num">§</span>习题与思考</h2><ol>' +
                   lih(ch["exercises"]) + "</ol></section>")

    out.append('<section id="extra-links"><h2><span class="sec-num">§</span>扩展学习</h2>')
    out.append(chapter_links_html(ch["id"], root))
    out.append("</section>")
    if ch["further"]:
        out.append('<section id="further"><h2><span class="sec-num">§</span>延伸阅读与内链</h2><ul>' +
                   lih(ch["further"]) + "</ul></section>")

    out.extend(footer(root))
    return resolve_refs("\n".join(out) + "\n", root=root, start=ch["folder"])


# ---------------------------------------------------------------- 生成
def build(force=False):
    created, skipped = [], []
    toc_target = ROOT / "assets/toc.js"
    toc_target.write_text(toc_js_text(), encoding="utf-8")
    idx = ROOT / "index.html"
    idx.write_text(render_index(), encoding="utf-8")
    created += ["assets/toc.js", "index.html"]
    for ch in CHAPTERS:
        target = ROOT / ch["folder"] / "index.html"
        if target.exists() and not force:
            skipped.append(str(target.relative_to(ROOT)))
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render(ch), encoding="utf-8")
        created.append(str(target.relative_to(ROOT)))
    return created, skipped


def main():
    ap = argparse.ArgumentParser(description="生成经济学教材 HTML")
    ap.add_argument("--force", action="store_true", help="覆盖已存在的章节页（会丢失手工修改）")
    ap.add_argument("--list", action="store_true", help="只列出章节清单")
    args = ap.parse_args()
    if args.list:
        for ch in CHAPTERS:
            p = PART_BY_ID[ch["part"]]
            print(ch["id"].rjust(2), p["key"].ljust(10), ch["folder"].ljust(38), ch["title"])
        print("共 %d 章（含附录）/ %d 个 Python 实例 / %d 条参考链接" %
              (len(CHAPTERS), demo_count(), link_count()))
        return
    created, skipped = build(force=args.force)
    for p in created:
        print("生成", p)
    print("共 %d 个页面：新建/重建 %d，跳过 %d（章节页使用 --force 可重建）" %
          (len(CHAPTERS) + 1, len(created), len(skipped)))


if __name__ == "__main__":
    main()

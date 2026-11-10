#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全书分部、学习阶段与章节数据接口。

五个学习阶段把「原理 → 微观 → 宏观 → 计量 → 投资」串成一条主线：
    稀缺 → 选择 → 均衡 → 效率 → 失灵 → 动态 → 不确定 → 证据 → 决策
"""
from __future__ import annotations

BOOK_TITLE = "经济学：从稀缺到证据"
SUBTITLE = "本科到研究生 · 原理、微观、宏观、计量与投资的一条主线"
VERSION = "v0.1 · 2026-11"

S1 = "第一阶段 · 个体、市场与效率"
S2 = "第二阶段 · 总量、货币与增长"
S3 = "第三阶段 · 数据与因果识别"
S4 = "第四阶段 · 不确定性与资产定价"
S5 = "第五阶段 · 综合与方法论"

PARTS = [
    dict(id="p0", title="卷首 · 共同语言", stage=S1, key="pre", folder="part0"),
    dict(id="p1", title="第一篇 · 原理与个体决策", stage=S1, key="micro", folder="part1"),
    dict(id="p2", title="第二篇 · 市场结构、策略与失灵", stage=S1, key="micro", folder="part2"),
    dict(id="p3", title="第三篇 · 宏观、货币与增长", stage=S2, key="macro", folder="part3"),
    dict(id="p4", title="第四篇 · 计量经济学与因果推断", stage=S3, key="metrics", folder="part4"),
    dict(id="p5", title="第五篇 · 投资学、资产定价与风险管理", stage=S4, key="finance", folder="part5"),
    dict(id="p6", title="第六篇 · 方法论与综合课题", stage=S5, key="synthesis", folder="part6"),
    dict(id="pa", title="附录 · 速查与资源总表", stage=S5, key="appendix", folder="appendix"),
]
PART_BY_ID = {p["id"]: p for p in PARTS}


def C(cid, part, folder, title, lede, *, hours="2 学时", goals=(), points=(),
      sections=(), demos=(), highlights=(), analogy="", bridge="",
      pitfalls=(), exercises=(), further=(), status="done"):
    """一章的全部数据。

    bridge     : 本章在全书主线中的位置（承接什么、引出什么）
    analogy    : 把本章核心概念映射到程序员熟悉的计算概念
    sections   : [(编号, 标题, HTML 正文), ...]
    demos      : [demo(...), ...] 零依赖、自包含的 Python 建模脚本
    highlights : [(资源 key, 推荐理由), ...] 本章必读参考资料卡片
    """
    return dict(id=cid, part=part, folder=folder, title=title, lede=lede,
                status=status, hours=hours, goals=list(goals), points=list(points),
                sections=list(sections), demos=list(demos), highlights=list(highlights),
                analogy=analogy, bridge=bridge, pitfalls=list(pitfalls),
                exercises=list(exercises), further=list(further))


def demo(file, title, code, steps, expect, params=""):
    """一段只用 Python 标准库、可独立运行的建模脚本。

    file 形如 code/04-supply-demand.py；params 说明改哪个参数会看到什么趋势。
    """
    return dict(file=file, title=title, code=code.strip("\n"), steps=steps,
                expect=expect, params=params)


def eq(text):
    """把一行公式排版成等宽公式块；text 里可以写 Unicode 数学符号。"""
    import html as html_mod
    return '<p class="eq">' + html_mod.escape(text, quote=False) + "</p>"


def table(headers, rows, widths=()):
    """生成一张对照表，headers 为字符串列表，rows 为二维字符串列表（已是 HTML）。"""
    w = [' style="width:%s"' % widths[i] if i < len(widths) else ""
         for i in range(len(headers))]
    out = ["<table><thead><tr>" + "".join("<th" + w[i] + ">" + h + "</th>"
                                        for i, h in enumerate(headers)) + "</tr></thead><tbody>"]
    for row in rows:
        out.append("<tr>" + "".join("<td>" + cell + "</td>" for cell in row) + "</tr>")
    out.append("</tbody></table>")
    return "\n".join(out)


STAGE_CLASS = {"p0": "s1", "p1": "s1", "p2": "s1", "p3": "s2",
               "p4": "s3", "p5": "s4", "p6": "s5", "pa": "s5"}
STAGE_SHORT = {"p0": "共同语言", "p1": "原理 · 个体", "p2": "市场 · 策略", "p3": "总量 · 增长",
               "p4": "数据 · 因果", "p5": "定价 · 决策", "p6": "方法论 · 综合", "pa": "速查 · 附录"}


# 所有示例共用的脚本骨架说明（写在页面里，代码里不强制重复）
DEMO_CONTRACT = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"本章建模实例：只用标准库；随机种子固定；结尾打印可手算核对的数值。\"\"\"
import math, random, statistics
random.seed(7)
# ---- 参数区：所有可调量集中在这里 ----
# ---- 模型 / 数据生成 ----
# ---- 算法：估计、求解或模拟 ----
# ---- 数值验证：打印可核对的量 ----
"""

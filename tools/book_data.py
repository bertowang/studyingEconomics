#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全书章节数据的唯一汇总入口。

正文分散在 chapters_*.py 七个文件里便于定位；build_book.py / check_book.py
都只从这里取 CHAPTERS。本文件同时做数据层面的基本一致性校验。
"""
from __future__ import annotations

from chapters_00_04 import CH as CH_00_04
from chapters_05_09 import CH as CH_05_09
from chapters_10_14 import CH as CH_10_14
from chapters_15_19 import CH as CH_15_19
from chapters_20_25 import CH as CH_20_25
from chapters_26_30 import CH as CH_26_30
from chapters_31_A import CH as CH_31_A
from book_schema import PARTS, PART_BY_ID
from book_resources import R, CHAPTER_RESOURCES

CHAPTERS = (CH_00_04 + CH_05_09 + CH_10_14 + CH_15_19 +
            CH_20_25 + CH_26_30 + CH_31_A)
BY_ID = {ch["id"]: ch for ch in CHAPTERS}

BANNED_IMPORTS = ("import numpy", "import pandas", "import scipy",
                  "import statsmodels", "import matplotlib", "from numpy",
                  "from pandas", "from scipy", "from statsmodels")
REQUIRED_TOKENS = ("#!/usr/bin/env python3", "random.seed(7)", "参数区", "print(")


def problems():
    """返回数据层面的问题列表，供自检脚本使用。"""
    out = []
    ids = [c["id"] for c in CHAPTERS]
    folders = [c["folder"] for c in CHAPTERS]
    if len(ids) != len(set(ids)):
        out.append("章节 id 重复")
    if len(folders) != len(set(folders)):
        out.append("章节目录重复")
    demo_files = []
    for ch in CHAPTERS:
        cid = ch["id"]
        p = PART_BY_ID.get(ch["part"])
        if not p:
            out.append("未知分部: " + cid)
            continue
        if not (ch["folder"] == p["folder"] or
                ch["folder"].startswith(p["folder"] + "/")):
            out.append("章节目录与分部不匹配: " + cid + " -> " + ch["folder"])
        if ch["status"] != "done":
            out.append("章节状态不是 done: " + cid)
        for field in ("goals", "points", "sections", "pitfalls", "exercises", "further"):
            if not ch[field]:
                out.append("章节缺少 %s: %s" % (field, cid))
        if not ch["bridge"] or not ch["analogy"]:
            out.append("章节缺少承接或程序员类比: " + cid)
        if cid not in CHAPTER_RESOURCES:
            out.append("参考链接库缺少章节: " + cid)
        for key, _why in ch["highlights"]:
            if key not in R:
                out.append("未知参考资源 key [%s]: %s" % (key, cid))
        if cid != "A":
            if not ch["demos"]:
                out.append("章节缺少 Python 建模实例: " + cid)
        for d in ch["demos"]:
            code = d["code"]
            demo_files.append((cid, d["file"]))
            if not d["file"].startswith("code/") or not d["file"].endswith(".py"):
                out.append("示例文件名不规范: %s -> %s" % (cid, d["file"]))
            for token in REQUIRED_TOKENS:
                if token not in code:
                    out.append("示例缺少 %s: %s -> %s" % (token, cid, d["file"]))
            for banned in BANNED_IMPORTS:
                if banned in code:
                    out.append("示例使用了第三方依赖 %s: %s" % (banned, d["file"]))
            try:
                compile(code, d["file"], "exec")
            except SyntaxError as e:
                out.append("示例语法错误 %s: %s" % (d["file"], e))
    files = [f for _cid, f in demo_files]
    if len(files) != len(set(files)):
        out.append("示例文件名重复")
    return out


def chapters_of(part_id):
    return [c for c in CHAPTERS if c["part"] == part_id]


def demo_count():
    return sum(len(c["demos"]) for c in CHAPTERS)


def link_count():
    return len(R)


if __name__ == "__main__":
    print("章节数:", len(CHAPTERS), "| Python 实例:", demo_count(), "| 外部资源:", link_count())
    for p in PARTS:
        print(p["id"], p["title"], "->", len(chapters_of(p["id"])), "章")
    for x in problems():
        print("问题:", x)

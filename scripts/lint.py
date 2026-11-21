"""腳本 lint：AGENTS.md 第 7 節第 1-6 項。全過 exit 0，否則 exit 1。
報告同時寫到 reports/lint-時間.md，作為檢查紀錄。
用法：python3 scripts/lint.py
"""
import re, sys, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI, RAW = ROOT / "wiki", ROOT / "raw"
CITE = re.compile(r"\[src:\s*([\w-]+)\s+((?:¶\d+(?:-\d+)?(?:,\s*)?)+)\]")
QUOTE = re.compile(r"[\"“]([^\"“”]+)[\"”]\s*\[src:\s*([\w-]+)\s+((?:¶\d+(?:-\d+)?(?:,\s*)?)+)\]")
LINK = re.compile(r"\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]")

def norm(t):
    for a, b in [("‘", "'"), ("’", "'"), ("“", '"'), ("”", '"'), ("﻿", ""), ("‑", "-"), ("…", "..."), ("*", ""), ("_", "")]:
        t = t.replace(a, b)
    return re.sub(r"\s+", " ", t).strip()

def paras(spec):
    out = []
    for part in re.findall(r"¶(\d+)(?:-(\d+))?", spec):
        a = int(part[0]); b = int(part[1]) if part[1] else a
        out += list(range(a, b + 1))
    return out

def load_raw():
    raw = {}
    for f in (RAW / "potter").glob("*.md"):
        d = {}
        for line in f.read_text(encoding="utf-8").splitlines():
            m = re.match(r"¶(\d+) (.*)", line)
            if m:
                d[int(m.group(1))] = norm(re.sub(r"^〔[^〕]+〕 ", "", m.group(2)))
        raw[f.stem] = d
    return raw

def main():
    raw = load_raw()
    sources_txt = (WIKI / "sources.md").read_text(encoding="utf-8")
    src_ids = set(re.findall(r"^\| `([\w-]+)` \|", sources_txt, re.M))
    pages = {p.stem: p for p in WIKI.rglob("*.md")}
    texts = {k: p.read_text(encoding="utf-8") for k, p in pages.items()}
    fails = {i: [] for i in range(1, 7)}; warns = []; nq = nc = 0

    for name, t in texts.items():
        if name in ("log", "sources"):
            continue
        rel = pages[name].relative_to(ROOT)
        for m in CITE.finditer(t):
            nc += 1; sid = m.group(1)
            if sid not in src_ids or sid not in raw:
                fails[2].append(f"{rel}: 短 ID `{sid}` 不在 sources.md 或 raw/potter/"); continue
            for n in paras(m.group(2)):
                if n not in raw[sid]:
                    fails[2].append(f"{rel}: `{sid} ¶{n}` 段落不存在（該篇只有 ¶1-¶{max(raw[sid])}）")
        for m in QUOTE.finditer(t):
            nq += 1; sid = m.group(2)
            if sid not in raw:
                continue
            body = " ".join(raw[sid].get(n, "") for n in paras(m.group(3)))
            for seg in [s.strip() for s in norm(m.group(1)).split("...") if s.strip()]:
                if seg not in body:
                    fails[1].append(f"{rel}: 引句片段「{seg}」不在 `{sid} {m.group(3)}`")
        if pages[name].is_relative_to(WIKI / "books"):
            body_lines = t.split("---", 2)[-1].splitlines()
            for i, line in enumerate(body_lines):
                s = line.strip()
                if s.startswith(("-", "*")) and len(s) > 12 and "[src:" not in s and "[[" not in s:
                    warns.append(f"{rel}: 可能缺出處 → {s[:60]}")

    inbound = {k: set() for k in pages}
    for name, t in texts.items():
        for m in LINK.finditer(t):
            tgt = m.group(1).strip()
            if tgt not in pages:
                fails[3].append(f"{pages[name].relative_to(ROOT)}: [[{tgt}]] 指向不存在的頁面")
            elif name not in ("index", tgt):
                inbound[tgt].add(name)
    for k, p in pages.items():
        if p.is_relative_to(WIKI / "books") and not inbound[k]:
            fails[4].append(f"{p.relative_to(ROOT)}: 孤兒頁（除 index 外沒有任何頁面連到它）")
    idx_links = {m.group(1).strip() for m in LINK.finditer(texts.get("index", ""))}
    for k, p in pages.items():
        if k != "index" and k not in idx_links:
            fails[5].append(f"{p.relative_to(ROOT)}: 沒有列在 index.md")
    for sid in raw:
        if sid not in src_ids:
            fails[6].append(f"raw/potter/{sid}.md: sources.md 沒有版權紀錄")
    for f in (RAW / "original").iterdir():
        if f.name not in sources_txt:
            fails[6].append(f"raw/original/{f.name}: sources.md 沒有紀錄")

    names = {1: "英文引句在所標段落找得到", 2: "出處 ID 與段落存在", 3: "連結不斷", 4: "沒有孤兒頁",
             5: "index.md 列出所有頁面", 6: "raw/ 都有版權紀錄"}
    ok = not any(fails.values())
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
    out = [f"# Lint 報告 {now}", "", f"結果：{'✅ 全部通過' if ok else '❌ 有失敗項目'}",
           f"檢查範圍：{len(pages)} 個 wiki 頁面、{nc} 個出處、{nq} 個英文引句", "",
           "| # | 項目 | 結果 |", "|---|---|---|"]
    out += [f"| {i} | {names[i]} | {'✅' if not fails[i] else '❌ ' + str(len(fails[i])) + ' 處'} |" for i in names]
    for i in names:
        if fails[i]:
            out += ["", f"## 第 {i} 項失敗：{names[i]}"] + [f"- {x}" for x in fails[i]]
    if warns:
        out += ["", "## 提醒（不算失敗，請人工判斷）"] + [f"- {x}" for x in warns]
    report = "\n".join(out) + "\n"
    (ROOT / "reports").mkdir(exist_ok=True)
    (ROOT / "reports" / f"lint-{now.replace(' ', '_').replace(':', '')}.md").write_text(report, encoding="utf-8")
    print(report)
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()

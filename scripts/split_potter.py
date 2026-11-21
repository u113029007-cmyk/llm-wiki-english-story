"""把 Standard Ebooks《Short Fiction》epub 切成每篇一個 raw 檔，段落以 ¶ 編號。
原文文字一字不改（只把換行與多個空白合成一個空白）。插圖複製到 raw/assets/potter/，
並產生 images.md：圖檔 ↔ 篇 ↔ 前後段落。alt 文字是 Standard Ebooks 製作者寫的描述（CC0），不是 Potter 原文。
用法：python3 scripts/split_potter.py
"""
import zipfile, re, shutil, sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EPUB = ROOT / "raw/original/beatrix-potter_short-fiction.epub"
OUT = ROOT / "raw/potter"
ASSETS = ROOT / "raw/assets/potter"
NS = "{http://www.w3.org/1999/xhtml}"
EPT = "{http://www.idpf.org/2007/ops}type"

def short_id(fname):
    s = fname.replace(".xhtml", "")
    for pre in ("the-tale-of-the-", "the-tale-of-", "the-story-of-a-", "the-story-of-", "the-"):
        if s.startswith(pre):
            return s[len(pre):]
    return s

def text_of(el):
    return re.sub(r"\s+", " ", "".join(el.itertext())).strip()

def walk(el, ctx, out):
    tag = el.tag.replace(NS, "")
    if tag == "section" and "dedication" in (el.get(EPT) or ""):
        ctx = "dedication"
    if tag == "blockquote" and "song" in (el.get(EPT) or ""):
        ctx = "song"
    if tag == "blockquote" and "epigraph" in (el.get(EPT) or ""):
        ctx = "epigraph"
    if tag == "hgroup":
        ctx = "subtitle"
    if tag == "p":
        out.append(("p", ctx, text_of(el)))
        return
    if tag == "img":
        out.append(("img", el.get("src").split("/")[-1], el.get("alt") or ""))
        return
    if tag in ("h2", "h3", "cite"):
        return
    for ch in el:
        walk(ch, ctx, out)

def main():
    OUT.mkdir(parents=True, exist_ok=True); ASSETS.mkdir(parents=True, exist_ok=True)
    z = zipfile.ZipFile(EPUB)
    toc = ET.fromstring(z.read("epub/toc.xhtml"))
    files = []
    for a in toc.iter(NS + "a"):
        href = a.get("href", "").split("#")[0]
        name = href.split("/")[-1]
        if name.startswith("the-") and name not in [f for f, _ in files]:
            files.append((name, text_of(a)))
    img_rows, summary = [], []
    for name, title in files:
        sid = short_id(name)
        root = ET.fromstring(z.read("epub/text/" + name))
        blocks = []; walk(root.find(f".//{NS}article"), "body", blocks)
        lines = [f"# {title}", "", f"- id: {sid}",
                 f"- source: Standard Ebooks, Beatrix Potter《Short Fiction》epub/text/{name}",
                 "- 由 scripts/split_potter.py 產生，請勿手動修改", ""]
        n = 0; words = 0
        for b in blocks:
            if b[0] == "p":
                n += 1; words += len(b[2].split())
                mark = {"dedication": "〔獻詞〕 ", "song": "〔歌謠〕 ", "epigraph": "〔題詞〕 ", "subtitle": "〔副標題〕 "}.get(b[1], "")
                lines.append(f"¶{n} {mark}{b[2]}"); lines.append("")
            else:
                img_rows.append((b[1], sid, n, n + 1, b[2]))
                data = z.read("epub/images/" + b[1])
                (ASSETS / b[1]).write_bytes(data)
        (OUT / f"{sid}.md").write_text("\n".join(lines), encoding="utf-8")
        summary.append((sid, title, n, words))
    rows = ["# 插圖對照表（由 scripts/split_potter.py 產生）", "",
            "alt 欄是 Standard Ebooks 製作者寫的圖片描述（CC0），不是 Potter 原文，不能當作故事事實引用。",
            "「前段」為 0 表示插圖在第一段之前。", "",
            "| 圖檔 | 篇 id | 前段 | 後段 | alt（SE 描述） |", "|---|---|---|---|---|"]
    rows += [f"| {f} | {s} | ¶{a} | ¶{b} | {alt.replace('|','/')} |" for f, s, a, b, alt in img_rows]
    (ASSETS / "images.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    for s in summary: print(*s, sep="\t")
    print("images", len(img_rows))

if __name__ == "__main__":
    main()

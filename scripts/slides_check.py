"""出處檢查（簡報逐頁稿）：依 .agents/workflows/topic-slides.md 的稿件格式檢查 slides/<主題>/drafts/。
全過 exit 0。報告附加到 slides/<主題>/report.md。用法：python3 scripts/slides_check.py <主題>
"""
import re, sys, datetime
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lint import norm
ROOT = Path(__file__).resolve().parent.parent
topic = sys.argv[1]
SD = ROOT / "slides" / topic
pages = {p.stem: p for p in (ROOT / "wiki").rglob("*.md")}
ptext = {k: norm(p.read_text(encoding="utf-8")) for k, p in pages.items()}
imgs = re.findall(r"^\| (illustration-\d+\.jpg) \| ([\w-]+) \|", (ROOT / "raw/assets/potter/images.md").read_text(encoding="utf-8"), re.M)
ok_imgs = {f for f, sid in imgs if sid == topic}
META_TYPES = {"cover", "agenda", "sources"}
fails = []; nb = nq = 0
files = sorted((SD / "drafts").glob("slide-*.md"))
for f in files:
    t = f.read_text(encoding="utf-8"); name = f.name
    typ = (re.search(r"^type: (\w+)", t, re.M) or [None, "content"])[1]
    if not re.match(r"^# \S", t): fails.append(f"{name}: 沒有標題")
    bullets = [l for l in t.splitlines() if l.startswith("- ")]
    content = typ in ("content", "map")
    limit = 4 if content else 5
    if len(bullets) > limit: fails.append(f"{name}: 條列 {len(bullets)} 條，超過 {limit} 條")
    if content:
        for b in bullets:
            if not re.match(r"^- [^｜]+ ｜ [\"“][^\"“”]+[\"”] \[wiki: [\w-]+\]$", b):
                fails.append(f"{name}: 內容頁條列必須是「中文 ｜ \"英文原文\" [wiki: 頁面]」→ {b[:50]}")
    for b in bullets:
        nb += 1
        m = re.search(r"\[wiki: ([\w-]+)\]\s*$", b)
        if not m:
            if b.rstrip().endswith("[meta]"):
                if typ not in META_TYPES: fails.append(f"{name}: [meta] 只能用在封面、本課目標、出處頁 → {b[:40]}")
                if re.search(r"[\"“]", b): fails.append(f"{name}: [meta] 條列不得含英文引句 → {b[:40]}")
            else:
                fails.append(f"{name}: 缺 [wiki: 頁面] → {b[:50]}")
            continue
        pg = m.group(1)
        if pg not in pages:
            fails.append(f"{name}: [wiki: {pg}] 頁面不存在"); continue
        for q in re.findall(r"[\"“]([^\"“”]+)[\"”]", b):
            nq += 1
            for seg in [s.strip() for s in norm(q).split("...") if s.strip()]:
                if seg not in ptext[pg]:
                    fails.append(f"{name}: 引句「{seg[:40]}」不在 wiki 頁 {pg}")
    for im in re.findall(r"^img: (\S+)", t, re.M):
        if im not in ok_imgs: fails.append(f"{name}: 插圖 {im} 不屬於 {topic}")
    md = re.search(r"^mood: (\w+) \[wiki: ([\w-]+)\]", t, re.M)
    if not md: fails.append(f"{name}: 缺 mood 行"); continue
    if md.group(1) not in ("bright", "dark", "warm"): fails.append(f"{name}: mood 只能是 bright/dark/warm")
    mp = md.group(2)
    if mp not in pages or "type: place" not in pages[mp].read_text(encoding="utf-8") or "氛圍判斷" not in pages[mp].read_text(encoding="utf-8"):
        fails.append(f"{name}: mood 依據 {mp} 必須是有「氛圍判斷」的地點頁")
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).strftime("%Y-%m-%d %H:%M")
res = f"\n## [{now}] 出處檢查 slides_check.py\n- 範圍：{len(files)} 頁、{nb} 條、{nq} 句英文引句\n- 結果：{'✅ 全過' if not fails else '❌ ' + str(len(fails)) + ' 處'}\n" + "".join(f"  - {x}\n" for x in fails)
rp = SD / "report.md"
rp.write_text((rp.read_text(encoding="utf-8") if rp.exists() else "# 簡報檢查紀錄：" + topic + "\n") + res, encoding="utf-8")
print(res); sys.exit(1 if fails else 0)

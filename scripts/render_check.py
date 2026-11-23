"""渲染檢查：逐頁截圖，檢查 (1) 右頁文字沒有超出頁面 (2) 插圖都載入 (3) 畫面文字與稿件一字不差。
在有瀏覽器的環境執行。用法：python3 render_check.py <slides/主題 資料夾> <截圖輸出資料夾>
"""
import re, sys, json
from pathlib import Path
from playwright.sync_api import sync_playwright
SD = Path(sys.argv[1]); OUT = Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
def clean(b): return re.sub(r"\s*(\[wiki: [\w-]+\]|\[meta\])\s*$", "", b[2:]).strip()
exp = []
for f in sorted((SD / "drafts").glob("slide-*.md")):
    t = f.read_text(encoding="utf-8")
    exp.append((re.search(r"^# (.+)$", t, re.M).group(1).strip(), [clean(l) for l in t.splitlines() if l.startswith("- ")]))
fails = []
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1600, "height": 900})
    pg.goto((SD / "deck.html").resolve().as_uri()); pg.wait_for_timeout(1500)
    n = pg.evaluate("document.querySelectorAll('.slide').length")
    if n != len(exp): fails.append(f"頁數不符：HTML {n} 頁，稿件 {len(exp)} 頁")
    for k in range(n):
        pg.evaluate(f"go({k})"); pg.wait_for_timeout(1000)
        info = pg.evaluate("""k=>{const s=document.querySelectorAll('.slide')[k];const r=s.querySelector('.page.right');const rb=r.getBoundingClientRect();
          const over=[...r.querySelectorAll('h2,li,.src')].filter(e=>{const b=e.getBoundingClientRect();return b.bottom>rb.bottom-2||b.right>rb.right+1}).map(e=>e.textContent.slice(0,30));
          const imgs=[...s.querySelectorAll('img')].map(i=>({src:i.getAttribute('src'),ok:i.complete&&i.naturalWidth>0}));
          return {over,scroll:r.scrollHeight>r.clientHeight+1,imgs,h2:s.querySelector('h2').dataset.text,
            lis:[...s.querySelectorAll('li')].map(l=>({d:l.dataset.text,t:l.textContent}))}}""", k)
        pg.screenshot(path=str(OUT / f"slide-{k+1:02d}.png"))
        title, bl = exp[k]
        if info["over"] or info["scroll"]: fails.append(f"第 {k+1} 頁文字超出頁面：{info['over'] or '整體高度超出'}")
        for im in info["imgs"]:
            if not im["ok"]: fails.append(f"第 {k+1} 頁插圖沒載入：{im['src']}")
        if info["h2"] != title: fails.append(f"第 {k+1} 頁標題與稿件不同")
        if [l["d"] for l in info["lis"]] != bl: fails.append(f"第 {k+1} 頁條列與稿件不同")
        for l in info["lis"]:
            vis = re.sub(r"翻開答案|展開|收合|\s", "", l["t"]); want = re.sub(r"\s", "", l["d"])
            if vis != want: fails.append(f"第 {k+1} 頁畫面文字被改動：{l['d'][:30]}")
    b.close()
print(json.dumps({"pages": len(exp), "fails": fails}, ensure_ascii=False, indent=1))
sys.exit(1 if fails else 0)

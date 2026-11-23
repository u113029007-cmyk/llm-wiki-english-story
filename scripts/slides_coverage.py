"""覆蓋率關卡：檢查 slides/<主題>/sources.md 列的 wiki 頁都存在、每個目標都有頁面、總數至少 3 頁。
不足就 exit 1（停下，不往下做大綱）。用法：python3 scripts/slides_coverage.py <主題>
"""
import re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
topic = sys.argv[1]
src = (ROOT / "slides" / topic / "sources.md").read_text(encoding="utf-8")
pages = {p.stem for p in (ROOT / "wiki").rglob("*.md")}
rows = re.findall(r"^\| ([^|]+?) \| ([^|]+?) \|$", src, re.M)
rows = [r for r in rows if r[0] not in ("目標", "---")]
fails, total = [], set()
for goal, lst in rows:
    names = [x.strip() for x in lst.split(",") if x.strip()]
    if not names: fails.append(f"目標「{goal}」沒有任何 wiki 頁")
    for n in names:
        total.add(n)
        if n not in pages: fails.append(f"目標「{goal}」列的 {n} 不存在於 wiki/")
for need in ("故事大綱", "主要角色", "關鍵單字或句子"):
    if need not in [g for g, _ in rows]: fails.append(f"缺少目標「{need}」")
if len(total) < 3: fails.append(f"相關 wiki 頁只有 {len(total)} 頁，少於 3 頁")
print(f"覆蓋率關卡：{len(rows)} 個目標、{len(total)} 個 wiki 頁")
print("✅ 通過" if not fails else "❌ 不足，停下：\n- " + "\n- ".join(fails))
sys.exit(1 if fails else 0)

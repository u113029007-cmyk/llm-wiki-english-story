"""決定一篇原文要不要分段讀、怎麼切（AGENTS.md 第 6 節）。
超過 MAX 段就平均切成每段不超過 MAX 段。
用法：python3 scripts/plan_reading.py 短ID
"""
import re, sys, math
from pathlib import Path

MAX = 60
ROOT = Path(__file__).resolve().parent.parent

def main(sid):
    f = ROOT / "raw/potter" / f"{sid}.md"
    n = len(re.findall(r"^¶\d+ ", f.read_text(encoding="utf-8"), re.M))
    if n <= MAX:
        print(f"{sid}: {n} 段，不需分段，一次讀完 ¶1-{n}")
        return
    k = math.ceil(n / MAX); size = math.ceil(n / k)
    parts = [(i * size + 1, min((i + 1) * size, n)) for i in range(k)]
    print(f"{sid}: {n} 段，超過 {MAX}，分 {k} 段讀：")
    for a, b in parts:
        print(f"  ¶{a}-{b}")
    print(f"每讀完一段，把重點寫進 notes/{sid}.md（每條附出處），全部讀完才寫 wiki。")

if __name__ == "__main__":
    main(sys.argv[1])

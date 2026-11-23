"""渲染 HTML：把 slides/<主題>/drafts/ 套進版型，輸出 deck.html。
文字完全來自稿件（去掉 [wiki:]、[meta] 標記），AI 不手寫 HTML，確保「渲染節點不改字」。
插圖複製到 slides/<主題>/img/，圖說只用 images.md 的段落位置，不用 alt。
用法：python3 scripts/build_deck.py <主題>
"""
import re, sys, html, shutil
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
topic = sys.argv[1]; SD = ROOT / "slides" / topic
rows = {f: (int(a), int(b)) for f, s, a, b in re.findall(r"^\| (illustration-\d+\.jpg) \| ([\w-]+) \| ¶(\d+) \| ¶(\d+) \|", (ROOT / "raw/assets/potter/images.md").read_text(encoding="utf-8"), re.M) if s == topic}
(SD / "img").mkdir(exist_ok=True)
E = html.escape
QRE = re.compile(r"[\"“]([^\"“”]+)[\"”]")

def clean(b):
    return re.sub(r"\s*(\[wiki: [\w-]+\]|\[meta\])\s*$", "", b[2:]).strip()

def render_bullet(txt, typ, i):
    m = re.match(r"^(Q\d+)：(.+?) → (.+)$", txt)
    if typ == "quiz" and m:
        return (f'<li class="quiz" data-text="{E(txt)}"><span class="q">{E(m.group(1))}：{E(m.group(2))}</span>'
                f'<button class="reveal" onclick="this.nextElementSibling.classList.add(\'shown\');this.remove();event.stopPropagation()">翻開答案</button>'
                f'<span class="a"> → {E(m.group(3))}</span></li>')
    m = re.match(r"^([a-z]+) ([^：]+)：[\"“](.+)[\"”]$", txt)
    if typ == "vocab" and m:
        return (f'<li class="vocab" data-text="{E(txt)}"><span class="word">{E(m.group(1))}</span>'
                f'<span class="zh"> {E(m.group(2))}：</span><span class="eg">"{E(m.group(3))}"</span></li>')
    if re.fullmatch(r"[\"“][^\"“”]+[\"”]", txt):
        return f'<li class="quote" data-text="{E(txt)}">{E(txt)}</li>'
    parts = QRE.split(txt)
    inner = "".join(E(p) if k % 2 == 0 else f'<em>"{E(p)}"</em>' for k, p in enumerate(parts))
    return f'<li data-text="{E(txt)}">{inner}</li>'

SPRIG = '<svg class="sprig" viewBox="0 0 120 60" aria-hidden="true"><path d="M5 55 C35 45 60 30 115 8" fill="none" stroke="currentColor" stroke-width="1.4"/><g fill="currentColor" opacity=".75"><ellipse cx="28" cy="44" rx="9" ry="3.4" transform="rotate(-35 28 44)"/><ellipse cx="34" cy="52" rx="8" ry="3" transform="rotate(20 34 52)"/><ellipse cx="55" cy="33" rx="9" ry="3.4" transform="rotate(-40 55 33)"/><ellipse cx="62" cy="42" rx="8" ry="3" transform="rotate(15 62 42)"/><ellipse cx="82" cy="22" rx="8" ry="3" transform="rotate(-45 82 22)"/><ellipse cx="90" cy="30" rx="7" ry="2.6" transform="rotate(10 90 30)"/></g><circle cx="112" cy="9" r="3" fill="currentColor"/><circle cx="104" cy="6" r="2.2" fill="currentColor" opacity=".7"/></svg>'
DIVIDER = '<svg class="divider" viewBox="0 0 200 16" aria-hidden="true"><path d="M10 8 H82 M118 8 H190" stroke="currentColor" stroke-width=".8"/><path d="M100 2 C106 6 106 10 100 14 C94 10 94 6 100 2Z" fill="currentColor"/><circle cx="88" cy="8" r="1.6" fill="currentColor"/><circle cx="112" cy="8" r="1.6" fill="currentColor"/></svg>'
WREATH = ('<svg class="wreath" viewBox="0 0 200 200" aria-hidden="true"><circle cx="100" cy="100" r="62" fill="none" stroke="currentColor" stroke-width=".8" opacity=".5"/>'
          + "".join(f'<ellipse cx="100" cy="36" rx="5" ry="12" fill="currentColor" opacity=".55" transform="rotate({a} 100 100)"/>' for a in range(0, 360, 24))
          + "".join(f'<circle cx="100" cy="46" r="2.4" fill="currentColor" transform="rotate({a+12} 100 100)"/>' for a in range(0, 360, 48)) + '</svg>')
MAP = ('<svg class="map" viewBox="0 0 300 340" aria-hidden="true">'
       + "".join(f'<g transform="translate({x} {y})"><path d="M0 26 L10 0 L20 26Z" fill="currentColor" opacity=".55"/><rect x="9" y="26" width="2" height="7" fill="currentColor"/></g>' for x, y in [(30,30),(70,18),(110,34),(150,20),(190,32),(230,18),(255,40),(50,70),(210,66)])
       + '<ellipse cx="128" cy="88" rx="16" ry="9" fill="currentColor" opacity=".8"/><path d="M20 140 H280" stroke="currentColor" stroke-width="4" stroke-dasharray="10 3"/>'
       + '<rect x="30" y="170" width="240" height="150" fill="none" stroke="currentColor" stroke-width="1"/>'
       + "".join(f'<path d="M{x} {y} q6 -8 12 0" fill="none" stroke="currentColor" stroke-width="1.2"/>' for x in range(50, 250, 28) for y in (220, 245))
       + '<circle cx="80" cy="190" r="13" fill="currentColor" opacity=".45"/><rect x="78" y="190" width="4" height="20" fill="currentColor"/>'
       + '<rect x="200" y="270" width="54" height="36" fill="none" stroke="currentColor" stroke-width="1.2"/><path d="M200 270 L227 254 L254 270" fill="none" stroke="currentColor" stroke-width="1.2"/>'
       + '<path d="M150 280 v-22 M140 264 h20" stroke="currentColor" stroke-width="2"/></svg>'
       + '<div class="maplabels"><span style="top:6%;left:58%">樹林</span><span style="top:21%;left:30%">兔子洞</span><span style="top:39%;left:70%">牆</span><span style="top:55%;left:18%">梨樹</span><span style="top:66%;left:40%">萵苣苗床</span><span style="top:84%;left:42%">稻草人</span><span style="top:91%;left:67%">溫室</span></div>')

slides = []
files = sorted((SD / "drafts").glob("slide-*.md"))
for n, f in enumerate(files, 1):
    t = f.read_text(encoding="utf-8")
    title = re.search(r"^# (.+)$", t, re.M).group(1).strip()
    typ = (re.search(r"^type: (\w+)", t, re.M) or [None, "content"])[1]
    mood, mood_pg = re.search(r"^mood: (\w+) \[wiki: ([\w-]+)\]", t, re.M).groups()
    bl = [l for l in t.splitlines() if l.startswith("- ")]
    wikis = []
    for b in bl:
        m = re.search(r"\[wiki: ([\w-]+)\]", b)
        if m and m.group(1) not in wikis: wikis.append(m.group(1))
    img = re.search(r"^img: (\S+)", t, re.M)
    if img:
        im = img.group(1); shutil.copy(ROOT / "raw/assets/potter" / im, SD / "img" / im)
        a, b = rows[im]
        left = (f'<figure><div class="mat"><img src="img/{im}" alt="Beatrix Potter 原書插圖"></div>'
                f'<figcaption>插圖：Beatrix Potter　原文 ¶{a} 與 ¶{b} 之間</figcaption></figure>')
    elif typ == "map":
        left = f'<div class="mapwrap">{MAP}</div>'
    else:
        left = f'<div class="vignette">{WREATH}</div>'
    kick, _, rest = title.partition("：")
    h = (f'<h2 data-text="{E(title)}"><span class="kicker">{E(kick)}</span>{E(rest)}</h2>' if rest and typ == "content"
         else f'<h2 data-text="{E(title)}">{E(title)}</h2>')
    lis = "".join(render_bullet(clean(b), typ, i) for i, b in enumerate(bl))
    src = "Wiki 出處：" + "、".join(wikis) if wikis else ""
    src += ("　｜　" if src else "") + f"氛圍依據：{mood_pg}"
    cls = "cover" if typ == "cover" else ""
    slides.append(f'''<section class="slide mood-{mood} {cls}" data-n="{n}" aria-label="第 {n} 頁">
<div class="spread"><div class="page left">{SPRIG.replace('class="sprig"','class="sprig tl"')}{left}</div><div class="gutter"></div>
<div class="page right">{h}{DIVIDER}<ul>{lis}</ul><div class="src">{E(src)}</div><div class="folio">· {n} ·</div>{SPRIG.replace('class="sprig"','class="sprig br"')}</div></div></section>''')

CSS = r"""
:root{--paper:#F6EFDD;--paper2:#EFE5CC;--ink:#3E3527;--muted:#7D6E55;--sage:#6E8B5E;--blue:#4A6F96;--rule:#CDBF9F;--accent:#9C4A2F}
.mood-warm{--paper:#F3E3C3;--paper2:#EAD5AE;--ink:#43321F;--muted:#86684A;--sage:#8A6B3E;--blue:#8A4F2A;--rule:#CFB283;--accent:#A5552C}
.mood-dark{--paper:#2F271C;--paper2:#261F16;--ink:#EFE4CC;--muted:#C2AF89;--sage:#B8A06A;--blue:#E0B65E;--rule:#5E4F38;--accent:#E0B65E}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;background:#1E1A14;overflow:hidden;font-family:"Noto Serif TC",serif}
.deck{position:relative;width:100vw;height:100vh;display:flex;align-items:center;justify-content:center}
.slide{position:absolute;width:min(96vw,calc(96vh*16/9));aspect-ratio:16/9;opacity:0;visibility:hidden;transition:opacity .9s ease,visibility .9s}
.slide.active{opacity:1;visibility:visible}
.spread{width:100%;height:100%;display:grid;grid-template-columns:1fr 2.2% 1fr;background:var(--paper);color:var(--ink);border-radius:6px;
 background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 .45 0 0 0 0 .38 0 0 0 0 .25 0 0 0 .07 0'/%3E%3C/filter%3E%3Crect width='200' height='200' filter='url(%23n)'/%3E%3C/svg%3E");
 box-shadow:0 1.5vh 4vh rgba(0,0,0,.45);transition:background-color .9s,color .9s}
.gutter{background:linear-gradient(90deg,transparent,rgba(60,40,20,.18) 45%,rgba(60,40,20,.28) 50%,rgba(60,40,20,.18) 55%,transparent)}
.page{position:relative;padding:5.5% 6%;display:flex;flex-direction:column;min-width:0;overflow:hidden}
.left{align-items:center;justify-content:center}
figure{display:flex;flex-direction:column;align-items:center;gap:1.2vh;height:100%;justify-content:center}
.mat{background:#FFFDF6;padding:1.6vh;border:1px solid var(--rule);outline:1px solid var(--rule);outline-offset:.6vh;height:82%;display:flex;align-items:center}
.mat img{height:100%;width:auto;display:block}
figcaption{font-size:clamp(9px,1.25vh,14px);color:var(--muted);font-style:italic;letter-spacing:.05em}
.vignette,.mapwrap{color:var(--sage);display:flex;align-items:center;justify-content:center;width:100%;height:100%;position:relative}
.wreath{width:62%;opacity:.8}
.mapwrap .map{height:88%;color:var(--sage)}
.maplabels{position:absolute;inset:6% 18%}
.maplabels span{position:absolute;font-size:clamp(10px,1.7vh,18px);color:var(--ink);background:var(--paper);padding:0 .4em}
.sprig{position:absolute;width:15%;color:var(--sage);opacity:.65}
.sprig.tl{top:2.5%;left:2.5%;transform:scaleY(-1)}
.sprig.br{bottom:2.5%;right:2.5%;transform:scaleX(-1)}
h2{font-weight:600;font-size:clamp(16px,4.1vh,46px);line-height:1.3;margin-top:4%;color:var(--ink)}
.kicker{display:block;font-size:.52em;font-weight:400;color:var(--accent);letter-spacing:.2em;margin-bottom:.4em}
.divider{width:42%;height:2.2vh;color:var(--sage);margin:1.6vh 0 2.2vh}
ul{list-style:none;display:flex;flex-direction:column;gap:2vh;font-size:clamp(12px,2.75vh,30px);line-height:1.6}
li{padding-left:1.3em;position:relative}
li::before{content:"";position:absolute;left:.15em;top:.62em;width:.42em;height:.42em;border-radius:50% 0;background:var(--sage);transform:rotate(-20deg)}
li em,.quote,.eg{font-family:"EB Garamond",Georgia,serif;font-style:italic;color:var(--blue)}
.quote{font-size:1.12em;border-left:2px solid var(--rule);padding-left:1em;margin-left:.2em}
.quote::before{display:none}
.vocab .word{font-family:"EB Garamond",Georgia,serif;font-weight:600;color:var(--accent);font-size:1.15em}
.vocab .zh{color:var(--muted)}
.vocab{font-size:.92em}
.quiz .a{display:none;color:var(--accent)}
.quiz .a.shown{display:inline;animation:fadein .8s}@keyframes fadein{from{opacity:0}to{opacity:1}}
.reveal{margin-left:.8em;font:inherit;font-size:.75em;color:var(--accent);background:transparent;border:1px solid var(--rule);border-radius:99px;padding:.1em .9em;cursor:pointer}
.src{margin-top:auto;font-size:clamp(8px,1.15vh,13px);color:var(--muted);letter-spacing:.03em;padding-top:1.5vh;padding-right:16%}
.folio{position:absolute;bottom:3.2%;left:0;right:0;text-align:center;font-family:"EB Garamond",serif;font-style:italic;color:var(--muted);font-size:clamp(10px,1.6vh,18px)}
.cover h2{font-family:"EB Garamond",serif;font-size:clamp(22px,6.4vh,72px);font-weight:500;margin-top:14%}
.cover ul{font-size:clamp(11px,2.5vh,28px)}
.cover li::before{display:none}.cover li{padding-left:0}
.hint{position:fixed;bottom:1.2vh;left:50%;transform:translateX(-50%);color:#9C8E73;font-size:12px;letter-spacing:.1em;font-family:"Noto Serif TC",serif;transition:opacity 1.5s}
@media (prefers-reduced-motion:reduce){.slide{transition:none}}
"""
JS = r"""
const S=[...document.querySelectorAll('.slide')];let i=0;
function go(n){i=Math.max(0,Math.min(S.length-1,n));S.forEach((s,k)=>s.classList.toggle('active',k===i));history.replaceState(null,'','#'+(i+1));}
document.addEventListener('keydown',e=>{if(['ArrowRight','PageDown',' '].includes(e.key))go(i+1);if(['ArrowLeft','PageUp'].includes(e.key))go(i-1);});
document.querySelector('.deck').addEventListener('click',e=>{if(e.target.closest('button'))return;go(e.clientX>innerWidth/2?i+1:i-1);});
let x0=null;addEventListener('touchstart',e=>x0=e.touches[0].clientX);addEventListener('touchend',e=>{if(x0==null)return;const d=e.changedTouches[0].clientX-x0;if(Math.abs(d)>40)go(d<0?i+1:i-1);x0=null;});
go((parseInt(location.hash.slice(1))||1)-1);setTimeout(()=>document.querySelector('.hint').style.opacity=0,6000);
"""
doc = f'''<!DOCTYPE html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Tale of Benjamin Bunny｜英文初學者故事導讀</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,500;0,600;1,400&family=Noto+Serif+TC:wght@400;600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body><main class="deck">
{"".join(slides)}
</main><div class="hint">← → 或點擊左右翻頁</div><script>{JS}</script></body></html>'''
(SD / "deck.html").write_text(doc, encoding="utf-8")
print(f"deck.html：{len(slides)} 頁")

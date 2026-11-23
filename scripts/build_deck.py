"""渲染 HTML：把 slides/<主題>/drafts/ 套進版型，輸出 deck.html。
文字完全來自稿件（去掉 [wiki:]、[meta] 標記），AI 不手寫 HTML，確保「渲染節點不改字」。
插圖複製到 slides/<主題>/img/，圖說只用 images.md 的段落位置，不用 alt。
用法：python3 scripts/build_deck.py <主題>
"""
import re, sys, html, shutil
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
topic = sys.argv[1]; SD = ROOT / "slides" / topic
_st = re.search(r"^篇章: (.+)$", (SD / "sources.md").read_text(encoding="utf-8"), re.M) if (SD / "sources.md").exists() else None
STORIES = [s.strip() for s in _st.group(1).split(",")] if _st else [topic]
rows = {f: (int(a), int(b), s) for f, s, a, b in re.findall(r"^\| (illustration-\d+\.jpg) \| ([\w-]+) \| ¶(\d+) \| ¶(\d+) \|", (ROOT / "raw/assets/potter/images.md").read_text(encoding="utf-8"), re.M) if s in STORIES}
(SD / "img").mkdir(exist_ok=True)
E = html.escape
QRE = re.compile(r"[\"“]([^\"“”]+)[\"”]")

def clean(b):
    return re.sub(r"\s*(\[wiki: [\w-]+\]|\[meta\])\s*$", "", b[2:]).strip()

sys.path.insert(0, str(ROOT / "scripts"))
from lint import norm
WQ = {pg.stem: re.findall(r"[\"“]([^\"“”]+)[\"”]\s*\[src:", pg.read_text(encoding="utf-8")) for pg in (ROOT / "wiki").rglob("*.md")}

VOCAB = sorted({m for f in (SD / "drafts").glob("slide-*.md") if "type: vocab" in f.read_text(encoding="utf-8")
                for m in re.findall(r"^- ([a-z]+) ", f.read_text(encoding="utf-8"), re.M)}, key=len, reverse=True)

def bold_vocab(escaped):
    if not VOCAB: return escaped
    return re.sub(r"\b(" + "|".join(VOCAB) + r")\b", r"<strong>\1</strong>", escaped, flags=re.I)

def full_sentence(short, page):
    segs = [x.strip() for x in norm(short).split("...") if x.strip()]
    cands = [q for q in WQ.get(page, []) if all(sg in norm(q) for sg in segs) and "..." not in q]
    return min(cands, key=len) if cands else None

def render_bullet(txt, typ, i, page=None):
    m = re.match(r'^(.+?) ｜ [\"“](.+)[\"”]$', txt)
    if m and typ in ("content", "map", "series", "tree", "storyline"):
        zh, en = m.groups(); full = full_sentence(en, page) if "..." in en else None
        btn = (f'<button class="expand" data-full="{E(full)}" data-short="{E(en)}" onclick="toggleFull(this,event)">展開</button>' if full else "")
        return (f'<li class="pair" data-text="{E(txt)}"><span class="zh">{E(zh)}</span><span class="sep"> ｜ </span>'
                f'<span class="en">"<span class="entext">{bold_vocab(E(en))}</span>"</span>{btn}</li>')
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

TREE = ('<svg class="tree" viewBox="0 0 300 372" role="img" aria-label="家族關係圖">'
 '<defs><marker id="tr-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>'
 '<g fill="none" stroke="currentColor" stroke-width="1.2">'
 '<rect x="15" y="22" width="120" height="38" rx="6"/><rect x="150" y="22" width="146" height="38" rx="6"/>'
 '<rect x="15" y="122" width="130" height="58" rx="6"/><rect x="175" y="130" width="110" height="40" rx="6"/>'
 '<rect x="85" y="248" width="130" height="40" rx="6"/><rect x="65" y="318" width="170" height="42" rx="6" stroke-dasharray="5 4"/>'
 '<path d="M75 60V122" marker-end="url(#tr-ar)"/><path d="M225 60V130" marker-end="url(#tr-ar)"/><path d="M145 150H175" />'
 '<path d="M80 180V214H230V170"/><path d="M150 214V248" marker-end="url(#tr-ar)"/><path d="M150 318V288" marker-end="url(#tr-ar)"/></g>'
 '<g fill="var(--ink)" text-anchor="middle" font-size="11">'
 '<text x="75" y="38" font-weight="700">Mrs. Rabbit</text><text x="75" y="53" font-size="10">兔媽媽</text>'
 '<text x="223" y="38" font-weight="700" font-size="10.5">old Mr. Benjamin Bunny</text><text x="225" y="53" font-size="10">Benjamin 的爸爸</text>'
 '<text x="80" y="140" font-weight="700">Peter・Flopsy</text><text x="80" y="155" font-weight="700">Mopsy・Cottontail</text><text x="80" y="171" font-size="10">四個兄弟姊妹</text>'
 '<text x="230" y="147" font-weight="700">Benjamin</text><text x="230" y="162" font-size="10">Peter 的 cousin</text>'
 '<text x="160" y="143" font-size="9">cousin</text>'
 '<text x="150" y="208" font-size="10">Benjamin 娶了 Flopsy</text>'
 '<text x="150" y="265" font-weight="700">Flopsy Bunnies</text><text x="150" y="280" font-size="10">他們的孩子們</text>'
 '<text x="150" y="335" font-weight="700">Thomasina Tittlemouse</text><text x="150" y="351" font-size="10">林鼠，第五篇主角（推論同一隻）</text>'
 '<text x="158" y="306" text-anchor="start" font-size="9">第三篇咬破麻袋救了他們</text></g></svg>')

STORY = ('<svg class="tree" viewBox="0 0 320 390" role="img" aria-label="五篇故事線">'
 '<defs><marker id="st-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>'
 '<g fill="none" stroke="currentColor" stroke-width="1.4">'
 '<rect x="15" y="24" width="170" height="52" rx="7"/><rect x="15" y="104" width="170" height="52" rx="7"/>'
 '<rect x="15" y="209" width="170" height="52" rx="7"/><rect x="15" y="294" width="170" height="52" rx="7"/>'
 '<rect x="205" y="209" width="110" height="52" rx="7" stroke-dasharray="5 4"/>'
 '<path d="M100 76V104" marker-end="url(#st-ar)"/><path d="M100 156V209" marker-end="url(#st-ar)"/><path d="M100 261V294" marker-end="url(#st-ar)"/>'
 '<path d="M185 235H205" stroke-dasharray="4 3"/><path d="M10 180H310" stroke-width=".8" stroke-dasharray="2 4"/></g>'
 '<g fill="var(--ink)" text-anchor="middle">'
 '<text x="22" y="15" text-anchor="start" font-size="11" font-weight="700" fill="var(--accent)">小時候</text>'
 '<text x="22" y="198" text-anchor="start" font-size="11" font-weight="700" fill="var(--accent)">長大以後</text>'
 '<text x="100" y="46" font-size="12.5" font-weight="700">① Peter Rabbit</text><text x="100" y="64" font-size="11">Peter 闖進花園</text>'
 '<text x="100" y="126" font-size="12.5" font-weight="700">② Benjamin Bunny</text><text x="100" y="144" font-size="11">回花園拿衣服</text>'
 '<text x="100" y="231" font-size="12.5" font-weight="700">③ Flopsy Bunnies</text><text x="100" y="249" font-size="11">小兔子被裝進麻袋</text>'
 '<text x="100" y="316" font-size="12.5" font-weight="700">④ Mr. Tod</text><text x="100" y="334" font-size="11">救回被偷的孩子</text>'
 '<text x="260" y="231" font-size="11" font-weight="700">⑤ Mrs. Tittlemouse</text><text x="260" y="249" font-size="10.5">林鼠的家</text>'
 '<text x="260" y="203" font-size="9.5" fill="var(--muted)">和前面沒有劇情先後</text>'
 '<text x="260" y="280" font-size="10">③ 裡救小兔子的林鼠</text><text x="260" y="295" font-size="10">當了 ⑤ 的主角</text><text x="260" y="310" font-size="10" fill="var(--muted)">（推論同一隻）</text>'
 '</g></svg>')
WIKIMAP = ('<svg class="tree" viewBox="0 0 300 380" role="img" aria-label="有沒有 Wiki 的差別">'
 '<defs><marker id="wm-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>'
 '<g fill="var(--ink)" font-size="11.5" font-weight="700"><text x="9" y="18">沒有 Wiki</text><text x="9" y="148">有了 Wiki</text></g>'
 + "".join(f'<rect x="{x}" y="28" width="50" height="34" rx="5" fill="none" stroke="var(--muted)" stroke-width="1.2"/><text x="{x+25}" y="44" text-anchor="middle" font-size="11" font-weight="700" fill="var(--muted)">{n}</text><text x="{x+25}" y="57" text-anchor="middle" font-size="9" fill="var(--muted)">原文</text>' for x, n in zip((9,67,125,183,241), "①②③④⑤"))
 + '<text x="150" y="80" text-anchor="middle" font-size="10.5" fill="var(--muted)">五篇各讀各的，看不出關聯</text>'
 '<path d="M150 88V126" stroke="currentColor" stroke-width="2" marker-end="url(#wm-ar)"/><text x="160" y="112" font-size="10" fill="var(--accent)" font-weight="700">ingest＋整合</text>'
 '<g stroke="currentColor" stroke-width="1" opacity=".75">'
 + "".join(f'<path d="M{hx} 228L{sx} 312"/>' for hx, sx in [(60,34),(60,92),(60,150),(60,208),(150,34),(150,92),(150,150),(150,208),(250,150),(250,266)])
 + '<path d="M150 184L60 204M150 184V204M150 184L250 204"/></g>'
 '<rect x="70" y="158" width="160" height="26" rx="13" fill="var(--paper2)" stroke="var(--accent)" stroke-width="1.6"/><text x="150" y="175" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--accent)">整合答案（query 頁）</text>'
 + "".join(f'<rect x="{x-40}" y="204" width="80" height="24" rx="12" fill="var(--paper)" stroke="currentColor" stroke-width="1.4"/><text x="{x}" y="220" text-anchor="middle" font-size="10" font-weight="700" fill="var(--ink)">{lab}</text>' for x, lab in [(60,"Peter 角色頁"),(150,"cousin 單字頁"),(250,"Thomasina 頁")])
 + "".join(f'<rect x="{x}" y="312" width="50" height="34" rx="5" fill="var(--paper)" stroke="currentColor" stroke-width="1.4"/><text x="{x+25}" y="333" text-anchor="middle" font-size="11" font-weight="700" fill="var(--ink)">{n}</text>' for x, n in zip((9,67,125,183,241), "①②③④⑤"))
 + '<text x="150" y="368" text-anchor="middle" font-size="10" fill="var(--muted)">每條線＝Wiki 頁之間的連結（舉 3 頁為例）</text></svg>')
STORIES_ORDER = [("peter-rabbit","① Peter Rabbit"),("benjamin-bunny","② Benjamin Bunny"),("flopsy-bunnies","③ Flopsy Bunnies"),("mr-tod","④ Mr. Tod"),("mrs-tittlemouse","⑤ Mrs. Tittlemouse")]
def storybar(lit, n, total):
    if lit is None: return ""
    on = {s for s, _ in STORIES_ORDER} if "all" in lit else set(lit)
    items = []
    for k, (sid, lab) in enumerate(STORIES_ORDER):
        if k == 4: items.append('<span class="sb-gap"></span>')
        elif k: items.append('<span class="sb-line"></span>')
        items.append(f'<span class="sb{" on" if sid in on else ""}">{lab}</span>')
    return f'<div class="storybar"><span class="sb-lab">故事線</span>{"".join(items)}<span class="sb-no">{n} / {total}</span></div>'

slides = []; titles = []
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
        a, b, sid = rows[im]
        left = (f'<figure><div class="mat"><img src="img/{im}" alt="Beatrix Potter 原書插圖"></div>'
                f'<figcaption>插圖：Beatrix Potter　{(sid + " ") if len(STORIES) > 1 else ""}原文 ¶{a} 與 ¶{b} 之間</figcaption></figure>')
    elif typ == "map":
        left = f'<figure class="mapfig"><div class="mapwrap">{MAP}</div><figcaption>地點名稱都來自 wiki；位置為示意，原文未描述相對位置</figcaption></figure>'
    elif typ == "storyline":
        left = f'<figure class="mapfig"><div class="mapwrap">{STORY}</div><figcaption>前四篇依劇情先後排列；⑤ 和前面沒有劇情先後</figcaption></figure>'
    elif typ == "wikimap":
        left = f'<figure class="mapfig"><div class="mapwrap">{WIKIMAP}</div><figcaption>上：原始的 5 篇原文　下：Wiki 把它們連起來</figcaption></figure>'
    elif typ == "tree":
        left = f'<figure class="mapfig"><div class="mapwrap">{TREE}</div><figcaption>關係依 wiki 角色頁的親屬連結；虛線框＝推論</figcaption></figure>'
    else:
        left = None
    kick, _, rest = title.partition("：")
    h = (f'<h2 data-text="{E(title)}"><span class="kicker">{E(kick)}</span>{E(rest)}</h2>' if rest and typ == "content"
         else f'<h2 data-text="{E(title)}">{E(title)}</h2>')
    lis = "".join(render_bullet(clean(b), typ, i, (re.search(r"\[wiki: ([\w-]+)\]", b) or [None, None])[1]) for i, b in enumerate(bl))
    src = "Wiki 出處：" + "、".join(wikis) if wikis else ""
    src += ("　｜　" if src else "") + f"氛圍依據：{mood_pg}"
    cls = ("cover " if typ == "cover" else "") + ("full " if left is None else "") + f"t-{typ}"
    stl = re.search(r"^story: (.+)$", t, re.M)
    lit = [x.strip() for x in stl.group(1).split(',')] if stl else None
    titles.append(title)
    slides.append(f'''<section class="slide mood-{mood} {cls}" data-n="{n}" aria-label="第 {n} 頁">
<div class="spread">{'' if left is None else '<div class="page left">' + SPRIG.replace('class="sprig"','class="sprig tl"') + left + '</div><div class="gutter"></div>'}
<div class="page right">{SPRIG.replace('class="sprig"','class="sprig tl"') if left is None else ''}{h}{DIVIDER}<ul>{lis}</ul><div class="src">{E(src)}</div>{'' if lit else '<div class="folio">· ' + str(n) + ' ·</div>'}{SPRIG.replace('class="sprig"','class="sprig br"')}</div>{storybar(lit, n, len(files))}</div></section>''')

CSS = r"""
:root{--paper:#F6EFDD;--paper2:#EFE5CC;--ink:#3E3527;--muted:#7D6E55;--sage:#6E8B5E;--blue:#4A6F96;--rule:#CDBF9F;--accent:#9C4A2F}
.mood-warm{--paper:#F3E3C3;--paper2:#EAD5AE;--ink:#43321F;--muted:#86684A;--sage:#8A6B3E;--blue:#8A4F2A;--rule:#CFB283;--accent:#A5552C}
.mood-dark{--paper:#2F271C;--paper2:#261F16;--ink:#EFE4CC;--muted:#C2AF89;--sage:#B8A06A;--blue:#E0B65E;--rule:#5E4F38;--accent:#E0B65E}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;background:#1E1A14;overflow:hidden;font-family:"Noto Sans TC","Microsoft JhengHei",sans-serif;font-weight:500}
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
.mapwrap .tree{height:96%;color:var(--sage)}
.maplabels{position:absolute;inset:6% 18%}
.maplabels span{position:absolute;font-size:clamp(10px,1.7vh,18px);color:var(--ink);background:var(--paper);padding:0 .4em}
.sprig{position:absolute;width:15%;color:var(--sage);opacity:.65}
.sprig.tl{top:2.5%;left:2.5%;transform:scaleY(-1)}
.sprig.br{bottom:2.5%;right:2.5%;transform:scaleX(-1)}
h2{font-weight:700;font-size:clamp(16px,4.1vh,46px);line-height:1.3;margin-top:4%;color:var(--ink)}
.kicker{display:block;font-size:.52em;font-weight:700;color:var(--accent);letter-spacing:.2em;margin-bottom:.4em}
.divider{width:42%;height:2.2vh;color:var(--sage);margin:1.6vh 0 2.2vh}
ul{list-style:none;display:flex;flex-direction:column;gap:2.2vh;font-size:calc(clamp(12px,2.75vh,30px)*var(--fs,1));line-height:1.6}
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
.cover h2{font-size:clamp(22px,5.6vh,64px);font-weight:700;margin-top:14%}
.cover ul{font-size:clamp(11px,2.5vh,28px)}
.cover li::before{display:none}.cover li{padding-left:0}
.hint{position:fixed;bottom:1.2vh;left:50%;transform:translateX(-50%);color:#9C8E73;font-size:12px;letter-spacing:.1em;font-family:"Noto Sans TC",sans-serif;transition:opacity 1.5s}
.full .spread{grid-template-columns:1fr}
.full .page.right{padding:5% 12% 5% 12%}
.full .page.right::after{content:"";position:absolute;top:8%;bottom:8%;left:50%;width:1px;background:linear-gradient(transparent,var(--rule),transparent);opacity:.35}
.full ul{display:grid;grid-template-columns:1fr 1fr;column-gap:7%;row-gap:2.2vh;position:relative;z-index:1}
.full.t-content ul,.full.t-series ul{grid-template-columns:1fr 1fr}
.full.t-agenda ul,.full.t-sources ul,.full.t-guide ul{grid-template-columns:1fr;width:72%;margin:0 auto}
.full.t-agenda h2,.full.t-sources h2,.full.t-guide h2,.full.t-agenda .divider,.full.t-sources .divider,.full.t-guide .divider{margin-left:14%}
.pair .en strong{font-weight:600;color:var(--accent);font-style:italic}
.mapfig{height:100%}.mapfig .mapwrap{height:88%}
.t-vocab li{background:color-mix(in srgb,var(--paper2) 70%,transparent);border:1px solid var(--rule);border-radius:4px;padding:1.4vh 1.4vh 1.4vh 2.6vh}
.t-vocab li::before{left:.9vh;top:2.1vh}
.t-vocab .eg{display:block;margin-top:.4vh}
.t-quiz ul{grid-template-columns:1fr;font-size:calc(clamp(14px,3.3vh,36px)*var(--fs,1));row-gap:5vh;margin:4vh auto 0;width:70%}.t-quiz h2,.t-quiz .divider{margin-left:15%}
.pair .zh{display:block}
.pair .sep{display:none}
.pair .en{display:block;font-family:"EB Garamond",Georgia,serif;font-style:italic;color:var(--blue);font-size:.92em;line-height:1.45;margin-top:.3vh}
.expand{font:inherit;font-size:.62em;font-style:normal;color:var(--accent);background:transparent;border:1px solid var(--rule);border-radius:99px;padding:0 .7em;margin-left:.5em;cursor:pointer;vertical-align:.15em}
body.no-zh .pair .zh{visibility:hidden;height:0;overflow:hidden;display:block}
.toolbar{position:fixed;top:1.4vh;right:1.4vw;display:flex;gap:.5vw;z-index:20;opacity:.35;transition:opacity .4s}
.toolbar:hover,.toolbar:focus-within{opacity:1}
.toolbar button{font:13px "Noto Sans TC",sans-serif;color:#E9DEC6;background:rgba(40,32,22,.7);border:1px solid #6B5C45;border-radius:99px;padding:.35em 1em;cursor:pointer}
.toolbar button[aria-pressed="true"]{background:#6E8B5E;border-color:#6E8B5E}
.progress{position:fixed;left:0;bottom:0;height:3px;background:#B8A06A;transition:width .9s ease;z-index:20}
.toc{position:fixed;top:0;right:0;height:100vh;width:min(360px,80vw);background:#2B241A;color:#EFE4CC;padding:6vh 2vw;transform:translateX(105%);transition:transform .6s ease;z-index:30;overflow:auto;font-family:"Noto Sans TC",sans-serif}
.toc.open{transform:none}
.toc h3{font-weight:500;font-size:18px;color:#D9C48F;margin-bottom:2vh;letter-spacing:.2em}
.toc ol{list-style:none;counter-reset:t}
.toc li{counter-increment:t;padding:.7em 0;border-bottom:1px solid #4A3E2C;cursor:pointer;font-size:14px;line-height:1.4}
.toc li::before{content:counter(t) "　";color:#B8A06A;font-family:"EB Garamond",serif;font-style:italic}
.toc li.cur{color:#E0B65E}
.spread{position:relative}
.storybar ~ *{}
.slide .page{padding-bottom:9%}
.storybar{position:absolute;left:3%;right:3%;bottom:1.6%;height:5.2%;display:flex;align-items:center;justify-content:center;gap:.6vw;font-size:clamp(8px,1.35vh,15px);font-weight:700;z-index:3}
.sb{padding:.25em .9em;border-radius:99px;border:1.5px solid var(--rule);color:var(--muted);opacity:.55;white-space:nowrap}
.sb.on{background:var(--accent);border-color:var(--accent);color:var(--paper);opacity:1}
.sb-line{width:2.2vw;height:2px;background:var(--rule)}
.sb-gap{width:2.2vw;border-top:2px dashed var(--rule)}
.sb-lab{color:var(--accent);margin-right:.4vw;letter-spacing:.1em}
.sb-no{margin-left:1vw;color:var(--muted);font-weight:500}
.navbtn{position:fixed;top:50%;transform:translateY(-50%);width:clamp(36px,4.2vw,56px);height:clamp(36px,4.2vw,56px);border-radius:50%;border:2px solid #CDBF9F;background:rgba(40,32,22,.65);color:#F3E9D2;font-size:clamp(20px,2.4vw,32px);line-height:1;cursor:pointer;z-index:25;display:flex;align-items:center;justify-content:center;transition:background .3s,opacity .3s}
.navbtn:hover{background:#9C4A2F;border-color:#9C4A2F}
.navbtn.prev{left:.6vw}.navbtn.next{right:.6vw}
.navbtn[hidden]{display:none}
.slide.active .spread{animation:turn .9s ease}
@keyframes turn{from{transform:perspective(1600px) rotateY(-4deg) translateX(1.5%);filter:brightness(.97)}to{transform:none;filter:none}}
@media (prefers-reduced-motion:reduce){.slide{transition:none}.slide.active .spread{animation:none}}
"""
JS = "const KEY='" + topic + "';" + r"""
const S=[...document.querySelectorAll('.slide')];let i=0;
const store={get(k){try{return localStorage.getItem(k)}catch(e){return null}},set(k,v){try{localStorage.setItem(k,v)}catch(e){}}};
const TOC=document.querySelector('.toc'),TL=[...TOC.querySelectorAll('li')],PV=document.querySelector('.navbtn.prev'),NX=document.querySelector('.navbtn.next');
function go(n){i=Math.max(0,Math.min(S.length-1,n));S.forEach((s,k)=>s.classList.toggle('active',k===i));TL.forEach((l,k)=>l.classList.toggle('cur',k===i));
 history.replaceState(null,'','#'+(i+1));document.querySelector('.progress').style.width=((i+1)/S.length*100)+'%';store.set(KEY+'-page',i);PV.hidden=i===0;NX.hidden=i===S.length-1;}
function toggleFull(b,e){e.stopPropagation();const t=b.parentElement.querySelector('.entext');const isFull=b.textContent==='收合';t.textContent=isFull?b.dataset.short:b.dataset.full;b.textContent=isFull?'展開':'收合';}
let fs=parseFloat(store.get(KEY+'-fs')||'1');document.documentElement.style.setProperty('--fs',fs);
function font(d){fs=Math.max(.8,Math.min(1.3,fs+d));document.documentElement.style.setProperty('--fs',fs);store.set(KEY+'-fs',fs);}
function zh(btn){const on=document.body.classList.toggle('no-zh');btn.setAttribute('aria-pressed',String(!on));btn.textContent=on?'顯示中文':'隱藏中文';}
TL.forEach((l,k)=>l.addEventListener('click',()=>{go(k);TOC.classList.remove('open');}));
document.addEventListener('keydown',e=>{if(['ArrowRight','PageDown',' '].includes(e.key))go(i+1);if(['ArrowLeft','PageUp'].includes(e.key))go(i-1);});
document.querySelector('.deck').addEventListener('click',e=>{if(e.target.closest('button'))return;if(TOC.classList.contains('open')){TOC.classList.remove('open');return;}go(e.clientX>innerWidth/2?i+1:i-1);});
let x0=null;addEventListener('touchstart',e=>x0=e.touches[0].clientX);addEventListener('touchend',e=>{if(x0==null)return;const d=e.changedTouches[0].clientX-x0;if(Math.abs(d)>40)go(d<0?i+1:i-1);x0=null;});
go(location.hash?parseInt(location.hash.slice(1))-1:parseInt(store.get(KEY+'-page')||'0'));setTimeout(()=>document.querySelector('.hint').style.opacity=0,6000);
"""
doc = f'''<!DOCTYPE html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(titles[0])}｜英文初學者故事導讀</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,500;0,600;1,400&family=Noto+Sans+TC:wght@500;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body><main class="deck">
{"".join(slides)}
</main>
<div class="toolbar" role="toolbar" aria-label="閱讀工具"><button onclick="TOC.classList.toggle('open')">目錄</button><button aria-pressed="true" onclick="zh(this)">隱藏中文</button><button onclick="font(-.1)" aria-label="字體縮小">A−</button><button onclick="font(.1)" aria-label="字體放大">A+</button></div>
<nav class="toc" aria-label="目錄"><h3>目　錄</h3><ol>{"".join(f"<li>{E(t)}</li>" for t in titles)}</ol></nav>
<button class="navbtn prev" aria-label="上一頁" onclick="go(i-1)">‹</button><button class="navbtn next" aria-label="下一頁" onclick="go(i+1)">›</button><div class="progress"></div><div class="hint">← → 或點擊左右翻頁　｜　右上角有目錄、中文開關、字體大小</div><script>{JS}</script></body></html>'''
(SD / "deck.html").write_text(doc, encoding="utf-8")
print(f"deck.html：{len(slides)} 頁")

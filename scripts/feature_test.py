import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
deck=Path(sys.argv[1]).resolve().as_uri(); res={}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":1600,"height":900}); pg.goto(deck); pg.wait_for_timeout(800)
    pg.evaluate("go(0)"); pg.keyboard.press("ArrowRight"); pg.wait_for_timeout(300); res["方向鍵翻頁"]=pg.evaluate("i")==1
    pg.click("text=目錄"); pg.wait_for_timeout(700); res["目錄打開"]=pg.evaluate("TOC.classList.contains('open')")
    pg.click(".toc li:nth-child(9)"); pg.wait_for_timeout(1000); res["目錄跳頁到第9頁"]=pg.evaluate("i")==8
    pg.click("text=隱藏中文"); pg.wait_for_timeout(300); res["隱藏中文"]=pg.evaluate("document.body.classList.contains('no-zh')")
    pg.screenshot(path="feat_nozh.png"); pg.click("text=顯示中文")
    before=pg.evaluate("S[8].querySelector('.entext').textContent"); pg.click(".slide.active .expand"); pg.wait_for_timeout(300)
    after=pg.evaluate("S[8].querySelector('.entext').textContent"); res["展開完整句"]=len(after)>len(before) and "..." not in after; res["完整句內容"]=after
    pg.click("text=A+"); res["字體放大"]=pg.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--fs').trim()")
    pg.evaluate("go(15)"); pg.wait_for_timeout(1000); pg.click(".slide.active .reveal >> nth=0"); res["翻開答案"]=pg.evaluate("S[15].querySelector('.a').classList.contains('shown')")
    pg.screenshot(path="feat_quiz.png"); b.close()
for k,v in res.items(): print(k, v)

# AI 審查指令（第 3 次：簡報 family-five-stories）

你是這份教學簡報的**審查者**，沒有參與製作，請獨立判斷。讀者設定：沒讀過彼得兔的英文初學者。
簡報主題：「用小故事學英文：彼得兔故事集是什麼？」，要把 Wiki 收的 5 篇故事整合起來，說明它們彼此的關聯。

## 你可以讀的檔案（只讀這些）
- `.agents/workflows/topic-slides.md`：簡報規格（了解稿件格式與規則）
- `slides/family-five-stories/sources.md`、`outline.md`、`drafts/` 全部
- `slides/family-five-stories/screenshots/`：每頁截圖（看版面；第 5 頁左邊是家族樹）
- 整合答案：`wiki/books/potter/queries/family-five-stories.md`
- 稿件標的 wiki 頁：`wiki/books/potter/` 與 `wiki/sources.md`
- 需要時可讀原文 `raw/potter/` 裡這 5 篇：peter-rabbit、benjamin-bunny、flopsy-bunnies、mr-tod、mrs-tittlemouse

## 不要讀
- `wiki/log.md`、`notes/`、`reports/`、`slides/family-five-stories/report.md`、`reviews/` 裡的其他檔案、`slides/benjamin-bunny/`

## 腳本已經檢查過（你不用再查）
每條都有 wiki 出處、英文引句逐字存在於該 wiki 頁、插圖屬於這 5 篇、文字沒超出頁面、畫面文字與稿件一致。

## 請檢查腳本做不到的
1. **有沒有回答主題**：看完整份，初學者能不能說出「彼得兔故事集是什麼」：有哪幾篇、篇和篇怎麼連、可以學到哪些英文？哪一頁沒有幫上這個目的？
2. **跨篇關聯對不對**：家族樹、上一代/這一代/下一代、長大前後、危險地點，這些跨篇的說法有沒有被 query 頁和原文支持？原文沒直接寫的，有沒有標「推論」？有沒有把推論講成事實？
3. **忠實度**：每一條中文是否真的被它的英文原句支持？中英意思對不對得上？有沒有說太滿、翻錯？
4. **教學性**：順序、份量、單字選擇是否合理？有沒有跳太快、重複太多（同一句英文用在好幾頁）？
5. **插圖與文字**：插圖和那頁內容是否相符（以圖說標的篇名與段落位置判斷，不要用你自己對圖的解讀當事實）？
6. **一致性**：頁與頁之間的稱謂（表哥/表弟、阿姨/姑姑、old Mr. Benjamin Bunny／old Mr. Bouncer）是否一致？

## 規則
- 不要修改任何檔案，不要執行 git。唯一可以寫的是 `reviews/review-3.md`。
- 做不完要誠實寫出哪些頁沒看。

## 輸出到 `reviews/review-3.md`
```
# 審查報告 3（簡報 family-five-stories）
- 審查範圍：N 頁；未檢查：（列出或寫「無」）

| # | 頁 | 原句（節錄） | 問題類型 | 依據（wiki 頁或原文 ¶） | 建議修正 | 嚴重度 |
|---|---|---|---|---|---|---|
問題類型：主題 / 跨篇關聯 / 忠實度 / 教學性 / 插圖 / 一致性
嚴重度：高 / 中 / 低

## 整體觀察（3-5 點）
```

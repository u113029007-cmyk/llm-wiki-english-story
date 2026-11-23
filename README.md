# 英文經典讀本 Wiki（LLM Wiki 作業）

用 Karpathy 的 LLM Wiki 架構，以 Beatrix Potter《Short Fiction》（Standard Ebooks 版）建立英文讀本 Wiki，再由 Wiki 產生給英文初學者的教學 HTML 簡報。

## 直接開啟（網頁）
- [作業成果首頁](https://u113029007-cmyk.github.io/llm-wiki-english-story/)
- [教學簡報：用小故事學英文：彼得兔故事集是什麼？（17 頁）](https://u113029007-cmyk.github.io/llm-wiki-english-story/slides/family-five-stories/deck.html)
- [第一版簡報（只講一篇，保留作改版紀錄）](https://u113029007-cmyk.github.io/llm-wiki-english-story/slides/benjamin-bunny/deck.html)

## 檔案
- Wiki：[wiki/](wiki/)（73 頁，含跨篇整合 [query 頁](wiki/books/potter/queries/family-five-stories.md)；目錄 [index.md](wiki/index.md)；ingest 5 篇：peter-rabbit、benjamin-bunny、flopsy-bunnies、mr-tod、mrs-tittlemouse）
- 規則：[AGENTS.md](AGENTS.md)（[CLAUDE.md](CLAUDE.md) 只有一行 `@AGENTS.md`）
- 簡報 graph 規格：[.agents/workflows/topic-slides.md](.agents/workflows/topic-slides.md)
- 執行與檢查紀錄：[wiki/log.md](wiki/log.md)、[reports/](reports/)、[簡報檢查紀錄](slides/family-five-stories/report.md)、[reviews/](reviews/)、[commit 紀錄](../../commits/main)

## 資料夾
```
raw/       原文（唯讀）：original/ 電子書、potter/ 切篇並編號、assets/ 插圖與對照表
wiki/      LLM 撰寫維護的 Wiki
scripts/   切篇、lint、分段閱讀、簡報各關卡檢查腳本（Python）
notes/     長篇分段閱讀筆記
slides/    簡報狀態檔：sources、outline、drafts、deck.html、screenshots、report
reviews/   新對話 AI 審查的指令與報告
```

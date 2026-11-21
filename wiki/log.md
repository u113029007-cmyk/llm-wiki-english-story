---
type: log
---
# Log

## [2026-11-21] setup | 建立 Wiki 骨架
- 需求訪談完成，需求摘要經 Joanna 確認；建立 AGENTS.md、CLAUDE.md（@AGENTS.md）。
- 版權檢查：Beatrix Potter 卒於 1943，台灣保護期 1993 年底屆滿，通過。記於 [[sources]]。

## [2026-11-21] setup | 切篇腳本 scripts/split_potter.py
- 第 1 版：把每篇開頭的 header 整塊跳過。驗證（原始 HTML `<p>` 數 vs raw ¶ 數）發現 3 篇不符：漏掉 pie-and-the-patty-pan 與 tailor-of-gloucester 的題詞、tailor-of-gloucester 的 1 張插圖、samuel-whiskers 的副標題。
- 第 2 版：header 只跳過標題，題詞、副標題保留並加標記。驗證結果：20 篇段落數全部一致；插圖 602 張 = 對照表 602 列。
- 發現原文含看不見的 U+FEFF（396 處）、U+2011、…，已寫入 AGENTS.md lint 第 1 項正規化規則，避免引句比對假警報。

## [2026-11-21] fix | AGENTS.md 依三份依據補缺口
- 對照老師作業說明、課程講義、Karpathy gist 逐項核對後補上：
  - 觸發條件（講義 p.21 loop 五件事之一）：使用者說「ingest 某篇」才開始。
  - AI 審查第 9 項加入「缺少的交叉連結」（Karpathy lint）。
  - 新增 7.5 節 Query：簡報大綱存回 Wiki 並記 log（Karpathy：好答案存回 Wiki）。
- 刻意不做：Karpathy lint 的「用網路搜尋補資料缺口」，因本 Wiki 鐵則禁止外部知識。

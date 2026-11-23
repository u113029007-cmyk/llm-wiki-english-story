# Workflow：/topic-slides（從 Wiki 產生教學 HTML 簡報）

依講義 p.41-47 設計。狀態全部是檔案，放在 `slides/<主題>/`，每一關的產出都能打開看、進 git、單獨重跑。

## loop 五件事（講義 p.21）
| 項目 | 內容 |
|---|---|
| 🎯 目標 | 只用 wiki，產出給英文初學者的教學 HTML 簡報：故事大綱與主要角色、關鍵英文單字或句子 |
| 🚧 限制 | 只能用 wiki/ 的內容；不得用外部知識；不得用 images.md 的 alt 描述當事實；渲染節點不得改字 |
| ✅ 完成標準 | coverage、slides_check、render_check 三支腳本全過，且使用者確認過大綱，新對話審查的問題已處理 |
| 🛑 停止條件 | 覆蓋率不足（相關 wiki 頁少於 3 頁或任一目標沒有頁面）就一開始停下；每個檢查關卡最多改 3 輪，還不過就停下交給使用者 |
| ⏰ 觸發 | 使用者說「做 <主題> 簡報」 |

## Graph
```
檢索 wiki → [覆蓋率關卡] → 大綱 → (使用者確認) → 逐頁稿 → [出處檢查] → 渲染 HTML → [渲染檢查] → 交件（大綱存回 wiki）
退回：使用者不同意 → 修大綱或補檢索；出處檢查失敗 → 只修那一頁稿；渲染檢查失敗 → 重新渲染（不改稿，除非是字太多 → 退回那一頁稿縮短）
```

## 每一關只能看什麼、不能做什麼（講義 p.44）
| 節點 | 只能看 | 產出 | 不能做 |
|---|---|---|---|
| 檢索 wiki | wiki/index.md、wiki/books/ | sources.md | 讀 raw/、用外部知識 |
| 覆蓋率關卡 | sources.md | 報告 | 改任何檔案（腳本） |
| 大綱 | sources.md 列的 wiki 頁、images.md 的「篇／段落」欄 | outline.md | 使用 alt 描述、加 sources.md 以外的頁 |
| 逐頁稿 | outline.md、該頁對應的 wiki 頁 | drafts/slide-NN.md | 引用該頁以外的內容 |
| 出處檢查 | drafts/、wiki/、images.md | 報告 | 改稿（腳本） |
| 渲染 HTML | drafts/（已通過出處檢查） | deck.html | 改任何一個字（由腳本 build_deck.py 產生，AI 不手寫） |
| 渲染檢查 | deck.html、drafts/ | 截圖、報告 | 改任何檔案（腳本） |

## 逐頁稿格式（腳本檢查依據）
```
# 投影片標題
- 一句內容 [wiki: 頁面檔名]
- "英文引句" [wiki: 頁面檔名]
img: illustration-NN.jpg
```
- 每一條 `- ` 都必須有 `[wiki: 頁面檔名]`，頁面必須存在於 wiki/。
- 英文引句必須出現在所標的 wiki 頁裡（正規化後比對）；wiki 頁本身的引句已由 lint 對過 raw。
- 封面、本課目標、出處說明三類頁面，可用 `[meta]` 代替 `[wiki: ...]`，但 `[meta]` 條列不得含英文引句。
- 插圖只能用 images.md 中屬於該篇的檔案（跨篇主題：在 sources.md 寫一行 `篇章: a, b, c`，插圖可用這幾篇的）；圖說由 build_deck.py 依 images.md 的「前段／後段」自動產生，不使用 alt。
- 內容頁（沒有 type，或 type: map）每一條都必須是中英對照：`- 中文 ｜ "英文原文" [wiki: 頁面]`，英文可用 `...` 縮短，渲染時可展開成 wiki 裡的完整句子。
- 內容頁每頁最多 4 條（中英兩行較長）；其他頁最多 5 條。
- type: series（跨篇整理頁）也必須中英對照，最多 5 條，可引用任何一篇的 wiki 頁；推論要在中文標（推論）。
- type: tree（家族樹）：左頁由 build_deck.py 畫關係圖，只畫 wiki 角色頁有寫的親屬連結，wiki 標（推論）的關係用虛線框；右頁條列同內容頁規則（中英對照、最多 4 條）。
- 沒有插圖的頁（agenda、vocab、quiz、sources、沒有 img 的內容頁）跨左右兩頁排版。
- 示意圖（例如故事地圖）只能畫 wiki 有寫的地點名稱；wiki 沒寫的相對位置、距離、方向，圖上必須標註「位置為示意，原文未描述」（審查 2 #1）。
- 條列順序就是閱讀順序：agenda、sources 用單欄，避免跨欄變成 Z 字閱讀（審查 2 #23）。

## 狀態檔
```
slides/<主題>/
├── sources.md      檢索結果：用到哪些 wiki 頁、為了哪個目標
├── outline.md      大綱（使用者確認後才往下）
├── drafts/         逐頁稿
├── deck.html       渲染結果（腳本產生）
├── screenshots/    渲染檢查截圖
└── report.md       各關卡檢查紀錄
```

## 檢查腳本
- scripts/slides_coverage.py <主題>：覆蓋率關卡（2026-11-23 起：必須有「角色之間的關聯」目標，且至少用到一頁 type: query 的整合頁）
- scripts/slides_check.py <主題>：出處檢查
- scripts/build_deck.py <主題>：渲染 HTML（不是檢查，是讓渲染不經 AI 手寫）
- scripts/render_check.py <主題>：渲染檢查（截圖、溢出、圖片載入、文字與稿一致）

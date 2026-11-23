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
- 插圖只能用 images.md 中屬於該篇的檔案；圖說由 build_deck.py 依 images.md 的「前段／後段」自動產生，不使用 alt。
- 每頁條列不超過 5 條（初學者可讀性；超過就退回縮短）。

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
- scripts/slides_coverage.py <主題>：覆蓋率關卡
- scripts/slides_check.py <主題>：出處檢查
- scripts/build_deck.py <主題>：渲染 HTML（不是檢查，是讓渲染不經 AI 手寫）
- scripts/render_check.py <主題>：渲染檢查（截圖、溢出、圖片載入、文字與稿一致）

# 英文經典讀本 Wiki：AGENTS.md

本檔是這個 Wiki 的唯一規則檔（schema）。CLAUDE.md 只有一行 `@AGENTS.md`，所有工具都讀這份。
架構參考 Karpathy 的 LLM Wiki：raw/（原始資料，唯讀）→ wiki/（LLM 撰寫維護）→ 本檔（規則）。

## 1. 讀者與目標
- Wiki 讀者：使用者本人（Joanna）。之後作為英文接龍 APP 的內容層（RAG 原文、單字、角色）。
- 簡報讀者：想學英文的初學者。簡報目標：故事大綱與主要角色、關鍵英文單字或句子。
- 本 Wiki 可容納多本書。第一批：Beatrix Potter《Short Fiction》（Standard Ebooks 版）兔子系列 4 篇，第 5 篇待使用者決定。之後可能加入 Alice's Adventures in Wonderland（使用 chapters/）。

## 2. 資料夾結構
```
CLAUDE.md              只有 @AGENTS.md
AGENTS.md              本檔
scripts/               切篇編號、lint 等腳本
raw/                   唯讀，AI 不得修改
  original/            下載的電子書原檔
  potter/              腳本切好的每篇原文，段落以 ¶ 編號
  assets/potter/       腳本取出的插圖 + images.md 對照表
wiki/
  index.md             所有頁面目錄，每頁一行連結 + 一句摘要
  log.md               時間紀錄，只能往後加
  sources.md           來源與版權紀錄
  books/potter/
    overview.md        全書總覽，每次 ingest 後更新
    stories/           每篇故事一頁
    characters/        每個角色一頁
    places/            每個地點一頁
    vocabulary/        每個單字一頁
```

## 3. 鐵則（任何情況都不能違反）
1. raw/ 唯讀。原文切篇、編號、取圖一律由 scripts/ 的腳本完成，AI 不得手動改寫 raw/。
2. Wiki 只能寫 raw/ 裡有的內容。不得使用外部知識、網路搜尋結果或記憶補內容。
3. 推論必須標「（推論）」，並寫出根據哪段原文。
4. raw/ 不放個資或機密文件。
5. 新來源必須先通過第 5 節版權檢查，才能放進 raw/。
6. 下載電子書只能由使用者用網站正式下載按鈕取得。不得讓 AI 爬 Standard Ebooks 網站（該站有防爬陷阱連結，會封鎖 IP）。
7. 不確定時停下來問使用者，不要自己決定。

## 4. 頁面格式
### 語言
中文說明 + 英文原文。英文引句保留原文，旁邊可附中文解釋。

### 出處格式
- 每篇來源有一個短 ID（定義在 wiki/sources.md），例如 `peter-rabbit`。
- 事實後面標 `[src: 短ID ¶段落]`，例如 `[src: peter-rabbit ¶3]`。
- 英文引句寫法：`"英文原文" [src: 短ID ¶段落]`，引句必須和該段原文一字不改。
- 引句只能是完整一句或完整片語，不准自己刪中間；要省略時用 `...` 分段，每段都必須一字不改。
- 不准為了好懂而改寫英文原文。要簡化就用中文解釋，原文保持不動。

### 頁面開頭（frontmatter）
```
---
type: story | character | place | vocabulary | overview
book: potter
sources: [peter-rabbit, benjamin-bunny]
---
```

### 連結
頁面之間用 `[[頁面檔名]]` 互連（Obsidian 格式）。只在原文有根據時才建立連結，不得為了圖好看而硬連。

### 各類頁面要有的內容
- stories/：故事摘要（依段落順序）、出場角色、出現地點、重要單字，全部附出處。
- characters/：角色特徵、出現在哪幾篇、和其他角色的關係，全部附出處。
- places/：分兩欄。「原文描述」附出處；「氛圍判斷」（例如偏暗、偏亮）一律標（推論）並寫根據哪段原文。供簡報配色使用。
- vocabulary/：單字、原文例句（一字不改，附出處）、中文解釋、出現在哪幾篇。
- overview.md：全書綜合整理，每次 ingest 後更新。

## 5. 版權檢查（第一關）
新來源進 raw/ 之前：
1. 列出所有著作人（作者、插畫家、譯者、編者）。
2. 每人查卒年，至少兩個可靠來源互相對照。
3. 依台灣著作權法第 30 條：卒年 + 50 年，算到該年 12 月 31 日。已過才算通過。
4. 記進 wiki/sources.md：短 ID、篇名、著作人、卒年、查證來源、保護期屆滿日、下載來源。
5. 不通過：停下來告訴使用者，換書。

已查證：Beatrix Potter 卒於 1943-12-22（Britannica；Cambridge Orlando），台灣保護期 1993-12-31 屆滿。作者兼插畫家。

## 6. Ingest 流程（一次一篇）
觸發：只有使用者明確說「ingest 某篇」時才開始。AI 不得自行開始下一篇 ingest。

1. 確認該篇已通過版權檢查、已由腳本切好放在 raw/potter/。
2. 讀該篇原文。
3. 前兩次 ingest：寫頁面前，先用 5 行以內向使用者報告重點，等使用者確認再寫。之後的 ingest 可直接寫，完成後報告。
4. 寫或更新：stories/ 該篇頁面、相關 characters/、places/、vocabulary/、overview.md。
5. 更新 index.md（新頁面加一行）、sources.md。
6. 在 log.md 最後加一筆（格式見第 10 節）。
7. 執行腳本 lint（第 7 節）。全過才能 git commit，訊息格式：`ingest: 篇名`。
8. lint 沒過：見第 9 節。

## 7. Lint
### 腳本 lint（每次 ingest 後執行，腳本說了才算）
1. 英文引句在所標段落中找得到（比對前兩邊都正規化：彎引號 ‘’“” 轉直引號、刪除看不見的 U+FEFF、不換行連字號 U+2011 轉 -、… 轉 ...、連續空白變一個、去掉斜體標記）。
2. 每個 `[src: ID ¶n]` 的 ID 存在於 sources.md，段落 ¶n 真的存在。
3. 所有 `[[連結]]` 指向的頁面都存在。
4. 沒有孤兒頁：每頁至少被一頁連到（index.md 不算）。
5. index.md 列出所有 wiki 頁面。
6. raw/ 每個檔案在 sources.md 都有版權紀錄。

### AI 審查（兔子系列 4 篇 ingest 完後，開新對話執行）
只給審查者 wiki/ 與 raw/，不給本次對話內容。檢查：
7. 推論都有標（推論），且寫出根據。
8. 頁面之間說法一致，以 raw/ 為準。
9. 原文提到但還沒建頁的重要角色或地點；以及應該互連卻沒有 [[連結]] 的頁面（缺少的交叉連結）。

## 7.5 Query（例如產生簡報）
- 依 Karpathy：好的答案要存回 Wiki。簡報完成後，把簡報大綱存成 wiki 頁面（放 books/potter/，連到它用到的頁面），並在 log.md 記一筆 `query`。
- 簡報階段的詳細流程另寫規格檔，到時再與使用者討論。

## 8. 矛盾處理
- Wiki 頁面之間不一致：是 AI 寫錯，以 raw/ 原文為準修正，記進 log.md。
- 版本差異：只認 Standard Ebooks 版，其他版本不進 raw/。
- 故事本身的荒謬或不合邏輯：是作者刻意寫的，照原文記錄，必要時標「原文如此」，不得修正。
- 推論和原文衝突：以原文為準，刪除或改寫推論。

## 9. 剎車
- 腳本 lint 失敗：只修檢查報告列出的問題，不得順手改其他內容。最多 3 輪。
- 3 輪還沒過：停止，把報告交給使用者決定。
- 原文資料不足以寫某頁：不要硬湊，留空並在 log.md 註明。

## 10. log.md 格式
每筆以固定開頭，方便 grep：
```
## [YYYY-MM-DD] ingest | 篇名
- 新增頁面：...
- 更新頁面：...
- lint：第 N 輪通過 / 失敗項目與修正
```
其他類型：`setup`（建置、腳本）、`lint`、`review`（AI 審查）、`query`（例如產生簡報）、`fix`。

## 11. 插圖
- 插圖由腳本從 epub 取出，放 raw/assets/potter/，並產生 images.md：圖檔名 ↔ 篇名 ↔ 緊鄰段落 ¶。
- images.md 的 alt 欄是 Standard Ebooks 製作者寫的描述，不是 Potter 原文，不得當故事事實引用。
- raw 段落開頭的〔獻詞〕〔歌謠〕〔題詞〕〔副標題〕是腳本加的標記，不是原文。
- Wiki 頁面不放圖。簡報階段才依 images.md 挑圖，圖說要標出對應段落。
- 不得讓 AI 看圖猜內容當作事實。

## 12. 目前進度
- 第一批：peter-rabbit、benjamin-bunny、flopsy-bunnies、mr-tod。
- 第 5 篇：4 篇完成後，依 Wiki 實際長出的連結由使用者決定。

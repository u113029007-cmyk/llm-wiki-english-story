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

## [2026-11-21] fix | 觸發可一次指定多篇
- Joanna 確認：「觸發」管 ingest 開始前，「前兩篇先報告重點」管 ingest 中途，兩者不衝突。改為可一次觸發多篇，依序做完一起報告。

## [2026-11-21] setup | 腳本 lint scripts/lint.py
- 實作 AGENTS.md 第 7 節第 1-6 項；報告存到 reports/。
- 驗證：在暫存複本放一頁故意寫錯的測試頁。6 種錯誤（AI 改寫引句、段落不存在、ID 打錯、斷連結、孤兒頁、未列 index、raw 無版權紀錄）全部抓到；2 個正確寫法（直引號、`...` 省略）沒有被誤判。
- 額外：沒有出處的長條列只列為「提醒」，因為腳本無法可靠判斷一行是不是事實，需人工判斷。

## [2026-11-21] fix | 「每條都要有出處」改為腳本強制
- 原本 lint 只把「沒出處的條列」列為提醒，因為頁面格式自由，腳本分不出哪行是事實。
- 改法：AGENTS.md 規定 books/ 頁面只能用標題、條列、表格；每條條列與每列表格都要有 [src:]（只放連結、格式為 `標籤：[[連結]]`的條列除外）。lint 第 2 項改為強制失敗。
- 驗證：測試頁中「Peter 吃了紅蘿蔔。」（無出處）、自由段落、無出處的表格列都被抓到；正確的條列、推論條列、純連結條列通過。
- 測試時發現 lint 誤判：表格標題列被要求出處 → 修正為跳過標題列與分隔列。
- 限制：腳本只能確認「有標出處、出處存在」，無法判斷中文摘要是否忠於原文（例：¶10 原文是 radishes 小蘿蔔，插圖描述卻是 carrot；若寫「吃了紅蘿蔔 [src: peter-rabbit ¶10]」腳本會通過）。這類錯誤交給新對話的 AI 審查。

## [2026-11-21] ingest | The Tale of Peter Rabbit
- 觸發：Joanna 說「ingest peter-rabbit」。
- 寫頁面前先報告 5 行重點；Joanna 決定 Flopsy、Mopsy、Cottontail 各一頁，配角（Mrs. McGregor、麻雀、老鼠、白貓）只寫在故事頁。
- 新增頁面（20）：stories/peter-rabbit；characters/peter、mrs-rabbit、flopsy、mopsy、cottontail、mr-mcgregor、benjamin-bunny-character；places/mr-mcgregors-garden、fir-tree-rabbit-hole、the-wood；vocabulary/naughty、mischief、lettuces、radishes、parsley、frightened、sieve、camomile-tea；potter-overview。
- 更新頁面：index。
- 跨篇線索：¶27 提到表弟 Benjamin Bunny，已建角色頁等下一篇補充。
- lint 第 1 輪失敗 2 處：(1) 故事頁「所屬：」那行忘了加 `- `，違反條列格式（AI 寫頁錯誤）；(2) log.md 中說明規則用的範例 `標籤：[[連結]]` 被當成斷連結（lint 誤判）。
- 修正：(1) 補上 `- `；(2) lint.py 改為忽略反引號內的文字，log 範例加上反引號。
- lint 第 2 輪：全過（23 頁、112 個出處、24 個英文引句）。
- 其他：總覽檔名改為 potter-overview.md（避免日後 Alice 撞名），AGENTS.md 同步更新。

## [2026-11-21] ingest | The Tale of Benjamin Bunny
- 觸發：Joanna 說「ingest benjamin-bunny」。寫頁面前先報告 5 行重點（第 2 次，最後一次需確認的 ingest）。
- Joanna 決定：(1) Mrs. McGregor 第二次出現，依規則建頁；(2) 本篇的貓原文只寫 "The cat"，不建頁、不和第一篇的白貓連結，故事頁註明不能推定為同一隻；(3) 8 個單字照提案。
- 新增頁面（11）：stories/benjamin-bunny；characters/old-mr-benjamin-bunny、mrs-mcgregor；vocabulary/cousin、widow、poorly、scarecrow、clogs、onions、basket、greenhouse。
- 更新頁面（14）：stories/peter-rabbit（上下篇連結、Mrs. McGregor 移出配角）；characters/benjamin-bunny-character、peter、mrs-rabbit、mr-mcgregor、flopsy、mopsy、cottontail；places 三頁；vocabulary/lettuces、camomile-tea；potter-overview；index。
- 跨篇連結：稻草人衣服（peter-rabbit ¶31 → benjamin-bunny ¶12、¶23）、兔媽媽是寡婦（peter-rabbit ¶4 → benjamin-bunny ¶7）、從 Benjamin 聽說貓（peter-rabbit ¶27 → benjamin-bunny ¶37-41）。
- 寫入程式第 1 次執行失敗：Python 3.10 f-string 引號衝突，整支未執行，無半成品；修正後重跑。
- lint 第 1 輪：全過（34 頁、231 個出處、42 個英文引句）。
- 自我檢查發現 1 處腳本抓不到的問題：fir-tree-rabbit-hole 把「最整齊的兔子洞」直接寫成冷杉樹下的家，實為接合 ¶6 與 ¶9 的推論 → 改標（推論）並寫出根據。lint 重跑全過。
- 其他：新增 .gitignore 忽略 Obsidian 的 .obsidian/ 設定資料夾。

## [2026-11-21] setup | 長篇分段閱讀機制 scripts/plan_reading.py
- 起因：mr-tod 有 156 段，是 peter-rabbit 的 4 倍多。原本「分段讀」只是對話裡的口頭計畫，換對話或換工具就會遺失，因此寫進規則與腳本。
- 規則（AGENTS.md 第 6 節第 2 步）：超過 60 段就由腳本平均切段；每段讀完把重點寫進 notes/短ID.md；全部讀完才寫 wiki。
- 門檻 60 為依目前資料選定（前兩篇 37、58 段一次讀完沒有問題），非研究標準，之後可調整。
- 試跑：peter-rabbit 37、benjamin-bunny 58、flopsy-bunnies 57 段不分段；mr-tod 156 段分 3 段（¶1-52、¶53-104、¶105-156）。

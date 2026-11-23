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

## [2026-11-21] ingest | The Tale of the Flopsy Bunnies
- 觸發：Joanna 說「ingest flopsy-bunnies 和 mr-tod」（一次觸發兩篇，依 B 規則連續做完一起報告；本篇起不需寫前確認）。
- plan_reading.py：57 段，一次讀完。
- 新增頁面：stories/flopsy-bunnies；characters/flopsy-bunnies-children、thomasina-tittlemouse（本篇主要救援者，雖只出現一篇仍建頁）；places/mr-mcgregors-rubbish-heap、mr-mcgregors-house；vocabulary/soporific、slumber、sack、rubbish、doleful、despair、resourceful、improvident。
- 跨篇連結：Benjamin 長大娶 Flopsy、Peter 開苗圃借高麗菜、萵苣第三次出現。
- 第 5 篇候選線索：Thomasina Tittlemouse 說她認識 Peter [src: flopsy-bunnies ¶16]；sources.md 裡有一篇 mrs-tittlemouse，是否同一隻需讀原文才能確定。

## [2026-11-21] ingest | The Tale of Mr. Tod
- plan_reading.py：156 段，分 3 段（¶1-52、¶53-104、¶105-156）讀；每段讀完寫入 notes/mr-tod.md，三段讀完才寫 wiki。
- 新增頁面：stories/mr-tod；characters/mr-tod-character（故事頁已用 mr-tod 檔名）、tommy-brock；places/mr-tod-stick-house、bull-banks-house；vocabulary/disagreeable、badger、snoring、oven、tunnel、furious、pail、grinning。
- 原文名字差異（依第 8 節照原文記錄）：Benjamin 的爸爸在 benjamin-bunny 篇叫 old Mr. Benjamin Bunny，本篇叫 old Mr. Benjamin Bouncer／old Mr. Bouncer；本篇明說其子為 Benjamin Bunny，判定同一角色，兩名並記。
- 數字差異照原文記錄、不推定：flopsy-bunnies 篇數到 6 隻，本篇 Benjamin 說 7 隻。
- 本篇的兔子洞是 Benjamin 一家的，不能推定是冷杉樹下 Peter 家，未寫入 fir-tree-rabbit-hole。

## [2026-11-21] lint | 兩篇 ingest 後
- 兩篇合計：新增 26 頁、更新 12 頁。
- 第 1 輪失敗 1 處：flopsy-bunnies 故事頁把 ¶20、¶23 兩個出處並排在引句後，引句實際在 ¶23，lint 以緊接引句的出處比對而失敗（AI 寫頁錯誤）。修正為各句各標。
- 第 2 輪全過（60 頁、473 個出處、82 個英文引句）。
- lint 過後自我重讀，發現 3 處腳本抓不到的問題並修正：
  1. potter-overview「四篇最後都靠家人或朋友救出」與原文衝突（peter-rabbit ¶18 是自己逃出）→ 改寫為四篇各自的脫身方式並附出處。
  2. mr-tod 故事頁「兩人角色互換」是比較詮釋，未標（推論）→ 補標。
  3. tommy-brock 頁把「後來害了他」寫在連結條列的標籤裡，繞過「純連結條列免出處」的規則 → 移除，改為附出處的條列。
- 發現規則漏洞：`標籤：[[連結]]` 的標籤本身可以夾帶沒出處的說法，lint 目前無法檢查。待與 Joanna 討論補法。

## [2026-11-21] fix | 連結條列標籤白名單（檢查往前移）
- Joanna 選 A：AGENTS.md 第 4 節加「允許的標籤」白名單，lint 直接讀 AGENTS.md 這一行（單一來源，避免規則與腳本不一致）。不在白名單的標籤 → lint 第 2 項失敗。
- 上線後在既有 Wiki 抓到 7 個白名單外標籤（potter-overview 4、flopsy 1、old-mr-benjamin-bunny 1、the-wood 1）。修正方式：描述性內容改成附出處的條列，標籤改用白名單詞。
- 同時又出現一次 log 範例被當斷連結（上一筆 log 說明漏加反引號），已補。
- 驗證：測試頁中「篇章：」通過、「後來害了他：」被擋下。修正後 Wiki lint 全過（60 頁、487 個出處）。
- 意義：原本只能靠 AI 審查發現的「標籤夾帶說法」，改成在寫入當下就由 lint 擋下（講義 p.26：檢查往前移）。

## [2026-11-23] review | 依審查報告 1 修正
- 審查：Joanna 另開新對話執行 reviews/review-prompt-1.md，審查者只讀 AGENTS.md、wiki/books/、sources.md、raw/potter 4 篇，未讀 log/notes/reports。報告存於 reviews/review-1.md。
- 結果：57 頁、約 487 條出處全數檢查；37 個問題（高 0、中 12、低 25）；類型：忠實度 16、推論未標 11、缺連結 5、不一致 3、缺頁 2。lint 全過的狀態下仍有 37 個問題，lint 一個都抓不到。
- Joanna 的決定：
  1. 親屬稱謂直譯，需分輩分或父系母系時兩種都寫並附原文（brother → 哥哥/弟弟、cousin → 表哥/表弟、aunt → 阿姨/姑姑、nephew → 姪子/外甥）；白名單同步更新。
  2. radishes 頁「插圖描述是 carrot」一條刪除（出處格式指不到 images.md），教訓留在 log。
  3. mr-tod 故事頁「閱讀方式」一條是工作紀錄，移除（本 log 已有）。
  4. #31、#32 新增地點頁：待 Joanna 決定。
  5. AGENTS.md 新增規則：跨篇、跨段認定同一角色或地點，一律標（推論）。
- 已修正：#1-#30、#33-#37（#31、#32 待決定）。另依 Joanna 決定 1 全域處理「阿姨」「表弟」等，並修正 index 與兩處把 foxey 直譯成狐狸的地方。
- lint：修正後第 1 輪全過（60 頁、531 個出處、88 個英文引句）。
- 已知限制：引句格式不能包含內層引號（例如 ¶2 的 “soporific.”），所以改引 ¶4 的完整句。

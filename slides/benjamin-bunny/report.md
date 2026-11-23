# 簡報檢查紀錄：benjamin-bunny

## [2026-11-23 11:54] 出處檢查 slides_check.py
- 範圍：17 頁、74 條、22 句英文引句
- 結果：✅ 全過

## [2026-11-23] 覆蓋率關卡 slides_coverage.py
- 4 個目標、22 個 wiki 頁：✅ 通過。測試：sources.md 列不存在的 carrots 頁 → 停下。

## [2026-11-23] 大綱
- 17 頁大綱經 Joanna 確認（第 11 頁依審查修正寫「轉角看到了某個東西（原文由插圖呈現）」）。
- 風格經 Joanna 決定：Potter 小書風、要有沉浸感的整體美編、依地點頁氛圍換深淺、左圖右文。

## [2026-11-23] 逐頁稿自我檢查
- 寫稿時發現第 6 頁「最整齊的洞是 Peter 家」在 wiki 是（推論），改用故事頁有出處的說法。
- 出處檢查測試：故意寫錯的測試頁 6 種錯誤（缺出處、改寫引句、濫用 [meta]、頁面不存在、插圖不屬於本篇、氛圍依據不是地點頁）全部被擋下。

## [2026-11-23] 渲染 build_deck.py + 渲染檢查 render_check.py
- 渲染由腳本產生，AI 不手寫 HTML；圖說只用 images.md 段落位置（不用 alt，例：illustration-104 的 alt 說老兔子也打了 Peter，原文 ¶52-53 只寫打 Benjamin）。
- 渲染檢查在雲端環境以 Chromium 執行（Joanna 電腦安裝 playwright 逾時），1600×900 逐頁截圖。
- 第 1 輪：✅ 全過（無溢出、10 張插圖載入、文字與稿件一致）。
- 人工看截圖（腳本看不到的美觀問題）：(1) 右頁字偏小、下方留白多 → 內文放大約 15%；(2) 小測驗隱藏答案仍佔位置，Q1 與 Q2 間空一大格 → 答案改為點擊才出現。
- 修改後第 2、3 輪：✅ 全過。截圖存於 screenshots/。

## [2026-11-23 16:24] 出處檢查 slides_check.py
- 範圍：17 頁、74 條、22 句英文引句
- 結果：❌ 52 處
  - slide-03.md: 條列 5 條，超過 4 條
  - slide-03.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - 媽媽交代不准去 Mr. McGregor 的花園 [wiki: peter-rabbit]
  - slide-03.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - "don't go into Mr. McGregor's garden." [wiki: pe
  - slide-03.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - Peter 不聽話偷跑進去，被追得弄丟外套和鞋子 [wiki: peter-rabbit]
  - slide-03.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - Mr. McGregor 把外套和鞋子掛起來當稻草人 [wiki: peter-rabbit]
  - slide-03.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - 這一篇就從「沒衣服穿的 Peter」開始 [wiki: benjamin-bunny]
  - slide-04.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - Benjamin 和 Peter 是表哥/表弟（cousin） [wiki: benjamin-
  - slide-04.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - "nearly tumbled upon the top of his Cousin Peter
  - slide-04.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - Benjamin：蹦蹦跳跳、在花園裡很自在 [wiki: benjamin-bunny-char
  - slide-04.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - Peter：這次身體不舒服、一直聽到聲音、想回家 [wiki: peter]
  - slide-05.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - 兔媽媽 Mrs. Rabbit 是寡婦，靠織手套、賣香草維生 [wiki: mrs-rabbit
  - slide-05.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - "Old Mrs. Rabbit was a widow" [wiki: widow]
  - slide-05.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - Benjamin 的爸爸 old Mr. Benjamin Bunny，一點也不怕貓 [wiki
  - slide-05.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - Mr. McGregor 和 Mrs. McGregor：花園的主人 [wiki: mr-mcg
  - slide-06.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - 樹林：兔子們住在花園後面的樹林裡 [wiki: the-wood]
  - slide-06.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - 兔子洞：Peter 一家住在樹林裡最整齊、沙最多的兔子洞 [wiki: benjamin-bun
  - slide-06.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - 樹林底有一道牆，牆頂可以往下看到花園 [wiki: mr-mcgregors-garden]
  - slide-06.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - 花園裡有梨樹、萵苣苗床、稻草人和溫室 [wiki: mr-mcgregors-garden]
  - slide-07.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - 早上，Benjamin 看到 McGregor 夫婦坐馬車出門 [wiki: benjamin-
  - slide-07.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - 他溜到路上，蹦蹦跳跳去找親戚 [wiki: benjamin-bunny]
  - slide-07.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - "with a hop, skip, and a jump" [wiki: benjamin-b
  - slide-07.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - 親戚就是阿姨/姑姑和 Peter 一家 [wiki: benjamin-bunny]
  - slide-08.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - Benjamin 在冷杉樹後面找到 Peter [wiki: benjamin-bunny]
  - slide-08.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - "He looked poorly, and was dressed in a red cott
  - slide-08.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - 問他衣服去哪了，Peter 說在稻草人身上 [wiki: benjamin-bunny]
  - slide-08.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - "The scarecrow in Mr. McGregor's garden" [wiki: 
  - slide-09.md: 條列 5 條，超過 4 條
  - slide-09.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - 兩人走到牆頂，看到掛著 Peter 衣服的稻草人 [wiki: benjamin-bunny]
  - slide-09.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - Benjamin 說鑽大門會弄壞衣服 [wiki: benjamin-bunny]
  - slide-09.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - "the proper way to get in is to climb down a pea
  - slide-09.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - Peter 頭朝下摔下去，還好苗床很軟 [wiki: benjamin-bunny]
  - slide-09.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - 穿木鞋的 Benjamin 留下很多小腳印 [wiki: clogs]
  - slide-10.md: 條列 5 條，超過 4 條
  - slide-10.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - 衣服拿回來了，但鞋子進水、外套縮水 [wiki: benjamin-bunny]
  - slide-10.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - Benjamin 提議用手帕裝洋蔥送阿姨/姑姑 [wiki: benjamin-bunny]
  - slide-10.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - "they should fill the pocket-handkerchief with o
  - slide-10.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - Benjamin 很自在，還吃了萵苣葉 [wiki: lettuces]
  - slide-10.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - "Benjamin, on the contrary, was perfectly at hom
  - slide-11.md: 條列 5 條，超過 4 條
  - slide-11.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - Peter 越來越害怕，眼睛睜得好大 [wiki: benjamin-bunny]
  - slide-11.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - "his eyes were as big as lolly-pops!" [wiki: ben
  - slide-11.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - 轉角看到了某個東西（原文由插圖呈現） [wiki: benjamin-bunny]
  - slide-11.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - Benjamin 立刻把大家藏到大籃子底下 [wiki: basket]
  - slide-11.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - 文字裡貓這時才出現：牠坐在籃子上五個小時 [wiki: benjamin-bunny]
  - slide-12.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - old Mr. Bunny 在牆頂上出現，正在找兒子 [wiki: benjamin-bunny
  - slide-12.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - "Old Mr. Bunny had no opinion whatever of cats."
  - slide-12.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - 他跳到貓身上，把貓踢進溫室，鎖上門 [wiki: benjamin-bunny]
  - slide-12.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - "kicked it into the greenhouse" [wiki: greenhous
  - slide-13.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - Mr. McGregor 回來，看到很小的木鞋腳印 [wiki: benjamin-bunny]
  - slide-13.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - 他也想不通貓怎麼會被鎖在溫室裡 [wiki: mr-mcgregor]
  - slide-13.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - 媽媽因為 Peter 找回衣服，就原諒了他 [wiki: mrs-rabbit]
  - slide-13.md: 內容頁條列必須是「中文 ｜ "英文原文" [wiki: 頁面]」→ - 洋蔥掛在廚房天花板上，和香草放在一起 [wiki: benjamin-bunny]

## [2026-11-23 16:25] 出處檢查 slides_check.py
- 範圍：17 頁、66 條、50 句英文引句
- 結果：✅ 全過

## [2026-11-23] 大圈退回：中英對照（Joanna 看成品發現）
- 問題：很多內容頁只有中文、沒有英文。源頭在 wiki（摘要多半沒附英文），已退回 wiki 補 30 句原文（見 wiki/log.md）。
- 檢查往前移：規格與 slides_check.py 新增「內容頁每條都必須是 中文 ｜ "英文原文" [wiki: 頁面]」。上線時在舊稿件擋下 52 處。
- 改寫第 3-13 頁稿件後：出處檢查 ✅ 全過。

## [2026-11-23] 電子書版型（Joanna 指示）
- 沒插圖的頁跨左右兩頁；加入目錄、隱藏／顯示中文、展開完整英文句、A−／A+、閱讀進度條、記住讀到哪一頁、翻頁動畫。
- 「展開」的完整句由 build_deck.py 從 wiki 頁自動找出（不經 AI 手寫），縮短版用 `...`。
- 渲染檢查：✅ 全過（render_check.py 已忽略按鈕文字）。
- 功能測試 feature_test.py：方向鍵翻頁、目錄開關與跳頁、隱藏中文、展開／收合完整句、字體放大、翻開答案，全部通過。第一次跑時「展開」顯示失敗，查證是測試讀錯元素（測試本身的錯），修正測試後通過。
- 人工看截圖：小測驗字小且擠在左邊 → 放大置中。

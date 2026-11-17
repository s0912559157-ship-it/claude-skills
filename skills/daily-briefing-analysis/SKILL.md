---
name: daily-briefing-analysis
description: Use when the user says 讀取今日簡報, asks for today's morning brief, or asks to analyze today's briefing: generate or summarize it, analyze market/international/AI news by the bundled frameworks with an independent subagent, discuss with the user, build PDF decks, then self-score and log improvement proposals.
---

# 每日簡報分析流程

一律用繁體中文。這個 Skill 自帶所需的一切（分析規則、交辦格式、追蹤表範本、簡報產生器），
換任何一台設備、任何使用者，只要有這個資料夾就能運作。Skill 不規定使用者電腦上的路徑：第一次使用時請使用者開一個資料夾，之後只在那裡存規定的檔案。

以下路徑都相對於這個 Skill 的資料夾：

| 檔案 | 用途 |
|---|---|
| `references/morning-brief.md` | 產生晨間簡報（當日簡報）的指令 |
| `references/market-framework.md` | 市場分析框架（五步） |
| `references/intl-framework.md` | 國際局勢分析框架（四步） |
| `references/ai-framework.md` | AI 新聞分析框架（以國際框架為底） |
| `references/subagent-brief.md` | 交辦 subagent 的格式（每一輪） |
| `references/tracker-template.md` | 三份簡報共用的追蹤表範本 |
| `references/deck-requirements.md` | 簡報規格：先和使用者討論、必備三項、存檔規則 |
| `references/scorecard.md` | 評分表：自評＋獨立 agent 評分，四項 1–5 分 |
| `references/source-registry.md` | 來源登記表：來源靠評分慢慢汰換 |
| `references/review-loop.md` | 自我檢討循環：每天評分與修改案，三天一輪改 GitHub |
| `scripts/deck.py`、`scripts/style.css` | 簡報產生器（10/20 市場簡報樣式，1440×810 PDF） |
| `scripts/example_deck.py` | 產生器範例，複製來改 |

## 0. 使用者資料夾與暫存區

### 使用者資料夾（下稱 `HOME_DIR`）

這個 Skill 只用**一個**使用者資料夾，裡面**只能有**下面這些檔案：

```
HOME_DIR/
├── 紀錄/
│   ├── tracker.md                       追蹤表（三份簡報共用）
│   ├── source-registry.md               來源登記表
│   ├── 評分/YYYY-MM-DD-scorecard.md       評分紀錄（每天一份）
│   └── 修改案/YYYY-MM-DD-proposal.md      修改案（每天一份）
└── YYYY-MM-DD/
    ├── morning-brief-YYYY-MM-DD.html    晨間簡報
    ├── YYYY-MM-DD-市場討論.pdf
    ├── YYYY-MM-DD-國際新聞討論.pdf
    └── YYYY-MM-DD-AI新聞討論.pdf
```

- 怎麼找：目前目錄（或使用者說的位置）有 `紀錄/tracker.md` 就是 `HOME_DIR`。
- 找不到：**請使用者開一個資料夾**（或指定一個空資料夾）給這個 Skill 用，拿到後建立 `紀錄/`，
  從 `references/tracker-template.md`、`references/source-registry.md` 複製出 `tracker.md`、`source-registry.md`。
- 有專案記憶的環境：把 `HOME_DIR` 的位置記下來，下次不用再問。

### 暫存區（下稱 `TMP`）

其餘所有檔案**都不能留在使用者的設備上**：底稿（main/agent 各輪）、簡報腳本、簡報 HTML、
純文字稿、截圖、任何為了方便自己閱讀而產生的檔案。

- 開工時用系統暫存資料夾建一個 `TMP`（例如 `mktemp -d`），這些檔案只能寫在 `TMP`。
- 當天第 6 步（評分與修改案）寫完後，**刪掉整個 `TMP`**。
- 收尾前列一次 `HOME_DIR` 的內容，確認只有上面那些檔案；多出來的是你產生的就刪掉，不是你產生的不要動。

### 今天是循環第幾天

讀 `紀錄/修改案/` 裡最新一份的開頭（寫著「第 N 輪第 N 天」）。沒有任何修改案時，今天是第 1 輪第 1 天。

## 1. 產生今日晨間簡報

- **由 agent 自己產生**：照 `references/morning-brief.md` 做今天的晨間簡報，存成 `HOME_DIR/YYYY-MM-DD/morning-brief-YYYY-MM-DD.html`。
  今天的檔案已經存在（例如排程已經做好）就直接用，不要重做。
- 使用者這次另外附了簡報檔或連結：以使用者給的為準，不另外產生。
- 讀來源前先看 `紀錄/source-registry.md`，優先用「常用」來源，不用「停用」來源。

拿到後：
- 核對簡報日期是不是今天（使用者的時區）。
- 給使用者簡短摘要：三則左右重點新聞＋行程。
- 把新聞分成市場、國際局勢、AI、每日新知四類。

## 2. 讀分析規則

- 讀 `references/` 裡對應的框架**全文**，以檔案內容為準，不要憑記憶套用。
- 使用者如果給了更新版的規則檔，以使用者給的為準，並提醒使用者把新版放回這個 Skill。

## 3. 依框架分析（市場、國際局勢、AI 各一份）

- 每份都要另開一個 subagent 做「先各自獨立，再交流」，交辦內容與交回格式照 `references/subagent-brief.md`：
  1. 主分析者先寫 `main-round1.md`（候選解釋、證據缺口、判別條件）。
  2. subagent 只拿簡報、框架、追蹤表，獨立寫 `agent-round1.md`。
  3. 雙方都寫完才交換，互相挑戰（`main-round2.md`、`agent-round2.md`）。
  4. 記下最強反對意見與它的去向。雙方一致不算多一份證據。
- 校正晨間簡報的錯誤說法（日期、程序階段、來源性質）。
- 底稿（main-round1、agent-round1/2、main-round2）都寫在 `TMP/{market|intl|ai}/`。
- 更新 `HOME_DIR/紀錄/tracker.md`：新增項目、改狀態、寫到期日（寫明時區）。
- 環境不能開 subagent 時：告訴使用者這次只有單一分析者，並在簡報封面註明「未經獨立 agent 挑戰」。

### 每日新知

- 簡報裡的「每日新知」不套三份框架，只做名詞解釋與重點整理。
- 要不要另外做成一份簡報，第一次遇到時先問使用者，之後照使用者的答案做。

## 3.5 先和使用者討論

- 照 `references/deck-requirements.md` 的「做簡報之前」：說重點與暫定判斷，主動問使用者 3–5 個問題，討論完才做簡報。
- 使用者的問題要在做簡報前回答完。

## 4. 做成簡報

- 必須符合 `references/deck-requirements.md`：一句話結論（含信心程度）、追蹤表頁、來源清單頁。

- 用 `scripts/deck.py`：照 `scripts/example_deck.py` 寫一支當日腳本放在 `TMP/decks/{market|intl|ai}.py`，呼叫 `render()` 在 `TMP/decks/` 產生 HTML＋PDF。腳本開頭用 `sys.path.insert(0, '<這個 Skill 的 scripts 資料夾>')` 匯入 `deck`。
- 需要 Python 3 與 Playwright：`pip install -r scripts/requirements.txt && python -m playwright install chromium`。已有 Chromium 時可設環境變數 `DECK_CHROMIUM=<chrome 執行檔路徑>`。
- 版面規則：
  - 每頁閱讀負擔輕、一眼可掃；寧可多頁也不要塞字。不需要問題目錄頁。
  - 必須涵蓋所有討論項目，包括使用者的每個追問與名詞解釋，不可只摘要。回答使用者提問的頁面用 `ask=True`。
  - 美台股並談要標日期與市場，依時序（前一晚美股→當天台股）。
  - 國際、AI 頁面依框架加刊出標籤（如【轉述】【程序中】）；Anthropic 是當事方時加關係註記。
  - 每頁頁尾寫來源；封面寫資訊截止時間。
- PDF 命名：`YYYY-MM-DD-{市場|國際新聞|AI新聞}討論.pdf`，做好後先給使用者看（有附檔功能就附上）。

## 5. 定稿與存檔

- 要不要存由使用者決定。使用者回「可以」或說要存 = 定稿，不用再問：只把 PDF 從 `TMP/decks/` 複製到 `HOME_DIR/YYYY-MM-DD/`。
- 使用者不要的簡報就不存，跟著 `TMP` 一起刪掉。

## 6. 評分、修改案、清理（每天）

1. 照 `references/scorecard.md` 打分（自評＋獨立 agent），存 `HOME_DIR/紀錄/評分/YYYY-MM-DD-scorecard.md`。
2. 照 `references/review-loop.md` 寫當天修改案，存 `HOME_DIR/紀錄/修改案/YYYY-MM-DD-proposal.md`，開頭寫「第 N 輪第 N 天」。
3. 更新 `HOME_DIR/紀錄/source-registry.md` 的使用次數與被更正次數。
4. 把分數與修改案重點告訴使用者。
5. 刪掉 `TMP`，列一次 `HOME_DIR` 確認只剩規定的檔案。
6. 第 3 天：合併成本輪修改案給使用者看，使用者同意的部分才改 Skill 並推到 GitHub。

## 出錯時怎麼辦

| 狀況 | 處理 |
|---|---|
| 晨間簡報產生不了（連不到來源） | 能連的來源照做，連不到的在簡報末尾註明；全部連不到就請使用者給簡報檔或連結 |
| 框架檔不見或讀不到 | 停下來告訴使用者缺哪一份，不要憑記憶分析 |
| 沒有 Playwright／Chromium 且裝不了 | 交付 `render(..., pdf=False)` 產生的 HTML，請使用者用瀏覽器「列印成 PDF」（版面 1440×810、背景圖形打開） |
| 字型載不到（離線） | 照樣產生，告訴使用者字型會是系統預設 |
| 不能開 subagent | 見第 3 步：單一分析者並在封面註明 |
| 使用者沒有給資料夾 | 請使用者開一個；拿到之前只在對話裡交付，不寫進使用者設備 |
| `HOME_DIR` 出現規定以外的檔案 | 是你產生的就刪掉並在當天修改案記一條；不是你產生的不要動 |
| 不能開 subagent 打分 | 只有自評，評分紀錄註明「無獨立評分」 |
| 使用者還沒回覆本輪修改案 | 不推 GitHub，未決的修改案帶到下一輪 |

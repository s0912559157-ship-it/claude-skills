---
name: daily-briefing-analysis
description: Use when the user says 讀取今日簡報, asks for today's morning brief, or asks to analyze today's briefing: generate or summarize it, analyze market/international/AI news by the bundled frameworks with an independent subagent, and build PDF decks.
---

# 每日簡報分析流程

一律用繁體中文。這個 Skill 自帶所需的一切（分析規則、交辦格式、追蹤表範本、簡報產生器），
換任何一台設備，只要有這個資料夾就能運作；本機資料夾是「有的話才用」。

以下路徑都相對於這個 Skill 的資料夾：

| 檔案 | 用途 |
|---|---|
| `references/morning-brief.md` | 產生晨間簡報（當日簡報）的指令 |
| `references/market-framework.md` | 市場分析框架（五步） |
| `references/intl-framework.md` | 國際局勢分析框架（四步） |
| `references/ai-framework.md` | AI 新聞分析框架（以國際框架為底） |
| `references/subagent-brief.md` | 交辦 subagent 的格式（每一輪） |
| `references/tracker-template.md` | 三份簡報共用的追蹤表範本 |
| `scripts/deck.py`、`scripts/style.css` | 簡報產生器（10/20 市場簡報樣式，1440×810 PDF） |
| `scripts/example_deck.py` | 產生器範例，複製來改 |

## 0. 準備工作資料夾

- 在目前環境找一個可寫的工作資料夾（下稱 `WORK`），例如專案的共用檔案夾或目前目錄下的 `briefings/`。
- 當日底稿放 `WORK/YYYY-MM-DD-{market|intl|ai}-discussion/`，PDF 放 `WORK/`。
- 追蹤表：`WORK/tracker.md`；沒有的話從 `references/tracker-template.md` 複製一份。

## 1. 取得今日簡報

依序嘗試，找到就停：
1. 用戶這次訊息附上的檔案（HTML／PDF）或連結。
2. 有連接用戶電腦時：`閒聊/每日簡報/MMDD/當日簡報/` 裡的晨間簡報。
3. 以上都沒有 → 問用戶要上傳現成的簡報，還是現在照 `references/morning-brief.md` 產生一份。用戶說「做今天的簡報」時直接產生。

拿到後：
- 先核對簡報日期是不是今天（台北時間）。不是的話，告訴用戶簡報日期，問要用這份還是等新的。
- 給用戶簡短摘要：三則左右重點新聞＋行程。
- 把新聞分成市場、國際局勢、AI、每日新知四類。

## 2. 讀分析規則

- 讀 `references/` 裡對應的框架**全文**，以檔案內容為準，不要憑記憶套用。
- 用戶如果給了更新版的規則檔，以用戶給的為準，並提醒用戶把新版放回這個 Skill。

## 3. 依框架分析（市場、國際局勢、AI 各一份）

- 每份都要另開一個 subagent 做「先各自獨立，再交流」，交辦內容與交回格式照 `references/subagent-brief.md`：
  1. 主分析者先寫 `main-round1.md`（候選解釋、證據缺口、判別條件）。
  2. subagent 只拿簡報、框架、追蹤表，獨立寫 `agent-round1.md`。
  3. 雙方都寫完才交換，互相挑戰（`main-round2.md`、`agent-round2.md`）。
  4. 記下最強反對意見與它的去向。雙方一致不算多一份證據。
- 校正晨間簡報的錯誤說法（日期、程序階段、來源性質）。
- 更新 `WORK/tracker.md`：新增項目、改狀態、寫到期日（寫明時區）。
- 環境不能開 subagent 時：告訴用戶這次只有單一分析者，並在簡報封面註明「未經獨立 agent 挑戰」。

### 每日新知

- 簡報裡的「每日新知」不套三份框架，只做名詞解釋與重點整理。
- 要不要另外做成一份簡報，第一次遇到時先問用戶，之後照用戶的答案做。

## 4. 做成簡報

- 用 `scripts/deck.py`：照 `scripts/example_deck.py` 寫一支當日腳本放在 `WORK/YYYY-MM-DD-{market|intl|ai}-deck/build.py`，呼叫 `render()` 產生 HTML＋PDF。
- 需要 Python 3 與 Playwright：`pip install -r scripts/requirements.txt && python -m playwright install chromium`。已有 Chromium 時可設環境變數 `DECK_CHROMIUM=<chrome 執行檔路徑>`。
- 版面規則：
  - 每頁閱讀負擔輕、一眼可掃；寧可多頁也不要塞字。不需要問題目錄頁。
  - 必須涵蓋所有討論項目，包括用戶的每個追問與名詞解釋，不可只摘要。回答用戶提問的頁面用 `ask=True`。
  - 美台股並談要標日期與市場，依時序（前一晚美股→當天台股）。
  - 國際、AI 頁面依框架加刊出標籤（如【轉述】【程序中】）；Anthropic 是當事方時加關係註記。
  - 每頁頁尾寫來源；封面寫資訊截止時間。
- PDF 命名：`WORK/YYYY-MM-DD-{市場|國際新聞|AI新聞}討論.pdf`，做好後直接附給用戶看。

## 5. 定稿與歸檔

- 用戶回「可以」= 定稿，不用再問。
- 有連接用戶電腦時：把 PDF 存到 `閒聊/每日簡報/MMDD/{市場|國際局勢|AI}/`。沒有連接就只交付 PDF，並告訴用戶檔案在哪裡。
- 有專案記憶時：記下當日主題、結論、追蹤到期日。

## 出錯時怎麼辦

| 狀況 | 處理 |
|---|---|
| 找不到今日簡報 | 請用戶上傳、給連結，或照 `references/morning-brief.md` 現在產生一份 |
| 簡報日期不是今天 | 告訴用戶簡報日期，問要用這份還是等新的 |
| 框架檔不見或讀不到 | 停下來告訴用戶缺哪一份，不要憑記憶分析 |
| 沒有 Playwright／Chromium 且裝不了 | 交付 `render(..., pdf=False)` 產生的 HTML，請用戶用瀏覽器「列印成 PDF」（版面 1440×810、背景圖形打開） |
| 字型載不到（離線） | 照樣產生，告訴用戶字型會是系統預設 |
| 不能開 subagent | 見第 3 步：單一分析者並在封面註明 |
| 本機資料夾不可用 | 略過歸檔，只交付 PDF，並告訴用戶 |

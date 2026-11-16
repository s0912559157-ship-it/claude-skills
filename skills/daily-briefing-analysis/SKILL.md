---
name: daily-briefing-analysis
description: Use when the user says 讀取今日簡報 or asks to analyze today's briefing: summarize it, analyze market/international/AI news by their frameworks with an independent agent, and build PDF decks.
---

# 每日簡報分析流程

一律用繁體中文。

## 1. 讀今日簡報
- 讀電腦 `閒聊/每日簡報/MMDD/當日簡報/` 裡的晨間簡報（HTML 或 PDF）。
- 先給用戶簡短摘要：三則左右重點新聞＋行程。

## 2. 讀分析規則
- 市場：`閒聊/分析規則/市場分析規則/討論框架-修訂版.md`（五步：定問題與口徑→現象與競爭解釋→分辨檢查→雙向挑戰與暫定判斷→預約更新與撤回）。
- 國際局勢：`閒聊/分析規則/國際局勢分析規則/國際簡報分析框架-修訂版.md`（四步：截止與檢核→選題分級→解釋與連結→影響與觀察點；刊出標籤如【轉述】【程序中】；「沒有共同主線」可以是結論）。
- AI：`閒聊/分析規則/ＡＩ分析框架/AI新聞分析框架-修訂版.md`（六張題型卡各答三問；先判斷核心是不是 AI 新聞；Anthropic 當事方加關係註記）。
- 以檔案當下內容為準，不要憑記憶套用。

## 3. 依框架分析（市場、國際、AI 各一份）
- 必須另開一個 subagent 做「先各自獨立，再交流」：主分析者與 agent 各自寫候選解釋、證據缺口、判別條件，寫完才交換結論、雙向挑戰，並記下最強反對意見與它的去向。雙方一致不算多一份證據。
- 底稿存 `/mnt/project-files/briefings/YYYY-MM-DD-{market|intl|ai}-discussion/`（main-round1、agent-round1/2 等）。
- 校正晨間簡報的錯誤說法（日期、程序階段、來源性質）。
- 更新三份簡報共用的追蹤表與到期日。

## 4. 做成簡報
- 模板：10/20 市場簡報樣式；產生器沿用 `/mnt/project-files/briefings/2026-11-16-news-deck/`（build.py＋style.css，Playwright 印 1440x810 PDF）；國際用 `2026-11-16-intl-deck/`，AI 用 `2026-11-16-ai-deck/`。
- 每頁閱讀負擔輕、一眼可掃；寧可多頁不要塞字；不需要問題目錄頁。
- 必須涵蓋所有討論項目，包括用戶的每個追問與名詞解釋，不可只摘要。
- 美台股並談要標日期與市場，依時序（前一晚美股→當天台股）。
- PDF 存 `/mnt/project-files/briefings/YYYY-MM-DD-{市場|國際新聞|AI新聞}討論.pdf`，附給用戶看。

## 5. 定稿與歸檔
- 用戶回「可以」= 定稿，不用再問：把 PDF 存到 `閒聊/每日簡報/MMDD/{市場|國際局勢|AI}/`。
- 若有要求，同步到 Heptabase 白板「每日新聞/新知」→ 該日期子白板（MMDD）的對應區，以 PDF 卡加入。
- 更新專案記憶：當日主題、結論、追蹤到期日。

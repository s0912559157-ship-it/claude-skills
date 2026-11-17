# claude-skills

個人的 Claude Skills 收藏。每個 Skill 是一個自給自足的資料夾：`skills/<名稱>/`，裡面有 `SKILL.md`，以及它需要的 `references/`（規則、範本）和 `scripts/`（程式）。不依賴任何一台電腦上的檔案。

| Skill | 用途 |
|---|---|
| [daily-briefing-analysis](skills/daily-briefing-analysis/SKILL.md) | 產生今日晨間簡報，依市場／國際局勢／AI 三份分析框架（搭配獨立 subagent 雙向挑戰）分析新聞，先和使用者討論再做成 PDF 簡報；每天自評打分、寫修改案，三天一輪經使用者同意後改進 Skill。 |

## 安裝到新設備

1. 下載這個 repo：`git clone https://github.com/s0912559157-ship-it/claude-skills.git`（或在 GitHub 上 Code → Download ZIP）。
2. 把 Skill 資料夾放到 Claude 讀得到的地方，擇一：
   - **Claude Code**：複製到 `~/.claude/skills/daily-briefing-analysis/`（所有專案可用），或專案內的 `.claude/skills/`。
   - **Codex**：複製到 `~/.agents/skills/daily-briefing-analysis/`。
   - **Claude.ai／Claude 桌面版**：把 `skills/daily-briefing-analysis/` 壓成 zip，到「設定 → 功能 → Skills」上傳。
3. 要產生 PDF 的話，裝 Python 3 與 Playwright：
   ```
   pip install -r skills/daily-briefing-analysis/scripts/requirements.txt
   python -m playwright install chromium
   ```
   試跑：`python skills/daily-briefing-analysis/scripts/example_deck.py`，會在 `skills/daily-briefing-analysis/out/` 產生範例 PDF。
4. 使用：在一個專門給這個 Skill 用的資料夾裡對 Claude 說「讀取今日簡報」。第一次會請你開（或指定）這個資料夾；之後裡面只會有晨間簡報、三份簡報 PDF、追蹤表、評分紀錄、修改案、來源登記表，其他過程檔都放系統暫存區，用完刪掉。

## 更新分析規則

規則以這個 repo 的 `references/` 為準。改了規則就更新這裡的檔案再推上來，各設備重新下載即可。

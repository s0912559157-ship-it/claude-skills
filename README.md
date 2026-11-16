# claude-skills

個人的 Claude Skills 收藏。每個 Skill 是一個自給自足的資料夾：`skills/<名稱>/`，裡面有 `SKILL.md`，以及它需要的 `references/`（規則、範本）和 `scripts/`（程式）。不依賴任何一台電腦上的檔案。

| Skill | 用途 |
|---|---|
| [daily-briefing-analysis](skills/daily-briefing-analysis/SKILL.md) | 產生或讀取今日簡報：摘要晨間簡報，依市場／國際局勢／AI 三份分析框架（搭配獨立 subagent 雙向挑戰）分析新聞，做成 PDF 簡報。 |

## 安裝到新設備

1. 下載這個 repo：`git clone https://github.com/s0912559157-ship-it/claude-skills.git`（或在 GitHub 上 Code → Download ZIP）。
2. 把 Skill 資料夾放到 Claude 讀得到的地方，擇一：
   - **Claude Code**：複製到 `~/.claude/skills/daily-briefing-analysis/`（所有專案可用），或專案內的 `.claude/skills/`。
   - **Claude.ai／Claude 桌面版**：把 `skills/daily-briefing-analysis/` 壓成 zip，到「設定 → 功能 → Skills」上傳。
3. 要產生 PDF 的話，裝 Python 3 與 Playwright：
   ```
   pip install -r skills/daily-briefing-analysis/scripts/requirements.txt
   python -m playwright install chromium
   ```
   試跑：`python skills/daily-briefing-analysis/scripts/example_deck.py`，會在 `skills/daily-briefing-analysis/out/` 產生範例 PDF。
4. 使用：對 Claude 說「讀取今日簡報」，並附上當天的晨間簡報檔案或連結。

## 更新分析規則

規則以這個 repo 的 `references/` 為準。改了規則就更新這裡的檔案再推上來，各設備重新下載即可。

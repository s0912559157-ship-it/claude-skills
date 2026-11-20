"""範例：示範每種元件。複製這個檔案改內容即可。
執行：python scripts/example_deck.py  → 產生 out/example.html 與 out/example.pdf
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deck import *

cover('2026 / 11 / 16（一）市場新聞討論', '範例標題，<br>一句話講結論', '今日簡報的市場新聞，依五步分析框架整理',
      '資料來源：今日簡報、…。資訊截至 11/16 約 11:20（台北），非投資建議。')
slide('你問｜「依據規則，討論今日簡報的市場新聞」', '三句話看懂今天',
      row(card('重點一', '說明。'), card('重點二', '說明。'), card('重點三', '說明。', hl=True)) +
      note('<b>補充</b>：一行補充說明。'), '依〈市場分析框架〉', ask=True)
slide('步驟 1｜關鍵數字', '數字頁', stats([('43,512', '開盤'), ('41,809', '盤中最低'), ('−4.27%', '跌幅', 'o')]) +
      row(card('A', '…'), card('B', '…')), '來源：…')
slide('步驟 3｜檢查結果', '表格頁', table(['解釋', '觀察', '結果'], [['A', '…', '削弱'], ['C', '…', '支持（輕度）']]), '分析整理')
slide('步驟 5｜接下來看什麼', '流程頁', flow(['<b>今天收盤後</b><br>…', '<b>11/18</b><br>…', '<b>11/19</b><br>…']), '分析整理')
end('結論', '一句話結論', '結論段落。')
render(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out', 'example'))

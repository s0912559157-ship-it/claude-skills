"""每日簡報 PDF 產生器（10/20 市場簡報樣式）。

用法（在自己的腳本裡）：
    import sys; sys.path.insert(0, "<skill>/scripts")
    from deck import *
    cover("2026 / 11 / 16（一）市場新聞討論", "標題第一行<br>第二行", "副標", "資料來源…")
    slide("你問｜…", "三句話看懂今天", row(card("A","…"), card("B","…", hl=True)) + note("…"), "來源…", ask=True)
    end("結論", "一句話結論", "結論段落")
    render("out/2026-11-16-市場新聞討論")   # 產生 .html 與 .pdf

版面原則：每頁一眼可掃；寧可多頁不要塞字。
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
S = []
FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@700'
         '&family=Noto+Sans+TC:wght@400;500;700&display=swap" rel="stylesheet">')

def foot(src): return f'<div class="foot"><span>{src}</span><span>{{PN}}</span></div>'

def slide(kicker, title, body, src, ask=False):
    """一般內容頁。ask=True 表示這頁回答用戶的提問（kicker 會變橘色）。"""
    S.append(f'<section class="slide"><div class="kick{" ask" if ask else ""}">{kicker}</div>'
             f'<h1>{title}</h1>{body}{foot(src)}</section>')

def cover(kicker, title, sub, src):
    S.append(f'<section class="slide cover"><div class="kick">{kicker}</div><h1>{title}</h1>'
             f'<p class="sub">{sub}</p><div class="foot"><span>{src}</span></div></section>')

def end(kicker, title, text, src='整理新聞與分析推論，非投資建議'):
    S.append(f'<section class="slide end"><div class="kick">{kicker}</div><h1>{title}</h1>'
             f'<p>{text}</p>{foot(src)}</section>')

def card(t, p, hl=False): return f'<div class="card{" hl" if hl else ""}"><h3>{t}</h3><p>{p}</p></div>'
def row(*cs): return f'<div class="cards c{len(cs)}">' + ''.join(cs) + '</div>'
def stats(ss):
    """ss = [(數字, 說明), (數字, 說明, 'o')]；第三個元素存在時數字為橘色。"""
    return '<div class="stats">' + ''.join(
        f'<div class="stat{" o" if len(x) > 2 else ""}"><div class="n">{x[0]}</div><div class="l">{x[1]}</div></div>'
        for x in ss) + '</div>'
def table(h, rows):
    return ('<table><tr>' + ''.join(f'<th>{x}</th>' for x in h) + '</tr>' +
            ''.join('<tr>' + ''.join(f'<td>{x}</td>' for x in r) + '</tr>' for r in rows) + '</table>')
def note(t): return f'<p class="note">{t}</p>'
def lead(t): return f'<p class="lead">{t}</p>'
def flow(steps): return '<div class="flow">' + '<div class="arr">→</div>'.join(f'<div class="step">{s}</div>' for s in steps) + '</div>'

def html():
    css = open(os.path.join(HERE, 'style.css'), encoding='utf-8').read()
    out = f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>{css}</style></head><body>'
    for i, s in enumerate(S, 1):
        out += s.replace('{PN}', f'{i:02d}')
    return out + '</body></html>'

def render(path_without_ext, pdf=True):
    """寫出 <path>.html，並用 Playwright（Chromium）印成 1440x810 的 <path>.pdf。"""
    os.makedirs(os.path.dirname(os.path.abspath(path_without_ext)) or '.', exist_ok=True)
    h = path_without_ext + '.html'
    open(h, 'w', encoding='utf-8').write(html())
    print(f'{len(S)} 頁 → {h}')
    if not pdf:
        return h
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit('缺少 Playwright：pip install playwright && python -m playwright install chromium')
    p_out = path_without_ext + '.pdf'
    with sync_playwright() as p:
        exe = os.environ.get('DECK_CHROMIUM')  # 已有 Chromium 時可指定路徑
        b = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
        pg = b.new_page(viewport={'width': 1440, 'height': 810})
        pg.goto('file://' + os.path.abspath(h), wait_until='networkidle')
        pg.wait_for_timeout(800)  # 等字型
        pg.pdf(path=p_out, width='1440px', height='810px', print_background=True,
               margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'})
        b.close()
    print(f'PDF → {p_out}')
    return p_out

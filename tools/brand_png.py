import asyncio, math, pathlib
from playwright.async_api import async_playwright

OUT = pathlib.Path('/home/claude/konfeta/brand')
OUT.mkdir(parents=True, exist_ok=True)
F = '/tmp/fonts'
CHOC, CREAM, PINK, MUTE = '#260307', '#F6EDE6', '#FF9CC2', '#A88784'

def spiral():
    th1 = math.pi * 2 * 2.55
    pts = []
    for i in range(141):
        th = th1 * i / 140
        r = 2 + 28 * (th / th1)
        ph = math.pi / 2 + math.pi * 0.08 - (th1 - th)
        pts.append(f'{50 + r * math.cos(ph):.2f} {45 + r * math.sin(ph):.2f}')
    return 'M' + ' L'.join(pts)

SP = spiral()

def mark(ring, swirl, stem=None, w=6):
    stem = stem or ring
    return (f'<svg viewBox="-4 -4 108 134" xmlns="http://www.w3.org/2000/svg" style="display:block;height:100%;width:auto;overflow:visible">'
            f'<circle cx="50" cy="45" r="38" fill="none" stroke="{ring}" stroke-width="{w}"/>'
            f'<path d="{SP}" fill="none" stroke="{swirl}" stroke-width="{w-1}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M50 84 V126" fill="none" stroke="{stem}" stroke-width="{w}" stroke-linecap="round"/></svg>')

HEAD = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Comfortaa;src:url(file://{F}/fontsource-variable-comfortaa-5.3.0/package/files/comfortaa-latin-wght-normal.woff2) format("woff2");font-weight:300 700;unicode-range:U+0000-00FF,U+2000-206F}}
@font-face{{font-family:Comfortaa;src:url(file://{F}/fontsource-variable-comfortaa-5.3.0/package/files/comfortaa-cyrillic-wght-normal.woff2) format("woff2");font-weight:300 700;unicode-range:U+0400-04FF}}
@font-face{{font-family:Nunito;src:url(file://{F}/fontsource-variable-nunito-5.3.0/package/files/nunito-latin-wght-normal.woff2) format("woff2");font-weight:200 1000;unicode-range:U+0000-00FF,U+2000-206F}}
@font-face{{font-family:Nunito;src:url(file://{F}/fontsource-variable-nunito-5.3.0/package/files/nunito-cyrillic-wght-normal.woff2) format("woff2");font-weight:200 1000;unicode-range:U+0400-04FF}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:transparent}}
.d{{font-family:Comfortaa,sans-serif}} .n{{font-family:Nunito,sans-serif}}
</style></head><body>'''
GRAIN = ('<svg style="position:absolute;inset:0;width:100%;height:100%;opacity:.22;mix-blend-mode:soft-light;pointer-events:none">'
         '<filter id="g"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter>'
         '<rect width="100%" height="100%" filter="url(#g)"/></svg>')

def lockup(color, fs, mark_h, gap, ring=None, swirl=None):
    ring = ring or color; swirl = swirl or color
    return (f'<div style="display:flex;align-items:center;gap:{gap}px">'
            f'<div class="d" style="color:{color};font-size:{fs}px;font-weight:400;line-height:1.08;letter-spacing:-.01em">konfeta<br>running<br>club</div>'
            f'<div style="height:{mark_h}px">{mark(ring, swirl)}</div></div>')

V = {}
# 1. Telegram post 1280x720
V['tg-post-1280x720'] = (1280, 720, False, f'''<div style="position:relative;width:1280px;height:720px;background:{CHOC};overflow:hidden;display:flex;align-items:center;justify-content:center">{GRAIN}
<div style="position:relative;display:flex;flex-direction:column;align-items:flex-start;gap:44px">
{lockup(CREAM, 116, 470, 90, CREAM, PINK)}
<div class="n" style="display:flex;gap:18px;font-size:26px;font-weight:700;color:{MUTE};letter-spacing:.02em"><span>женский беговой клуб</span><span style="color:{PINK}">·</span><span>Москва</span></div>
</div></div>''')
# 2. Instagram 4:5 1080x1350
V['instagram-post-1080x1350'] = (1080, 1350, False, f'''<div style="position:relative;width:1080px;height:1350px;background:{CHOC};overflow:hidden;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:64px">{GRAIN}
<div style="position:relative;height:600px">{mark(CREAM, PINK)}</div>
<div style="position:relative;display:flex;flex-direction:column;align-items:center;gap:22px;text-align:center">
<div class="d" style="color:{CREAM};font-size:92px;font-weight:700;line-height:1;letter-spacing:-.03em">konfeta</div>
<div class="d" style="color:{CREAM};font-size:44px;font-weight:400;line-height:1;opacity:.85">running club</div>
<div class="n" style="margin-top:22px;font-size:30px;font-weight:700;color:{PINK}">Бегаем медленно. Болтаем много.</div>
</div></div>''')
# 3. Instagram square 1080x1080 (original lockup)
V['instagram-square-1080x1080'] = (1080, 1080, False, f'''<div style="position:relative;width:1080px;height:1080px;background:{CHOC};overflow:hidden;display:flex;align-items:center;justify-content:center">{GRAIN}
<div style="position:relative">{lockup(CREAM, 112, 470, 80, CREAM, PINK)}</div></div>''')
# 4. Avatar / app icon 1024 (safe for circle crop)
V['avatar-1024'] = (1024, 1024, False, f'''<div style="position:relative;width:1024px;height:1024px;background:{CHOC};overflow:hidden;display:flex;align-items:center;justify-content:center">{GRAIN}
<div style="position:relative;height:620px;transform:translateY(24px)">{mark(CREAM, PINK, w=6.5)}</div></div>''')
# 5-6. Desktop logo, transparent, @2x (1600 wide)
for name, col, sw in [('logo-desktop-cream', CREAM, CREAM), ('logo-desktop-chocolate', CHOC, CHOC), ('logo-desktop-color', CREAM, PINK)]:
    V[name] = (800, 260, True, f'<div style="width:800px;height:260px;display:flex;align-items:center;justify-content:center">{lockup(col, 62, 232, 44, col, sw)}</div>')
# 7-8. Mobile logo, transparent, @3x: mark + one-line wordmark
for name, col, sw in [('logo-mobile-cream', CREAM, CREAM), ('logo-mobile-chocolate', CHOC, CHOC), ('logo-mobile-color', CREAM, PINK)]:
    V[name] = (300, 96, True, f'''<div style="width:300px;height:96px;display:flex;align-items:center;justify-content:center;gap:14px">
<div style="height:72px">{mark(col, sw, w=7)}</div>
<div style="display:flex;flex-direction:column;gap:4px"><span class="d" style="color:{col};font-size:30px;font-weight:700;line-height:1;letter-spacing:-.02em">konfeta</span><span class="d" style="color:{col};font-size:16px;font-weight:400;line-height:1;opacity:.85">running club</span></div></div>''')
# 9. Mark only, transparent, 512
for name, col, sw in [('mark-cream-512', CREAM, CREAM), ('mark-chocolate-512', CHOC, CHOC)]:
    V[name] = (512, 512, True, f'<div style="width:512px;height:512px;display:flex;align-items:center;justify-content:center"><div style="height:440px">{mark(col, sw, w=7)}</div></div>')

SCALE = {'logo-desktop': 2, 'logo-mobile': 3}

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--allow-file-access-from-files'])
        for name, (w, h, transparent, body) in V.items():
            sc = next((v for k, v in SCALE.items() if name.startswith(k)), 1)
            pg = await b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=sc)
            f = pathlib.Path(f'/tmp/logo_{name}.html'); f.write_text(HEAD + body + '</body></html>', encoding='utf-8')
            await pg.goto('file://' + str(f))
            await pg.evaluate('document.fonts.ready')
            await pg.wait_for_timeout(200)
            ok = await pg.evaluate("document.fonts.check('700 40px Comfortaa')")
            await pg.screenshot(path=str(OUT / f'{name}.png'), omit_background=transparent)
            print(name, f'{w*sc}x{h*sc}', 'font ok' if ok else 'FONT MISSING')
            await pg.close()
        await b.close()

asyncio.run(main())

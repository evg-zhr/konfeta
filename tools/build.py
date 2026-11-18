#!/usr/bin/env python3
"""Build index.html for GitHub Pages from the design canvas file design/Main.dc.html.

Usage:  python3 tools/build.py
The .dc.html template is embedded as-is in a <template>; tools/runtime.js renders it in the
browser (holes, sc-for, sc-if, handlers) and morphdom applies state updates.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "design" / "Main.dc.html"
OUT = ROOT / "index.html"

TITLE = "konfeta running club — женский беговой клуб в Москве"
DESC = ("Женский беговой клуб в Москве. Бегаем медленно, болтаем и поддерживаем друг друга "
        "на Шелепихинской набережной. Пробежки бесплатные.")


def main() -> None:
    src = SRC.read_text(encoding="utf-8")

    xdc = re.search(r"<x-dc>(.*)</x-dc>", src, re.S).group(1)
    helmet = re.search(r"<helmet>(.*?)</helmet>", xdc, re.S).group(1).strip()
    body_tpl = re.sub(r"<helmet>.*?</helmet>", "", xdc, count=1, flags=re.S).strip()
    # Attributes holding {{holes}} get a dc-a- prefix so the browser does not try to parse
    # "{{...}}" as an SVG length or path while the template sits inert; runtime.js restores them.
    body_tpl = re.sub(r'(\s)(?!on)([a-zA-Z][\w:-]*)="([^"]*\{\{[^"]*)"', r'\1dc-a-\2="\3"', body_tpl)

    m = re.search(r"<script type=\"text/x-dc\" data-dc-script data-props='(.*?)'>(.*?)</script>", src, re.S)
    props_json = html.unescape(m.group(1))
    code = m.group(2).strip()
    props = {k: v.get("default") for k, v in json.loads(props_json).items() if not k.startswith("$")}

    runtime = (ROOT / "tools" / "runtime.js").read_text(encoding="utf-8")
    morph = (ROOT / "tools" / "vendor" / "morphdom-umd.min.js").read_text(encoding="utf-8")

    page = f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<meta name="theme-color" content="#260307">
<meta property="og:type" content="website">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{helmet}
</head>
<body>
<div id="app"></div>
<template id="dc-template">
{body_tpl}
</template>
<noscript><p style="padding:24px;color:#F6EDE6;font-family:sans-serif">konfeta running club — женский беговой клуб в Москве. Включите JavaScript, чтобы увидеть сайт.</p></noscript>
<script>/* morphdom 2.7.8 — MIT License, (c) Patrick Steele-Idem */
{morph}</script>
<script>
{runtime}</script>
<script>
{code}
dcMount(Component, {json.dumps(props, ensure_ascii=False)});
</script>
</body>
</html>
"""
    OUT.write_text(page, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(page.encode('utf-8')) // 1024} KB)")


if __name__ == "__main__":
    main()

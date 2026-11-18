# konfeta running club

Лендинг женского бегового клуба konfeta running club (Москва, Шелепихинская набережная).

## Структура

- `index.html` — готовая страница для GitHub Pages (собирается, руками не править).
- `design/` — исходники с дизайн-холста: `Main.dc.html` (лендинг), `Mobile`, `Moodboard`, `UIKit`, две концепции hero, `canvas.json`.
- `tools/build.py` — собирает `index.html` из `design/Main.dc.html`.
- `tools/runtime.js` — маленький рантайм шаблонов (`{{...}}`, `sc-for`, `sc-if`, обработчики), обновления через [morphdom](https://github.com/patrick-steele-idem/morphdom) (MIT, `tools/vendor/`).

## Обновить сайт

```bash
# заменить design/Main.dc.html новой версией с холста, затем:
python3 tools/build.py
git add -A && git commit -m "Обновить лендинг" && git push
```

## Что ещё заполнить

В тексте остались плейсхолдеры в квадратных скобках: дни и время сбора, ориентир на набережной,
ссылки на Telegram и соцсети, имена и фото участниц, длина маршрута.

## Логотип и PNG для соцсетей

Готовые файлы — в `brand/`: пост для Telegram (1280×720), пост Instagram (1080×1350 и 1080×1080),
аватар 1024, логотипы для desktop (@2x) и mobile (@3x) на прозрачном фоне в трёх цветах, знак 512.
Пересобрать: `python3 tools/brand_png.py` (нужны Playwright и шрифты `@fontsource-variable/comfortaa`
и `@fontsource-variable/nunito`, распакованные в `/tmp/fonts`).

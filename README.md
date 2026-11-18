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

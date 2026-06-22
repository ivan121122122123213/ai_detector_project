# AI Detector / Intelligence Dashboard

Локальный MVP-сервис для безопасного анализа архивов, бэкапов и логов. Он помогает владельцу данных быстро понять, что лежит в архиве, какие файлы потенциально чувствительные и где есть риск случайной утечки секретов.

## Что делает

- Загружает архивы `.zip`, `.tar`, `.tar.gz`, `.tgz`.
- Индексирует дерево файлов.
- Классифицирует файлы: configs, databases, logs, source code, backups, spreadsheets, browser-like data.
- Ищет сущности: emails, domains, IP, Telegram mentions, Discord mentions, wallets, API-like keys, JWT-like strings, SSH private key markers, environment variables.
- Маскирует найденные значения, чтобы не светить секреты в отчёте.
- Считает Risk Score.
- Строит AI-like Summary без внешнего API.
- Показывает Entity Graph в интерфейсе.
- Позволяет искать по результатам анализа.
- Экспортирует отчёты в JSON и HTML.

## Что НЕ делает

- Не ворует данные.
- Не отправляет архивы наружу.
- Не показывает пароли полностью.
- Не пытается логиниться в сервисы.
- Не проверяет валидность аккаунтов, токенов или кошельков.
- Не предназначен для чужих данных без разрешения.

## Быстрый запуск

```bash
cd ai_detector_project
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Открыть:

```text
http://127.0.0.1:8000
```

## Тестовый архив

Можно создать тестовый архив:

```bash
python create_sample_archive.py
```

Появится файл:

```text
sample_sensitive_project.zip
```

Загрузи его в интерфейсе.

## Структура

```text
ai_detector_project/
├─ app/
│  ├─ main.py
│  ├─ core/
│  │  ├─ archive.py
│  │  ├─ classifier.py
│  │  ├─ database.py
│  │  ├─ graph.py
│  │  ├─ models.py
│  │  ├─ patterns.py
│  │  ├─ report.py
│  │  ├─ risk.py
│  │  ├─ scanner.py
│  │  └─ summary.py
│  ├─ static/
│  │  ├─ app.js
│  │  └─ styles.css
│  ├─ templates/
│  │  └─ index.html
│  ├─ uploads/
│  └─ reports/
├─ create_sample_archive.py
├─ requirements.txt
├─ Dockerfile
├─ docker-compose.yml
└─ README.md
```

# 🖥️ Server Control Panel — Пульт управления проектами (VPS)

Локальное графическое приложение на **Python + Tkinter** для быстрого управления сервером `skewer-public-api` и четырьмя проектами без постоянного переключения окон в VS Code. Тратит **0 МБ** оперативной памяти на VPS, так как работает на ноутбуке и выполняет все команды через SSH-туннель.

---

## 🏗️ Структура проекта

Проект разбит на компактные логические модули и командные скрипты в папке `scripts/`:

```text
~/Projects/ServerPanel/
├── scripts/
│   ├── install_deps.sh      # Установка системного пакета python3-tk
│   ├── setup_env.sh         # Создание .env из шаблона .env.example с правами 600
│   ├── run.sh               # Проверка окружения и запуск панели управления
│   └── install_desktop.sh   # Установка ярлыка в меню приложений и на рабочий стол
├── main.py                  # Точка входа, главное окно, стили и поле вывода
├── config.py                # Загрузка .env, пути к проектам и конфиг ботов
├── sql_queries.py           # Шаблоны SQL-запросов для аналитики и чтения диалогов
├── executor.py              # Асинхронный запуск SSH, локальных скриптов и psql в потоках
├── tab_server.py            # Вкладка «Сервер & SBrowserV2»
├── tab_bot.py               # Универсальный конструктор вкладок для всех ботов
├── prompt_editor.py         # Редактор промптов и базы знаний с автодеплоем
├── .env.example             # Шаблон переменных окружения для Git
├── .env                     # Локальные секреты (IP, SSH-пользователь, токены — в .gitignore)
├── .gitignore               # Исключения Git
└── README.md                # Документация проекта
```

---

## ⚙️ Установка и настройка с нуля

1. **Перейди в папку проекта и сделай скрипты исполняемыми:**
   ```bash
   cd ~/Projects/ServerPanel
   chmod +x scripts/*.sh
   ```

2. **Установи системный пакет `python3-tk` (потребуется пароль `sudo`):**
   ```bash
   ./scripts/install_deps.sh
   ```

3. **Создай файл `.env` из шаблона и заполни секреты:**
   ```bash
   ./scripts/setup_env.sh
   ```
   Открой `~/Projects/ServerPanel/.env` и впиши реальные данные:
   ```env
   SERVER_IP=твой_ip_сервера
   SSH_USER=root
   SBROWSER_ADMIN_TOKEN=твой_токен_админа_поисковика
   ```

4. **Проверь беспарольный доступ по SSH** к серверу (должен быть настроен SSH-ключ в `~/.ssh/`) и наличие локальных папок проектов, указанных в `config.py`.

---

## 🚀 Запуск и установка ярлыка

* **Запустить вручную из терминала** (скрипт сам проверит наличие `tkinter` и `.env` перед стартом):
  ```bash
  ~/Projects/ServerPanel/scripts/run.sh
  ```
* **Установить ярлык в меню приложений и на рабочий стол** (выполняется один раз):
  ```bash
  ~/Projects/ServerPanel/scripts/install_desktop.sh
  ```

---

## 🎛️ Возможности по вкладкам

### 1. Вкладка «🖥 Сервер & SBrowserV2»
* **Мониторинг VPS:** проверка RAM и CPU всех контейнеров (`docker stats`), свободного места на диске (`df -h`), безопасная очистка кэша образов и сборки Docker, чтение последних строк логов Nginx.
* **Управление SBrowserV2:** получение живой статистики и Топ-5 поисковых запросов из Manticore (`/api/admin/stats`), запуск `./deploy.sh`, просмотр логов `sbrowser_fastapi` и рестарт бэкенда.

### 2. Вкладки ботов («⚖️ Быстрый Юрист», «⚓ Морской бот», «👔 Менеджер-бот»)
* **Деплой, промпты и логи:** предварительная проверка изменений (`--check`), боевой деплой с пересборкой Docker, встроенный **редактор промптов и базы знаний** (`.md`/`.txt`) с кнопкой «Сохранить и задеплоить», просмотр логов, фильтрация ошибок, проверка таблиц **Manticore** (для Менеджер-бота) и бэкап PostgreSQL (для Юриста).
* **Аналитика PostgreSQL:** общая сводка (всего пользователей / активные чаты / оплаты), конверсия по веткам, воронка событий из `audit_logs`, поиск «слепых зон» (4+ хода без оплаты) и список 15 последних активных пользователей.
* **Чтение диалогов и 152-ФЗ:** просмотр только вопросов клиента или всей переписки целиком по `user_id`, а также проверка тегов обезличивания персональных данных.

---

## ➕ Как добавить нового бота

Открой файл `config.py` и добавь новый словарь в список `BOTS_CONFIG` по образцу:

```python
{
    "tab_name": "🆕 Новый бот",
    "local_dir": os.path.expanduser("~/Projects/NewBot"),
    "server_dir": "~/NewBot",
    "deploy_cmd": "./deploy.sh",
    "check_cmd": "./deploy.sh --check",
    "bot_container": "new_bot_container",
    "db_container": "new_postgres_container",
    "manticore_container": None,
    "has_backup_script": False,
}
```
При следующем запуске приложения новая вкладка со всеми кнопками аналитики и деплоя появится автоматически.

## 📄 Лицензия со строкой: Проект распространяется под лицензией MIT. Подробнее см. в файле LICENSE. Автор: Мазо Андрей Александрович.
---

## License Summary & Terms

This software is licensed under the **PolyForm Noncommercial License 1.0.0**.  
Full canonical license text: <https://polyformproject.org/licenses/noncommercial/1.0.0>

* **Permitted Use:** You may use, copy, modify, and distribute this software strictly for **noncommercial purposes** (personal use, education, research, or nonprofit organizations).
* **Commercial Restriction:** Any commercial use, sale, or integration into commercial products and services is prohibited without prior written permission from the licensor.
* **Attribution:** All copies and derivative works must retain this Required Notice and a link to the license terms.
* **No Warranty:** The software is provided "as is", without warranty or liability of any kind.

### Краткое пояснение на русском языке

Программное обеспечение распространяется по лицензии **PolyForm Noncommercial License 1.0.0** (юридическую силу имеет официальный текст на английском языке по ссылке выше).

* **Разрешено:** бесплатно скачивать, изучать, изменять и распространять код в личных, учебных или некоммерческих целях.
* **Запрещено:** использовать код в коммерческих продуктах, продавать его или внедрять в бизнес-процессы без письменного разрешения автора.
* **Обязательное условие:** при копировании или форке необходимо сохранять указание авторства (**Мазо Андрей Александрович**) и ссылку на текст лицензии.

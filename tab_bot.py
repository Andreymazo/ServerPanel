from tkinter import ttk
from config import SSH_TARGET
from executor import CommandExecutor
from prompt_editor import PromptEditorWindow
import sql_queries as sql


def build_bot_tab(notebook: ttk.Notebook, bot: dict, executor: CommandExecutor):
    tab = ttk.Frame(notebook, padding=10)
    notebook.add(tab, text=bot["tab_name"])

    db = bot["db_container"]
    container = bot["bot_container"]
    local_dir = bot["local_dir"]

    # Блок 1: Деплой, промпты и логи
    ops_frame = ttk.LabelFrame(tab, text="Деплой, промпты и обслуживание", padding=8)
    ops_frame.pack(fill="x", pady=(0, 8))

    ttk.Button(
        ops_frame,
        text="🔍 Проверить (--check)",
        command=lambda: executor.run_local(bot["check_cmd"], local_dir, f"Проверка {bot['tab_name']}"),
    ).pack(side="left", padx=4)

    ttk.Button(
        ops_frame,
        text="🚀 Боевой деплой",
        style="Accent.TButton",
        command=lambda: executor.run_local(bot["deploy_cmd"], local_dir, f"Деплой {bot['tab_name']}"),
    ).pack(side="left", padx=4)

    ttk.Button(
        ops_frame,
        text="📝 Промпты / База",
        command=lambda: PromptEditorWindow(tab, bot, executor),
    ).pack(side="left", padx=4)

    ttk.Button(
        ops_frame,
        text="📜 Логи (50)",
        command=lambda: executor.run_ssh(f"docker logs {container} --tail 50", f"Логи {container}"),
    ).pack(side="left", padx=4)

    ttk.Button(
        ops_frame,
        text="⚠️ Ошибки",
        command=lambda: executor.run_ssh(
            f"docker logs {container} 2>&1 | grep -iE 'error|exception|traceback|ocr' | tail -n 30",
            f"Ошибки {container}",
        ),
    ).pack(side="left", padx=4)

    if bot.get("manticore_container"):
        mc = bot["manticore_container"]
        ttk.Button(
            ops_frame,
            text="🔎 Manticore статус",
            command=lambda: executor.run_ssh(
                f'docker exec {mc} mysql -P 9306 -e "SHOW TABLES; SHOW STATUS LIKE \'uptime\';"',
                f"Состояние {mc}",
            ),
        ).pack(side="left", padx=4)

    if bot["has_backup_script"]:
        ttk.Button(
            ops_frame,
            text="💾 Бэкап БД",
            command=lambda: executor.run_shell(
                f'ssh {SSH_TARGET} "cd {bot["server_dir"]} && ./scripts/backup_db.sh" && '
                f'scp {SSH_TARGET}:{bot["server_dir"]}/backups/*.sql.gz "{local_dir}/"',
                "Резервное копирование БД",
            ),
        ).pack(side="left", padx=4)

    # Блок 2: Аналитика PostgreSQL
    sql_frame = ttk.LabelFrame(tab, text="Аналитика воронки и конверсий (PostgreSQL)", padding=8)
    sql_frame.pack(fill="x", pady=(0, 8))

    buttons_sql = [
        ("📊 Общая сводка", sql.QUERY_SUMMARY, "Общая статистика"),
        ("🌿 По веткам", sql.QUERY_BRANCHES, "Конверсия по веткам"),
        ("🌪 Воронка событий", sql.QUERY_FUNNEL, "Воронка audit_logs"),
        ("🕳 Слепые зоны (4+ ходов)", sql.QUERY_BLIND_SPOTS, "Длинные диалоги без оплаты"),
        ("👥 15 активных", sql.QUERY_RECENT_USERS, "Последние 15 активных пользователей"),
    ]
    for btn_text, query, label in buttons_sql:
        ttk.Button(
            sql_frame,
            text=btn_text,
            command=lambda q=query, lbl=label: executor.run_psql(db, q, lbl),
        ).pack(side="left", padx=4)

    # Блок 3: Разбор диалога и 152-ФЗ
    chat_frame = ttk.LabelFrame(tab, text="Чтение диалогов и аудит 152-ФЗ", padding=8)
    chat_frame.pack(fill="x")

    ttk.Label(chat_frame, text="User ID:").pack(side="left", padx=4)
    uid_entry = ttk.Entry(chat_frame, width=16)
    uid_entry.pack(side="left", padx=(0, 8))

    def open_dialog(only_questions: bool):
        uid = uid_entry.get().strip()
        if not uid.isdigit():
            executor.on_output("⚠️ Введите числовой user_id из таблицы активных пользователей.\n")
            return
        query = sql.build_user_questions_query(uid) if only_questions else sql.build_full_dialog_query(uid)
        title = f"Вопросы пользователя {uid}" if only_questions else f"Полный диалог с {uid}"
        executor.run_psql(db, query, title)

    ttk.Button(chat_frame, text="💬 Только вопросы юзера", command=lambda: open_dialog(True)).pack(side="left", padx=4)
    ttk.Button(chat_frame, text="📖 Весь диалог целиком", command=lambda: open_dialog(False)).pack(side="left", padx=4)

    ttk.Button(
        chat_frame,
        text="🛡 Аудит тегов 152-ФЗ",
        command=lambda: executor.run_psql(db, sql.QUERY_AUDIT_152FZ, "Проверка анонимайзера 152-ФЗ"),
    ).pack(side="right", padx=4)

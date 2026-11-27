from tkinter import ttk
from config import SBROWSER_DIR, SBROWSER_ADMIN_TOKEN
from executor import CommandExecutor


def build_server_tab(notebook: ttk.Notebook, executor: CommandExecutor):
    tab = ttk.Frame(notebook, padding=10)
    notebook.add(tab, text="🖥 Сервер & SBrowserV2")

    vps_frame = ttk.LabelFrame(tab, text="Мониторинг и очистка VPS (2 ГБ RAM / 29 ГБ диск)", padding=8)
    vps_frame.pack(fill="x", pady=(0, 8))

    ttk.Button(
        vps_frame,
        text="📊 RAM и CPU контейнеров",
        command=lambda: executor.run_ssh("docker stats --no-stream", "Замер ресурсов Docker"),
    ).pack(side="left", padx=4)

    ttk.Button(
        vps_frame,
        text="💾 Место на диске и Docker",
        command=lambda: executor.run_ssh("df -h / && echo '---' && docker system df", "Проверка диска"),
    ).pack(side="left", padx=4)

    ttk.Button(
        vps_frame,
        text="🧹 Очистить кэш Docker (безопасно)",
        command=lambda: executor.run_ssh(
            "docker image prune -af && docker builder prune -af && df -h /",
            "Очистка кэша образов и сборки",
        ),
    ).pack(side="left", padx=4)

    ttk.Button(
        vps_frame,
        text="🌐 Nginx Access (25 строк)",
        command=lambda: executor.run_ssh("tail -n 25 /var/log/nginx/access.log", "Логи Nginx"),
    ).pack(side="left", padx=4)

    sb_frame = ttk.LabelFrame(tab, text="Поисковик SBrowserV2 (Manticore + FastAPI)", padding=8)
    sb_frame.pack(fill="x")

    ttk.Button(
        sb_frame,
        text="📈 Статистика и Топ-5 запросов",
        command=lambda: executor.run_ssh(
            f"curl -s -H 'X-Admin-Token: {SBROWSER_ADMIN_TOKEN}' http://localhost:8000/api/admin/stats | python3 -m json.tool",
            "Статистика SBrowserV2",
        ),
    ).pack(side="left", padx=4)

    ttk.Button(
        sb_frame,
        text="🚀 Деплой SBrowserV2",
        style="Accent.TButton",
        command=lambda: executor.run_local("./deploy.sh", SBROWSER_DIR, "Деплой SBrowserV2"),
    ).pack(side="left", padx=4)

    ttk.Button(
        sb_frame,
        text="📜 Логи sbrowser_fastapi (50)",
        command=lambda: executor.run_ssh("docker logs sbrowser_fastapi --tail 50", "Логи SBrowserV2"),
    ).pack(side="left", padx=4)

    ttk.Button(
        sb_frame,
        text="🔄 Рестарт fastapi_backend",
        command=lambda: executor.run_ssh(
            "cd ~/SBrowserV2 && docker compose restart fastapi_backend",
            "Перезапуск SBrowserV2",
        ),
    ).pack(side="left", padx=4)

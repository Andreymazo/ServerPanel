import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def _load_env(filepath: str):
    if not os.path.isfile(filepath):
        return
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))


_load_env(os.path.join(BASE_DIR, ".env"))

SERVER_IP = os.getenv("SERVER_IP", "127.0.0.1")
SSH_USER = os.getenv("SSH_USER", "root")
SSH_TARGET = f"{SSH_USER}@{SERVER_IP}"
SBROWSER_ADMIN_TOKEN = os.getenv("SBROWSER_ADMIN_TOKEN", "")
SBROWSER_DIR = os.path.expanduser("~/Projects/SBrowserV2")

BOTS_CONFIG = [
    {
        "tab_name": "⚖️ Быстрый Юрист",
        "local_dir": os.path.expanduser("~/Projects/Juridical_maxbot"),
        "server_dir": "~/Juridical_maxbot",
        "deploy_cmd": "./deploy.sh",
        "check_cmd": "./deploy.sh --check",
        "bot_container": "juridical_maxbot",
        "db_container": "juridical_postgres",
        "manticore_container": None,
        "has_backup_script": True,
    },
    {
        "tab_name": "⚓ Морской бот",
        "local_dir": os.path.expanduser("~/Projects/Maritime_maxbot"),
        "server_dir": "~/Maritime_maxbot",
        "deploy_cmd": "./deploy.sh",
        "check_cmd": "./deploy.sh --check",
        "bot_container": "maritime_maxbot",
        "db_container": "maritime_postgres",
        "manticore_container": None,
        "has_backup_script": False,
    },
    {
        "tab_name": "👔 Менеджер-бот",
        "local_dir": os.path.expanduser("~/Projects/ManagerMaxBot"),
        "server_dir": "~/ManagerMaxBot",
        "deploy_cmd": "./scripts/deploy.sh",
        "check_cmd": "./scripts/deploy.sh --check",
        "bot_container": "manager_bot",
        "db_container": "manager_postgres",
        "manticore_container": "manager_manticore",
        "has_backup_script": False,
    },
]

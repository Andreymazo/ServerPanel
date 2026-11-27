import os
import subprocess
import threading
import tkinter as tk
from config import SSH_TARGET


class CommandExecutor:
    def __init__(self, root: tk.Tk, on_start, on_output, on_finish):
        self.root = root
        self.on_start = on_start
        self.on_output = on_output
        self.on_finish = on_finish

    def run_ssh(self, remote_cmd: str, label: str):
        cmd = ["ssh", SSH_TARGET, remote_cmd]
        self._execute_async(cmd, None, label)

    def run_local(self, local_cmd: str, cwd: str, label: str):
        if not os.path.isdir(cwd):
            self.on_output(f"❌ Локальная папка не найдена: {cwd}\n")
            return
        self._execute_async(local_cmd, cwd, label, shell=True)

    def run_shell(self, shell_cmd: str, label: str):
        self._execute_async(shell_cmd, None, label, shell=True)

    def run_psql(self, db_container: str, sql: str, label: str):
        cmd = [
            "ssh",
            SSH_TARGET,
            f'docker exec -i {db_container} sh -c "psql -U \\$POSTGRES_USER -d \\$POSTGRES_DB"',
        ]
        self._execute_async(cmd, None, label, stdin_data=sql)

    def _execute_async(self, cmd, cwd, label: str, shell: bool = False, stdin_data: str = None):
        self.on_start(label)

        def worker():
            try:
                proc = subprocess.run(
                    cmd,
                    cwd=cwd,
                    shell=shell,
                    input=stdin_data,
                    text=True,
                    capture_output=True,
                    timeout=180,
                )
                result = proc.stdout or ""
                if proc.stderr:
                    result += f"\n[STDERR / INFO]\n{proc.stderr}"
                if not result.strip():
                    result = "(Пустой вывод / Успешно выполнено)\n"
                self.root.after(0, lambda: self.on_finish(result, f"✅ Готово: {label}"))
            except subprocess.TimeoutExpired:
                self.root.after(0, lambda: self.on_finish("⏱ Превышено время ожидания (180 сек).\n", "❌ Таймаут"))
            except Exception as exc:
                self.root.after(0, lambda: self.on_finish(f"❌ Ошибка запуска: {exc}\n", "❌ Ошибка"))

        threading.Thread(target=worker, daemon=True).start()

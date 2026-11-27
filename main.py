import tkinter as tk
from tkinter import ttk, scrolledtext
from executor import CommandExecutor
from tab_server import build_server_tab
from tab_bot import build_bot_tab
from config import BOTS_CONFIG, SERVER_IP


class ServerControlPanel:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(f"Панель управления проектами — skewer-public-api ({SERVER_IP})")
        self.root.geometry("1040x740")
        self.root.minsize(900, 620)

        self._setup_styles()
        self._build_ui()

        self.executor = CommandExecutor(
            root=self.root,
            on_start=self._on_task_start,
            on_output=self.append_output,
            on_finish=self._on_task_finish,
        )

        build_server_tab(self.notebook, self.executor)
        for bot in BOTS_CONFIG:
            build_bot_tab(self.notebook, bot, self.executor)

    def _setup_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TNotebook.Tab", padding=(10, 5), font=("Sans", 10, "bold"))
        style.configure("TButton", padding=(8, 4), font=("Sans", 9))
        style.configure("Accent.TButton", padding=(8, 4), font=("Sans", 9, "bold"))
        style.configure("TLabelframe.Label", font=("Sans", 9, "bold"))

    def _build_ui(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        top_bar = ttk.Frame(main_frame)
        top_bar.pack(fill=tk.X, pady=(0, 8))

        self.status_var = tk.StringVar(value="Готов к работе")
        ttk.Label(top_bar, textvariable=self.status_var, font=("Sans", 9, "italic")).pack(side=tk.LEFT)

        ttk.Button(top_bar, text="Копировать вывод", command=self.copy_output).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(top_bar, text="Очистить окно", command=self.clear_output).pack(side=tk.RIGHT)

        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.X, pady=(0, 8))

        out_frame = ttk.LabelFrame(main_frame, text="Результат выполнения и аналитика", padding=6)
        out_frame.pack(fill=tk.BOTH, expand=True)

        self.output_text = scrolledtext.ScrolledText(
            out_frame,
            wrap=tk.WORD,
            font=("Monospace", 10),
            bg="#1e1e1e",
            fg="#e6e6e6",
            insertbackground="white",
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)

    def _on_task_start(self, label: str):
        self.status_var.set(f"⏳ Выполняется: {label}...")
        self.clear_output()
        self.append_output(f"=== {label} ===\n\n")

    def _on_task_finish(self, text: str, status: str):
        self.append_output(text)
        self.status_var.set(status)

    def append_output(self, text: str):
        self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)

    def clear_output(self):
        self.output_text.delete("1.0", tk.END)

    def copy_output(self):
        content = self.output_text.get("1.0", tk.END).strip()
        if content:
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            self.status_var.set("📋 Вывод скопирован в буфер обмена")


if __name__ == "__main__":
    root = tk.Tk()
    app = ServerControlPanel(root)
    root.mainloop()

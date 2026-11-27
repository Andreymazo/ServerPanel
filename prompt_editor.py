import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from executor import CommandExecutor


class PromptEditorWindow:
    def __init__(self, parent: tk.Widget, bot: dict, executor: CommandExecutor):
        self.bot = bot
        self.executor = executor
        self.local_dir = bot["local_dir"]
        self.files_map = self._scan_files()

        if not self.files_map:
            messagebox.showinfo("Файлы не найдены", f"В {self.local_dir} нет папок prompts/ или knowledge/ с .md/.txt файлами.")
            return

        self.win = tk.Toplevel(parent)
        self.win.title(f"Редактор промптов и базы знаний — {bot['tab_name']}")
        self.win.geometry("860x620")
        self._build_ui()

    def _scan_files(self) -> dict:
        found = {}
        for folder in ("prompts", "knowledge"):
            target = os.path.join(self.local_dir, folder)
            if not os.path.isdir(target):
                continue
            for root_dir, _, files in os.walk(target):
                for fname in sorted(files):
                    if fname.endswith((".md", ".txt")):
                        full_path = os.path.join(root_dir, fname)
                        rel_path = os.path.relpath(full_path, self.local_dir)
                        found[rel_path] = full_path
        return found

    def _build_ui(self):
        top = ttk.Frame(self.win, padding=8)
        top.pack(fill="x")

        ttk.Label(top, text="Файл:").pack(side="left", padx=(0, 6))
        self.file_var = tk.StringVar()
        combo = ttk.Combobox(top, textvariable=self.file_var, values=list(self.files_map.keys()), state="readonly", width=45)
        combo.pack(side="left", padx=(0, 8))
        combo.bind("<<ComboboxSelected>>", lambda _: self._load_file())

        ttk.Button(top, text="💾 Сохранить", command=self._save_file).pack(side="left", padx=4)
        ttk.Button(top, text="🚀 Сохранить и задеплоить", style="Accent.TButton", command=self._save_and_deploy).pack(side="left", padx=4)

        self.status_lbl = ttk.Label(top, text="", font=("Sans", 9, "italic"))
        self.status_lbl.pack(side="right")

        self.editor = scrolledtext.ScrolledText(
            self.win, wrap=tk.WORD, font=("Monospace", 10), bg="#1e1e1e", fg="#e6e6e6", insertbackground="white"
        )
        self.editor.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        combo.current(0)
        self._load_file()

    def _load_file(self):
        rel = self.file_var.get()
        path = self.files_map.get(rel)
        if not path:
            return
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        self.editor.delete("1.0", tk.END)
        self.editor.insert("1.0", content)
        self.status_lbl.config(text=f"Открыт: {rel}")

    def _save_file(self) -> bool:
        rel = self.file_var.get()
        path = self.files_map.get(rel)
        if not path:
            return False
        content = self.editor.get("1.0", "end-1c")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        self.status_lbl.config(text=f"✅ Сохранено: {rel}")
        return True

    def _save_and_deploy(self):
        if self._save_file():
            self.executor.run_local(self.bot["deploy_cmd"], self.local_dir, f"Деплой после правки {self.file_var.get()}")
            self.win.destroy()

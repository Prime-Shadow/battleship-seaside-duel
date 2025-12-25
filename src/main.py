import tkinter as tk
from tkinter import Toplevel, Label, Canvas
from gui.app import App


class StartWindow:
    def __init__(self, root):
        self.root = root
        # hide main root while start window shown
        self.root.withdraw()
        self.win = Toplevel(root)
        self.win.title("Start Battleship")
        self.win.resizable(False, False)
        # Canvas-driven UI (no widgets that behave like buttons)
        self.header_label = Label(self.win, text="Battleship — Seaside Duel", font=("Helvetica", 16, "bold"))
        self.header_label.pack(pady=(8,4))
        self.author_label = Label(self.win, text="Author: Mihai Sirbu", font=("Helvetica", 10))
        self.author_label.pack(pady=(0,6))
        self.license_label = Label(self.win, text="License: MIT License 2025", font=("Helvetica", 10))
        self.license_label.pack(pady=(0,6))

        self.canvas = Canvas(self.win, width=360, height=220, bg="#f5fbff", highlightthickness=0)
        self.canvas.pack(padx=8, pady=6)

        # interactive areas positions
        self.langs = ["English", "Spanish", "French", "German", "Romanian"]
        self.lang_index = 0
        self.diffs = ["Easy", "Medium", "Hard"]
        self.diff_index = 1

        # small translations map used by the start window so labels update live
        self._translations = {
            "English": {"language_label": "Language:", "ai_label": "AI Difficulty:", "author": "Author:", "license": "License:", "start": "Start", "exit": "Exit"},
            "Spanish": {"language_label": "Idioma:", "ai_label": "Dificultad IA:", "author": "Autor:", "license": "Licencia:", "start": "Iniciar", "exit": "Salir"},
            "French": {"language_label": "Langue:", "ai_label": "Difficulté IA:", "author": "Auteur:", "license": "Licence:", "start": "Démarrer", "exit": "Quitter"},
            "German": {"language_label": "Sprache:", "ai_label": "KI Schwierigkeit:", "author": "Autor:", "license": "Lizenz:", "start": "Start", "exit": "Beenden"},
            "Romanian": {"language_label": "Limbă:", "ai_label": "Dificultate AI:", "author": "Autor:", "license": "Licență:", "start": "Start", "exit": "Ieșire"},
        }

        # language box
        self.lang_box = (20, 20, 320, 60)
        self.canvas.create_rectangle(*self.lang_box, fill="#ffffff", outline="#a9d0ff")
        tr = self._translations[self.langs[self.lang_index]]
        self.lang_text = self.canvas.create_text(170, 40, text=f"{tr.get('language_label','Language:')} {self.langs[self.lang_index]}", font=("Helvetica", 12))

        # difficulty box
        self.diff_box = (20, 80, 320, 120)
        self.canvas.create_rectangle(*self.diff_box, fill="#ffffff", outline="#a9d0ff")
        self.diff_text = self.canvas.create_text(170, 100, text=f"{tr.get('ai_label','AI Difficulty:')} {self.diffs[self.diff_index]}", font=("Helvetica", 12))

        # start box (drawn like a button but handled via canvas events)
        self.start_box = (110, 140, 250, 180)
        self.canvas.create_rectangle(*self.start_box, fill="#9bb7a8", outline="#5a8f6a", width=2, tags="start_rect")
        self.start_text = self.canvas.create_text(180, 160, text=tr.get('start','Start'), font=("Helvetica", 12, "bold"), fill="white", tags="start_text")

        # exit box
        self.exit_box = (20, 140, 100, 180)
        self.canvas.create_rectangle(*self.exit_box, fill="#e86a6a", outline="#a94444", width=2, tags="exit_rect")
        self.exit_text = self.canvas.create_text(60, 160, text=tr.get('exit','Exit'), font=("Helvetica", 10, "bold"), fill="white", tags="exit_text")

        # click handling
        self.canvas.bind("<Button-1>", self._on_click)
        self.win.protocol("WM_DELETE_WINDOW", self.win.destroy)

    def start(self):
        # apply selections and launch main app
        diff = self.diffs[self.diff_index]
        lang = self.langs[self.lang_index]
        self.win.destroy()
        self.root.deiconify()
        App(self.root, difficulty=diff, language=lang)

    def _on_click(self, ev):
        x, y = ev.x, ev.y
        lx0, ly0, lx1, ly1 = self.lang_box
        dx0, dy0, dx1, dy1 = self.diff_box
        sx0, sy0, sx1, sy1 = self.start_box
        if lx0 <= x <= lx1 and ly0 <= y <= ly1:
            # cycle language
            self.lang_index = (self.lang_index + 1) % len(self.langs)
            tr = self._translations.get(self.langs[self.lang_index], self._translations['English'])
            self.canvas.itemconfigure(self.lang_text, text=f"{tr.get('language_label','Language:')} {self.langs[self.lang_index]}")
            # update other widgets (labels and buttons)
            try:
                self.header_label.config(text="Battleship — Seaside Duel")
                self.author_label.config(text=f"{tr.get('author','Author:')} Mihai Sirbu")
                self.license_label.config(text=f"{tr.get('license','License:')} MIT License 2025")
            except Exception:
                pass
            try:
                self.canvas.itemconfigure(self.diff_text, text=f"{tr.get('ai_label','AI Difficulty:')} {self.diffs[self.diff_index]}")
                self.canvas.itemconfigure(self.start_text, text=tr.get('start','Start'))
                self.canvas.itemconfigure(self.exit_text, text=tr.get('exit','Exit'))
            except Exception:
                pass
            try:
                self.canvas.update_idletasks()
                self.win.update()
            except Exception:
                pass
            return
        if dx0 <= x <= dx1 and dy0 <= y <= dy1:
            # cycle difficulty
            self.diff_index = (self.diff_index + 1) % len(self.diffs)
            self.canvas.itemconfigure(self.diff_text, text=f"AI Difficulty: {self.diffs[self.diff_index]}")
            return
        if sx0 <= x <= sx1 and sy0 <= y <= sy1:
            # start
            self.start()
            return
        # exit
        ex0, ey0, ex1, ey1 = self.exit_box
        if ex0 <= x <= ex1 and ey0 <= y <= ey1:
            self.root.quit()


def main():
    root = tk.Tk()
    root.title("Battleship")
    StartWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
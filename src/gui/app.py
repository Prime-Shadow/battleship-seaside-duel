from tkinter import Tk, Frame, Label, messagebox, Canvas, Toplevel
from game.board import Board
from game.player import Player
from game.ai import AI
from game.ship import Ship
from gui.widgets import BoardCanvas, draw_ship_preview

class App:
    def __init__(self, master, difficulty="Medium", language="English"):
        self.master = master
        self.master.title("Battleship Game")
        self.master.title("Battleship — Seaside Duel")
        # overall window styling
        self.master.configure(bg="#bfe6ff")
        self.frame = Frame(self.master, padx=12, pady=12, bg="#bfe6ff")
        self.frame.pack(padx=6, pady=6)
        # game model
        self.player = Player("Player")
        self.player_board = Board()
        self.ai_board = Board()
        self.player.board = self.player_board
        # settings from start window
        self.difficulty = difficulty
        self.language = language
        self.ai = AI(self.player_board, difficulty=self.difficulty)

        # placement state
        self.ship_specs = [
            ("Carrier", 5, "C"),
            ("Battleship", 4, "B"),
            ("Cruiser", 3, "R"),
            ("Submarine", 3, "S"),
            ("Destroyer", 2, "D"),
        ]
        self.current_ship_index = None   # selected ship index (None = none selected)
        self.placement_orientation = "H"  # 'H' or 'V'
        self.placement_phase = True

        # top status
        self.status_label = Label(self.frame, text="Place your ships", bg="#cfe8ff", font=("Helvetica", 12, "bold"))
        self.hdr = Label(self.frame, text="Battleship — Seaside Duel", bg="#bfe6ff", fg="#022f40", font=("Helvetica", 18, "bold"))
        self.hdr.grid(row=0, column=0, columnspan=4, pady=(0, 8))

        # controls (no buttons in gameplay window)
        self.currship_lbl = Label(self.frame, text="Select a ship to place", bg="#cfe8ff")
        self.currship_lbl.grid(row=1, column=0, columnspan=4)
        # key bindings for orientation and reset (no buttons)
        self.master.bind('<Key-o>', lambda e: self.toggle_orientation())
        self.master.bind('<Key-r>', lambda e: self.reset_game())
        # orientation indicator as a Canvas (clickable, not a Button)
        self.orient_canvas = Canvas(self.frame, width=120, height=28, bg="#f5fbff", highlightthickness=1, highlightbackground="#a9d0ff")
        self.orient_canvas.grid(row=1, column=3, sticky="e")
        self._orient_rect = self.orient_canvas.create_rectangle(2, 2, 118, 26, fill="#ffffff", outline="")
        self._orient_text = self.orient_canvas.create_text(60, 14, text=f"Orientation: {self.placement_orientation}", font=("Helvetica", 10))
        self.orient_canvas.bind('<Button-1>', lambda ev: self.toggle_orientation())
        # back-to-main indicator (canvas clickable area)
        self.back_canvas = Canvas(self.frame, width=100, height=28, bg="#f5fbff", highlightthickness=1, highlightbackground="#a9d0ff")
        self.back_canvas.grid(row=1, column=2, sticky="e")
        self.back_canvas.create_rectangle(2, 2, 98, 26, fill="#ffffff", outline="")
        self.back_canvas_text = self.back_canvas.create_text(50, 14, text="Back", font=("Helvetica", 10))
        self.back_canvas.bind('<Button-1>', lambda ev: self.open_start_modal())

        # simple translations dict
        self._translations = {
            "English": {
                "ships_to_place": "Ships to place:",
                "your_board": "Your board",
                "enemy_board": "Enemy board",
                "selected": "Selected: {name} ({size})",
                "place_ships": "Place your ships",
                "select_ship": "Select a ship to place",
                "no_ship_selected": "Please select which ship to place first.",
                "cannot_place": "Cannot place {name} at {coord} {orient}",
                "already_placed": "{name} already placed.",
                "all_placed": "All ships placed. Starting game...",
                "game_started": "Game started. Your move: click enemy grid to fire.",
                "place_first": "Finish placing your ships first.",
                "invalid_move": "You already shot there or it's out of bounds",
                "ship_sunk": "You sunk my {name}!",
                "you_win": "You win!",
                "ai_win": "AI wins!",
                "ai_miss": "AI missed at {guess}.",
                "orientation": "Orientation:",
                "back": "Back",
                "start": "Start",
                "exit": "Exit",
                "language_label": "Language:",
                "ai_label": "AI Difficulty:",
                "author": "Author:",
                "license": "License:",
            },
            "Spanish": {
                "ships_to_place": "Barcos a colocar:",
                "your_board": "Tu tablero",
                "enemy_board": "Tablero enemigo",
                "selected": "Seleccionado: {name} ({size})",
                "place_ships": "Coloca tus barcos",
                "select_ship": "Selecciona un barco",
                "no_ship_selected": "Por favor selecciona primero un barco.",
                "cannot_place": "No se puede colocar {name} en {coord} {orient}",
                "already_placed": "{name} ya colocado.",
                "all_placed": "Todos los barcos colocados. Iniciando...",
                "game_started": "Juego iniciado. Tu turno: haz clic en el tablero enemigo.",
                "place_first": "Termina de colocar tus barcos primero.",
                "invalid_move": "Ya disparaste ahí o está fuera de los límites",
                "ship_sunk": "¡Hundiste mi {name}!",
                "you_win": "¡Has ganado!",
                "ai_win": "¡La IA gana!",
                "ai_miss": "La IA falló en {guess}.",
                "orientation": "Orientación:",
                "back": "Volver",
                "start": "Iniciar",
                "exit": "Salir",
                "language_label": "Idioma:",
                "ai_label": "Dificultad IA:",
                "author": "Autor:",
                "license": "Licencia:",
            },
            "Romanian": {
                "ships_to_place": "Nave de plasat:",
                "your_board": "Tabela ta",
                "enemy_board": "Tabela inamică",
                "selected": "Selectat: {name} ({size})",
                "place_ships": "Plasează-ți navele",
                "select_ship": "Selectează o navă de plasat",
                "no_ship_selected": "Te rugăm să selectezi mai întâi o navă.",
                "cannot_place": "Nu se poate plasa {name} la {coord} {orient}",
                "already_placed": "{name} a fost deja plasat.",
                "all_placed": "Toate navele au fost plasate. Începem jocul...",
                "game_started": "Jocul a început. E rândul tău: fă clic pe tabla inamică pentru a trage.",
                "place_first": "Finalizează plasarea navelor înainte.",
                "invalid_move": "Ai tras deja acolo sau coordonatele sunt în afara grilei",
                "ship_sunk": "Ai scufundat {name}!",
                "you_win": "Ai câștigat!",
                "ai_win": "AI a câștigat!",
                "ai_miss": "AI a ratat la {guess}.",
                "orientation": "Orientare:",
                "back": "Înapoi",
                "start": "Start",
                "exit": "Ieșire",
                "language_label": "Limbă:",
                "ai_label": "Dificultate AI:",
                "author": "Autor:",
                "license": "Licență:",
            },
            "French": {
                "ships_to_place": "Navires à placer:",
                "your_board": "Votre plateau",
                "enemy_board": "Plateau ennemi",
                "selected": "Sélectionné: {name} ({size})",
                "place_ships": "Placez vos navires",
                "select_ship": "Sélectionnez un navire à placer",
                "no_ship_selected": "Veuillez d'abord sélectionner un navire.",
                "cannot_place": "Impossible de placer {name} en {coord} {orient}",
                "already_placed": "{name} déjà placé.",
                "all_placed": "Tous les navires sont placés. Démarrage...",
                "game_started": "Le jeu a commencé. À vous: cliquez sur la grille ennemie pour tirer.",
                "place_first": "Terminez d'abord de placer vos navires.",
                "invalid_move": "Vous avez déjà tiré ici ou c'est hors limites",
                "ship_sunk": "Vous avez coulé {name}!",
                "you_win": "Vous avez gagné!",
                "ai_win": "L'IA a gagné!",
                "ai_miss": "L'IA a raté en {guess}.",
                "orientation": "Orientation:",
                "back": "Retour",
                "start": "Démarrer",
                "exit": "Quitter",
                "language_label": "Langue:",
                "ai_label": "Difficulté IA:",
                "author": "Auteur:",
                "license": "Licence:",
            },
            "German": {
                "ships_to_place": "Schiffe zum Platzieren:",
                "your_board": "Dein Feld",
                "enemy_board": "Gegnerisches Feld",
                "selected": "Ausgewählt: {name} ({size})",
                "place_ships": "Platziere deine Schiffe",
                "select_ship": "Wähle ein Schiff zum Platzieren",
                "no_ship_selected": "Bitte wähle zuerst ein Schiff aus.",
                "cannot_place": "Kann {name} nicht bei {coord} {orient} platzieren",
                "already_placed": "{name} bereits platziert.",
                "all_placed": "Alle Schiffe platziert. Spiel startet...",
                "game_started": "Spiel gestartet. Dein Zug: Klicke auf das gegnerische Feld, um zu feuern.",
                "place_first": "Beende zuerst das Platzieren deiner Schiffe.",
                "invalid_move": "Dort wurde bereits geschossen oder es liegt außerhalb",
                "ship_sunk": "Du hast {name} versenkt!",
                "you_win": "Du hast gewonnen!",
                "ai_win": "KI gewinnt!",
                "ai_miss": "KI hat bei {guess} verfehlt.",
                "orientation": "Ausrichtung:",
                "back": "Zurück",
                "start": "Start",
                "exit": "Beenden",
                "language_label": "Sprache:",
                "ai_label": "KI Schwierigkeit:",
                "author": "Autor:",
                "license": "Lizenz:",
            }
        }

        # apply initial translations for chosen language
        self.apply_translations()

        # ship preview canvases (replaces buttons)
        self.ship_preview_canvases = []
        self.ship_preview_overlays = []
        self.ship_sel_frame = Frame(self.frame, bg="#cfe8ff")
        self.ship_sel_frame.grid(row=2, column=4, rowspan=10, sticky="n")
        self.ship_sel_label = Label(self.ship_sel_frame, text="Ships to place:", bg="#cfe8ff")
        self.ship_sel_label.pack(anchor="w", pady=(0,6))
        preview_cell = 20
        for idx, (name, size, sym) in enumerate(self.ship_specs):
            # each preview Canvas sized to fit the ship horizontally
            width = size * preview_cell + 12
            height = preview_cell + 12
            cv = Canvas(self.ship_sel_frame, width=width, height=height, bg="#f5fbff", highlightthickness=1, highlightbackground="#a9d0ff")
            cv.pack(pady=6)
            draw_ship_preview(cv, size, cell=preview_cell, color="#9bb7a8", emoji="⛴️")
            cv.bind("<Button-1>", lambda ev, i=idx: self.select_ship(i))
            # double-click preview to toggle orientation if desired
            cv.bind("<Double-1>", lambda ev: self.toggle_orientation())
            # store canvas and overlay id placeholder
            self.ship_preview_canvases.append(cv)
            self.ship_preview_overlays.append(None)

        # canvases/boards
        self.player_canvas = BoardCanvas(self.frame, self.player_board, cell_size=34, show_ships=True,
                         click_callback=self.player_board_click, title="Your board")
        self.player_canvas.grid(row=2, column=0, columnspan=2, padx=(0,8))
        self.ai_canvas = BoardCanvas(self.frame, self.ai_board, cell_size=34, show_ships=False,
                        click_callback=self.ai_board_click, title="Enemy board")
        self.ai_canvas.grid(row=2, column=2, columnspan=2)

        # initialize placement
        self.setup_placement()

    def setup_placement(self):
        self.player_board.reset()
        self.ai_board.reset()
        self.player_canvas.clear()
        self.ai_canvas.clear()
        self.current_ship_index = None
        self.placement_orientation = "H"
        self.placement_phase = True
        self.currship_lbl.config(text="Select a ship to place")
        self.status_label.config(text="Select a ship, press 'o' to toggle orientation, then click a start cell. Press 'r' to reset.")
        # update orientation indicator
        try:
            self.orient_canvas.itemconfigure(self._orient_text, text=f"Orientation: {self.placement_orientation}")
        except Exception:
            pass
        # ensure header/labels reflect current language
        self.apply_translations()
        # enable all ship previews (clear overlays)
        for i, cv in enumerate(self.ship_preview_canvases):
            cv.config(state="normal")
            # remove overlay if exists
            oid = self.ship_preview_overlays[i]
            if oid:
                try:
                    cv.delete(oid)
                except Exception:
                    pass
                self.ship_preview_overlays[i] = None
        # no start button in gameplay window

    def select_ship(self, index):
        # If already placed, do nothing
        if index < 0 or index >= len(self.ship_specs):
            return
        name, size, sym = self.ship_specs[index]
        for s in self.player_board.ships:
            if s.name == name:
                messagebox.showinfo(self._t('already_placed').split('\n')[0], self._t('already_placed').format(name=name))
                return
        self.current_ship_index = index
        # use localized selected text if available
        try:
            sel_text = self._t('selected').format(name=name, size=size)
        except Exception:
            sel_text = f"Selected: {name} ({size})"
        self.currship_lbl.config(text=sel_text)
        # highlight selected preview with a border rectangle
        for i, cv in enumerate(self.ship_preview_canvases):
            cv.delete("selrect")
            if i == index:
                cv.create_rectangle(2, 2, int(cv['width'])-2, int(cv['height'])-2, outline="#ff9f1c", width=3, tags="selrect")

    def toggle_orientation(self):
        self.placement_orientation = "V" if self.placement_orientation == "H" else "H"
        self.status_label.config(text=f"Orientation: {self.placement_orientation}")
        # update indicator text
        try:
            self.orient_canvas.itemconfigure(self._orient_text, text=f"Orientation: {self.placement_orientation}")
        except Exception:
            pass

    def apply_translations(self):
        # update visible UI texts based on self.language
        try:
            self.hdr.config(text="Battleship — Seaside Duel")
        except Exception:
            pass
        try:
            self.status_label.config(text=self._t('place_ships'))
        except Exception:
            pass
        try:
            self.currship_lbl.config(text=self._t('select_ship'))
        except Exception:
            pass
        try:
            # ships palette label
            self.ship_sel_label.config(text=self._t('ships_to_place'))
        except Exception:
            pass
        try:
            # update board titles if available
            self.player_canvas.set_title(self._t('your_board'))
        except Exception:
            pass
        try:
            self.ai_canvas.set_title(self._t('enemy_board'))
        except Exception:
            pass
        try:
            # update orientation canvas text
            orient_label = self._t('orientation') if isinstance(self._t('orientation'), str) else self._t('orientation')
            self.orient_canvas.itemconfigure(self._orient_text, text=f"{orient_label} {self.placement_orientation}")
        except Exception:
            pass
        try:
            # back button text
            self.back_canvas.itemconfigure(self.back_canvas_text, text=self._t('back'))
        except Exception:
            pass

    def player_board_click(self, row, col):
        if not self.placement_phase:
            return
        if self.current_ship_index is None:
            messagebox.showwarning(self._t('select_ship'), self._t('no_ship_selected'))
            return
        name, size, symbol = self.ship_specs[self.current_ship_index]
        ship = Ship(name, size, [], symbol)
        success = self.player_board.place_ship(ship, (row, col), self.placement_orientation)
        if not success:
            messagebox.showwarning(self._t('cannot_place').split('\n')[0], self._t('cannot_place').format(name=name, coord=(row, col), orient=self.placement_orientation))
            return
        # draw placed ship on player canvas
        self.player_canvas.draw_ship(ship, color="#9bb7a8")
        # disable the placed ship preview (overlay a greyscale rect)
        cv = self.ship_preview_canvases[self.current_ship_index]
        w = int(cv['width']); h = int(cv['height'])
        oid = cv.create_rectangle(0, 0, w, h, fill="#cccccc", stipple="gray25")
        self.ship_preview_overlays[self.current_ship_index] = oid
        cv.delete("selrect")
        cv.config(state="disabled")
        self.current_ship_index = None
        self.currship_lbl.config(text="Select a ship to place")
        # check if all placed
        if len(self.player_board.ships) >= len(self.ship_specs):
            self.placement_phase = False
            self.currship_lbl.config(text="All ships placed")
            self.status_label.config(text=self._t('all_placed'))
            # automatically start the game when placement is complete
            self.master.after(150, self.start_game)

    def start_game(self):
        # AI places randomly
        self.ai_board.place_ships_randomly()
        # recreate AI with selected difficulty
        self.ai = AI(self.player_board, difficulty=self.difficulty)
        # ensure AI canvas does not reveal ships; it will draw hits only
        self.ai_canvas.clear()
        self.status_label.config(text=self._t('game_started'))

    def ai_board_click(self, row, col):
        if self.placement_phase:
            messagebox.showinfo(self._t('place_ships'), self._t('place_first'))
            return
        if not self.ai_board.is_valid_guess(row, col):
            messagebox.showwarning(self._t('invalid_move'), self._t('invalid_move'))
            return
        result, ship_name = self.ai_board.receive_shot((row, col))
        if result in ("hit", "sunk"):
            self.ai_canvas.mark_hit(row, col)
            self.status_label.config(text=f"You {result.upper()} {ship_name or ''}".strip())
            if result == "sunk":
                messagebox.showinfo(self._t('ship_sunk').split('\n')[0], self._t('ship_sunk').format(name=ship_name))
                # draw sunk ship on AI canvas for effect
                for s in self.ai_board.ships:
                    if s.name == ship_name and s.is_sunk():
                        self.ai_canvas.draw_ship(s, color="#7a3b3b")
                        self.ai_canvas.mark_sunk(s)
                if self.ai_board.all_ships_sunk():
                    messagebox.showinfo(self._t('you_win').split('\n')[0], self._t('you_win'))
                    self.reset_game()
                    return
            # player gets another shot (click again)
            return
        else:
            self.ai_canvas.mark_miss(row, col)
            self.status_label.config(text="Miss! AI's turn...")
            self.master.after(300, self.ai_turn)

    def ai_turn(self):
        while True:
            guess = self.ai.make_guess()
            result, ship_name = self.player_board.receive_shot(guess)
            self.ai.record_result(guess, result)
            r, c = guess
            if result in ("hit", "sunk"):
                self.player_canvas.mark_hit(r, c)
                self.status_label.config(text=f"AI {result.upper()} at {guess}")
                if result == "sunk":
                    for s in self.player_board.ships:
                        if s.name == ship_name and s.is_sunk():
                            self.player_canvas.mark_sunk(s)
                    if self.player_board.all_ships_sunk():
                        messagebox.showinfo(self._t('ai_win').split('\n')[0], self._t('ai_win'))
                        self.reset_game()
                        return
                # AI continues (extra turn)
            else:
                self.player_canvas.mark_miss(r, c)
                self.status_label.config(text=self._t('ai_miss').format(guess=guess) + " Your turn.")
                break

    def _t(self, key):
        # simple translator with fallback to English
        lang = self.language if self.language in self._translations else "English"
        return self._translations.get(lang, self._translations["English"]).get(key, self._translations["English"].get(key, key))

    def reset_game(self):
        """Reset the game state to allow replay/placement.

        This reinitializes boards and canvases and returns the UI
        to the placement phase.
        """
        try:
            # re-create AI with current difficulty and clear any state
            self.ai = AI(self.player_board, difficulty=self.difficulty)
        except Exception:
            pass
        # reuse existing setup_placement which clears boards/canvases
        try:
            self.setup_placement()
        except Exception:
            # fallback: manually clear boards/canvases
            try:
                self.player_board.reset()
                self.ai_board.reset()
                self.player_canvas.clear()
                self.ai_canvas.clear()
                self.current_ship_index = None
                self.placement_phase = True
            except Exception:
                pass
        # ensure translations/states are applied
        try:
            self.apply_translations()
        except Exception:
            pass

    def open_start_modal(self):
        # create a modal start dialog (canvas-driven) to change language/difficulty and restart
        # hide the entire main window so only the start/modal is visible
        try:
            self.master.withdraw()
        except Exception:
            pass
        # create an independent modal dialog (use default root window)
        w = Toplevel()
        w.title(self._t('start') if hasattr(self, '_t') else "Start")
        w.resizable(False, False)
        canvas = Canvas(w, width=380, height=260, bg="#f5fbff", highlightthickness=0)
        canvas.pack(padx=8, pady=6)

        # make this dialog modal (grab input)
        try:
            w.grab_set()
        except Exception:
            pass

        langs = ["English", "Spanish", "French", "German", "Romanian"]
        diffs = ["Easy", "Medium", "Hard"]
        lang_idx = langs.index(self.language) if self.language in langs else 0
        diff_idx = diffs.index(self.difficulty) if self.difficulty in diffs else 1

        # layout boxes
        lang_box = (20, 40, 340, 80)
        diff_box = (20, 100, 340, 140)
        start_box = (140, 180, 260, 220)
        exit_box = (20, 180, 120, 220)

        # author/license header
        header_id = canvas.create_text(190, 18, text="Battleship — Seaside Duel", font=("Helvetica", 14, "bold"))
        author_id = canvas.create_text(190, 34, text=f"{self._t('author')} Mihai Sirbu", font=("Helvetica", 9))
        license_id = canvas.create_text(190, 48, text=f"{self._t('license')} MIT License 2025", font=("Helvetica", 8))

        # create language area with tag so clicks on any item in the area are captured
        lang_rect_id = canvas.create_rectangle(*lang_box, fill="#ffffff", outline="#a9d0ff", tags=("lang_area",))
        lang_text = canvas.create_text(190, 60, text=f"{self._t('language_label')} {langs[lang_idx]}", font=("Helvetica", 12), tags=("lang_area",))
        diff_rect_id = canvas.create_rectangle(*diff_box, fill="#ffffff", outline="#a9d0ff", tags=("diff_area",))
        diff_text = canvas.create_text(190, 120, text=f"{self._t('ai_label')} {diffs[diff_idx]}", font=("Helvetica", 12), tags=("diff_area",))

        canvas.create_rectangle(*start_box, fill="#9bb7a8", outline="#5a8f6a", width=2, tags=("start_area",))
        start_text_id = canvas.create_text((start_box[0]+start_box[2])//2, (start_box[1]+start_box[3])//2, text=self._t('start'), font=("Helvetica", 12, "bold"), fill="white", tags=("start_area",))

        canvas.create_rectangle(*exit_box, fill="#e86a6a", outline="#a94444", width=2, tags=("exit_area",))
        exit_text_id = canvas.create_text((exit_box[0]+exit_box[2])//2, (exit_box[1]+exit_box[3])//2, text=self._t('exit'), font=("Helvetica", 10, "bold"), fill="white", tags=("exit_area",))

        def apply_and_close():
            # apply selections and restore main window
            try:
                self.language = langs[lang_idx]
                self.difficulty = diffs[diff_idx]
                self.ai = AI(self.player_board, difficulty=self.difficulty)
                self.reset_game()
                self.apply_translations()
            except Exception:
                pass
            try:
                w.grab_release()
            except Exception:
                pass
            try:
                w.destroy()
            except Exception:
                pass
            # restore the main window and re-pack the game frame
            try:
                self.master.deiconify()
            except Exception:
                pass
            try:
                self.frame.pack(padx=6, pady=6)
            except Exception:
                pass
            try:
                self.master.lift()
                self.master.focus_force()
                # force redraw of canvases
                try:
                    self.player_canvas.clear()
                    self.ai_canvas.clear()
                except Exception:
                    pass
                self.master.update_idletasks()
            except Exception:
                pass

        def cancel_and_close():
            try:
                w.grab_release()
            except Exception:
                pass
            try:
                w.destroy()
            except Exception:
                pass
            # restore main window
            try:
                self.master.deiconify()
            except Exception:
                pass
            try:
                self.frame.pack(padx=6, pady=6)
            except Exception:
                pass
            try:
                self.master.lift()
                self.master.focus_force()
                self.master.update_idletasks()
            except Exception:
                pass

        def on_click(ev):
            nonlocal lang_idx, diff_idx
            x, y = ev.x, ev.y
            # debug: mark where clicks land
            try:
                # a small dot to visualize clicks during debugging
                dot = canvas.create_oval(x-2, y-2, x+2, y+2, fill="#333333", outline="")
                canvas.after(300, lambda: canvas.delete(dot))
            except Exception:
                pass
            lx0, ly0, lx1, ly1 = lang_box
            dx0, dy0, dx1, dy1 = diff_box
            sx0, sy0, sx1, sy1 = start_box
            ex0, ey0, ex1, ey1 = exit_box
            # prefer tag-based handling when clicking on specific items
            # (ensures clicks on text/rectangle are captured)
            try:
                tags = canvas.gettags(canvas.find_closest(x, y))
            except Exception:
                tags = ()
            if 'lang_area' in tags or (lx0 <= x <= lx1 and ly0 <= y <= ly1):
                lang_idx = (lang_idx + 1) % len(langs)
                # update modal labels using the newly selected language translations
                trans = self._translations.get(langs[lang_idx], self._translations.get('English'))
                canvas.itemconfigure(lang_text, text=f"{trans.get('language_label','Language:')} {langs[lang_idx]}")
                canvas.itemconfigure(diff_text, text=f"{trans.get('ai_label','AI Difficulty:')} {diffs[diff_idx]}")
                canvas.itemconfigure(start_text_id, text=trans.get('start','Start'))
                canvas.itemconfigure(exit_text_id, text=trans.get('exit','Exit'))
                canvas.itemconfigure(author_id, text=f"{trans.get('author','Author:')} Mihai Sirbu")
                canvas.itemconfigure(license_id, text=f"{trans.get('license','License:')} MIT License 2025")
                try:
                    canvas.update_idletasks()
                    w.update()
                except Exception:
                    pass
                return
            if 'diff_area' in tags or (dx0 <= x <= dx1 and dy0 <= y <= dy1):
                diff_idx = (diff_idx + 1) % len(diffs)
                # update difficulty label using currently selected language
                trans = self._translations.get(langs[lang_idx], self._translations.get('English'))
                canvas.itemconfigure(diff_text, text=f"{trans.get('ai_label','AI Difficulty:')} {diffs[diff_idx]}")
                try:
                    canvas.update_idletasks()
                    w.update()
                except Exception:
                    pass
                return
            if 'start_area' in tags or (sx0 <= x <= sx1 and sy0 <= y <= sy1):
                apply_and_close()
                return
            if 'exit_area' in tags or (ex0 <= x <= ex1 and ey0 <= y <= ey1):
                # Exit the entire application
                try:
                    w.grab_release()
                except Exception:
                    pass
                try:
                    w.destroy()
                except Exception:
                    pass
                try:
                    self.master.destroy()
                except Exception:
                    pass

        # bind canvas click fallback and also bind tags to ensure text/rect item clicks are handled
        canvas.bind('<Button-1>', on_click)
        try:
            canvas.tag_bind('lang_area', '<Button-1>', on_click)
            canvas.tag_bind('diff_area', '<Button-1>', on_click)
            canvas.tag_bind('start_area', '<Button-1>', on_click)
            canvas.tag_bind('exit_area', '<Button-1>', on_click)
        except Exception:
            pass
        def on_wm_close():
            cancel_and_close()
        w.protocol('WM_DELETE_WINDOW', on_wm_close)

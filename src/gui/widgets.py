from tkinter import Canvas, Frame, Label
from tkinter import Canvas, Frame, Label
import math


class BoardCanvas(Frame):
    """Canvas-based board widget with improved visuals:
    - stylized water background
    - rounded, textured ships with shadow
    - animated hit pegs and subtle miss pegs
    - grid labels
    """

    def __init__(self, master, board, cell_size=36, show_ships=False, click_callback=None, title=None):
        super().__init__(master, bg="#cfe8ff")
        self.board = board
        self.cell = cell_size
        self.size = board.size
        self.show_ships = show_ships
        self.click_callback = click_callback
        if title:
            lbl = Label(self, text=title, bg="#cfe8ff", font=("Helvetica", 10, "bold"))
            lbl.pack(anchor="w")
            self.title_label = lbl
        else:
            self.title_label = None
        self.canvas = Canvas(self, width=self.cell * (self.size) + 40, height=self.cell * (self.size) + 40, bg="#e6f2ff", highlightthickness=0)
        self.canvas.pack()
        self._ship_items = {}
        self._peg_items = {}
        self._draw_grid()
        self.canvas.bind("<Button-1>", self._on_click)
        if self.show_ships:
            self.draw_ships()

    # --- drawing helpers ---
    def _draw_grid(self):
        cs = self.cell
        off = 30
        w = off + self.size * cs + 10
        h = off + self.size * cs + 10
        # water background: alternating subtle waves
        self.canvas.create_rectangle(0, 0, w + 10, h + 10, fill="#cde7ff", outline="")
        for i in range(0, int(h / 8)):
            y = i * 8 + 18
            color = "#cfefff" if i % 2 == 0 else "#d9f2ff"
            self.canvas.create_line(0, y, w + 10, y, fill=color)

        # column letters and row numbers
        for c in range(self.size):
            self.canvas.create_text(off + c * cs + cs / 2, 12, text=chr(ord("A") + c), font=("Helvetica", 10, "bold"), fill="#034f84")
        for r in range(self.size):
            self.canvas.create_text(12, off + r * cs + cs / 2, text=str(r + 1), font=("Helvetica", 10, "bold"), fill="#034f84")

        # grid lines with softened color
        for i in range(self.size + 1):
            x = off + i * cs
            self.canvas.create_line(x, off, x, off + self.size * cs, fill="#7ea9ff")
        for j in range(self.size + 1):
            y = off + j * cs
            self.canvas.create_line(off, y, off + self.size * cs, y, fill="#7ea9ff")

    def _on_click(self, event):
        off = 30
        x = event.x - off
        y = event.y - off
        if x < 0 or y < 0:
            return
        col = int(x // self.cell)
        row = int(y // self.cell)
        if 0 <= row < self.size and 0 <= col < self.size:
            if callable(self.click_callback):
                self.click_callback(row, col)

    def clear(self):
        self.canvas.delete("all")
        self._ship_items.clear()
        self._peg_items.clear()
        self._draw_grid()

    def set_title(self, text):
        """Update the optional title label for the board widget."""
        if getattr(self, 'title_label', None):
            try:
                self.title_label.config(text=text)
            except Exception:
                pass

    # --- ships ---
    def draw_ships(self):
        for ship in self.board.ships:
            self.draw_ship(ship)

    def draw_ship(self, ship, color="#8c6a43"):
        if not hasattr(ship, "coordinates") or not ship.coordinates:
            return
        coords = sorted(ship.coordinates)
        rs = [r for (r, c) in coords]
        cs = [c for (r, c) in coords]
        r0, r1 = min(rs), max(rs)
        c0, c1 = min(cs), max(cs)
        x0 = 30 + c0 * self.cell + 6
        y0 = 30 + r0 * self.cell + 6
        x1 = 30 + (c1 + 1) * self.cell - 6
        y1 = 30 + (r1 + 1) * self.cell - 6

        # shadow
        shadow = self.canvas.create_rectangle(x0 + 4, y0 + 6, x1 + 6, y1 + 10, fill="#5b6b75", outline="", stipple="gray25")

        # textured body: draw layered rounded shape to suggest wood/metal
        radius = max(8, min(16, self.cell // 3))
        body = self.canvas.create_rectangle(x0 + radius / 2, y0, x1 - radius / 2, y1, fill=color, outline="#3e2e2e", width=2)
        left_cap = self.canvas.create_oval(x0, y0, x0 + radius, y1, fill=color, outline="#3e2e2e", width=2)
        right_cap = self.canvas.create_oval(x1 - radius, y0, x1, y1, fill=color, outline="#3e2e2e", width=2)
        items = [shadow, body, left_cap, right_cap]

        # planking lines
        length_pixels = max(1, int((x1 - x0)))
        planks = max(1, int(length_pixels // 12))
        for i in range(1, planks):
            px = x0 + radius / 2 + i * ((x1 - x0 - radius) / planks)
            items.append(self.canvas.create_line(px, y0 + 6, px, y1 - 6, fill="#6f4f36", width=1))

        # central label (subtle emoji scaled to cell)
        try:
            items.append(self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text="⛴️", font=("Helvetica", int(self.cell / 1.8))))
        except Exception:
            pass

        self._ship_items[ship] = items

    # --- pegs and animations ---
    def mark_hit(self, row, col):
        key = (row, col)
        if key in self._peg_items:
            return
        off = 30
        cx = off + col * self.cell + self.cell / 2
        cy = off + row * self.cell + self.cell / 2
        # slightly smaller peg for a less dominant look
        r = self.cell * 0.20

        oval = self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill="#d62828", outline="#7b0000", width=1)
        cross1 = self.canvas.create_line(cx - r * 0.55, cy - r * 0.55, cx + r * 0.55, cy + r * 0.55, fill="white", width=1.5)
        cross2 = self.canvas.create_line(cx + r * 0.55, cy - r * 0.55, cx - r * 0.55, cy + r * 0.55, fill="white", width=1.5)
        self._peg_items[key] = [oval, cross1, cross2]

        # simple pop animation (scale up then settle)
        def pop(step=0):
            if step >= 5:
                return
            # subtle scale animation
            s = 1.0 + 0.04 * (5 - step)
            try:
                self.canvas.scale(oval, cx, cy, s, s)
                self.canvas.scale(cross1, cx, cy, s, s)
                self.canvas.scale(cross2, cx, cy, s, s)
            except Exception:
                pass
            self.after(25, lambda: pop(step + 1))

        pop()

    def mark_miss(self, row, col):
        key = (row, col)
        if key in self._peg_items:
            return
        off = 30
        cx = off + col * self.cell + self.cell / 2
        cy = off + row * self.cell + self.cell / 2
        r = self.cell * 0.14
        peg = self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill="#ffffff", outline="#bfbfbf", width=2)
        self._peg_items[key] = [peg]

        # gentle fade-out highlight to simulate a small splash
        def pulse(alpha=0):
            if alpha > 6:
                return
            try:
                self.canvas.itemconfig(peg, fill="#ffffff")
            except Exception:
                pass
            self.after(80, lambda: pulse(alpha + 1))

        pulse()

    def mark_sunk(self, ship):
        items = self._ship_items.get(ship)
        if not items:
            return
        for it in items:
            try:
                self.canvas.itemconfig(it, fill="#5a1f1f")
            except Exception:
                pass
        coords = ship.coordinates
        r = sum([c[0] for c in coords]) / len(coords)
        c = sum([c[1] for c in coords]) / len(coords)
        cx = 30 + c * self.cell + self.cell / 2
        cy = 30 + r * self.cell + self.cell / 2
        self.canvas.create_text(cx, cy, text="SUNK!", fill="yellow", font=("Helvetica", int(self.cell / 2), "bold"))


# utility to draw a small ship preview onto any Canvas (used by the UI ship palette)
def draw_ship_preview(canvas, length, cell=28, color="#9bb7a8", emoji="⛴️"):
    pad = 6
    x0 = pad
    y0 = pad
    x1 = pad + length * cell
    y1 = pad + cell
    radius = max(6, min(12, cell // 3))
    body = canvas.create_rectangle(x0 + radius / 2, y0, x1 - radius / 2, y1, fill=color, outline="#5a3e2a", width=2)
    left_cap = canvas.create_oval(x0, y0, x0 + radius, y1, fill=color, outline="#5a3e2a", width=2)
    right_cap = canvas.create_oval(x1 - radius, y0, x1, y1, fill=color, outline="#5a3e2a", width=2)
    length_pixels = x1 - x0
    planks = max(1, int(length_pixels // 12))
    for i in range(1, planks):
        px = x0 + radius / 2 + i * ((x1 - x0 - radius) / planks)
        canvas.create_line(px, y0 + 5, px, y1 - 5, fill="#6f4f36", width=1)
    try:
        canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=emoji, font=("Helvetica", max(10, int(cell / 1.6))))
    except Exception:
        pass

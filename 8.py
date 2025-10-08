import math
import os
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser

class Square:  # class
    def __init__(self, cx, cy, side, angle=0.0, color="#888888"):  # method
        self.cx = float(cx)        # attribute
        self.cy = float(cy)        # attribute
        self.side = float(side)    # attribute
        self.angle = float(angle)  # attribute
        self.color = str(color)    # attribute
        if self.side <= 0:
            raise ValueError("Сторона должна быть > 0")

    def _coords(self):  # method
        s = self.side / 2.0
        pts = [(-s, -s), (s, -s), (s, s), (-s, s)]
        ang = math.radians(self.angle)
        c, sn = math.cos(ang), math.sin(ang)
        res = []
        for x, y in pts:
            xr = x * c - y * sn + self.cx
            yr = x * sn + y * c + self.cy
            res.extend([xr, yr])
        return res

    def draw(self, canvas):  # method
        return canvas.create_polygon(self._coords(), fill=self.color, outline="#cfcfcf", width=2)

    def recolor(self, new_color):  # method
        self.color = new_color

    def rotate(self, delta_angle):  # method
        self.angle = (self.angle + float(delta_angle)) % 360

    def segment(self, canvas):  # method
        s = self.side / 2.0
        ang = math.radians(self.angle)
        c, sn = math.cos(ang), math.sin(ang)
        x1 = (-s) * c + self.cx; y1 = (-s) * sn + self.cy
        x2 = (s) * c + self.cx;  y2 = (s) * sn + self.cy
        x3 = (s) * (-sn) + self.cx; y3 = (s) * c + self.cy
        x4 = (s) * sn + self.cx;   y4 = (s) * (-c) + self.cy
        canvas.create_line(x1, y1, x2, y2, width=2, dash=(4, 3), fill="#d0d0d0", tags=("seg",))
        canvas.create_line(x3, y3, x4, y4, width=2, dash=(4, 3), fill="#d0d0d0", tags=("seg",))


class App:  # class
    def __init__(self, root):  # method
        self.root = root                   # attribute
        self.root.title("ЛР8 — Вариант 7: Квадраты (Tkinter, ООП)")
        self.squares = []                  # attribute
        self.items = []                    # attribute
        self.filepath = None               # attribute
        self.seg_tag = "seg"               # attribute

        bg = "#1e1e1e"; bg2 = "#232323"; fg = "#e6e6e6"; acc = "#3a3a3a"
        self.root.configure(bg=bg)

        control = tk.Frame(root, padx=8, pady=6, bg=bg)
        control.pack(side=tk.TOP, fill=tk.X)

        def dbtn(txt, cmd):
            return tk.Button(control, text=txt, command=cmd,
                             bg=bg2, fg=fg, activebackground=acc, activeforeground=fg,
                             relief=tk.FLAT, padx=10, pady=5, highlightthickness=0)

        dbtn("Открыть файл…", self.pick_file).pack(side=tk.LEFT, padx=3)
        dbtn("Загрузить", self.load_file).pack(side=tk.LEFT, padx=3)

        tk.Label(control, text="Цвет:", bg=bg, fg=fg).pack(side=tk.LEFT, padx=(12, 3))
        self.color_entry = tk.Entry(control, width=10, bg=bg2, fg=fg, insertbackground=fg, relief=tk.FLAT)
        self.color_entry.insert(0, "#33cc99"); self.color_entry.pack(side=tk.LEFT)
        dbtn("…", self.pick_color).pack(side=tk.LEFT, padx=(3, 10))
        dbtn("Раскрасить", self.recolor_all).pack(side=tk.LEFT, padx=3)

        tk.Label(control, text="Поворот, °:", bg=bg, fg=fg).pack(side=tk.LEFT, padx=(12, 3))
        self.angle_entry = tk.Entry(control, width=6, bg=bg2, fg=fg, insertbackground=fg, relief=tk.FLAT)
        self.angle_entry.insert(0, "15"); self.angle_entry.pack(side=tk.LEFT)
        dbtn("Повернуть", self.rotate_all).pack(side=tk.LEFT, padx=3)
        dbtn("Сегментация", self.segment_all).pack(side=tk.LEFT, padx=3)
        dbtn("Сохранить", self.save_file).pack(side=tk.RIGHT, padx=3)

        self.status = tk.Label(root, anchor="w", fg=fg, bg=bg, padx=8)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

        self.canvas = tk.Canvas(root, width=900, height=600, bg="#121212", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def pick_file(self):  # method
        path = filedialog.askopenfilename(title="Выберите входной файл",
                                          filetypes=[("Text", "*.txt"), ("All files", "*.*")])
        if path:
            self.filepath = path
            self.load_file()

    def parse_line(self, line, lineno):  # method
        parts = line.strip().split()
        if len(parts) < 3:
            raise ValueError(f"Строка {lineno}: минимум 3 значения (cx cy side)")
        cx, cy, side = parts[0:3]
        angle = 0.0; color = "#888888"
        if len(parts) >= 4:
            try:
                if parts[3].startswith("#") or parts[3].isalpha():
                    color = parts[3]
                else:
                    angle = float(parts[3])
            except Exception:
                color = parts[3]
        if len(parts) >= 5:
            color = parts[4]
        return Square(cx, cy, side, angle, color)

    def load_file(self):  # method
        if not self.filepath or not os.path.exists(self.filepath):
            messagebox.showerror("Ошибка", "Файл не выбран или не найден.")
            return
        self.squares.clear()
        errors = []
        with open(self.filepath, "r", encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                if not line.strip():
                    continue
                try:
                    self.squares.append(self.parse_line(line, i))
                except Exception as e:
                    errors.append(str(e))
        self.status.config(text=f"Загружено: {len(self.squares)}. Ошибок: {len(errors)}.")
        if errors:
            messagebox.showwarning("Проблемы при загрузке", "\n".join(errors))
        self.visualize()

    def visualize(self):  # method
        self.canvas.delete(self.seg_tag)
        for it in self.items:
            self.canvas.delete(it)
        self.items.clear()
        for sq in self.squares:
            self.items.append(sq.draw(self.canvas))
        self.status.config(text=f"Отрисовано: {len(self.squares)}")

    def pick_color(self):  # method
        initial = self.color_entry.get().strip() or "#33cc99"
        chosen = colorchooser.askcolor(initialcolor=initial, title="Выберите цвет")
        if chosen and chosen[1]:
            self.color_entry.delete(0, tk.END)
            self.color_entry.insert(0, chosen[1])

    def recolor_all(self):  # method
        color = self.color_entry.get().strip()
        try:
            self.canvas.winfo_rgb(color)
        except Exception:
            messagebox.showerror("Ошибка", "Некорректный цвет. Пример: #33cc99 или red")
            return
        for sq in self.squares:
            sq.recolor(color)
        self.visualize()

    def rotate_all(self):  # method
        try:
            da = float(self.angle_entry.get().strip())
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректный угол.")
            return
        for sq in self.squares:
            sq.rotate(da)
        self.visualize()

    def segment_all(self):  # method
        self.visualize()
        for sq in self.squares:
            sq.segment(self.canvas)
        self.status.config(text="Сегментация выполнена")

    def save_file(self):  # method
        path = filedialog.asksaveasfilename(title="Сохранить как",
                                            defaultextension=".txt",
                                            filetypes=[("Text", "*.txt"), ("All files", "*.*")])
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            for sq in self.squares:
                f.write(f"{sq.cx} {sq.cy} {sq.side} {sq.angle} {sq.color}\n")
        self.status.config(text=f"Сохранено: {path}")
        messagebox.showinfo("Готово", f"Файл сохранён:\n{path}")


def main():  # method
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":  # method
    main()

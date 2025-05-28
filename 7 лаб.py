import tkinter as tk
from tkinter import scrolledtext, messagebox
import timeit
from itertools import combinations

def algorithmic_method(players, team_size):
    result = []
    team = []

    def backtrack(start):
        if len(team) == team_size:
            result.append(team.copy())
            return
        for i in range(start, len(players)):
            team.append(players[i])
            backtrack(i + 1)
            team.pop()

    backtrack(0)
    return result


def python_method(players, team_size):
    return list(combinations(players, team_size))

def run_computation():
    try:
        team_size_str = team_size_entry.get().strip()
        if not team_size_str.isdigit():
            messagebox.showerror("Ошибка", "Введите корректный размер команды (целое число).")
            return
        team_size = int(team_size_str)
        if not (1 <= team_size <= len(players)):
            messagebox.showerror("Ошибка", f"Размер команды должен быть от 1 до {len(players)}.")
            return

        result_text.config(state='normal')
        result_text.delete(1.0, tk.END)


        t_alg = timeit.timeit(lambda: algorithmic_method(players, team_size), number=2)
        alg_res = algorithmic_method(players, team_size)


        t_py = timeit.timeit(lambda: python_method(players, team_size), number=2)
        py_res = python_method(players, team_size)

        result_text.insert(tk.END, f"Алгоритмический метод:\n"
                                   f"Найдено команд: {len(alg_res)}\n"
                                   f"Время: {t_alg:.6f} сек\n\n"
                                   f"Первые 50 команд:\n")
        for team in alg_res[:50]:
            result_text.insert(tk.END, ", ".join(team) + "\n")

        result_text.insert(tk.END, "\nМетод с использованием itertools:\n"
                                   f"Найдено команд: {len(py_res)}\n"
                                   f"Время: {t_py:.6f} сек\n\n"
                                   f"Первые 50 команд:\n")
        for team in py_res[:50]:
            result_text.insert(tk.END, ", ".join(team) + "\n")

        result_text.config(state='disabled')

    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

def center_window(win, width=700, height=600):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    win.geometry(f"{width}x{height}+{x}+{y}")


professionals = [f'P{i}' for i in range(1, 6)]
amateurs = [f'A{i}' for i in range(1, 6)]
players = professionals + amateurs


root = tk.Tk()
root.title("Формирование команд для игры в гольф")


center_window(root, width=700, height=600)


tk.Label(root, text=f"Введите размер команды (от 1 до {len(players)}):").pack(pady=5)
team_size_entry = tk.Entry(root, width=10)
team_size_entry.pack(pady=5)
team_size_entry.insert(0, "4")


compute_btn = tk.Button(root, text="Сформировать команды", command=run_computation)
compute_btn.pack(pady=10)


tk.Label(root, text="Результаты (первые 50 вариантов):").pack()
result_text = scrolledtext.ScrolledText(root, width=80, height=25, state='disabled')
result_text.pack(padx=10, pady=10, fill='both', expand=True)

root.mainloop()
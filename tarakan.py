''' Tarakashka ishet vihod '''
import random
import tkinter as tk

N, M = 14, 14

maze = [[1] * M for _ in range(N)]
start = (1, 1)
maze[1][1] = 0
stack = [start]
visited = {start}
dirs = [(0,2), (2,0), (0,-2), (-2,0)]

while stack:
    r, c = stack[-1]
    neighbors = []
    for dr, dc in dirs:
        nr, nc = r + dr, c + dc
        if 1 <= nr <= N-2 and 1 <= nc <= M-2 and (nr, nc) not in visited:
            neighbors.append((nr, nc, r + dr//2, c + dc//2))
    if neighbors:
        nr, nc, wr, wc = random.choice(neighbors)
        maze[nr][nc] = 0
        maze[wr][wc] = 0
        visited.add((nr, nc))
        stack.append((nr, nc))
    else:
        stack.pop()

exit_row = None
for r in range(1, N-1):
    if maze[r][M-2] == 0:
        exit_row = r
        break

if exit_row is None:
    exit_row = N // 2
    maze[exit_row][M-2] = 0

maze[exit_row][M-1] = 0
exit_pos = (exit_row, M-1)

CELL_SIZE = 30
root = tk.Tk()
root.title("Таракан ищет выход 🐜")
canvas = tk.Canvas(root, width=M*CELL_SIZE, height=N*CELL_SIZE, bg='white')
canvas.pack()

COLOR_WALL = 'black'
COLOR_PATH = 'white'
COLOR_VISITED = '#cccccc'
COLOR_PATH_FINAL = 'yellow'
COLOR_START = 'green'
COLOR_EXIT = 'red'

search_stack = [start]
visited_search = {start}
parent = {start: None}
found = False
final_path = []

def draw():
    canvas.delete("all")
    for r in range(N):
        for c in range(M):
            x1, y1 = c * CELL_SIZE, r * CELL_SIZE
            x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
            if maze[r][c] == 1:
                canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_WALL, outline='gray')
            else:
                if (r, c) in visited_search:
                    canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_VISITED, outline='gray')
                else:
                    canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_PATH, outline='gray')
    for r, c in final_path:
        canvas.create_rectangle(c*CELL_SIZE, r*CELL_SIZE, (c+1)*CELL_SIZE, (r+1)*CELL_SIZE, fill=COLOR_PATH_FINAL, outline='orange')
    sr, sc = start
    er, ec = exit_pos
    canvas.create_rectangle(sc*CELL_SIZE, sr*CELL_SIZE, (sc+1)*CELL_SIZE, (sr+1)*CELL_SIZE, fill=COLOR_START, outline='darkgreen')
    canvas.create_rectangle(ec*CELL_SIZE, er*CELL_SIZE, (ec+1)*CELL_SIZE, (er+1)*CELL_SIZE, fill=COLOR_EXIT, outline='darkred')

def step():
    global found, final_path
    if found:
        return  

    if not search_stack:
        print("Выход не найден!")
        return

    r, c = search_stack.pop()

    if (r, c) == exit_pos:
        found = True
    
        cur = exit_pos
        while cur != start:
            final_path.append(cur)
            cur = parent[cur]
        draw()
        return  

    for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < N and 0 <= nc < M and maze[nr][nc] == 0 and (nr, nc) not in visited_search:
            visited_search.add((nr, nc))
            parent[(nr, nc)] = (r, c)
            search_stack.append((nr, nc))

    draw()
    root.after(80, step)

draw()
root.after(500, step)
root.mainloop()

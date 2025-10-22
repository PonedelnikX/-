''' Tarakashka ishet vihod '''

import random
import matplotlib.pyplot as plt

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

stack = [start]
visited_search = {start}
parent = {start: None}

while stack:
    r, c = stack.pop()
    if (r, c) == exit_pos:
        break
    for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < N and 0 <= nc < M and maze[nr][nc] == 0 and (nr, nc) not in visited_search:
            visited_search.add((nr, nc))
            parent[(nr, nc)] = (r, c)
            stack.append((nr, nc))

final_path = []
cur = exit_pos
while cur != start:
    final_path.append(cur)
    cur = parent[cur]

plt.figure(figsize=(5,5))
plt.imshow(maze, cmap='binary', origin='upper')  # 1=чёрный, 0=белый

if final_path:
    ys, xs = zip(*final_path)
    plt.plot(xs, ys, color='yellow', linewidth=6, solid_capstyle='round')

plt.plot(start[1], start[0], 's', color='green', markersize=12)
plt.plot(exit_pos[1], exit_pos[0], 's', color='red', markersize=12)

plt.axis('off')
plt.tight_layout()
plt.show()
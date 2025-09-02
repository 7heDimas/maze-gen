import random
from .cells import WALL, ROAD

def _make_odd(n: int) -> int:
    return n if n % 2 == 1 else n - 1 if n > 1 else 1

def carve_maze(rows: int, cols: int, rng: random.Random):
    """
    Randomized DFS (recursive backtracker) in the “chamber” grid.
    Returns a grid of rows x cols (internally truncated to odd numbers).
    """
    rows = _make_odd(rows)
    cols = _make_odd(cols)
    grid = [[WALL for _ in range(cols)] for __ in range(rows)]

    def is_cell(r, c):
        return 0 < r < rows - 1 and 0 < c < cols - 1 and r % 2 == 1 and c % 2 == 1

    sr = rng.randrange(1, rows, 2) if rows >= 3 else 0
    sc = rng.randrange(1, cols, 2) if cols >= 3 else 0
    grid[sr][sc] = ROAD

    stack = [(sr, sc)]
    dirs = [(2, 0), (-2, 0), (0, 2), (0, -2)]

    while stack:
        r, c = stack[-1]
        neighbors = []
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if is_cell(nr, nc) and grid[nr][nc] == WALL:
                neighbors.append((nr, nc))
        if neighbors:
            nr, nc = rng.choice(neighbors)
            grid[(r + nr) // 2][(c + nc) // 2] = ROAD
            grid[nr][nc] = ROAD
            stack.append((nr, nc))
        else:
            stack.pop()
    return grid

def add_loops(grid, rng: random.Random, percent: int = 0):
    """
    Removes part of the internal walls between two corridors, forming cycles.
    percent: 0..100 (% of candidate walls). 0 — do not touch (the only path).
    """
    if percent <= 0:
        return
    R, C = len(grid), len(grid[0])
    candidates = []

    for r in range(1, R - 1):
        for c in range(1, C - 1):
            if grid[r][c] != WALL:
                continue
            # горизонтальна стіна між двома коридорами
            if (r % 2 == 1 and c % 2 == 0 and grid[r][c - 1] != WALL and grid[r][c + 1] != WALL):
                candidates.append((r, c))
            # вертикальна стіна між двома коридорами
            elif (r % 2 == 0 and c % 2 == 1 and grid[r - 1][c] != WALL and grid[r + 1][c] != WALL):
                candidates.append((r, c))

    if not candidates:
        return

    k = int(len(candidates) * max(0, min(100, percent)) / 100.0)
    if k <= 0:
        return

    for r, c in rng.sample(candidates, k=min(k, len(candidates))):
        grid[r][c] = ROAD

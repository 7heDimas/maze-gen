from collections import deque
from .cells import WALL, TRAP

def bfs_distances(grid, start):
    R, C = len(grid), len(grid[0])
    sr, sc = start
    if not (0 <= sr < R and 0 <= sc < C) or grid[sr][sc] == WALL:
        return {}
    dist = {(sr, sc): 0}
    dq = deque([(sr, sc)])
    while dq:
        r, c = dq.popleft()
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] != WALL and (nr, nc) not in dist:
                dist[(nr, nc)] = dist[(r, c)] + 1
                dq.append((nr, nc))
    return dist

def solve_path_any(grid, start, goal):
    """BFS-шлях по всіх клітинках, що != WALL (ігнорує типи)."""
    if not start or not goal:
        return None
    R, C = len(grid), len(grid[0])
    dq = deque([start])
    prev = {start: None}
    while dq:
        r, c = dq.popleft()
        if (r, c) == goal:
            path = []
            cur = goal
            while cur is not None:
                path.append(cur)
                cur = prev[cur]
            return list(reversed(path))
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] != WALL and (nr, nc) not in prev:
                prev[(nr, nc)] = (r, c)
                dq.append((nr, nc))
    return None

def solve_bfs_with_trap_limit(grid, start, goal, max_traps):
    """
    BFS in the state space (r,c,t), where t is the number of traps passed.
    Allows movement only if t <= max_traps. max_traps=0 → completely safe path.
    """
    if not start or not goal:
        return None
    R, C = len(grid), len(grid[0])
    dq = deque([(start[0], start[1], 0)])
    prev = {(start[0], start[1], 0): None}

    while dq:
        r, c, t = dq.popleft()
        if (r, c) == goal:
            path = []
            cur = (r, c, t)
            while cur is not None:
                path.append((cur[0], cur[1]))
                cur = prev[cur]
            return list(reversed(path))
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] != WALL:
                nt = t + (1 if grid[nr][nc] == TRAP else 0)
                if nt <= max_traps and (nr, nc, nt) not in prev:
                    prev[(nr, nc, nt)] = (r, c, t)
                    dq.append((nr, nc, nt))
    return None

def solve_bfs_with_traps(grid, start, goal):
    """Compatibility: path with a limit of 2 traps."""
    return solve_bfs_with_trap_limit(grid, start, goal, max_traps=2)

def adj_road(grid, p):
    """Returns the first adjacent cell that is not a wall (for the start/end of BFS)."""
    r, c = p
    for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != WALL:
            return (nr, nc)
    return None

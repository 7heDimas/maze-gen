import random
from .cells import WALL, ROAD, TRAP, TREASURE
from .validate import bfs_distances, solve_path_any, solve_bfs_with_traps, adj_road, solve_bfs_with_trap_limit


def _border_candidates(grid):
    R, C = len(grid), len(grid[0])
    items = []
    for c in range(1, C-1):
        if grid[1][c] != WALL: items.append(((0, c), (1, c)))
        if grid[R-2][c] != WALL: items.append(((R-1, c), (R-2, c)))
    for r in range(1, R-1):
        if grid[r][1] != WALL: items.append(((r, 0), (r, 1)))
        if grid[r][C-2] != WALL: items.append(((r, C-1), (r, C-2)))
    return items

def _farthest(candidates, dist_map):
    best, best_d = None, -1
    for p in candidates:
        d = dist_map.get(p, -1)
        if d > best_d:
            best, best_d = p, d
    return best

def pick_entrance_exit_diameter(grid, rng: random.Random):
    items = _border_candidates(grid)
    if len(items) < 2:
        R, C = len(grid), len(grid[0])
        a = (0, 1 if C > 1 else 0)
        b = (R-1, C-2 if C > 1 else 0)
        grid[a[0]][a[1]] = ROAD
        grid[b[0]][b[1]] = ROAD
        return a, b

    any_inner = items[0][1]
    d1 = bfs_distances(grid, any_inner)
    A = _farthest([inner for (_b, inner) in items], d1)
    if not A:
        a, b = items[0][0], items[1][0]
        grid[a[0]][a[1]] = ROAD; grid[b[0]][b[1]] = ROAD
        return a, b

    d2 = bfs_distances(grid, A)
    B = _farthest([inner for (_b, inner) in items], d2)
    if not B or B == A:
        a, b = items[0][0], items[1][0]
        grid[a[0]][a[1]] = ROAD; grid[b[0]][b[1]] = ROAD
        return a, b

    a_border = next(b for (b, inner) in items if inner == A)
    b_border = next(b for (b, inner) in items if inner == B)
    grid[a_border[0]][a_border[1]] = ROAD
    grid[b_border[0]][b_border[1]] = ROAD
    return a_border, b_border

def place_traps_safely(
    grid,
    entrance,
    exit_,
    rng,
    rows,
    cols,
    attempts: int = 50,
    require_safe_path: bool = True,
):
    """
    Places 0..5 traps (≈1 per 100 cells, but ≤5) so that:
      - if require_safe_path=True → there is AT LEAST ONE path E→X WITHOUT traps (0),
      - otherwise → there is a path with a limit of up to 2 traps.
    We place traps outside the base path; on the base path:
      - if require_safe_path=True → 0 traps,
      - otherwise → ≤2 traps.
    """
    R, C = len(grid), len(grid[0])
    max_traps_auto = min(5, (rows * cols) // 100)

    start = adj_road(grid, entrance)
    goal = adj_road(grid, exit_)
    base_path = solve_path_any(grid, start, goal) or []
    base_path_set = set(base_path)

    def all_roads():
        return [(r, c) for r in range(R) for c in range(C)
                if grid[r][c] == ROAD and (r, c) not in [entrance, exit_]]

    for k in range(max_traps_auto, -1, -1):
        for _ in range(attempts):
            # remove previous traps
            for r in range(R):
                for c in range(C):
                    if grid[r][c] == TRAP:
                        grid[r][c] = ROAD

            roads = all_roads()
            if not roads or k == 0:
                ok = solve_bfs_with_trap_limit(grid, start, goal, 0 if require_safe_path else 2)
                if ok: return []
                else: break

            off_path = [p for p in roads if p not in base_path_set]
            on_path  = [p for p in roads if p in base_path_set]

            traps, need = [], k
            # 1) maximum off the road
            if off_path:
                take = min(len(off_path), need)
                traps.extend(rng.sample(off_path, take)); need -= take
            # 2) on the baseline path — 0 or ≤2
            if need > 0 and on_path:
                take_on_cap = 0 if require_safe_path else 2
                take_on = min(len(on_path), min(need, take_on_cap))
                traps.extend(rng.sample(on_path, take_on)); need -= take_on
            if need > 0:
                continue

            for r, c in traps:
                grid[r][c] = TRAP

            ok = solve_bfs_with_trap_limit(grid, start, goal, 0 if require_safe_path else 2)
            if ok:
                return traps

    # alternative: without traps
    for r in range(R):
        for c in range(C):
            if grid[r][c] == TRAP:
                grid[r][c] = ROAD
    return []

def place_treasure(grid, entrance, exit_, rng, treasure_prob: float = 0.5):
    """Place ≤1 treasure ($) on ROAD (not on E/X/T), guaranteed to be reachable considering traps."""
    if rng.random() > treasure_prob:
        return None
    R, C = len(grid), len(grid[0])
    start = adj_road(grid, entrance)
    if not start: return None
    candidates = [(r,c) for r in range(R) for c in range(C)
                  if grid[r][c] == ROAD and (r,c) not in [entrance, exit_]]
    if not candidates: return None
    dist = bfs_distances(grid, start)
    candidates.sort(key=lambda p: dist.get(p, -1), reverse=True)
    for cell in candidates:
        if solve_bfs_with_traps(grid, start, cell):
            r, c = cell
            grid[r][c] = TREASURE
            return cell
    return None

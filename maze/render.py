from .cells import TREASURE

def print_maze(grid, entrance, exit_, path=None, treasure=None):
    R, C = len(grid), len(grid[0])
    er, ec = entrance
    xr, xc = exit_
    path_set = set(path) if path else set()

    for r in range(R):
        row = []
        for c in range(C):
            if (r, c) == (er, ec):
                row.append("E")
            elif (r, c) == (xr, xc):
                row.append("X")
            elif treasure and (r, c) == treasure:
                row.append(TREASURE)
            elif (r, c) in path_set:
                row.append("*")
            else:
                row.append(grid[r][c])
        print("".join(row))

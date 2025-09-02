import random
from maze.cli import parse_args
from maze.carve import carve_maze, add_loops
from maze.place import pick_entrance_exit_diameter, place_traps_safely, place_treasure
from maze.validate import adj_road, solve_bfs_with_trap_limit, solve_bfs_with_traps
from maze.render import print_maze

def main():
    args = parse_args()
    rng = random.Random(args.seed) if args.seed is not None else random.Random()

    # 1) Generation and, if desired, loops (multiple paths)
    grid = carve_maze(args.rows, args.cols, rng)
    add_loops(grid, rng, percent=args.loops)

    # 2) Inlet/outlet diameter
    entrance, exit_ = pick_entrance_exit_diameter(grid, rng)

    # 3) Traps with a guarantee that there is AT LEAST ONE safe route (0 traps on the route)
    place_traps_safely(
        grid, entrance, exit_, rng,
        rows=args.rows, cols=args.cols,
        attempts=50, require_safe_path=True
    )

    # 4) Treasure (optional, 0–1), guaranteed to be attainable considering traps
    treasure = place_treasure(grid, entrance, exit_, rng, treasure_prob=args.treasure_prob)

    # 5) First, we try the safe route; if that doesn't work, we try the limit 2 route.
    path = None
    if not args.no_path:
        start = adj_road(grid, entrance)
        goal = adj_road(grid, exit_)
        path = solve_bfs_with_trap_limit(grid, start, goal, 0)
        if path is None:
            path = solve_bfs_with_traps(grid, start, goal)

    print_maze(grid, entrance, exit_, path, treasure)

if __name__ == "__main__":
    main()

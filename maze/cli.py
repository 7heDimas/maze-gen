import argparse

def parse_args():
    p = argparse.ArgumentParser(description="Console maze generator")
    p.add_argument("--rows", type=int, default=21, help="Grid rows (>=3). Even will be reduced by 1.")
    p.add_argument("--cols", type=int, default=31, help="Grid cols (>=3). Even will be reduced by 1.")
    p.add_argument("--seed", type=int, default=None, help="Random seed (optional)")
    p.add_argument("--no-path", action="store_true", help="Do not draw the solution path")
    p.add_argument("--treasure-prob", type=float, default=0.5,
                   help="Probability to place treasure (0..1)")
    # Нове: створення циклів (декілька шляхів)
    p.add_argument("--loops", type=int, default=0,
                   help="Percent of interior walls to remove to add loops (0..100). 0 keeps a unique path.")
    return p.parse_args()

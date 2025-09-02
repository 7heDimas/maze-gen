# Console Maze Generator (Python)

A 2D maze generator for consoles with support for traps `T`, optional treasure `$`, 
at least one **safe** path from the entrance `E` to the exit `X`, 
and the ability to create multiple routes (`--loops`).

# Cell symbols

WALL = "#"
ROAD = "."
TRAP = "T"
TREASURE = "$"
ENTER = "E"
EXIT = "X"
CORRECT PATH = "*"

# Start

# from the root of the project

python main.py

# reproducible result
python main.py --rows 10 --cols 15 --seed 123

# several routes (remove ~15% of interior walls)
python main.py --rows 21 --cols 31 --loops 15

# CLI parameters

- `--rows N` — grid rows (≥3).
- `--cols M` — grid columns (≥3).
- `--seed S` — fix randomness (identical result).
- `--no-path` — do not draw the path `*`.  
- `--loops PERCENT` — remove % of internal walls (0 = one path, >0 = multiple).  
- `--treasure {auto,on,off}` — treasure: auto / always / never.  
- `--treasure-prob P` — treasure probability in `auto` mode (0..1).  
- `--max-traps K` — maximum traps (0..5, `-1` = auto by area).


# Examples
python main.py                      
python main.py --rows 21 --cols 31  
python main.py --loops 15 --seed 1  
python main.py --treasure off       

# Algorithms for creating a maze
Chamber grid (odd dimensions). 
Passable “chambers” on odd indices, walls between them. Makes it easier to break through walls.

Randomized DFS (Recursive Backtracker). 
Start from a random cell; as long as there are unvisited neighbors within 2 cells, randomly select one, 
break through the intermediate wall, and move; otherwise, roll back. Produces a perfect maze (connected, without cycles).

Adding cycles (--loops). 
Post-generation, we remove some of the internal walls between two corridors, creating alternative paths.

Entrance/exit selection (pseudo-diameter). 
Two BFS on the internal cells adjacent to the border: 
we find the two most distant ones and open the corresponding border positions as E and X.

# Algorithms for traversing a graph

BFS (standard).
Search for any minimum (by steps) path between two points through cells != WALL.
Used for the base path and distance maps.


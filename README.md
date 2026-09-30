# The Farmer Was Replaced Algorithms
`the-farmer-was-replaced-algorithms`

A community collection of automation strategies and reusable algorithms for [The Farmer Was Replaced](https://store.steampowered.com/app/2060160/The_Farmer_Was_Replaced/).

## About the Game

*The Farmer Was Replaced* is a programming and farming game where you write instructions for a drone to automate farm work, gather resources, and unlock new technology. Its programming language resembles Python, but runs inside the game and is not standard Python.

This repository explores ways to make those in-game tasks more efficient and interesting: grid traversal, resource-aware planting, sorting, maze solving, and multi-drone coordination.

## Strategies and Features

- **Grid movement:** Coordinate resets and reusable vertical routes for visiting rectangular regions.
- **Crop layouts:** Setups for mixed grass/tree and pumpkin/entity fields, single-entity fields, sunflowers, and cacti.
- **Resource-aware planting:** `plant_or_fallback()` checks item costs and plants fallback crops when the preferred crop is not affordable.
- **Sorting:** Bubble sort and gnome sort helpers, plus row/column matrix sorting with parallel line workers.
- **Snake navigation:** A target-seeking step routine that tries direct moves first and sidesteps when the preferred route is blocked.
- **Maze generation and solving:** Bush-grid maze creation, depth-first search, and parallel exploration with rotated search directions.
- **Multi-maze layouts:** A square grid of independent mazes, with drone workers distributed as evenly as possible.
- **Parallel farming:** Drone-based traversal and setup helpers for larger fields.

## Function Guide

### `main.py`

| Function | What it does |
| --- | --- |
| `infinite_loop()` | Repeats the cactus planting and matrix-sorting workflow. |
| `harvest_energy_loop()` | Repeatedly runs the parallel sunflower setup. |
| `parallel_loop(size)` | Repeatedly runs the parallel grass setup over the requested field size. |
| `maze_loop(size)` | Starts the repeated single-maze sequence. |
| `maze_loop_parallel(size)` | Starts one maze with multiple exploring drones. |
| `maze_grid_loop(size)` | Starts the square multi-maze workflow. |
| `set_world_size(width, height)` | Returns the requested dimensions; its defaults use the current world size. |

### `compose.py`

| Function | What it does |
| --- | --- |
| `reset_x_axis(x)`, `reset_y_axis(y)`, `reset_position(x, y)` | Move the current drone to the requested coordinates. |
| `vertical_route(size, exec, args, x0, y0)` | Visits each cell in a region by sweeping north through columns, calling `exec(x, y, args)` at each tile. |
| `vertical_route_parallel(exec, size)` | Splits a region into vertical strips, runs strips on worker drones, waits for them, and returns the caller to the origin. |
| `vertical_route_parallel_loop(size, exec, args, n_drones)` | Experimental repeating worker helper. It starts workers at successive x positions; verify coverage and overlap for the chosen field before relying on it. |
| `plant_or_fallback(entity, do_harvest)` | Checks the crop's resource cost, recursively selects a configured fallback when resources are short, tills when needed, and plants. `ITEM_MAP` defines the fallback choices. |
| `plant_power_grid(size)` | Waters and harvests tiles, planting sunflowers on even x/y coordinates. |
| `bubble_sort(size, move_dir, reset)` / `gnome_sort(size, move_dir, reset)` | Sort a line in place using measurements and swaps, optionally resetting between passes. |
| `sort_matrix(size, reset_x, reset_y)` | Sorts rows and then columns using bubble sort. |
| `sort_matrix_parallel(size)` | Sorts columns and rows using worker drones for individual lines, then restores the caller's starting position. |
| `snake_game()` | Reads the next target with `measure()` and moves toward it, trying alternate directions when the direct route is blocked. |
| `snake_loop()` | Clears the field, prepares soil, repeatedly runs the dinosaur-hat snake task, and resets after each run ends. |
| `dfs_maze(came_from, visited)` | Searches a maze depth-first, tracks visited coordinates, and backtracks from dead ends. |
| `maze_game(size, on_treasure)` / `maze_game_once(size)` | Builds a maze and searches it; the one-shot wrapper harvests the treasure when found. |
| `maze_game_sequence(size)` | Keeps solving and regrowing a single maze. |
| `dfs_maze_parallel(came_from, visited, dirs)` | DFS variant whose direction order can differ between workers. |
| `maze_game_sequence_parallel(size, n_drones)` | Builds one maze, starts explorer workers, and uses the calling drone as another explorer. |
| `multi_maze_game_parallel(size, n_drones)` | Clears the field, lays out a square grid of mazes that fits the world and drone budget, and divides workers among them. |
| `clear_land_parallel(size)` / `plant_cactus_parallel(size)` | Visit the field in parallel to harvest and prepare soil, or water, harvest, and plant cacti. |

### `setup.py`

| Function | What it does |
| --- | --- |
| `grass_50_tree_50_setup()` | Uses a checkerboard tree pattern on one half of the field and grass on the other, with bushes filling the tree pattern's gaps. |
| `entity_50_tree_50_setup(entity, powergrid_size)` | Combines an entity crop, a checkerboard tree/bush region, and optional sunflower power-grid corners. |
| `pumpkin_50_entity_50_setup(entity)` | Plants pumpkins in two diagonal quadrants and the selected entity in the other two. |
| `plant_trees_setup(size, powergrid_size)` | Plants a checkerboard tree/bush pattern, optionally reserving corner squares for sunflowers. |
| `single_entity_setup(entity, size, x0, y0, powergrid_size, fertilizer)` | Maintains a selected crop across a region, with optional fertilizer and sunflower power-grid corners; trees use the dedicated tree pattern. |
| `single_entity_parallel_setup(entity, size, powergrid_size, fertilizer)` | Parallel wrapper for the single-entity strategy; tree requests use the tree setup wrapper. Its worker loop uses the experimental parallel helper above. |
| `plant_cactus_and_sort_setup(size)` | Plants cacti with parallel strip traversal, then sorts the resulting matrix. |

Functions ending in `_exec` are per-tile callbacks used by the setup and traversal helpers; the underscored sorting and maze functions are implementation helpers rather than typical entry points.

## Project Files

- `main.py` selects and starts a workflow. The checked-in entry point currently runs `snake_loop()`.
- `compose.py` contains movement, planting, sorting, snake, maze, and parallel-worker helpers.
- `setup.py` contains reusable field setup strategies.
- `__builtins__.py` provides editor type hints for game-provided APIs. It is an approximation, not a standalone implementation of those APIs.
- `save.json` is local game save data, not source code. Review it carefully and normally keep it out of a public repository.

## Running in the Game

These scripts depend on game-provided values and functions such as `Entities`, `move()`, `spawn_drone()`, and `use_item()`. They are not intended to run with the normal Python interpreter.

1. Open the scripts through the game's code workspace or an external editor configured for the game's save files.
2. Select the workflow to run in the `if __name__ == "__main__":` section of `main.py`.
3. Execute the program in the game and observe the drone. Check the selected workflow against your world size, unlocked items, and available drone count.

Other workflows can be selected by replacing the active call in `main.py`, for example:

```python
snake_loop()
# maze_loop_parallel(8)
# maze_grid_loop(4)
# infinite_loop()
```

Only run one long-running workflow at a time. Several strategies intentionally loop forever or block while their worker drones solve or maintain a task.

## Contributing

Contributions that improve an existing strategy, add a focused algorithm, or document game-specific behavior are welcome.

- Keep changes focused and follow the existing helper conventions in `compose.py` and `setup.py`.
- Test behavior in the game. A normal Python syntax check cannot verify game APIs, tick behavior, drone scheduling, or maze traversal.
- Include the relevant conditions when reporting results, such as world size, unlocked technologies, and drone limits.
- Avoid committing `save.json` or other personal game state. Review staged files before publishing.
- There is no automated test suite in this folder yet; describe the in-game scenario used to verify a chang
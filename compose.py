# Composed actions in grid

ITEM_MAP = {
   Items.Wood: Entities.Bush,
   Items.Hay: Entities.Grass,
   Items.Carrot: Entities.Carrot,
   Items.Pumpkin: Entities.Pumpkin
}


def is_even(i):
	return i % 2 == 0

def reset_y_axis(y=0):
	ycurr = get_pos_y()
	while ycurr > y:
		move(South)
		ycurr = ycurr - 1
	while ycurr < y:
		move(North)
		ycurr = ycurr + 1

def reset_x_axis(x=0):
	xcurr = get_pos_x()
	while xcurr > x:
		move(West)
		xcurr = xcurr - 1
	while xcurr < x:
		move(East)
		xcurr = xcurr + 1

def reset_position(x0=0, y0=0):
	reset_x_axis(x0)
	reset_y_axis(y0)

def vertical_route(size, exec, args=None, x0=0, y0=0):
	# offset for the starting position (x0, y0)
	reset_position(x0, y0)
	for _ in range(size[0]):
		for _ in range(size[1]): 
			x, y = get_pos_x(), get_pos_y()
			#quick_print(x,y)
			exec(x, y, args)
			if size != get_world_size() and y == y0 + size[1] - 1:
				reset_y_axis(y0)
			else:
				move(North)
		if size != get_world_size() and x == x0 + size[0] - 1: # type: ignore
			reset_x_axis(x0)
		else:
			move(East)

def vertical_route_parallel_loop(size, exec, args=None, n_drones=None):
	# lets enforce that size must be a square
	if size[0] != size[1]:
		print("Size must be a square")
		return
	# divide the area size into squares closets to the max drones possbile
	if n_drones == None:
		n_drones = max_drones()
	square_size = n_drones
	# use vertical_route with the exec function for each square spawning drones
	print("Spawning:", square_size, "drone(s)")
	for i in range(square_size):
		x_start = i
		y_start = 0
		print("starting at:", x_start, y_start, "with size:", square_size)
		# spawn a drone for each square and assign it the vertical_route task
		# This is a placeholder for actual drone spawning logic
		# The drones will loop over their assigned squares independently
		def loop(size, exec, x_start, y_start, args=None):
			while True:
				vertical_route((size,size), exec, args, x_start, y_start)
		spawn_drone(loop, size[0], exec, x_start, y_start, args) # type: ignore

def vertical_route_parallel(exec, size=None):
	if size == None:
		w = get_world_size()
		size = (w, w)
	n_drones = min(max_drones(), size[0])
	strip_width = size[0] // n_drones
	drones = []
	x_start = 0
	for _ in range(n_drones - 1):  # last strip is handled by the calling drone itself
		d = spawn_drone(vertical_route, (strip_width, size[1]), exec, None, x_start, 0)
		if d == None:
			break
		drones.append(d)
		x_start += strip_width
	vertical_route((size[0] - x_start, size[1]), exec, None, x_start, 0)
	for d in drones:
		wait_for(d)  # only continue once the whole area is pure soil
	reset_position(0, 0)


def needs_soil(entity):
	return get_ground_type() == Grounds.Grassland and (entity != Entities.Grass or entity != Entities.Bush or entity != Entities.Tree)


def plant_or_fallback(entity, do_harvest=True):
	cost = get_cost(entity)
	#quick_print("len:", len(cost), cost)
	if len(cost) == 0: # type: ignore
		if do_harvest and can_harvest():
			harvest()
		plant(entity)
		return True
	for key in cost: # type: ignore
		if num_items(key) < cost[key]: # type: ignore
			plant_or_fallback(ITEM_MAP[key], do_harvest)

	if needs_soil(entity):
		till()
	plant(entity)
	return True

def plant_power_grid(size=(12, 12)):
	def exec(x, y, args):
		if get_water() < 1:
			use_item(Items.Water)
		if can_harvest():
			harvest()
		if is_even(x) and is_even(y):
			plant(Entities.Sunflower)
	vertical_route(size, exec)


def bubble_sort(size: int, move_dir: Direction=North, reset: Callable|None=None):
	if size <=1:
		return
	for _ in range(size):
		swapped = False
		for i in range(size-1):
			curr = measure()
			nxt = measure(move_dir)
			if i < size-1 and curr > nxt: # type: ignore
				swap(move_dir)
				swapped = True
			move(move_dir)
		if reset == None:
			move(move_dir)
		else:
			reset()
		if not swapped:
			break

def gnome_sort(size: int, move_dir: Direction=North, reset: Callable|None=None):
	if size <= 1:
		return
	opposite = {North: South, South: North, East: West, West: East}
	backward = opposite[move_dir]
	position_index = 1
	move(move_dir)
	while position_index < size:
		current = measure()
		previous = measure(backward)
		if previous <= current: # type: ignore
			position_index += 1
			if position_index < size:
				move(move_dir)
		else:
			swap(backward)
			if position_index > 1:
				move(backward)
				position_index -= 1
	if reset == None:
		move(move_dir)
	else:
		reset()

def sort_matrix(size: int, reset_x: Callable|None=None, reset_y: Callable|None=None):
	if size <= 1:
		return

	for row in range(size):
		bubble_sort(size, North, reset_y)
		if row < size - 1:
			move(East)
	if reset_x == None:
		move(East)
	else:
		reset_x()
	for col in range(size):
		bubble_sort(size, East, reset_x)
		if col < size - 1:
			move(North)
	if reset_y == None:
		move(North)
	else:
		reset_y()

def _sort_line(x, y, size, move_dir):
	reset_position(x, y)
	def reset():
		reset_position(x, y)
	bubble_sort(size, move_dir, reset)

def _sort_lines(size, move_dir, starts):
	drones = []
	i = 0
	while i < len(starts):
		if num_drones() < max_drones():
			x, y = starts[i]
			d = spawn_drone(_sort_line, x, y, size, move_dir)
			if d != None:
				drones.append(d)
				i += 1
				continue
		freed = False
		while not freed:  # pool is full, wait for the first drone to finish and take its slot
			for d in drones:
				if has_finished(d):
					wait_for(d)
					drones.remove(d)
					freed = True
					break
	for d in drones:
		wait_for(d)  # next phase needs every line from this phase fully sorted first

def sort_matrix_parallel(size: int):
	if size <= 1:
		return
	x0, y0 = get_pos_x(), get_pos_y()

	col_starts = []
	for i in range(size):
		col_starts.append((x0 + i, y0))
	_sort_lines(size, North, col_starts)

	row_starts = []
	for i in range(size):
		row_starts.append((x0, y0 + i))
	_sort_lines(size, East, row_starts)

	reset_position(x0, y0)

def _step_towards(tx, ty):
	dx = tx - get_pos_x()
	dy = ty - get_pos_y()
	preferred = []
	if dx > 0:
		preferred.append(East)
	elif dx < 0:
		preferred.append(West)
	if dy > 0:
		preferred.append(North)
	elif dy < 0:
		preferred.append(South)
	for d in preferred:
		if move(d):
			return True
	for d in (North, South, East, West):  # sidestep our own tail instead of giving up
		if d not in preferred and move(d):
			return True
	return False

def snake_game():
	t = measure()
	if t == None:
		return
	xnext, ynext = t  # type: ignore
	while (get_pos_x(), get_pos_y()) != (xnext, ynext):
		if not _step_towards(xnext, ynext):
			return False  # surrounded on all sides, truly stuck
	return True

def clear_land_exec(x, y, args):
	if can_harvest():
		harvest()
	if get_ground_type() != Grounds.Soil:
		till()

def clear_land_parallel(size=None):
	vertical_route_parallel(clear_land_exec, size)

def plant_cactus_exec(x, y, args):
	if get_water() < 1:
		use_item(Items.Water)
	if can_harvest():
		harvest()
	if get_ground_type() == Grounds.Grassland:
		till()
	plant_or_fallback(Entities.Cactus)

def plant_cactus_parallel(size=None):
	vertical_route_parallel(plant_cactus_exec, size)

def snake_loop():
	clear()
	clear_land_parallel()
	while True:
		change_hat(Hats.Dinosaur_Hat)
		while snake_game():
			pass
		change_hat(Hats.Wizard_Hat)
		reset_position(0,0)

def random_position(size=None):
	if size == None:
		w = get_world_size()
		size = (w, w)
	x = random() * size[0] // 1
	y = random() * size[1] // 1
	return (x, y)

# def snake_worker():
# 	x, y = random_position()
# 	reset_position(x, y)
# 	change_hat(Hats.Dinosaur_Hat)
# 	while snake_game():
# 		pass
# 	change_hat(Hats.Wizard_Hat)
# 	reset_position(0, 0)

# def snake_loop_parallel():
# 	clear_land_parallel()
# 	while True:
# 		drones = []
# 		for _ in range(max_drones() - 1):  # leave one slot for the calling drone itself
# 			d = spawn_drone(snake_worker)
# 			if d == None:
# 				break
# 			drones.append(d)
# 		snake_worker()
# 		for d in drones:
# 			wait_for(d)  # start the next round only once every drone is done

def dfs_maze(came_from=None, visited=None):
	_OPPOSITE = {North: South, South: North, East: West, West: East}
	if visited == None:
		visited = []
	position = (get_pos_x(), get_pos_y())
	if position in visited:
		return False
	visited.append(position)
	if get_entity_type() == Entities.Treasure:
		return True
	for d in (North, South, East, West):
		if came_from != None and d == _OPPOSITE[came_from]:
			continue  # don't immediately backtrack to the parent cell
		if can_move(d) and move(d):
			if dfs_maze(d, visited):
				return True
			move(_OPPOSITE[d])  # dead end, back up one cell
	return False


def maze_game(size=get_world_size(), on_treasure: Callable|None=None):
	def build_maze():
		reset_position()
		def set_bush_grid(x,y,args):
			plant_or_fallback(Entities.Bush)
		vertical_route((size, size), set_bush_grid)
		n = size * 2**(num_unlocked(Unlocks.Mazes) - 1)
		use_item(Items.Weird_Substance, n)
		
	#reset
	if get_entity_type() == Entities.Hedge and get_entity_type() != Entities.Treasure:
		harvest()
	build_maze()

	if get_entity_type() == Entities.Treasure:
		if on_treasure == None:
			return harvest()
		return on_treasure()
	elif get_entity_type() != Entities.Hedge:
		return False	
	res = dfs_maze()
	if res and on_treasure:
		on_treasure()
	return res



def maze_game_once(size=get_world_size()):
	def on_treasure():
		harvest()
	return maze_game(size, on_treasure)
 
def maze_game_sequence(size=get_world_size()):
	def on_treasure():
		n = size * 2**(num_unlocked(Unlocks.Mazes) - 1)
		use_item(Items.Weird_Substance, n)
	maze_game(size, on_treasure)
	while True:
		if dfs_maze():
			on_treasure()

def _rotate_dirs(offset=0):
	dirs = (North, South, East, West)
	offset = offset % len(dirs) # type: ignore
	return dirs[offset:] + dirs[:offset]  # gives each drone a different first branch to explore

def dfs_maze_parallel(came_from=None, visited=None, dirs=(North, South, East, West)):
	_OPPOSITE = {North: South, South: North, East: West, West: East}
	if visited == None:
		visited = []
	position = (get_pos_x(), get_pos_y())
	if position in visited:
		return False
	visited.append(position)
	if get_entity_type() == Entities.Treasure:
		return True
	for d in dirs:
		if came_from != None and d == _OPPOSITE[came_from]:
			continue  # don't immediately backtrack to the parent cell
		if can_move(d) and move(d):
			if dfs_maze_parallel(d, visited, dirs):
				return True
			move(_OPPOSITE[d])  # dead end, back up one cell
	return False

def maze_worker(size, offset=0):
	dirs = _rotate_dirs(offset)
	while True:
		if dfs_maze_parallel(None, None, dirs):
			#harvest()
			n = size * 2**(num_unlocked(Unlocks.Mazes) - 1)
			use_item(Items.Weird_Substance, n)  # regrow in place, no other drone is told directly

def maze_game_sequence_parallel(size=get_world_size(), n_drones= max_drones()):
	def build_maze():
		reset_position()
		def set_bush_grid(x, y, args):
			plant_or_fallback(Entities.Bush)
		vertical_route_parallel(set_bush_grid, (size, size))
		n = size * 2**(num_unlocked(Unlocks.Mazes) - 1)
		use_item(Items.Weird_Substance, n)
	#reset
	if get_entity_type() == Entities.Hedge and get_entity_type() != Entities.Treasure:
		harvest()
	build_maze()
	for offset in range(1, n_drones):
		if num_drones() >= n_drones:
			break
		spawn_drone(maze_worker, size, offset) #type: ignore
	maze_worker(size, 0)  # caller joins the pool as well, so this never returns

def _build_maze_at(size, x_start, y_start, n_workers):
	reset_position(x_start, y_start)
	def set_bush_grid(x, y, args):
		plant_or_fallback(Entities.Bush)
	vertical_route((size, size), set_bush_grid, None, x_start, y_start)
	n = size * 2**(num_unlocked(Unlocks.Mazes) - 1)
	use_item(Items.Weird_Substance, n)
	for offset in range(1, n_workers):
		spawn_drone(maze_worker, size, offset) # type: ignore
	maze_worker(size, 0)  # this maze's own solver, so this never returns

def multi_maze_game_parallel(size=8, n_drones=None):
	clear()
	if n_drones == None:
		n_drones = max_drones()
	world_width = get_world_size()
	mazes_per_axis = world_width // size
	drone_limited_side = 1
	while (drone_limited_side + 1) ** 2 <= n_drones:
		drone_limited_side += 1
	num_mazes = min(max(mazes_per_axis, 1), drone_limited_side)
	total_mazes = num_mazes ** 2
	workers_per_maze = n_drones // total_mazes
	extra = n_drones % total_mazes
	drones = []
	for i in range(1, total_mazes):
		n_workers = workers_per_maze
		if i < extra:
			n_workers += 1
		x_start = (i % num_mazes) * size
		y_start = (i // num_mazes) * size
		d = spawn_drone(_build_maze_at, size, x_start, y_start, n_workers)
		if d != None:
			drones.append(d)
	n_workers = workers_per_maze
	if extra > 0:
		n_workers += 1
	_build_maze_at(size, 0, 0, n_workers)  # this drone's own maze, so this never returns

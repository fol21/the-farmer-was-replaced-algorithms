
from compose import plant_cactus_parallel, plant_or_fallback, sort_matrix, sort_matrix_parallel, vertical_route, vertical_route_parallel_loop, reset_x_axis, reset_y_axis, is_even

def grass_50_tree_50_setup():
	size = get_world_size(), get_world_size()
	def exec(x, y, args):
		if get_water() < 1:
			use_item(Items.Water)
		if can_harvest():
			harvest()
		if x < size[0] // 2:
			if is_even(x) and is_even(y):
				plant(Entities.Tree)
			elif (not is_even(x)) and not is_even(y):
				plant(Entities.Tree)
			else:
				plant(Entities.Bush)
		else:
			plant(Entities.Grass)
	vertical_route(size, exec)

def entity_50_tree_50_setup(entity, powergrid_size=-1):
	size = get_world_size(), get_world_size()
	def exec(x, y, args):
		if get_water() < 1:
			use_item(Items.Water)
		if can_harvest():
			harvest()
		if (x < powergrid_size and y < powergrid_size) or (x >= size[0] - powergrid_size and y >= size[1] - powergrid_size):
			plant_or_fallback(Entities.Sunflower)
		elif x < size[0] // 2:
			if is_even(x) and is_even(y):
				plant_or_fallback(Entities.Tree)
			elif (not is_even(x)) and not is_even(y):
				plant_or_fallback(Entities.Tree)
			else:
				plant_or_fallback(Entities.Bush)
		else:
			if entity == Entities.Pumpkin or entity == Entities.Carrot:
				if get_ground_type() == Grounds.Grassland:
					till()
			plant_or_fallback(entity)
	vertical_route(size, exec)

def pumpkin_50_entity_50_setup(entity):
	size = get_world_size(), get_world_size()
	def exec(x, y, args):
		if get_water() < 1:
			use_item(Items.Water)
		if can_harvest():
			harvest()
		if (x < size[0] // 2 and y < size[1] // 2) or (x >= size[0] // 2 and y >= size[1] // 2):
			if get_ground_type() == Grounds.Grassland:
				till()
			plant(Entities.Pumpkin)
		else:
			if entity == Entities.Pumpkin or entity == Entities.Carrot:
				if get_ground_type() == Grounds.Grassland:
					till()
			plant(entity)
	vertical_route(size, exec)

def plant_trees_exec(x, y, args):
	if get_water() < 1:
		use_item(Items.Water)
	if can_harvest():
		harvest()
	if (x < args["powergrid_size"] and y < args["powergrid_size"]) or (x >= args["size"][0] - args["powergrid_size"] and y >= args["size"][1] - args["powergrid_size"]	):
		plant_or_fallback(Entities.Sunflower)
	elif is_even(x) and is_even(y):
		plant_or_fallback(Entities.Tree)
	elif (not is_even(x)) and not is_even(y):
		plant_or_fallback(Entities.Tree)
	else:
		plant_or_fallback(Entities.Bush)

def plant_trees_setup(size=(get_world_size(), get_world_size()), powergrid_size=-1):
	vertical_route(size, plant_trees_exec, {"size": size, "powergrid_size": powergrid_size})

def plant_trees_parallel_setup(size=(get_world_size(), get_world_size()), powergrid_size=-1):
	vertical_route_parallel_loop(size,
							plant_trees_exec, 
							{"size": size,"powergrid_size": powergrid_size}
	)

def single_entity_exec(x, y, args):
	if args and args["fertilizer"]:
		use_item(Items.Fertilizer)
	if not (args and args["fertilizer"]) and get_water() < 1:
		use_item(Items.Water)
	if can_harvest():
		harvest()
	if (x < args["powergrid_size"] and y < args["powergrid_size"]) or (x >= args["size"][0] - args["powergrid_size"] and y >= args["size"][1] - args["powergrid_size"]):
		if get_ground_type() == Grounds.Grassland:
			till()
		plant_or_fallback(Entities.Sunflower)
	else:
		if (args and args["entity"] == Entities.Carrot or args["entity"] == Entities.Pumpkin) and get_ground_type() == Grounds.Grassland:
			till()
		plant_or_fallback(args["entity"])

def single_entity_setup(entity, size=(get_world_size(), get_world_size()), x0=0, y0=0, powergrid_size=-1, fertilizer=False):
	if entity == Entities.Tree:
		plant_trees_setup(size, powergrid_size)
		return
	vertical_route(size, single_entity_exec,
		{"size": size, "powergrid_size": powergrid_size, "fertilizer": fertilizer, "entity": entity},
		x0, y0
	)

def single_entity_parallel_setup(entity, size=(get_world_size(), get_world_size()), powergrid_size=-1, fertilizer=False):
	if entity == Entities.Tree:
		plant_trees_parallel_setup(size, powergrid_size)
		return
	vertical_route_parallel_loop(size,
							single_entity_exec, 
							{"size": size,"powergrid_size": powergrid_size, "fertilizer": fertilizer, "entity": entity,}
	)

def plant_cactus_and_sort_setup(size=(get_world_size(), get_world_size())):
	plant_cactus_parallel(size)
	sort_matrix_parallel(size[0])

		

		
		
	
	
	
	
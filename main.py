
from setup import entity_50_tree_50_setup, grass_50_tree_50_setup, plant_cactus_and_sort_setup, pumpkin_50_entity_50_setup, single_entity_parallel_setup, single_entity_setup
from compose import maze_game_once, maze_game_sequence, maze_game_sequence_parallel, multi_maze_game_parallel, reset_position, snake_loop

def set_world_size(width=get_world_size(), height=get_world_size()):
	return (width, height)
 


# Configurations
size = set_world_size() 
print("World Size", size)
reset_position(0,0)
change_hat(Hats.Wizard_Hat)


def infinite_loop():
	while True:
		#single_entity_setup(Entities.Bush, size, 0, 9)
		#grass_50_tree_50_setup()
		#pumpkin_50_entity_50_setup(Entities.Carrot)
		#entity_50_tree_50_setup(Entities.Grass, 4)
		plant_cactus_and_sort_setup(size)


def harvest_energy_loop():
	while True:
		single_entity_parallel_setup(Entities.Sunflower, size, -1)

def harvest_pumpkin_loop():
	while True:
		single_entity_parallel_setup(Entities.Pumpkin, size, -1)

def harvest_carrot_loop():
	while True:
		single_entity_parallel_setup(Entities.Carrot, size, -1)

def parallel_loop(size):
	single_entity_parallel_setup(Entities.Grass, size, -1)

def maze_loop(size):
	# while True:
	# 	maze_game_once(size)
	maze_game_sequence(size)

def maze_loop_parallel(size):
	maze_game_sequence_parallel(size)
	#multi_maze_game_parallel(size)

def maze_grid_loop(size):
	multi_maze_game_parallel(size)

# Loop
if __name__ == "__main__":
	#infinite_loop()
	#harvest_energy_loop()
	#harvest_pumpkin_loop()
	harvest_carrot_loop()
	#snake_loop()
	#maze_loop_parallel(8)
	#maze_grid_loop(4)
	#parallel_loop(size)
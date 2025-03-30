from bfs import *
from dfs import *
from a_star import *

loaded_board, rows, cols = load_board()
board_dict = {loaded_board : "0"}

print("Rozpoczynam przeszukiwanie BFS")
bfs("LRUD",board_dict, time.time())
print("-----------------------------------------------------------------")
print("Rozpoczynam przeszukiwanie DFS")
dfs("LRUD", board_dict, time.time())
print("-----------------------------------------------------------------")
print("Rozpoczynam przeszukiwanie A* Hamming")
a_star(hamming_distance, board_dict, time.time())
print("-----------------------------------------------------------------")
print("Rozpoczynam przeszukiwanie A* Manhattan")
a_star(manhattan_distance, board_dict, time.time())
from bfs import *
from dfs import *

loaded_board, rows, cols = load_board()
board_dict = {loaded_board : "0"}

print("Rozpoczynam przeszukiwanie BFS")
bfs("LRUD",board_dict, rows, cols, time.time())
print("-----------------------------------------------------------------")
print("Rozpoczynam przeszukiwanie DFS")
dfs("LRUD", board_dict, rows, cols, time.time())
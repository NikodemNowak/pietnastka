
from bfs import *

loaded_board, rows, cols = load_board()
board_dict = {loaded_board : "0"}

bfs("LRUD",board_dict, rows, cols, time.time())

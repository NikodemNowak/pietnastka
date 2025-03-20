from board import *
from bfs import *

loaded_board, rows, cols = load_board()

bfs("LRUD",loaded_board, rows, cols)

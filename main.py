from board import *
from bfs import *

loaded_board, rows, cols = load_board()
# print(loaded_board)
# print(generate_final_board())
# print(check_board(loaded_board))
bfs("LRUD",loaded_board, rows, cols)

# print(hash_board(loaded_board))
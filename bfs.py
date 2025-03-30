from temporary_algorithm import *
from board import *

def bfs(order, board_dict, start_time):
    visited_bfs = set()
    all_layer_states_bfs = Queue()
    processed_bfs = 0

    is_in_set(hash(next(iter(board_dict.keys()))), visited_bfs)

    temporary_alghorithm(order, board_dict, all_layer_states_bfs, visited_bfs, 0)

    while not all_layer_states_bfs.empty():
        b = all_layer_states_bfs.get()
        processed_bfs = processed_bfs + 1

        if check_board(next(iter(b.keys()))) == 0:
            return True, str(next(iter(b.keys()))), str(list(b.values())[0][1:]), visited_bfs, processed_bfs, start_time

        temporary_alghorithm(order, b, all_layer_states_bfs, visited_bfs, 0)

    return False, '', '-1', visited_bfs, processed_bfs, start_time



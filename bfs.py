import time
from temporary_algorithm import *
from board import *



def bfs(order, board_dict, rows, cols, start_time):
    visited_bfs = set()
    all_layer_states_bfs = Queue()
    processed_bfs = 0

    is_in_set(hash(next(iter(board_dict.keys()))), visited_bfs)

    temporary_alghorithm(order, board_dict, rows, cols, all_layer_states_bfs, visited_bfs, 0)

    while not all_layer_states_bfs.empty():
        b = all_layer_states_bfs.get()
        processed_bfs = processed_bfs + 1

        if check_board(next(iter(b.keys()))) == 0:
            print("Znaleziono rozwiazanie: " + str(next(iter(b.keys()))) + " z krokiem: " + str(list(b.values())[0][1:]))
            print("Ilosc krokow: " + str(len(list(b.values())[0]) - 1))
            print("Ilosc odwiedzonych stanow: " + str(len(visited_bfs)))
            print("Ilosc przetworzonych stanow: " + str(processed_bfs))
            print("Czas wykonania: " + str(time.time() - start_time) + " sekund")
            break

        temporary_alghorithm(order, b, rows, cols, all_layer_states_bfs, visited_bfs, 0)




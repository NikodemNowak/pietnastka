from temporary_algorithm import temporary_algorithm
from board import add_to_set_dfs, check_board
from collections import deque, ChainMap

def dfs(order, board_dict):
    stack = deque()  #Stos LIFO
    visited_dfs = ChainMap()
    proccessed_dfs = 0
    max_depth = 20
    max_processed_depth = 0
    add_to_set_dfs(board_dict, visited_dfs)  # Dodaje do zbioru odwiedzonych
    stack.append(board_dict)  # Dodaje na koniec kolejki

    while stack:

        b = stack.pop()  # Usuwa ostatni element z kolejki, czyli ten ostatni dodany

        current_depth = len(list(b.values())[0]) - 1
        if current_depth > max_processed_depth:
            max_processed_depth = current_depth

        proccessed_dfs = proccessed_dfs + 1

        # Sprawdza czy dany stan jest poszukiwanym
        if check_board(next(iter(b.keys()))) == 0:
            return True, str(next(iter(b.keys()))), str(
                list(b.values())[0][1:]), visited_dfs, proccessed_dfs, max_processed_depth

        # Sprawdza czy nie przekroczono głębokości
        all_steps = list(b.values())[0]
        if len(all_steps) - 1 >= max_depth:
            max_processed_depth = max_depth
            continue

        temporary_algorithm(order, b, stack, visited_dfs, 0, True)

    return False, '', '-1', visited_dfs, proccessed_dfs, max_processed_depth

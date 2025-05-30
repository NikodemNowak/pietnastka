from board import *
from queue import Queue, PriorityQueue


def temporary_algorithm(order_or_heuristic, board_dict, algorithm_structure, algorithm_visited, additional_counter, is_dfs):

    x = where_zero(next(iter(board_dict.keys())))
    board_moves = []

    # Pobranie pierwszej wartości słownika
    all_steps = list(board_dict.values())[0]

    # Pobranie ostatniego znaku
    last_step = all_steps[-1]

    # Które ruchy są możliwe
    check_possible_move(x, last_step, board_moves)

    if isinstance(order_or_heuristic, str):
        # Posortuje możliwe ruchy zgodnie z order
        board_moves = sorted(board_moves, key=lambda z: order_or_heuristic.index(z))

    for move in board_moves:
        if move == 'L':
            new_board, new_step = move_left(next(iter(board_dict.keys())))
        elif move == 'U':
            new_board, new_step = move_up(next(iter(board_dict.keys())))
        elif move == 'R':
            new_board, new_step = move_right(next(iter(board_dict.keys())))
        elif move == 'D':
            new_board, new_step = move_down(next(iter(board_dict.keys())))

        new_board_dict = {new_board: ''.join(list(board_dict.values())) + str(new_step)}

        if is_dfs:
            if add_to_set_dfs( new_board_dict, algorithm_visited):
                algorithm_structure.append(new_board_dict)
        else:
            if is_in_set(hash_board(next(iter(new_board_dict.keys()))), algorithm_visited):
                if isinstance(algorithm_structure, PriorityQueue):  # Kolejka z priorytetem (A*)
                    priority = order_or_heuristic(next(iter(new_board_dict.keys()))) + len(list(new_board_dict.values())[0]) - 1
                    algorithm_structure.put((priority, additional_counter[0], new_board_dict))
                    additional_counter[0] += 1
                elif isinstance(algorithm_structure, Queue):  # Kolejka (BFS)
                    algorithm_structure.put(new_board_dict)

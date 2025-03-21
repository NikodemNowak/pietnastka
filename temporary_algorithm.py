from board import *
from collections import deque
from queue import Queue

def temporary_alghorithm(order, board_dict, rows, cols, algorithm_structure, algorithm_visited):
    x = where_zero(next(iter(board_dict.keys())))
    board_moves = []
    all_steps = list(board_dict.values())[0]  # Pobranie pierwszej wartości słownika
    last_step = all_steps[-1]  # Pobranie ostatniego znaku

    # Które ruchy są możliwe
    check_possible_move(x, last_step, cols, rows, board_moves)

    # Posortuje możliwe ruchy zgodnie z order
    board_moves = sorted(board_moves, key=lambda z: order.index(z))


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

        if is_in_set(hash_board(next(iter(new_board_dict.keys()))), algorithm_visited):
            if isinstance(algorithm_structure, Queue):  # Kolejka (BFS)
                algorithm_structure.put(new_board_dict)
            elif isinstance(algorithm_structure, deque):  # Stos (DFS)
                algorithm_structure.append(new_board_dict)

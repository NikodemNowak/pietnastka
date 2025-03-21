from queue import Queue
import time

from board import *

visited_bfs = set()
all_layer_states_bfs = Queue()

def bfs(order, board_dict, rows, cols, start_time):

    is_in_set(hash(next(iter(board_dict.keys()))), visited_bfs)

    temporary_bfs(order, board_dict, rows, cols)

    while not all_layer_states_bfs.empty():
        b = all_layer_states_bfs.get()

        if check_board(next(iter(b.keys()))) == 0:
            print("Znaleziono rozwiazanie: " + str(next(iter(b.keys()))) + " z krokiem: " + str(list(b.values())[0][1:]))
            print("Ilosc krokow: " + str(len(list(b.values())[0]) - 1))
            print("Ilosc odwiedzonych stanow: " + str(len(visited_bfs)))
            print("Czas wykonania: " + str(time.time() - start_time) + " sekund")
            break

        temporary_bfs(order, b, rows, cols)

    #print("dlugosc visited: " + str(len(visited)))
    #print("dlugosc all_layer_states: " + str(all_layer_states.qsize()))

def temporary_bfs(order, board_dict, rows, cols):
    x = where_zero(next(iter(board_dict.keys())))
    board_moves = []
    all_steps = list(board_dict.values())[0]  # Pobranie pierwszej wartości słownika
    last_step = all_steps[-2:] if all_steps[-1] == '2' else all_steps[-1] # Pobranie 2 lub 1 znaków

    # Które ruchy są możliwe
    check_possible_move(x, last_step, cols, rows, board_moves)

    # Posortuje możliwe ruchy zgodnie z order
    board_moves = sorted(board_moves, key=lambda z: order.index(z))


    for move in board_moves:
        if move == 'L':
            new_board, new_step = move_left(next(iter(board_dict.keys())))
            new_board_dict = {new_board: ''.join(list(board_dict.values())) + str(new_step)}
        elif move == 'U':
            new_board, new_step = move_up(next(iter(board_dict.keys())))
            new_board_dict = {new_board: ''.join(list(board_dict.values())) + str(new_step)}
        elif move == 'R':
            new_board, new_step = move_right(next(iter(board_dict.keys())))
            new_board_dict = {new_board: ''.join(list(board_dict.values())) + str(new_step)}
        elif move == 'D':
            new_board, new_step = move_down(next(iter(board_dict.keys())))
            new_board_dict = {new_board: ''.join(list(board_dict.values())) + str(new_step)}


        if is_in_set(hash_board(next(iter(new_board_dict.keys()))), visited_bfs):
            all_layer_states_bfs.put(new_board_dict)
            #print("New board added to queue: " + str(next(iter(new_board_dict.keys()))) + " with steps: " + str(list(new_board_dict.values())[0]))

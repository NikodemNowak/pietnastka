from queue import Queue
import time

from board import *

visited = set()
all_layer_states = Queue()

def bfs(order, board_dict, rows, cols, start_time):

    is_in_set(hash(next(iter(board_dict.keys()))))

    temporary_bfs(order, board_dict, rows, cols)

    while not all_layer_states.empty():
        b = all_layer_states.get()

        if check_board(next(iter(b.keys()))) == 0:
            print("Znaleziono rozwiazanie: " + str(next(iter(b.keys()))) + " z krokiem: " + str(list(b.values())[0][1:]))
            print("Ilosc krokow: " + str(len(list(b.values())[0]) - 1))
            print("Ilosc odwiedzonych stanow: " + str(len(visited)))
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


        if is_in_set(hash_board(next(iter(new_board_dict.keys())))):
            all_layer_states.put(new_board_dict)
            #print("New board added to queue: " + str(next(iter(new_board_dict.keys()))) + " with steps: " + str(list(new_board_dict.values())[0]))

def check_possible_move(x, last_step, width, height, layer_moves):
    if left_ok(x, last_step, width):
        layer_moves.append('L')

    if up_ok(x, last_step, width):
        layer_moves.append('U')

    if right_ok(x, last_step, width):
        layer_moves.append('R')

    if down_ok(x, last_step, width, height):
        layer_moves.append('D')
    return layer_moves

def left_ok(x, last_step, width):
    if last_step == 'R':
        return False

    if x % width == 0:
        return False

    return True

def up_ok(x, last_step, width):
    if last_step == 'D':
        return False

    if x < width:
        return False

    return True

def right_ok(x, last_step, width):
    if last_step == 'L':
        return False

    if x % width == width - 1:
        return False

    return True

def down_ok(x, last_step, width, height):
    if last_step == 'U':
        return False

    if x >= (width - 1) * height:
        return False

    return True

def is_in_set(hash_param):
    if hash_param not in visited:
        visited.add(hash_param)
        return True
    else:
        return False

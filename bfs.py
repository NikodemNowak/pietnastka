from queue import Queue

from board import *

visited = set()
all_layer_states = Queue()

def bfs(order, board, rows, cols):

    is_in_set(hash(board))

    temporary_bfs(order, board, rows, cols)

    while not all_layer_states.empty():
        b = all_layer_states.get()
        temporary_bfs(order, b, rows, cols)

    print("dlugosc visited: " + str(len(visited)))

def temporary_bfs(order, board, rows, cols):
    x = where_zero(board)
    board_moves = []
    last_step = -1

    # Które ruchy są możliwe
    check_possible_move(x, last_step, cols, rows, board_moves)

    # Posortuje możliwe ruchy zgodnie z order
    board_moves = sorted(board_moves, key=lambda z: order.index(z))

    # for letter in order:
    #     if letter in layer_moves:
    #         print(letter)

    for move in board_moves:
        if move == 'L':
            new_board = move_left(board)
        elif move == 'U':
            new_board = move_up(board)
        elif move == 'R':
            new_board = move_right(board)
        elif move == 'D':
            new_board = move_down(board)

        # print(new_board)
        # print(hash_board(new_board))
        # print(check_board(new_board))
        # print(where_zero(new_board))

        if is_in_set(hash_board(new_board)):
            all_layer_states.put(new_board)
            print("New board added to queue: " + str(new_board))

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
    if last_step == 3:
        return False

    if x % width == 0:
        return False

    return True

def up_ok(x, last_step, width):
    if last_step == 6:
        return False

    if x < width:
        return False

    return True

def right_ok(x, last_step, width):
    if last_step == 9:
        return False

    if x % width == width - 1:
        return False

    return True

def down_ok(x, last_step, width, height):
    if last_step == 12:
        return False

    if x >= (width - 1) * height:
        return False

    return True

def is_in_set(hash_param):
    if hash_param not in visited:
        visited.add(hash_param)
        # print(str(hash_param) + " added to set")
        return True
    else:
        # print(str(hash_param) + " already in set")
        return False

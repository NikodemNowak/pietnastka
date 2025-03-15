from board import *

visited = set()

def bfs(order, board):

    y, x = where_zero(board)
    layer_moves = []
    last_step = -1

    # Które ruchy są możliwe
    check_possible_move(x, y , last_step, len(board[0]), len(board), layer_moves)

    # Posortuje możliwe ruchy zgodnie z order
    layer_moves = sorted(layer_moves, key=lambda z: order.index(z))
    print(layer_moves)




def check_possible_move(x, y, last_step, width, height, layer_moves):
    if left_ok(x, last_step):
        layer_moves.append('L')

    if up_ok(y, last_step):
        layer_moves.append('U')

    if right_ok(x, last_step, width):
        layer_moves.append('R')

    if down_ok(y, last_step, height):
        layer_moves.append('D')
    return layer_moves

def left_ok(x, last_step):
    if last_step == 3:
        return False

    if x == 0:
        return False

    return True

def up_ok(y, last_step):
    if last_step == 6:
        return False

    if y == 0:
        return False

    return True

def right_ok(x, last_step, width):
    if last_step == 9:
        return False

    if x == width - 1:
        return False

    return True

def down_ok(y, last_step, height):
    if last_step == 12:
        return False

    if y == height - 1:
        return False

    return True

def is_in_set(hash_param):
    if hash_param not in visited:
        visited.add(hash_param)
        print(str(hash_param) + " added to set")
    else:
        print(str(hash_param) + " already in set")

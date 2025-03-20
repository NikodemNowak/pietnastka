import hashlib as hl
import copy as cp

f = open("plansza.txt", "r")
rows, cols = map(int, f.readline().split())


def load_board():
    arr = []

    for i in range(rows):
        line = f.readline().split()
        for j in range(cols):
            arr.append(int(line[j]))

    return tuple(arr), rows, cols


def generate_final_board():
    i = 1
    final_board = []
    for _ in range(rows*cols):
        final_board.append(i)
        i += 1
    final_board[rows*cols-1] = 0
    return tuple(final_board)


def check_board(board):
    final_board = generate_final_board()
    x = 0
    for i in range(rows):
        for j in range(cols):
            x += board[j+i*rows] != final_board[j+i*rows]
    return x


def hash_board(board):
    return hash(board)

def where_zero(board):
    for i in range(rows*cols):
        if board[i] == 0:
            return i

def move_left(board):
    x = where_zero(board)
    temp_board = list(board)
    temp_board[x], temp_board[x-1] = board[x-1], board[x]
    return tuple(temp_board), 'L'

def move_right(board):
    x = where_zero(board)
    temp_board = list(board)
    temp_board[x], temp_board[x+1] = board[x+1], board[x]
    return tuple(temp_board), 'R'

def move_up(board):
    x = where_zero(board)
    temp_board = list(board)
    temp_board[x], temp_board[x-cols] = board[x-cols], board[x]
    return tuple(temp_board), 'U'

def move_down(board):
    x = where_zero(board)
    temp_board = list(board)
    temp_board[x], temp_board[x+cols] = board[x+cols], board[x]
    return tuple(temp_board), 'D'
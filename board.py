import hashlib as hl
import copy as cp

f = open("plansza.txt", "r")
rows, cols = map(int, f.readline().split())


def load_board():
    # arr = [[0 for _ in range(cols)] for _ in range(rows)]
    arr = []

    for i in range(rows):
        line = f.readline().split()
        for j in range(cols):
            arr.append(int(line[j]))

    return tuple(arr), rows, cols


def generate_final_board():
    # ok_arr = [[i * cols + j + 1 for j in range(cols)] for i in range(rows)]
    # ok_arr[rows - 1][cols - 1] = 0
    # return ok_arr
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
    # for i in range(rows):
    #     for j in range(cols):
    #         if board[i][j] != final_board[i][j]:
    #             x += 1
    for i in range(rows):
        for j in range(cols):
            x += board[j+i*rows] != final_board[j+i*rows]
    return x


def hash_board(board):
    # board_str = str(board).encode() #Zamiana tablicy na string i zakodowanie go na bajty
    # return hl.sha256(board_str).hexdigest() #Zahashowanie w formacie hexadecymalnym
    return hash(board)

def where_zero(board):
    # for i in range(rows):
    #     for j in range(cols):
    #         if board[i][j] == 0:
    #             return i, j
    for i in range(rows*cols):
        if board[i] == 0:
            return i

def move_left(board):
    # x, y = where_zero(board)
    # temp_board = cp.deepcopy(board)
    # temp_board[x][y], temp_board[x][y-1] = board[x][y-1], board[x][y]
    # return temp_board
    x = where_zero(board)
    temp_board = list(board)
    temp_board[x], temp_board[x-1] = board[x-1], board[x]
    return tuple(temp_board)

def move_right(board):
    # x, y = where_zero(board)
    # temp_board = cp.deepcopy(board)
    # temp_board[x][y], temp_board[x][y+1] = board[x][y+1], board[x][y]
    # return temp_board
    x = where_zero(board)
    temp_board = list(board)
    temp_board[x], temp_board[x+1] = board[x+1], board[x]
    return tuple(temp_board)

def move_up(board):
    # x, y = where_zero(board)
    # temp_board = cp.deepcopy(board)
    # temp_board[x][y], temp_board[x-1][y] = board[x-1][y], board[x][y]
    # return temp_board
    x = where_zero(board)
    temp_board = list(board)
    temp_board[x], temp_board[x-cols] = board[x-cols], board[x]
    return tuple(temp_board)

def move_down(board):
    # x, y = where_zero(board)
    # temp_board = cp.deepcopy(board)
    # temp_board[x][y], temp_board[x+1][y] = board[x+1][y], board[x][y]
    # return temp_board
    x = where_zero(board)
    temp_board = list(board)
    temp_board[x], temp_board[x+cols] = board[x+cols], board[x]
    return tuple(temp_board)
import time

f = ''
rows, cols = 0, 0

def get_rows():
    return rows
def get_cols():
    return cols

# Wczytuje planszę z pliku
def load_board(path):
    global f
    global rows
    global cols
    f = open(path, "r")
    rows, cols = map(int, f.readline().split())
    arr = []

    for i in range(rows):
        line = f.readline().split()
        for j in range(cols):
            arr.append(int(line[j]))

    return tuple(arr), rows, cols

# Generuje finalną planszę
def generate_final_board():
    i = 1
    final_board = []
    for _ in range(rows*cols):
        final_board.append(i)
        i += 1
    final_board[rows*cols-1] = 0
    return tuple(final_board)

# Sprawdza czy plansza jest rozwiazana
def check_board(board):
    final_board = generate_final_board()
    x = 0
    for i in range(rows):
        for j in range(cols):
            x += board[j+i*rows] != final_board[j+i*rows]
    return x


# Zwraca hash planszy
def hash_board(board):
    return hash(board)

# Znajduje pustą komórkę
def where_zero(board):
    for i in range(rows*cols):
        if board[i] == 0:
            return i

# Przesuwa pustą komórkę w lewo
def move_left(board):
    x = where_zero(board)
    temp_board = list(board)
    temp_board[x], temp_board[x-1] = board[x-1], board[x]
    return tuple(temp_board), 'L'

# Przesuwa pustą komórkę w prawo
def move_right(board):
    x = where_zero(board)
    temp_board = list(board)
    temp_board[x], temp_board[x+1] = board[x+1], board[x]
    return tuple(temp_board), 'R'

# Przesuwa pustą komórkę w górę
def move_up(board):
    x = where_zero(board)
    temp_board = list(board)
    temp_board[x], temp_board[x-cols] = board[x-cols], board[x]
    return tuple(temp_board), 'U'

# Przesuwa pustą komórkę w dół
def move_down(board):
    x = where_zero(board)
    temp_board = list(board)
    temp_board[x], temp_board[x+cols] = board[x+cols], board[x]
    return tuple(temp_board), 'D'

# Sprawdza czy można iść w lewo
def left_ok(x, last_step):
    if last_step == 'R':
        return False

    if x % cols == 0:
        return False

    return True

# Sprawdza czy można iść w górę
def up_ok(x, last_step):
    if last_step == 'D':
        return False

    if x < cols:
        return False

    return True

# Sprawdza czy można iść w prawo
def right_ok(x, last_step):
    if last_step == 'L':
        return False

    if x % cols == cols - 1:
        return False

    return True

# Sprawdza czy można iść w dół
def down_ok(x, last_step):
    if last_step == 'U':
        return False

    if x >= (cols - 1) * rows:
        return False

    return True

# Sprawdza które ruchy są możliwe
def check_possible_move(x, last_step, layer_moves):
    if left_ok(x, last_step):
        layer_moves.append('L')

    if up_ok(x, last_step):
        layer_moves.append('U')

    if right_ok(x, last_step):
        layer_moves.append('R')

    if down_ok(x, last_step):
        layer_moves.append('D')
    return layer_moves

# Sprawdza czy dany stan jest w zbiorze odwiedzonych
def is_in_set(hash_param, visited):
    if hash_param not in visited:
        visited.add(hash_param)
        return True
    else:
        return False

def summary_info(is_ok, final_board, steps, visited, processed, max_processed_depth, time_taken):
    if is_ok:
        print("Znaleziono rozwiązanie: " + final_board + " z krokiem: " + steps)
        print("Ilość kroków: " + str(len(steps)))
    else:
        print("Nie znaleziono rozwiązania")
        print("Ilość kroków: " + str(steps))

    print("Ilość odwiedzonych stanów: " + str(len(visited)))
    print("Ilość przetworzonych stanów: " + str(processed))
    print("Maksymalna głębokość przetworzonych stanów: " + str(max_processed_depth))
    print(f"Czas wykonania: {time_taken*1000:.3f} milisekund")
    return

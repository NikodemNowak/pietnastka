# Zmienne globalne dotyczące planszy
f = ''  # Uchwyt do pliku
rows, cols = 0, 0  # Wymiary planszy: liczba wierszy i kolumn


def get_rows():
    """Zwraca liczbę wierszy planszy."""
    return rows


def get_cols():
    """Zwraca liczbę kolumn planszy."""
    return cols


def load_board(path):
    """
    Wczytuje planszę z pliku.

    Args:
        path: Ścieżka do pliku z danymi planszy

    Returns:
        tuple: Krotka zawierająca (plansza, liczba wierszy, liczba kolumn)
    """
    global f, rows, cols
    f = open(path, "r")
    rows, cols = map(int, f.readline().split())
    arr = []

    for i in range(rows):
        line = f.readline().split()
        for j in range(cols):
            arr.append(int(line[j]))

    return tuple(arr), rows, cols


def generate_final_board():
    """
    Generuje finalną planszę, gdzie liczby są ułożone po kolei, a 0 jest na końcu.

    Returns:
        tuple: Krotka reprezentująca stan końcowy planszy
    """
    i = 1
    final_board = []
    for _ in range(rows * cols):
        final_board.append(i)
        i += 1
    final_board[rows * cols - 1] = 0
    return tuple(final_board)


def check_board(board):
    """
    Sprawdza, ile pól planszy różni się od stanu końcowego.

    Args:
        board: Stan planszy do sprawdzenia

    Returns:
        int: Liczba różniących się pól
    """
    final_board = generate_final_board()
    x = 0
    for i in range(rows):
        for j in range(cols):
            x += board[j + i * rows] != final_board[j + i * rows]
    return x


def hash_board(board):
    """
    Hash planszy.

    Args:
        board: Stan planszy

    Returns:
        int: Hash planszy
    """
    return hash(board)


def where_zero(board):
    """
    Znajduje indeks pustej komórki (oznaczonej jako 0) na planszy.

    Args:
        board: Stan planszy

    Returns:
        int: Indeks komórki z zerem
    """
    for i in range(rows * cols):
        if board[i] == 0:
            return i



def move_left(board):
    """
    Przesuwa pustą komórkę w lewo.

    Args:
        board: Aktualny stan planszy

    Returns:
        tuple: (nowy stan planszy, symbol ruchu)
    """
    x = where_zero(board)
    temp_board = list(board)
    temp_board[x], temp_board[x - 1] = board[x - 1], board[x]
    return tuple(temp_board), 'L'


def move_right(board):
    """
    Przesuwa pustą komórkę w prawo.

    Args:
        board: Aktualny stan planszy

    Returns:
        tuple: (nowy stan planszy, symbol ruchu)
    """
    x = where_zero(board)
    temp_board = list(board)
    temp_board[x], temp_board[x + 1] = board[x + 1], board[x]
    return tuple(temp_board), 'R'


def move_up(board):
    """
    Przesuwa pustą komórkę w górę.

    Args:
        board: Aktualny stan planszy

    Returns:
        tuple: (nowy stan planszy, symbol ruchu)
    """
    x = where_zero(board)
    temp_board = list(board)
    temp_board[x], temp_board[x - cols] = board[x - cols], board[x]
    return tuple(temp_board), 'U'


def move_down(board):
    """
    Przesuwa pustą komórkę w dół.

    Args:
        board: Aktualny stan planszy

    Returns:
        tuple: (nowy stan planszy, symbol ruchu)
    """
    x = where_zero(board)
    temp_board = list(board)
    temp_board[x], temp_board[x + cols] = board[x + cols], board[x]
    return tuple(temp_board), 'D'



def left_ok(x, last_step):
    """
    Sprawdza czy można przesunąć pustą komórkę w lewo.

    Args:
        x: Indeks pustej komórki
        last_step: Ostatni wykonany ruch

    Returns:
        bool: Czy ruch jest możliwy
    """
    if last_step == 'R':  # Nie pozwalamy na cofnięcie ostatniego ruchu
        return False

    if x % cols == 0:  # Sprawdza czy komórka jest na lewej krawędzi
        return False

    return True


def up_ok(x, last_step):
    """
    Sprawdza czy można przesunąć pustą komórkę w górę.

    Args:
        x: Indeks pustej komórki
        last_step: Ostatni wykonany ruch

    Returns:
        bool: Czy ruch jest możliwy
    """
    if last_step == 'D':  # Nie pozwalamy na cofnięcie ostatniego ruchu
        return False

    if x < cols:  # Sprawdza czy komórka jest w pierwszym wierszu
        return False

    return True


def right_ok(x, last_step):
    """
    Sprawdza czy można przesunąć pustą komórkę w prawo.

    Args:
        x: Indeks pustej komórki
        last_step: Ostatni wykonany ruch

    Returns:
        bool: Czy ruch jest możliwy
    """
    if last_step == 'L':  # Nie pozwalamy na cofnięcie ostatniego ruchu
        return False

    if x % cols == cols - 1:  # Sprawdza czy komórka jest na prawej krawędzi
        return False

    return True


def down_ok(x, last_step):
    """
    Sprawdza czy można przesunąć pustą komórkę w dół.

    Args:
        x: Indeks pustej komórki
        last_step: Ostatni wykonany ruch

    Returns:
        bool: Czy ruch jest możliwy
    """
    if last_step == 'U':  # Nie pozwalamy na cofnięcie ostatniego ruchu
        return False

    if x >= (cols - 1) * rows:  # Sprawdza czy komórka jest w ostatnim wierszu
        return False

    return True


def check_possible_move(x, last_step, layer_moves):
    """
    Sprawdza które ruchy są możliwe i dodaje je do listy.

    Args:
        x: Indeks pustej komórki
        last_step: Ostatni wykonany ruch
        layer_moves: Lista możliwych ruchów

    Returns:
        list: Zaktualizowana lista możliwych ruchów
    """
    if left_ok(x, last_step):
        layer_moves.append('L')

    if up_ok(x, last_step):
        layer_moves.append('U')

    if right_ok(x, last_step):
        layer_moves.append('R')

    if down_ok(x, last_step):
        layer_moves.append('D')
    return layer_moves




def is_in_set(dict_param, visited):
    """
    Sprawdza czy dany stan jest w zbiorze odwiedzonych.
    Jeśli nie, dodaje go do zbioru.

    Args:
        dict_param: Stan do sprawdzenia
        visited: Zbiór odwiedzonych stanów

    Returns:
        bool: True jeśli stan nie był wcześniej w zbiorze, False w przeciwnym przypadku
    """
    if dict_param not in visited:
        visited.add(dict_param)
        return True
    else:
        return False


def add_to_set_dfs(dict_param, visited_chainmap):
    """
    Dodaje stan do zbioru odwiedzonych dla algorytmu DFS.
    Jeśli stan już istnieje, zachowuje krótszą ścieżkę.

    Args:
        dict_param: Słownik {plansza: ścieżka}
        visited_chainmap: ChainMap z odwiedzonymi stanami

    Returns:
        bool: True jeśli dodano nowy stan lub zaktualizowano ścieżkę, False gdy zachowano starą ścieżkę
    """
    board = list(dict_param.keys())[0]
    path = dict_param[board]

    # Sprawdza czy dany stan jest w ChainMap
    if board in visited_chainmap:
        # Jeśli długość ścieżki jest mniejsza, to zamienia
        if len(path) < len(visited_chainmap[board]):
            # Znajduje słownik, w którym jest plansza i aktualizuje ścieżkę
            for d in visited_chainmap.maps:
                if board in d:
                    d[board] = path
                    break
            return True
        else:
            return False
    else:
        # Dodaje nowy stan do pierwszego słownika w ChainMap
        visited_chainmap.maps[0][board] = path
        return True


def summary_info(is_ok, final_board, steps, visited, processed, max_processed_depth, time_taken):
    """
    Wyświetla podsumowanie wykonania algorytmu.

    Args:
        is_ok: Czy znaleziono rozwiązanie
        final_board: Końcowy stan planszy
        steps: Liczba kroków lub sekwencja kroków
        visited: Zbiór odwiedzonych stanów
        processed: Liczba przetworzonych stanów
        max_processed_depth: Maksymalna głębokość przetworzonych stanów
        time_taken: Czas wykonania w sekundach
    """
    if is_ok:
        print("Znaleziono rozwiązanie: " + final_board + " z krokiem: " + steps)
        print("Ilość kroków: " + str(len(steps)))
    else:
        print("Nie znaleziono rozwiązania")
        print("Ilość kroków: " + str(steps))

    print("Ilość odwiedzonych stanów: " + str(len(visited)))
    print("Ilość przetworzonych stanów: " + str(processed))
    print("Maksymalna głębokość przetworzonych stanów: " + str(max_processed_depth))
    print(f"Czas wykonania: {time_taken * 1000:.3f} milisekund")
    return

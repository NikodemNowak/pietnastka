from queue import PriorityQueue
from temporary_algorithm import temporary_algorithm
from board import check_board, get_rows, get_cols


def hamming_distance(board):
    """
    Funkcja heurystyczna obliczająca odległość Hamminga (liczbę kafelków nie na swoim miejscu).

    Args:
        board: Układ planszy jako krotka

    Returns:
        int: Liczba kafelków nie na właściwym miejscu
    """
    return check_board(board)


def manhattan_distance(board):
    """
    Funkcja heurystyczna obliczająca odległość Manhattan dla wszystkich kafelków.

    Args:
        board: Układ planszy jako krotka

    Returns:
        int: Suma odległości Manhattan dla wszystkich kafelków
    """
    distance = 0
    rows = get_rows()
    cols = get_cols()

    for i in range(len(board)):
        if board[i] == 0:  # Pomijamy pusty kafelek
            continue

        # Aktualna pozycja
        current_row = i // rows
        current_col = i % cols

        # Docelowa pozycja dla tej wartości
        value = board[i]
        target_row = (value - 1) // rows
        target_col = (value - 1) % cols

        # Dodajemy odległość Manhattan dla tego kafelka
        distance += abs(current_row - target_row) + abs(current_col - target_col)

    return distance


def a_star(heuristics, board_dict):
    """
    Implementacja algorytmu A* do rozwiązywania układanki.

    Args:
        heuristics: Funkcja heurystyczna używana do oceny stanów
        board_dict: Słownik reprezentujący początkowy stan planszy

    Returns:
        tuple: (czy znaleziono, stan końcowy, sekwencja ruchów, odwiedzone stany, liczba przetworzonych stanów, maksymalna głębokość)
    """
    # Inicjalizacja struktur danych
    queue_a_star = PriorityQueue()
    visited_a_star = set()
    processed_a_star = 0
    additional_counter = [0]  # Lista, aby licznik był mutowalny przez referencję - służy do rozstrzygania remisów
    max_depth = 20
    max_processed_depth = 0

    # Obliczenie początkowego priorytetu (f = g + h)
    # g = koszt dotychczasowej ścieżki (długość kroków - 1)
    # h = wartość funkcji heurystycznej
    board = next(iter(board_dict.keys()))
    steps = list(board_dict.values())[0]
    priority = heuristics(board) + len(steps) - 1

    # Dodanie stanu początkowego do zbioru odwiedzonych i kolejki priorytetowej
    visited_a_star.add(board)
    queue_a_star.put((priority, additional_counter[0], board_dict))
    additional_counter[0] += 1

    while not queue_a_star.empty():
        # Pobranie stanu o najniższym priorytecie
        # Drugi element (counter) zapewnia deterministyczne zachowanie przy równych priorytetach
        _, _, b = queue_a_star.get()
        processed_a_star += 1

        # Aktualizacja informacji o głębokości przeszukiwania
        current_depth = len(list(b.values())[0]) - 1
        if current_depth > max_processed_depth:
            max_processed_depth = current_depth

        # Sprawdzenie czy osiągnięto stan docelowy
        board = next(iter(b.keys()))
        if check_board(board) == 0:
            return True, str(board), str(list(b.values())[0][1:]), visited_a_star, processed_a_star, max_processed_depth

        # Generowanie kolejnych stanów
        temporary_algorithm(heuristics, b, queue_a_star, visited_a_star, additional_counter, False)

    # W przypadku niepowodzenia
    return False, '', '-1', visited_a_star, processed_a_star, max_depth
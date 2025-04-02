from temporary_algorithm import *
from board import *


def bfs(order, board_dict):
    """
    Implementacja algorytmu przeszukiwania wszerz (BFS).

    Parametry:
    ----------
    order : list
        Kolejność ruchów do sprawdzenia (np. ['L', 'R', 'U', 'D']).
    board_dict : dict
        Słownik zawierający początkowy stan planszy jako klucz i pustą ścieżkę jako wartość.

    Zwraca:
    -------
    tuple
        (znaleziono_rozwiązanie, stan_końcowy, ścieżka_rozwiązania, liczba_odwiedzonych, liczba_przetworzonych)
    """
    # Inicjalizacja struktur danych
    visited_bfs = set()  # Zbiór odwiedzonych stanów
    all_layer_states_bfs = Queue()  # Kolejka stanów do sprawdzenia
    processed_bfs = 0  # Licznik przetworzonych stanów

    # Dodanie początkowego stanu do zbioru odwiedzonych
    initial_state = next(iter(board_dict.keys()))
    is_in_set(initial_state, visited_bfs)

    # Wygenerowanie pierwszej warstwy stanów
    temporary_algorithm(order, board_dict, all_layer_states_bfs, visited_bfs, 0, False)

    # Główna pętla BFS
    while not all_layer_states_bfs.empty():
        current_board = all_layer_states_bfs.get()
        processed_bfs += 1

        # Sprawdzenie czy aktualny stan jest stanem końcowym
        current_state = next(iter(current_board.keys()))
        if check_board(current_state) == 0:
            # Zwróć informacje o znalezionym rozwiązaniu
            path = str(list(current_board.values())[0][1:])  # Ścieżka kroków bez stanu początkowego
            return True, str(current_state), path, visited_bfs, processed_bfs

        # Wygenerowanie kolejnych stanów na podstawie aktualnego
        temporary_algorithm(order, current_board, all_layer_states_bfs, visited_bfs, 0, False)

    # Jeśli nie znaleziono rozwiązania
    return False, '', '-1', visited_bfs, processed_bfs

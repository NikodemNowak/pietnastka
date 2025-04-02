from temporary_algorithm import temporary_algorithm
from board import add_to_set_dfs, check_board
from collections import deque, ChainMap


def dfs(order, board_dict):
    """
    Implementacja algorytmu przeszukiwania w głąb (DFS).

    Parametry:
    ----------
    order : list
        Kolejność ruchów do sprawdzenia (np. ['L', 'R', 'U', 'D']).
    board_dict : dict
        Słownik zawierający początkowy stan planszy jako klucz i pustą ścieżkę jako wartość.

    Zwraca:
    -------
    tuple
        (znaleziono_rozwiązanie, stan_końcowy, ścieżka_rozwiązania,
         liczba_odwiedzonych, liczba_przetworzonych, maksymalna_głębokość)
    """
    # Inicjalizacja struktur danych
    stack = deque()  # Stos LIFO do przechowywania stanów do sprawdzenia
    visited_dfs = ChainMap()  # Struktura do przechowywania odwiedzonych stanów
    processed_dfs = 0  # Licznik przetworzonych stanów
    max_depth = 20  # Maksymalna dopuszczalna głębokość przeszukiwania
    max_processed_depth = 0  # Aktualnie osiągnięta maksymalna gł��bokość

    # Dodanie początkowego stanu do zbioru odwiedzonych i na stos
    add_to_set_dfs(board_dict, visited_dfs)
    stack.append(board_dict)

    # Główna pętla DFS
    while stack:
        # Pobierz stan z wierzchołka stosu (zgodnie z zasadą LIFO)
        current_board = stack.pop()

        # Oblicz głębokość aktualnego stanu
        current_depth = len(list(current_board.values())[0]) - 1
        if current_depth > max_processed_depth:
            max_processed_depth = current_depth

        processed_dfs += 1

        # Sprawdzenie czy aktualny stan jest stanem końcowym
        current_state = next(iter(current_board.keys()))
        if check_board(current_state) == 0:
            # Zwróć informacje o znalezionym rozwiązaniu
            path = str(list(current_board.values())[0][1:])
            return True, str(current_state), path, visited_dfs, processed_dfs, max_processed_depth

        # Sprawdzenie czy nie przekroczono maksymalnej głębokości
        all_steps = list(current_board.values())[0]
        if len(all_steps) - 1 >= max_depth:
            max_processed_depth = max_depth
            continue

        # Generowanie kolejnych stanów i dodanie ich na stos
        temporary_algorithm(order, current_board, stack, visited_dfs, 0, True)

    # Jeśli nie znaleziono rozwiązania
    return False, '', '-1', visited_dfs, processed_dfs, max_processed_depth
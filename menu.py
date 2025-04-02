import re
import sys
import time

from bfs import *
from dfs import *
from a_star import *
from output import *


def check(strategy, param, input_file, solution_output_file, stats_output_file):
    """
    Sprawdza poprawność argumentów przekazanych do programu.

    Parametry:
    ----------
    strategy : str
        Strategia przeszukiwania (bfs, dfs, astr)
    param : str
        Parametr strategii (kolejność przeszukiwania lub typ heurystyki)
    input_file : str
        Ścieżka do pliku wejściowego
    solution_output_file : str
        Ścieżka do pliku z rozwiązaniem
    stats_output_file : str
        Ścieżka do pliku ze statystykami
    """
    # Lista wszystkich możliwych permutacji liter L, R, U, D (24 różne opcje)
    order_options = [
        # Zaczynające się od L
        'LRUD', 'LRDU', 'LURD', 'LUDR', 'LDRU', 'LDUR',

        # Zaczynające się od R
        'RLUD', 'RLDU', 'RULD', 'RUDL', 'RDLU', 'RDUL',

        # Zaczynające się od U
        'ULRD', 'ULDR', 'URLD', 'URDL', 'UDLR', 'UDRL',

        # Zaczynające się od D
        'DLRU', 'DLUR', 'DRLU', 'DRUL', 'DULR', 'DURL'
    ]

    # Sprawdzenie poprawności algorytmu
    if strategy not in ('bfs', 'dfs', 'astr'):
        print("Niepoprawny algorytm. Wybierz: bfs, dfs, astr")
        return False

    # Sprawdzenie poprawności parametru w zależności od wybranego algorytmu
    if strategy == 'bfs' or strategy == 'dfs':
        if param not in order_options:
            print("Niepoprawny porządek. Wybierz jedną z opcji: " + ", ".join(order_options))
            return False
    elif strategy == 'astr':
        if param not in ('hamm', 'manh'):
            print("Niepoprawna heurystyka. Wybierz: hamm, manh")
            return False

    # Wzorzec: co najmniej jeden dowolny znak + .txt na końcu
    pattern = r'^.+\.txt$'

    # Sprawdzenie poprawności nazw plików
    if not re.match(pattern, input_file):
        print("Niepoprawny plik wejściowy. Upewnij się, że plik ma rozszerzenie .txt")
        return False
    if not re.match(pattern, solution_output_file):
        print("Niepoprawny plik wyjściowy. Upewnij się, że plik ma rozszerzenie .txt")
        return False
    if not re.match(pattern, stats_output_file):
        print("Niepoprawny plik statystyk. Upewnij się, że plik ma rozszerzenie .txt")
        return False


def run(strategy, param, board_dict, solution_output_file, stats_output_file):
    """
    Uruchamia wybrany algorytm przeszukiwania i zapisuje wyniki.

    Parametry:
    ----------
    strategy : str
        Strategia przeszukiwania (bfs, dfs, astr)
    param : str
        Parametr strategii (kolejność przeszukiwania lub typ heurystyki)
    board_dict : dict
        Słownik zawierający początkową planszę i ścieżkę
    solution_output_file : str
        Ścieżka do pliku z rozwiązaniem
    stats_output_file : str
        Ścieżka do pliku ze statystykami
    """
    # Inicjalizacja zmiennych wynikowych
    found = False  # Czy znaleziono rozwiązanie
    final_board = ""  # Końcowy stan planszy
    path = ""  # Ścieżka rozwiązania
    visited = set()  # Zbiór odwiedzonych stanów
    processed = 0  # Liczba przetworzonych stanów
    max_processed_depth = 0  # Maksymalna głębokość przeszukiwania

    start_time = time.perf_counter()  # Rozpoczęcie pomiaru czasu

    # Uruchomienie odpowiedniego algorytmu
    if strategy == 'bfs':
        print("Rozpoczynam przeszukiwanie BFS z parametrem: " + param)
        found, final_board, path, visited, processed = bfs(param, board_dict)
        max_processed_depth = len(path) if path != "-1" else 0  # Dla BFS głębokość to długość ścieżki
    elif strategy == 'dfs':
        print("Rozpoczynam przeszukiwanie DFS z parametrem: " + param)
        found, final_board, path, visited, processed, max_processed_depth = dfs(param, board_dict)
    elif strategy == 'astr':
        print("Rozpoczynam przeszukiwanie A* z parametrem: " + param)
        if param == 'hamm':
            # Uruchomienie A* z heurystyką Hamminga
            found, final_board, path, visited, processed, max_processed_depth = a_star(hamming_distance, board_dict)
        else:
            # Uruchomienie A* z heurystyką Manhattan
            found, final_board, path, visited, processed, max_processed_depth = a_star(manhattan_distance, board_dict)
    else:
        print(f"Nieznana strategia: {strategy}")
        sys.exit(1)

    # Obliczenie czasu wykonania
    time_taken = time.perf_counter() - start_time

    # Zapisanie wyników do plików
    write_solution(solution_output_file, found, path)
    write_stats(stats_output_file, found, path, visited, processed, max_processed_depth, time_taken)

    # Wyświetlenie podsumowania
    summary_info(found, final_board, path, visited, processed, max_processed_depth, time_taken)
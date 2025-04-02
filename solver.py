#!/usr/bin/env python3
"""
Solver układanki przesuwnej (puzzle).
Uruchomienie: python solver.py <strategia> <parametr> <plik_wejściowy> <plik_wyjściowy> <plik_statystyk>
gdzie:
- strategia: bfs, dfs lub astr
- parametr: dla bfs/dfs - kolejność przeszukiwania (np. LRUD), dla astr - heurystyka (hamm lub manh)
- plik_wejściowy: plik .txt zawierający układ początkowy planszy
- plik_wyjściowy: plik .txt do zapisu rozwiązania
- plik_statystyk: plik .txt do zapisu statystyk wykonania
"""

import sys
from menu import check, run, load_board


def main():
    # Sprawdzenie liczby argumentów
    if len(sys.argv) != 6:
        print("Użycie: python solver.py <strategia> <parametr> <plik_wejściowy> <plik_wyjściowy> <plik_statystyk>")
        sys.exit(1)

    # Wczytanie argumentów z linii poleceń
    strategy = sys.argv[1]  # Strategia: bfs, dfs lub astr
    param = sys.argv[2]  # Parametr: kolejność przeszukiwania lub heurystyka
    input_file = sys.argv[3]  # Plik wejściowy z układem planszy
    solution_output_file = sys.argv[4]  # Plik do zapisu rozwiązania
    stats_output_file = sys.argv[5]  # Plik do zapisu statystyk

    # Sprawdzenie poprawności argumentów
    check(strategy, param, input_file, solution_output_file, stats_output_file)

    # Wczytanie planszy z pliku
    loaded_board, rows, cols = load_board(input_file)

    # Utworzenie początkowego stanu (plansza + ścieżka)
    # "0" oznacza brak wykonanych ruchów
    board_dict = {loaded_board: "0"}

    # Uruchomienie wybranego algorytmu
    run(strategy, param, board_dict, solution_output_file, stats_output_file)


if __name__ == "__main__":
    main()
import re
import sys

from bfs import *
from dfs import *
from a_star import *
from output import *

def check(strategy, param, input_file, solution_output_file, stats_output_file):
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

    if strategy not in ('bfs', 'dfs', 'astr'):
        print("Niepoprawny algorytm. Wybierz: bfs, dfs, astr")
        return False

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

    found, final_board, path, visited, processed, max_processed_depth, start_time = False, "", "", set(),0, 0, 0

    if strategy == 'bfs':
        print("Rozpoczynam przeszukiwanie BFS z parametrem: " + param)
        found, final_board, path, visited, processed, start_time = bfs(param, board_dict, time.time())
        max_processed_depth =  str(len(path))
    elif strategy == 'dfs':
        print("Rozpoczynam przeszukiwanie DFS z parametrem: " + param)
        found, final_board, path, visited, processed, max_processed_depth, start_time = dfs(param, board_dict, time.time())
    elif strategy == 'astr':
        print("Rozpoczynam przeszukiwanie A* z parametrem: " + param)
        if param == 'hamm':
            found, final_board, path, visited, processed, max_processed_depth, start_time = a_star(hamming_distance, board_dict, time.time())
        else:
            found, final_board, path, visited, processed, max_processed_depth, start_time = a_star(manhattan_distance, board_dict, time.time())
    else:
        print(f"Unknown strategy: {strategy}")
        sys.exit(1)

    # Write output files
    write_solution(solution_output_file, found, path)
    time_taken = time.time() - start_time
    write_stats(stats_output_file, found, path, visited, processed, max_processed_depth, time_taken)

    # Print summary
    summary_info(found, final_board, path, visited, processed, max_processed_depth, start_time)
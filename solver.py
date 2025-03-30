from menu import *

# Parametry
strategy = ""
param = ""
input_file = ""
solution_output_file = ""
stats_output_file = ""

# Sprawdzenie liczby argumentów
if len(sys.argv) != 6:
    print("Usage: python solver.py <strategy> <param> <input_file> <solution_output_file> <stats_output_file>")
    sys.exit(1)

# Wczytanie argumentów podczas odpalania programu solver.py
if len(sys.argv) == 6:
    strategy = sys.argv[1]
    param = sys.argv[2]
    input_file = sys.argv[3]
    solution_output_file = sys.argv[4]
    stats_output_file = sys.argv[5]

# Sprawdzenie poprawności argumentów
check(strategy, param, input_file, solution_output_file, stats_output_file)

loaded_board, rows, cols = load_board(input_file)
board_dict = {loaded_board : "0"}

run(strategy, param, board_dict, solution_output_file, stats_output_file)

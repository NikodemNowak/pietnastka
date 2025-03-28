import time
from temporary_algorithm import *

def hamming_distance(board):
    return check_board(board)

def manhattan_distance(board):
    distance = 0
    rows = get_rows()
    cols = get_cols()

    numbers = generate_final_board()
    current_pos = [0, 0]
    for i in range(len(numbers)):
        for j in range(len(numbers)):
            if numbers[i] == board[j]:
                current_pos[0] = j // rows
                current_pos[1] = j % cols
                break
        target_pos = (i-1 // rows, i-1 % cols)
        distance += abs(current_pos[0] - target_pos[0]) + abs(current_pos[1] - target_pos[1])

    return distance

def a_star(heuristics, board_dict, rows, cols, start_time):

    processed_a_star = 0
    queue_a_star = PriorityQueue()
    visited_a_star = set()

    additional_counter = [0] # Aby było mutowalne
    queue_a_star.put((heuristics(next(iter(board_dict.keys()))), additional_counter[0], board_dict))  # Dodaje do kolejki z priorytetem
    additional_counter[0] += 1

    while not queue_a_star.empty():

        prio, _, b = queue_a_star.get()  # SYPIE BŁĘDEM, BO JAK HEURYSTYKA DA TO SAMO TO NIE UMIE POSOROTWAĆ
        processed_a_star = processed_a_star + 1

        if check_board(next(iter(b.keys()))) == 0:
            print("Znaleziono rozwiązanie: " + str(next(iter(b.keys()))) + " z krokiem: " + str(list(b.values())[0][1:]))
            print("Ilość kroków: " + str(len(list(b.values())[0]) - 1))
            print("Ilość odwiedzonych stanów: " + str(len(visited_a_star)))
            print("Ilość przetworzonych stanów: " + str(processed_a_star))
            print("Czas wykonania: " + str(time.time() - start_time) + " sekund")
            return

        temporary_alghorithm(heuristics, b, rows, cols, queue_a_star, visited_a_star,additional_counter)

    if queue_a_star.empty():
        print("Nie znaleziono rozwiązania")
        print("Ilość odwiedzonych stanów: " + str(len(visited_a_star)))
        print("Ilość przetworzonych stanów: " + str(processed_a_star))
        print("Czas wykonania: " + str(time.time() - start_time) + " sekund")
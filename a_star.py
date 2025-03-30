import time
from temporary_algorithm import *

def hamming_distance(board):
    return check_board(board)


def manhattan_distance(board):
    distance = 0

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


def a_star(heuristics, board_dict, start_time):

    queue_a_star = PriorityQueue()
    visited_a_star = set()
    processed_a_star = 0
    additional_counter = [0] # Aby było mutowalne

    priority = heuristics(next(iter(board_dict.keys()))) + len(list(board_dict.values())[0]) - 1

    queue_a_star.put((priority, additional_counter[0], board_dict))  # Dodaje do kolejki z priorytetem
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

        temporary_alghorithm(heuristics, b, queue_a_star, visited_a_star,additional_counter)

    if queue_a_star.empty():
        print("Nie znaleziono rozwiązania")
        print("Ilość odwiedzonych stanów: " + str(len(visited_a_star)))
        print("Ilość przetworzonych stanów: " + str(processed_a_star))
        print("Czas wykonania: " + str(time.time() - start_time) + " sekund")
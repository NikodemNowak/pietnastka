from temporary_algorithm import *
from board import *

def hamming_distance(board):
    return check_board(board)


def manhattan_distance(board):
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

    queue_a_star = PriorityQueue()
    visited_a_star = set()
    processed_a_star = 0
    additional_counter = [0] # Aby było mutowalne
    max_depth = 20
    max_processed_depth = 0

    priority = heuristics(next(iter(board_dict.keys()))) + len(list(board_dict.values())[0]) - 1

    visited_a_star.add(next(iter(board_dict.keys())))
    queue_a_star.put((priority, additional_counter[0], board_dict))  # Dodaje do kolejki z priorytetem
    additional_counter[0] += 1

    while not queue_a_star.empty():

        prio, _, b = queue_a_star.get()  # SYPIE BŁĘDEM, BO JAK HEURYSTYKA DA TO SAMO TO NIE UMIE POSOROTWAĆ
        processed_a_star += 1

        current_depth = len(list(b.values())[0]) - 1
        if current_depth > max_processed_depth:
            max_processed_depth = current_depth

        if check_board(next(iter(b.keys()))) == 0:
            return True, str(next(iter(b.keys()))), str(list(b.values())[0][1:]), visited_a_star, processed_a_star, max_processed_depth

        temporary_algorithm(heuristics, b, queue_a_star, visited_a_star, additional_counter, False)


    return False, '', '-1', visited_a_star, processed_a_star, max_depth
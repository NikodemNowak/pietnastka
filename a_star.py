from datetime import time

from board import check_board, generate_final_board
from queue import PriorityQueue
import time

from temporary_algorithm import temporary_alghorithm

visited_a_star = set()
processed_a_star = 0
queue_a_star = PriorityQueue()

def hamming_distance(board):
    return check_board(board)

def manhattan_distance(board, rows, cols):
    distance = 0
    numbers = generate_final_board()
    current_pos = [0, 0]
    for i in range(len(numbers)):
        for j in range(len(numbers)):
            if numbers[i] == board[j]:
                current_pos[0] = j // rows
                current_pos[1] = j % cols
                break
        target_pos = (i // rows, i % cols)
        distance += abs(current_pos[0] - target_pos[0]) + abs(current_pos[1] - target_pos[1])

    return distance

def a_star(heuristics, board_dict, rows, cols, start_time):

    queue_a_star.put((heuristics(next(iter(board_dict.keys()))), board_dict))  # Dodaje do kolejki z priorytetem

    while not queue_a_star.empty():
        priority, b = queue_a_star.get()
        global processed_a_star
        processed_a_star = processed_a_star + 1

        if check_board(next(iter(b.keys()))) == 0:
            print("Znaleziono rozwiązanie: " + str(next(iter(b.keys()))) + " z krokiem: " + str(list(b.values())[0][1:]))
            print("Ilość kroków: " + str(len(list(b.values())[0]) - 1))
            print("Ilość odwiedzonych stanów: " + str(len(visited_a_star)))
            print("Ilość przetworzonych stanów: " + str(processed_a_star))
            print("Czas wykonania: " + str(time.time() - start_time) + " sekund")
            return

        temporary_alghorithm(heuristics, b, rows, cols, queue_a_star, visited_a_star)

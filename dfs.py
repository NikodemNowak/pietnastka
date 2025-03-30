from temporary_algorithm import *
from collections import deque

def dfs(order, board_dict, start_time):
    stack = deque() #Stos LIFO
    visited_dfs = set()
    proccessed_dfs = 0
    max_depth = 30
    stack.append(board_dict) # Dodaje na koniec kolejki

    while stack:
        b = stack.pop() # Usuwa ostatni element z kolejki, czyli ten ostatni dodany
        proccessed_dfs = proccessed_dfs + 1

        if check_board(next(iter(b.keys()))) == 0:
            print("Znaleziono rozwiązanie: " + str(next(iter(b.keys()))) + " z krokiem: " + str(list(b.values())[0][1:]))
            print("Ilość kroków: " + str(len(list(b.values())[0]) - 1))
            print("Ilość odwiedzonych stanów: " + str(len(visited_dfs)))
            print("Ilość przetworzonych stanów: " + str(proccessed_dfs))
            print("Czas wykonania: " + str(time.time() - start_time) + " sekund")
            return

        # Sprawdza czy nie przekroczono głębokości
        all_steps = list(b.values())[0]
        if len(all_steps) - 1 >= max_depth:
            continue

        temporary_alghorithm(order, b, stack, visited_dfs, 0)

    summary_info(False, "", max_depth, visited_dfs, proccessed_dfs, start_time)
from temporary_algorithm import *
from collections import deque
import time

visited_dfs = set()
proccessed_dfs = 0

def dfs(order, board_dict, rows, cols, start_time):
    stack = deque() #Stos LIFO
    stack.append(board_dict) # Dodaje na koniec kolejki

    while stack:
        b = stack.pop() # Usuwa ostatni element z kolejki, czyli ten ostatni dodany
        global proccessed_dfs
        proccessed_dfs = proccessed_dfs + 1

        if check_board(next(iter(b.keys()))) == 0:
            print("Znaleziono rozwiązanie: " + str(next(iter(b.keys()))) + " z krokiem: " + str(list(b.values())[0][1:]))
            print("Ilość kroków: " + str(len(list(b.values())[0]) - 1))
            print("Ilość odwiedzonych stanów: " + str(len(visited_dfs)))
            print("Ilość przetworzonych stanów: " + str(proccessed_dfs))
            print("Czas wykonania: " + str(time.time() - start_time) + " sekund")
            return

        temporary_alghorithm(order, b, rows, cols, stack, visited_dfs)


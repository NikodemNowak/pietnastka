from board import *
from queue import Queue, PriorityQueue


def temporary_algorithm(order_or_heuristic, board_dict, algorithm_structure, algorithm_visited, additional_counter,
                        is_dfs):
    """
    Generuje kolejne stany planszy na podstawie aktualnego stanu i dodaje je do struktury danych algorytmu.

    Parametry:
    ----------
    order_or_heuristic : list lub str lub funkcja
        Kolejność ruchów do sprawdzenia (np. 'LRUD') lub funkcja heurystyczna dla A*.
    board_dict : dict
        Słownik zawierający aktualny stan planszy jako klucz i ścieżkę jako wartość.
    algorithm_structure : Queue lub PriorityQueue lub deque
        Struktura danych używana przez algorytm (kolejka dla BFS, stos dla DFS lub kolejka priorytetowa dla A*).
    algorithm_visited : set lub ChainMap
        Struktura przechowująca odwiedzone stany.
    additional_counter : list
        Licznik używany w algorytmie A* do zachowania stabilnego sortowania przy równych priorytetach.
    is_dfs : bool
        Flaga określająca czy używany jest algorytm DFS (True) czy inny (False).
    """
    # Znajdź pozycję zera na planszy
    current_board = next(iter(board_dict.keys()))
    zero_position = where_zero(current_board)

    # Inicjalizacja listy możliwych ruchów
    possible_moves = []

    # Pobranie historii ruchów
    moves_history = list(board_dict.values())[0]

    # Pobranie ostatniego ruchu (jeśli istnieje)
    last_move = moves_history[-1]

    # Określ, które ruchy są możliwe z aktualnej pozycji
    check_possible_move(zero_position, last_move, possible_moves)

    # Jeśli order_or_heuristic jest stringiem, posortuj ruchy zgodnie z tym porządkiem
    if isinstance(order_or_heuristic, str):
        possible_moves = sorted(possible_moves, key=lambda move_var: order_or_heuristic.index(move_var))

    # Przetwórz każdy możliwy ruch
    for move in possible_moves:
        # Wykonaj ruch i uzyskaj nowy stan planszy
        if move == 'L':
            new_board, move_code = move_left(current_board)
        elif move == 'U':
            new_board, move_code = move_up(current_board)
        elif move == 'R':
            new_board, move_code = move_right(current_board)
        elif move == 'D':
            new_board, move_code = move_down(current_board)

        # Utwórz nowy słownik stanu z zaktualizowaną ścieżką
        new_board_dict = {new_board: moves_history + str(move_code)}

        # Dodaj nowy stan do odpowiedniej struktury algorytmu, jeśli nie był wcześniej odwiedzony
        if is_dfs:
            # Dla DFS - dodaj na stos, jeśli stan nie był odwiedzony
            if add_to_set_dfs(new_board_dict, algorithm_visited):
                algorithm_structure.append(new_board_dict)
        else:
            # Dla BFS/A* - dodaj do kolejki, jeśli stan nie był odwiedzony
            board_hash = hash_board(new_board)
            if is_in_set(board_hash, algorithm_visited):
                if isinstance(algorithm_structure, PriorityQueue):
                    # Dla A* - oblicz priorytet jako suma heurystyki i długości ścieżki
                    path_length = len(list(new_board_dict.values())[0]) - 1
                    priority = order_or_heuristic(new_board) + path_length
                    # Dodaj stan do kolejki priorytetowej (priorytet, licznik, stan)
                    algorithm_structure.put((priority, additional_counter[0], new_board_dict))
                    additional_counter[0] += 1  # Inkrementuj licznik dla stabilnego sortowania
                elif isinstance(algorithm_structure, Queue):
                    # Dla BFS - po prostu dodaj do kolejki FIFO
                    algorithm_structure.put(new_board_dict)
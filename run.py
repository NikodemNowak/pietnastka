import os
import concurrent.futures
import multiprocessing


def process_file(filename, permutations):
    """
    Przetwarza pojedynczy plik z planszą, uruchamiając dla niego wszystkie
    algorytmy przeszukiwania z odpowiednimi parametrami.

    Parametry:
    ----------
    filename : str
        Nazwa pliku z planszą do przetworzenia
    permutations : tuple
        Krotka zawierająca dozwolone permutacje kierunków dla BFS i DFS
    """
    commands = []
    # Pobierz pierwszą część nazwy pliku (do 12 znaków)
    base_name = filename[:12]
    file_path = f'./boards/{filename}'

    # Generowanie komend dla BFS i DFS dla każdej permutacji
    for perm in permutations:
        # Komenda dla algorytmu BFS
        commands.append(
            f'python solver.py bfs {perm} {file_path} '
            f'./solutions/{base_name}_bfs_{perm.lower()}_sol.txt '
            f'./additional_info/{base_name}_bfs_{perm.lower()}_stats.txt'
        )
        # Komenda dla algorytmu DFS
        commands.append(
            f'python solver.py dfs {perm} {file_path} '
            f'./solutions/{base_name}_dfs_{perm.lower()}_sol.txt '
            f'./additional_info/{base_name}_dfs_{perm.lower()}_stats.txt'
        )

    # Komenda dla A* z heurystyką Hamminga
    commands.append(
        f'python solver.py astr hamm {file_path} '
        f'./solutions/{base_name}_astr_hamm_sol.txt '
        f'./additional_info/{base_name}_astr_hamm_stats.txt'
    )

    # Komenda dla A* z heurystyką Manhattan
    commands.append(
        f'python solver.py astr manh {file_path} '
        f'./solutions/{base_name}_astr_manh_sol.txt '
        f'./additional_info/{base_name}_astr_manh_stats.txt'
    )

    # Wykonanie wszystkich wygenerowanych komend
    for cmd in commands:
        os.system(cmd)


def main():
    """
    Funkcja główna programu. Odczytuje pliki z planszami i uruchamia na nich
    wszystkie algorytmy przeszukiwania równolegle, wykorzystując dostępne rdzenie CPU.
    """
    # Definicja wszystkich możliwych permutacji kierunków ruchu
    permutation = ('RDUL', 'RDLU', 'DRUL', 'DRLU', 'LUDR', 'LURD', 'ULDR', 'ULRD')
    directory = './boards'

    # Pobranie listy plików z katalogu z planszami
    file_list = [
        f for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f))
    ]

    # Utworzenie katalogów wyjściowych, jeśli nie istnieją
    os.makedirs('./solutions', exist_ok=True)
    os.makedirs('./additional_info', exist_ok=True)

    # Uruchomienie równoległego przetwarzania plików
    with concurrent.futures.ProcessPoolExecutor(
            max_workers=multiprocessing.cpu_count()
    ) as executor:
        futures = [
            executor.submit(process_file, filename, permutation)
            for filename in file_list
        ]
        # Oczekiwanie na zakończenie wszystkich procesów
        concurrent.futures.wait(futures)


if __name__ == '__main__':
    main()
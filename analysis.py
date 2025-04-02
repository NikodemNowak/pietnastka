import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, ScalarFormatter, FuncFormatter
import os
import glob

def read_data():
    directory = "./additional_info"
    data_rows = []

    # Znajdź wszystkie pliki w katalogu
    all_files = glob.glob(os.path.join(directory, "*.txt"))

    for file in all_files:
        file_name = os.path.basename(file)

        try:
            parts = file_name.split('_')

            depth_of_moves = parts[1]
            algorithm = parts[3]
            heuristic_or_order = parts[4]

            # Wczytaj dane z pliku
            with open(file, 'r') as f:
                lines = f.readlines()
                steps = int(lines[0].strip())
                visited = int(lines[1].strip())
                processed = int(lines[2].strip())
                max_algo_depth = int(lines[3].strip())
                time = float(lines[4].strip())

                data_rows.append([
                    depth_of_moves,
                    algorithm,
                    heuristic_or_order,
                    steps,
                    visited,
                    processed,
                    max_algo_depth,
                    time
                ])

        except (IndexError, ValueError) as e:
            print(f"Błąd podczas przetwarzania pliku {file_name}: {str(e)}")


    data = pd.DataFrame(data_rows, columns=['Depth_Of_Moves', 'Algorithm', 'Heuristic/Order','Steps', 'Visited', 'Processed', 'Max_Algo_Depth', 'Time'])
    return data

# średnie arytmetyczne wyznaczone dla strategii
# BFS (dla wszystkich porządków przeszukiwania łącznie),
# DFS (dla wszystkich porządków przeszukiwania łącznie)
# oraz A* (dla obu heurystyk łącznie) względem głębokości rozwiązania
def plot_data1(df, column):
    data = df[['Depth_Of_Moves', 'Algorithm', column]].copy()

    # Zamiana "astr" na "A*"
    data['Algorithm'] = data['Algorithm'].replace('astr', 'A*')

    # Grupowanie danych
    grouped_data = data.groupby(['Algorithm', 'Depth_Of_Moves']).mean().reset_index()

    # Zaokrąglanie wartości Steps do całości
    grouped_data[column] = grouped_data[column].round(3)

    # Unikalne wartości głębokości
    depths = sorted(grouped_data['Depth_Of_Moves'].unique())
    algorithms = grouped_data['Algorithm'].unique()

    # Szerokość słupka
    bar_width = 0.25

    plt.figure(figsize=(12, 7))

    # Tworzenie indeksów dla pozycji słupków
    positions = np.arange(len(depths))

    # Rysowanie słupków dla każdego algorytmu
    for i, algorithm in enumerate(algorithms):
        subset = grouped_data[grouped_data['Algorithm'] == algorithm]

        # Tworzenie słownika aby dopasować dane do właściwych pozycji
        steps_by_depth = {row['Depth_Of_Moves']: row[column] for _, row in subset.iterrows()}

        # Zbieranie wartości dla każdej głębokości
        values = [steps_by_depth.get(depth, 0) for depth in depths]

        # Rysowanie słupków z przesunięciem
        offset = (i - 1) * bar_width
        label_text = algorithm if algorithm == "A*" else algorithm.upper()
        plt.bar(positions + offset, values, width=bar_width, label=label_text)

    # Dodawanie etykiet i legendy
    plt.xlabel('Głębokość rozwiązania')
    match column:
        case 'Steps':
            plt.ylabel('Średnia liczba kroków')
            plt.title('Średnia liczba kroków w zależności od głębokości rozwiązania')
        case 'Visited':
            plt.ylabel('Średnia liczba odwiedzonych stanów')
            plt.title('Średnia liczba odwiedzonych stanów w zależności od głębokości rozwiązania')
        case 'Processed':
            plt.ylabel('Średnia liczba przetworzonych stanów')
            plt.title('Średnia liczba przetworzonych stanów w zależności od głębokości rozwiązania')
        case 'Max_Algo_Depth':
            plt.ylabel('Średnia maksymalna głębokość algorytmu')
            plt.title('Średnia lmaksymalna głębokość algorytmu w zależności od głębokości rozwiązania')
        case 'Time':
            plt.ylabel('Średni czas wykonania [ms]')
            plt.title('Średni czas wykonania w zależności od głębokości rozwiązania')
        case _:
            raise ValueError('Nieznana kolumna' + column)

    plt.xticks(positions, depths)
    plt.legend()
    plt.grid(axis='y')

    # plt.yscale('log')
    # # Ustawienie znaczników tylko na potęgach 10
    # plt.gca().yaxis.set_major_locator(LogLocator(base=10))
    # # Usunięcie mniejszych podziałek
    # plt.gca().yaxis.set_minor_locator(LogLocator(base=10, subs=()))
    #
    # # Formatowanie etykiet
    # formatter = ScalarFormatter()
    # formatter.set_scientific(False)
    # Po ustawieniu skali logarytmicznej:
    plt.yscale('log')

    # Automatyczne dopasowanie do danych
    plt.autoscale(enable=True, axis='y')

    # Pobranie obecnych granic
    ymin, ymax = plt.ylim()

    # Rozszerzenie granic o +/- 1 potęgę 10
    log_ymin = np.floor(np.log10(ymin)) - 1  # Jedna potęga niżej
    log_ymax = np.ceil(np.log10(ymax)) + 1  # Jedna potęga wyżej

    # Ustawienie nowych granic
    plt.ylim(10 ** log_ymin, 10 ** log_ymax)

    # Ustawienie znaczników tylko na potęgach 10
    plt.gca().yaxis.set_major_locator(LogLocator(base=10))
    # Usunięcie mniejszych podziałek
    plt.gca().yaxis.set_minor_locator(LogLocator(base=10, subs=()))

    # Formatowanie etykiet
    def log_format(value, pos):
        exponent = int(np.log10(value))
        return f'$10^{{{exponent}}}$'

    plt.gca().yaxis.set_major_formatter(FuncFormatter(log_format))
    plt.tight_layout()
    plt.show()

# średnie arytmetyczne wyznaczone dla strategii BFS względem głębokości rozwiązania
# z podziałem na poszczególne porządki przeszukiwania

# średnie arytmetyczne wyznaczone dla strategii DFS względem głębokości rozwiązania
# z podziałem na poszczególne porządki przeszukiwania;
def plot_data2(algorithm, df, column):
    data = df.copy()

    # Zamiana "astr" na "A*" dla wyświetlania
    display_name = "A*" if algorithm == "astr" else algorithm.upper()

    # Filtrowanie tylko dla wybranego algorytmu
    filtered_data = data[data['Algorithm'] == algorithm]

    # Wybieranie potrzebnych kolumn
    filtered_data = filtered_data[['Depth_Of_Moves', 'Heuristic/Order', column]]

    # Grupowanie danych
    grouped_data = filtered_data.groupby(['Heuristic/Order', 'Depth_Of_Moves']).mean().reset_index()

    # Zaokrąglanie wartości Steps
    grouped_data[column] = grouped_data[column].round(3)

    # Unikalne wartości
    depths = sorted(grouped_data['Depth_Of_Moves'].unique())
    variants = grouped_data['Heuristic/Order'].unique()

    # Szerokość słupka
    bar_width = 0.25 if len(variants) <= 4 else 0.05

    plt.figure(figsize=(12, 7))
    positions = np.arange(len(depths))

    # Dostosowanie tytułu i etykiet do typu algorytmu
    param_type = "heurystyki" if algorithm == "astr" else "porządku przeszukiwania"

    # Rysowanie słupków dla każdego wariantu
    for i, variant in enumerate(variants):
        subset = grouped_data[grouped_data['Heuristic/Order'] == variant]

        column_by_depth = {row['Depth_Of_Moves']: row[column] for _, row in subset.iterrows()}
        values = [column_by_depth.get(depth, 0) for depth in depths]

        offset = (i - len(variants) / 2 + 0.5) * bar_width
        plt.bar(positions + offset, values, width=bar_width, label=variant.upper())

    # Dodawanie etykiet i legendy
    plt.xlabel('Głębokość rozwiązania')
    match column:
        case 'Steps':
            plt.ylabel(f'Średnia liczba kroków dla {display_name}')
            plt.title(f'{display_name} - średnia liczba kroków w zależności od {param_type}')
        case 'Visited':
            plt.ylabel(f'Średnia liczba odwiedzonych stanów dla {display_name}')
            plt.title(f'{display_name} - średnia liczba odwiedzonych stanów w zależności od {param_type}')
        case 'Processed':
            plt.ylabel(f'Średnia liczba przetworzonych stanów dla {display_name}')
            plt.title(f'{display_name} - średnia liczba przetworzonych stanów w zależności od {param_type}')
        case 'Max_Algo_Depth':
            plt.ylabel(f'Średnia maksymalna głębokość algorytmu dla {display_name}')
            plt.title(f'{display_name} - średnia maksymalna głębokość algorytmu w zależności od {param_type}')
        case 'Time':
            plt.ylabel(f'Średni czas wykonania [ms] dla {display_name}')
            plt.title(f'{display_name} - średni czas wykonania w zależności od {param_type}')
        case _:
            raise ValueError('Nieznana kolumna' + column)

    plt.xticks(positions, depths)
    plt.legend()
    plt.grid(axis='y')

    plt.yscale('log')
    # # Ustawienie znaczników tylko na potęgach 10
    # plt.gca().yaxis.set_major_locator(LogLocator(base=10))
    # # Usunięcie mniejszych podziałek
    # plt.gca().yaxis.set_minor_locator(LogLocator(base=10, subs=()))
    #
    # # Formatowanie etykiet
    # formatter = ScalarFormatter()
    # formatter.set_scientific(False)
    # Po ustawieniu skali logarytmicznej:
    plt.yscale('log')

    # Automatyczne dopasowanie do danych
    plt.autoscale(enable=True, axis='y')

    # Pobranie obecnych granic
    ymin, ymax = plt.ylim()

    # Rozszerzenie granic o +/- 1 potęgę 10
    log_ymin = np.floor(np.log10(ymin)) - 1  # Jedna potęga niżej
    log_ymax = np.ceil(np.log10(ymax)) + 1  # Jedna potęga wyżej

    # Ustawienie nowych granic
    plt.ylim(10 ** log_ymin, 10 ** log_ymax)

    # Ustawienie znaczników tylko na potęgach 10
    plt.gca().yaxis.set_major_locator(LogLocator(base=10))
    # Usunięcie mniejszych podziałek
    plt.gca().yaxis.set_minor_locator(LogLocator(base=10, subs=()))

    # Formatowanie etykiet
    def log_format(value, pos):
        exponent = int(np.log10(value))
        return f'$10^{{{exponent}}}$'

    plt.gca().yaxis.set_major_formatter(FuncFormatter(log_format))
    plt.tight_layout()
    plt.show()

loaded_data = read_data()

params = ['Steps', 'Visited', 'Processed', 'Max_Algo_Depth', 'Time']

for param in params:
    plot_data1(loaded_data, param)
    plot_data2('bfs', loaded_data, param)
    plot_data2('dfs', loaded_data, param)
    plot_data2('astr', loaded_data, param)

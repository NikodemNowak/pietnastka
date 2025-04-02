import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, FuncFormatter
import os
import glob


def read_data():
    """
    Wczytuje dane statystyczne z plików wynikowych i tworzy ramkę danych.

    Returns:
        pd.DataFrame: Dane statystyczne algorytmów przeszukiwania.
    """
    directory = "./additional_info"
    data_rows = []

    # Znajdź wszystkie pliki statystyk
    all_files = glob.glob(os.path.join(directory, "*.txt"))

    for file in all_files:
        file_name = os.path.basename(file)

        try:
            # Parsowanie nazwy pliku, aby uzyskać informacje o algorytmie
            parts = file_name.split('_')
            depth_of_moves = parts[1]
            algorithm = parts[3]
            heuristic_or_order = parts[4]

            # Wczytanie danych z pliku
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

    # Utworzenie ramki danych z odpowiednimi nazwami kolumn
    columns = [
        'Depth_Of_Moves', 'Algorithm', 'Heuristic/Order',
        'Steps', 'Visited', 'Processed', 'Max_Algo_Depth', 'Time'
    ]
    data = pd.DataFrame(data_rows, columns=columns)

    return data


def plot_data1(df, column, ax):
    """
    Tworzy wykres porównujący średnie wartości wybranej metryki dla różnych algorytmów.

    Args:
        df (pd.DataFrame): Ramka danych zawierająca statystyki.
        column (str): Nazwa kolumny z danymi do wizualizacji.
        ax (matplotlib.axes.Axes): Obiekt osi do rysowania wykresu.

    Returns:
        matplotlib.axes.Axes: Zaktualizowany obiekt osi.
    """
    data = df[['Depth_Of_Moves', 'Algorithm', column]].copy()

    # Zamiana "astr" na "A*" dla lepszej czytelności wykresów
    data['Algorithm'] = data['Algorithm'].replace('astr', 'A*')

    # Grupowanie danych według algorytmu i głębokości
    grouped_data = data.groupby(['Algorithm', 'Depth_Of_Moves']).mean().reset_index()
    grouped_data[column] = grouped_data[column].round(3)

    # Uzyskanie unikalnych wartości do wykresu
    depths = sorted(grouped_data['Depth_Of_Moves'].unique())
    algorithms = grouped_data['Algorithm'].unique()
    bar_width = 0.25
    positions = np.arange(len(depths))

    # Ustawienia czcionki
    ax.tick_params(axis='both', which='major', labelsize=14)

    # Rysowanie słupków dla każdego algorytmu
    for i, algorithm in enumerate(algorithms):
        subset = grouped_data[grouped_data['Algorithm'] == algorithm]

        # Mapowanie głębokości na wartości
        values_by_depth = {row['Depth_Of_Moves']: row[column] for _, row in subset.iterrows()}
        values = [values_by_depth.get(depth, 0) for depth in depths]

        # Rysowanie słupków z odpowiednim przesunięciem
        offset = (i - 1) * bar_width
        label_text = algorithm if algorithm == "A*" else algorithm.upper()
        ax.bar(positions + offset, values, width=bar_width, label=label_text)

    # Konfiguracja etykiet i tytułu w zależności od wybranej kolumny
    match column:
        case 'Steps':
            ax.set_ylabel('Średnia liczba kroków', fontsize=16)
        case 'Visited':
            ax.set_ylabel('Średnia liczba odwiedzonych stanów', fontsize=16)
        case 'Processed':
            ax.set_ylabel('Średnia liczba przetworzonych stanów', fontsize=16)
        case 'Max_Algo_Depth':
            ax.set_ylabel('Średnia max głębokość algorytmu', fontsize=16)
        case 'Time':
            ax.set_ylabel('Średni czas wykonania [ms]', fontsize=16)
        case _:
            raise ValueError(f'Nieznana kolumna: {column}')

    ax.set_title('Ogółem', fontsize=16)

    # Konfiguracja osi i skali
    ax.set_xticks(positions, depths)
    ax.legend()
    ax.grid(axis='y')
    ax.set_yscale('log')

    # Automatyczne dopasowanie zakresu skali logarytmicznej
    ax.autoscale(enable=True, axis='y')
    ymin, ymax = ax.get_ylim()

    # Rozszerzenie granic o +/- 1 potęgę 10 dla lepszej czytelności
    log_ymin = np.floor(np.log10(ymin)) - 1
    log_ymax = np.ceil(np.log10(ymax)) + 1
    ax.set_ylim(10 ** log_ymin, 10 ** log_ymax)

    # Formatowanie znaczników osi Y w notacji wykładniczej
    ax.yaxis.set_major_locator(LogLocator(base=10))
    ax.yaxis.set_minor_locator(LogLocator(base=10, subs=()))

    def log_format(value, pos):
        exponent = int(np.log10(value))
        return f'$10^{{{exponent}}}$'

    ax.yaxis.set_major_formatter(FuncFormatter(log_format))

    return ax


def plot_data2(algorithm, df, column, ax, x_label_ok, y_label_ok):
    """
    Tworzy wykres dla konkretnego algorytmu, pokazujący metryki z podziałem
    na warianty (heurystyki lub porządki przeszukiwania).

    Args:
        algorithm (str): Nazwa algorytmu do analizy.
        df (pd.DataFrame): Ramka danych zawierająca statystyki.
        column (str): Nazwa kolumny z danymi do wizualizacji.
        ax (matplotlib.axes.Axes): Obiekt osi do rysowania wykresu.
        x_label_ok (bool): Czy dodać etykietę osi X.
        y_label_ok (bool): Czy dodać etykietę osi Y.

    Returns:
        matplotlib.axes.Axes: Zaktualizowany obiekt osi.
    """
    data = df.copy()

    # Zamiana "astr" na "A*" dla wyświetlania
    display_name = "A*" if algorithm == "astr" else algorithm.upper()

    # Filtrowanie danych tylko dla wybranego algorytmu
    filtered_data = data[data['Algorithm'] == algorithm]
    filtered_data = filtered_data[['Depth_Of_Moves', 'Heuristic/Order', column]]

    # Grupowanie danych według wariantu i głębokości
    grouped_data = filtered_data.groupby(['Heuristic/Order', 'Depth_Of_Moves']).mean().reset_index()
    grouped_data[column] = grouped_data[column].round(3)

    # Uzyskanie unikalnych wartości do wykresu
    depths = sorted(grouped_data['Depth_Of_Moves'].unique())
    variants = grouped_data['Heuristic/Order'].unique()

    # Dostosowanie szerokości słupków do liczby wariantów
    bar_width = 0.25 if len(variants) <= 4 else 0.05
    positions = np.arange(len(depths))

    # Ustawienia czcionki
    ax.tick_params(axis='both', which='major', labelsize=14)

    # Rysowanie słupków dla każdego wariantu
    for i, variant in enumerate(variants):
        subset = grouped_data[grouped_data['Heuristic/Order'] == variant]

        # Mapowanie głębokości na wartości
        column_by_depth = {row['Depth_Of_Moves']: row[column] for _, row in subset.iterrows()}
        values = [column_by_depth.get(depth, 0) for depth in depths]

        # Rysowanie słupków z odpowiednim przesunięciem
        offset = (i - len(variants) / 2 + 0.5) * bar_width
        ax.bar(positions + offset, values, width=bar_width, label=variant.upper())

    # Konfiguracja etykiet i tytułu
    if x_label_ok:
        ax.set_xlabel('Głębokość rozwiązania', fontsize=16)

    match column:
        case 'Steps':
            if y_label_ok:
                ax.set_ylabel('Średnia liczba kroków', fontsize=16)
        case 'Visited':
            if y_label_ok:
                ax.set_ylabel('Średnia liczba odwiedzonych stanów', fontsize=16)
        case 'Processed':
            if y_label_ok:
                ax.set_ylabel('Średnia liczba przetworzonych stanów', fontsize=16)
        case 'Max_Algo_Depth':
            if y_label_ok:
                ax.set_ylabel('Średnia maksymalna głębokość algorytmu', fontsize=16)
        case 'Time':
            if y_label_ok:
                ax.set_ylabel('Średni czas wykonania [ms]', fontsize=16)
        case _:
            raise ValueError(f'Nieznana kolumna: {column}')

    ax.set_title(f'{display_name}', fontsize=16)

    # Konfiguracja osi i skali
    ax.set_xticks(positions)
    ax.set_xticklabels(depths)
    ax.legend()
    ax.grid(axis='y')
    ax.set_yscale('log')

    # Automatyczne dopasowanie zakresu skali logarytmicznej
    ax.autoscale(enable=True, axis='y')
    ymin, ymax = ax.get_ylim()

    # Rozszerzenie granic dla lepszej czytelności
    log_ymin = np.floor(np.log10(ymin)) - 1
    log_ymax = np.ceil(np.log10(ymax)) + 1
    ax.set_ylim(10 ** log_ymin, 10 ** log_ymax)

    # Formatowanie znaczników osi Y w notacji wykładniczej
    ax.yaxis.set_major_locator(LogLocator(base=10))
    ax.yaxis.set_minor_locator(LogLocator(base=10, subs=()))

    def log_format(value, pos):
        exponent = int(np.log10(value))
        return f'$10^{{{exponent}}}$'

    ax.yaxis.set_major_formatter(FuncFormatter(log_format))

    return ax


def create_analysis_figures(data):
    """
    Tworzy serię wykresów analizujących różne metryki wydajności algorytmów.

    Args:
        data (pd.DataFrame): Ramka danych zawierająca statystyki do analizy.

    Returns:
        list: Lista obiektów Figure z utworzonymi wykresami.
    """
    # Parametry do analizy
    params = ['Steps', 'Visited', 'Processed', 'Max_Algo_Depth', 'Time']
    figures = []

    for param in params:
        # Tworzenie figury z 4 wykresami (układ 2x2)
        fig, axs = plt.subplots(2, 2, figsize=(15, 12))

        # Wykres zbiorczy - porównanie wszystkich algorytmów
        plot_data1(data, param, axs[0, 0])

        # Wykresy szczegółowe dla poszczególnych algorytmów
        plot_data2('astr', data, param, axs[0, 1], False, False)  # A* (górny prawy)
        plot_data2('bfs', data, param, axs[1, 0], True, True)  # BFS (dolny lewy)
        plot_data2('dfs', data, param, axs[1, 1], True, False)  # DFS (dolny prawy)

        # Optymalne rozmieszczenie wykresów
        fig.tight_layout()
        figures.append(fig)

    return figures


# Wykonanie analizy
if __name__ == "__main__":
    loaded_data = read_data()
    all_figures = create_analysis_figures(loaded_data)
    plt.show()
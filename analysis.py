import pandas as pd
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



df = read_data()

# Wyświetlenie pierwszych 15 wierszy DataFrame z nagłówkami
print(df.head(15))
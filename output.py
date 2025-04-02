def write_solution(filename: str, found: bool, path: str) -> None:
    """
    Zapisuje rozwiązanie do pliku wyjściowego.

    Parametry:
    ----------
    filename : str
        Ścieżka do pliku wyjściowego
    found : bool
        Flaga określająca czy znaleziono rozwiązanie
    path : str
        Ścieżka ruchów prowadząca do rozwiązania (lub "-1" jeśli nie znaleziono)
    """
    with open(filename, 'w') as f:
        if found:
            # Zapisz długość ścieżki i samą ścieżkę, gdy rozwiązanie istnieje
            f.write(f"{len(path)}\n{path}\n")
        else:
            # Zapisz -1, gdy rozwiązanie nie zostało znalezione
            f.write("-1\n")


def write_stats(filename: str, found: bool, path: str, visited: set,
                processed: int, max_processed_depth: int, time_taken: float) -> None:
    """
    Zapisuje statystyki wykonania algorytmu do pliku.

    Parametry:
    ----------
    filename : str
        Ścieżka do pliku statystyk
    found : bool
        Flaga określająca czy znaleziono rozwiązanie
    path : str
        Ścieżka ruchów prowadząca do rozwiązania
    visited : set
        Zbiór odwiedzonych stanów
    processed : int
        Liczba przetworzonych stanów
    max_processed_depth : int
        Maksymalna głębokość przeszukiwania
    time_taken : float
        Czas wykonania algorytmu w sekundach
    """
    with open(filename, 'w') as f:
        # Długość ścieżki rozwiązania lub -1 jeśli nie znaleziono
        if found:
            f.write(f"{len(path)}\n")
        else:
            f.write("-1\n")

        # Pozostałe statystyki
        f.write(f"{len(visited)}\n")  # Liczba stanów odwiedzonych
        f.write(f"{processed}\n")  # Liczba stanów przetworzonych
        f.write(f'{max_processed_depth}\n')  # Maksymalna osiągnięta głębokość
        f.write(f"{time_taken * 1000:.3f}\n")  # Czas w milisekundach (z dokładnością do 3 miejsc)
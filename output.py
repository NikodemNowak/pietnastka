# Write solution to output file
def write_solution(filename, found, path):
    with open(filename, 'w') as f:
        if found:
            f.write(f"{len(path)}\n{path}\n")
        else:
            f.write("-1\n")

# Write stats to stats file
def write_stats(filename, found, path, visited, processed, max_processed_depth, time_taken):
    with open(filename, 'w') as f:
        if found:
            f.write(f"{len(path)}\n")
        else:
            f.write("-1\n")
        f.write(f"{len(visited)}\n")
        f.write(f"{processed}\n")
        f.write(f'{max_processed_depth}\n')
        f.write(f"{time_taken*1000:.3f}\n")

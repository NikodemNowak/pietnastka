import os
import concurrent.futures
import multiprocessing

def process_file(filename, permutations):
    commands = []
    base_name = filename[:12]
    file_path = f'./boards/{filename}'

    for perm in permutations:
        commands.append(
            f'python solver.py bfs {perm} {file_path} '
            f'./solutions/{base_name}_bfs_{perm.lower()}_sol.txt '
            f'./additional_info/{base_name}_bfs_{perm.lower()}_stats.txt'
        )
        commands.append(
            f'python solver.py dfs {perm} {file_path} '
            f'./solutions/{base_name}_dfs_{perm.lower()}_sol.txt '
            f'./additional_info/{base_name}_dfs_{perm.lower()}_stats.txt'
        )
    commands.append(
        f'python solver.py astr hamm {file_path} '
        f'./solutions/{base_name}_astr_hamm_sol.txt '
        f'./additional_info/{base_name}_astr_hamm_stats.txt'
    )
    commands.append(
        f'python solver.py astr manh {file_path} '
        f'./solutions/{base_name}_astr_manh_sol.txt '
        f'./additional_info/{base_name}_astr_manh_stats.txt'
    )

    for cmd in commands:
        os.system(cmd)

def main():
    permutation = ('RDUL', 'RDLU', 'DRUL', 'DRLU', 'LUDR', 'LURD', 'ULDR', 'ULRD')
    directory = './boards'
    file_list = [
        f for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f))
    ]

    with concurrent.futures.ProcessPoolExecutor(
        max_workers=multiprocessing.cpu_count()
    ) as executor:
        futures = [
            executor.submit(process_file, filename, permutation)
            for filename in file_list
        ]
        concurrent.futures.wait(futures)

if __name__ == '__main__':
    main()
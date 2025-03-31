import os

permutation = ('RDUL', 'RDLU', 'DRUL', 'DRLU', 'LUDR', 'LURD', 'ULDR', 'ULRD')

directory = './boards'
for filename in os.listdir(directory):
    if os.path.isfile(os.path.join(directory, filename)):
        for j in range(8):
            os.system('python solver.py bfs ' + permutation[j] + ' ' + './boards/' + filename + ' ' + './solutions/' + filename[:12] + '_bfs_' + permutation[j].lower() + '_sol.txt' + ' ' + './additional_info/' + filename[:12] + '_bfs_' + permutation[j].lower() + '_stats.txt')
            os.system('python solver.py dfs ' + permutation[j] + ' ' + './boards/' + filename + ' ' + './solutions/' + filename[:12] + '_dfs_' + permutation[j].lower() + '_sol.txt' + ' ' + './additional_info/' + filename[:12] + '_dfs_' + permutation[j].lower() + '_stats.txt')
        os.system('python solver.py astr hamm ' + './boards/' + filename + ' ' + './solutions/' + filename[:12] + '_astr_hamm_sol.txt' + ' ' + './additional_info/' + filename[:12] + '_astr_hamm_stats.txt')
        os.system('python solver.py astr manh ' + './boards/' + filename + ' ' + './solutions/' + filename[:12] + '_astr_manh_sol.txt' + ' ' + './additional_info/' + filename[:12] + '_astr_manh_stats.txt')

f = open("plansza.txt", "r")
rows, cols = map(int, f.readline().split())

def load_board():
    arr = [[0 for _ in range(cols)] for _ in range(rows)]

    for i in range(rows):
        line = f.readline().split()
        for j in range(cols):
            arr[i][j] = int(line[j])

    print(arr)
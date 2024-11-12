from curses.ascii import isalnum


def load_instance(input_file_name: str) -> list[list[int]]:
    global K, N, M
    cells = []

    with open(input_file_name, 'r') as file:
        K = int(next(file))
        N, M = map(int, next(file).split())
        for line in file:
            line = line.split()
            if line:
                line = [int(x) if isalnum(x) else 0 for x in line]
                cells.append(line)

    return cells

def encode_var(k: int, i: int, j: int) -> int:
    return (k+K) * N * M + (i-1) * M + (j-1) + 1

def decode_var(var: int) -> tuple[int, int, int]:
    var -= 1

    k = var // (N * M) - K
    var %= N * M
    i = var // M + 1
    j = var % M + 1

    return k, i, j

def encode(instance: list[list[int]]) -> tuple[list[list[int]], int]:
    clauses = []
    number_of_variables = (2 * K + 1) * N * M

    # 1. Initial values
    for i in range(N):
        for j in range(M):
            if instance[i][j] == 0:
                for k in range(-K, 0):
                    clauses.append([-encode_var(k, i + 1, j + 1)])
            else:
                clauses.append([encode_var(-instance[i][j], i + 1, j + 1)])

    # 2. No zeros
    for i in range(N):
        for j in range(M):
            clauses.append([-encode_var(0, i + 1, j + 1)])

    # 3. Each cell has exactly one value
    # 3.1. Each cell has at least one value
    for i in range(N):
        for j in range(M):
            clauses.append([encode_var(k, i + 1, j + 1) for k in range(-K, K + 1)])

    # 3.2. Each cell has at most one value
    for i in range(N):
        for j in range(M):
            for k1 in range(-K, K + 1):
                for k2 in range(k1 + 1, K + 1):
                    clauses.append([-encode_var(k1, i + 1, j + 1), -encode_var(k2, i + 1, j + 1)])

    # 4. Each start point has exactly one neighbour (cell with path with the same value)
    # 4.1. Each start point has at least one neighbour
    for i in range(N):
        for j in range(M):
            if (k := instance[i][j]) != 0:
                clause = []

                if i > 0: clause.append(encode_var(k, *get_top_neighbour(i + 1, j + 1)))
                if j > 0: clause.append(encode_var(k, *get_left_neighbour(i + 1, j + 1)))
                if i < N - 1: clause.append(encode_var(k, *get_bottom_neighbour(i + 1, j + 1)))
                if j < M - 1: clause.append(encode_var(k, *get_right_neighbour(i + 1, j + 1)))

                if clause: clauses.append(clause)

    # 4.2. Each start point has at most one neighbour
    for i in range(N):
        for j in range(M):
            if (k := instance[i][j]) != 0:
                if 1 < i + 1 < N and 1 < j + 1 < M:
                    # !1 or !2, !1 or !3, !1 or !4, !2 or !3, !2 or !4, !3 or !4
                    clauses.append([-encode_var(k, *get_top_neighbour(i + 1, j + 1)), -encode_var(k, *get_left_neighbour(i + 1, j + 1))])
                    clauses.append([-encode_var(k, *get_top_neighbour(i + 1, j + 1)), -encode_var(k, *get_bottom_neighbour(i + 1, j + 1))])
                    clauses.append([-encode_var(k, *get_top_neighbour(i + 1, j + 1)), -encode_var(k, *get_right_neighbour(i + 1, j + 1))])
                    clauses.append([-encode_var(k, *get_left_neighbour(i + 1, j + 1)), -encode_var(k, *get_bottom_neighbour(i + 1, j + 1))])
                    clauses.append([-encode_var(k, *get_left_neighbour(i + 1, j + 1)), -encode_var(k, *get_right_neighbour(i + 1, j + 1))])
                    clauses.append([-encode_var(k, *get_bottom_neighbour(i + 1, j + 1)), -encode_var(k, *get_right_neighbour(i + 1, j + 1))])

    return clauses, number_of_variables

def get_top_neighbour(i: int, j: int) -> tuple[int, int]:
    return i - 1, j

def get_bottom_neighbour(i: int, j: int) -> tuple[int, int]:
    return i + 1, j

def get_left_neighbour(i: int, j: int) -> tuple[int, int]:
    return i, j - 1

def get_right_neighbour(i: int, j: int) -> tuple[int, int]:
    return i, j + 1

def get_neighbours(i: int, j: int) -> list[tuple[int, int]]:
    return [get_top_neighbour(i, j), get_bottom_neighbour(i, j), get_left_neighbour(i, j), get_right_neighbour(i, j)]

def main():
    pass


if __name__ == '__main__':
    main()

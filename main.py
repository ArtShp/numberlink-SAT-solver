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

    return clauses, number_of_variables

def main():
    pass


if __name__ == '__main__':
    main()

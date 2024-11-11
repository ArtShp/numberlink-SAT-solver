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

    return clauses, number_of_variables

def main():
    pass


if __name__ == '__main__':
    main()

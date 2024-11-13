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

                if i + 1 > 1: clause.append([encode_var(k, *get_top_neighbour(i + 1, j + 1))])
                if j + 1 > 1: clause.append([encode_var(k, *get_left_neighbour(i + 1, j + 1))])
                if i + 1 < N: clause.append([encode_var(k, *get_bottom_neighbour(i + 1, j + 1))])
                if j + 1 < M: clause.append([encode_var(k, *get_right_neighbour(i + 1, j + 1))])

                if clause: clauses.append(clause)

    # 4.2. Each start point has at most one neighbour
    for i in range(N):
        for j in range(M):
            if (k := instance[i][j]) != 0:
                if i + 1 == 1 and j + 1 == 1:  # left top corner
                    # !3 or !4
                    clauses.append([-encode_var(k, *get_bottom_neighbour(i + 1, j + 1)),
                                    -encode_var(k, *get_right_neighbour(i + 1, j + 1))])
                elif i + 1 == 1 and j + 1 == M:  # right top corner
                    # !2 or !3
                    clauses.append([-encode_var(k, *get_left_neighbour(i + 1, j + 1)),
                                    -encode_var(k, *get_bottom_neighbour(i + 1, j + 1))])
                elif i + 1 == N and j + 1 == 1:  # left bottom corner
                    # !1 or !4
                    clauses.append([-encode_var(k, *get_top_neighbour(i + 1, j + 1)),
                                    -encode_var(k, *get_right_neighbour(i + 1, j + 1))])
                elif i + 1 == N and j + 1 == M:  # right bottom corner
                    # !1 or !2
                    clauses.append([-encode_var(k, *get_top_neighbour(i + 1, j + 1)),
                                    -encode_var(k, *get_left_neighbour(i + 1, j + 1))])
                elif i + 1 == 1:  # top
                    # !2 or !3, !2 or !4, !3 or !4
                    clauses.append([-encode_var(k, *get_left_neighbour(i + 1, j + 1)),
                                    -encode_var(k, *get_bottom_neighbour(i + 1, j + 1))])
                    clauses.append([-encode_var(k, *get_left_neighbour(i + 1, j + 1)),
                                    -encode_var(k, *get_right_neighbour(i + 1, j + 1))])
                    clauses.append([-encode_var(k, *get_bottom_neighbour(i + 1, j + 1)),
                                    -encode_var(k, *get_right_neighbour(i + 1, j + 1))])
                elif j + 1 == 1:  # left
                    # !1 or !3, !1 or !4, !3 or !4
                    clauses.append([-encode_var(k, *get_top_neighbour(i + 1, j + 1)),
                                    -encode_var(k, *get_bottom_neighbour(i + 1, j + 1))])
                    clauses.append([-encode_var(k, *get_top_neighbour(i + 1, j + 1)),
                                    -encode_var(k, *get_right_neighbour(i + 1, j + 1))])
                    clauses.append([-encode_var(k, *get_bottom_neighbour(i + 1, j + 1)),
                                    -encode_var(k, *get_right_neighbour(i + 1, j + 1))])
                elif i + 1 == N:  # bottom
                    # !1 or !2, !1 or !4, !2 or !4
                    clauses.append([-encode_var(k, *get_top_neighbour(i + 1, j + 1)),
                                    -encode_var(k, *get_left_neighbour(i + 1, j + 1))])
                    clauses.append([-encode_var(k, *get_top_neighbour(i + 1, j + 1)),
                                    -encode_var(k, *get_right_neighbour(i + 1, j + 1))])
                    clauses.append([-encode_var(k, *get_left_neighbour(i + 1, j + 1)),
                                    -encode_var(k, *get_right_neighbour(i + 1, j + 1))])
                elif j + 1 == M:  # right
                    # !1 or !2, !1 or !3, !2 or !3
                    clauses.append([-encode_var(k, *get_top_neighbour(i + 1, j + 1)),
                                    -encode_var(k, *get_left_neighbour(i + 1, j + 1))])
                    clauses.append([-encode_var(k, *get_top_neighbour(i + 1, j + 1)),
                                    -encode_var(k, *get_bottom_neighbour(i + 1, j + 1))])
                    clauses.append([-encode_var(k, *get_left_neighbour(i + 1, j + 1)),
                                    -encode_var(k, *get_bottom_neighbour(i + 1, j + 1))])
                else:  # center
                    # !1 or !2, !1 or !3, !1 or !4, !2 or !3, !2 or !4, !3 or !4
                    clauses.append([-encode_var(k, *get_top_neighbour(i + 1, j + 1)),
                                    -encode_var(k, *get_left_neighbour(i + 1, j + 1))])
                    clauses.append([-encode_var(k, *get_top_neighbour(i + 1, j + 1)),
                                    -encode_var(k, *get_bottom_neighbour(i + 1, j + 1))])
                    clauses.append([-encode_var(k, *get_top_neighbour(i + 1, j + 1)),
                                    -encode_var(k, *get_right_neighbour(i + 1, j + 1))])
                    clauses.append([-encode_var(k, *get_left_neighbour(i + 1, j + 1)),
                                    -encode_var(k, *get_bottom_neighbour(i + 1, j + 1))])
                    clauses.append([-encode_var(k, *get_left_neighbour(i + 1, j + 1)),
                                    -encode_var(k, *get_right_neighbour(i + 1, j + 1))])
                    clauses.append([-encode_var(k, *get_bottom_neighbour(i + 1, j + 1)),
                                    -encode_var(k, *get_right_neighbour(i + 1, j + 1))])

    # 5. Each path cell has exactly 2 neighbours
    for i in range(N):
        for j in range(M):
            if (k := instance[i][j]) != 0:
                if i + 1 == 1 and j + 1 == 1:  # left top corner
                    clauses += generate_exactly_one_true_for_path(i + 1, j + 1, k, [1, 2])
                elif i + 1 == 1 and j + 1 == M:  # right top corner
                    clauses += generate_exactly_one_true_for_path(i + 1, j + 1, k, [1, 4])
                elif i + 1 == N and j + 1 == 1:  # left bottom corner
                    clauses += generate_exactly_one_true_for_path(i + 1, j + 1, k, [2, 3])
                elif i + 1 == N and j + 1 == M:  # right bottom corner
                    clauses += generate_exactly_one_true_for_path(i + 1, j + 1, k, [3, 4])
                elif i + 1 == 1:  # top
                    clauses += generate_exactly_one_true_for_path(i + 1, j + 1, k, [1])
                elif j + 1 == 1:  # left
                    clauses += generate_exactly_one_true_for_path(i + 1, j + 1, k, [2])
                elif i + 1 == N:  # bottom
                    clauses += generate_exactly_one_true_for_path(i + 1, j + 1, k, [3])
                elif j + 1 == M:  # right
                    clauses += generate_exactly_one_true_for_path(i + 1, j + 1, k, [4])
                else:  # center
                    clauses += generate_exactly_one_true_for_path(i + 1, j + 1, k)

    return clauses, number_of_variables

def foo_1(i: int, j: int, k: int, sides: tuple[int, int]) -> list[list[int]]:
    neighbours = get_neighbours(i, j)

    all_sides = (1, 2, 3, 4)
    sides = list(set(all_sides) - set(sides))

    K1, K2 = encode_var(-k, *neighbours[sides[0] - 1]), encode_var(-k, *neighbours[sides[1] - 1])
    C1, C2 = encode_var(k, *neighbours[sides[0] - 1]), encode_var(k, *neighbours[sides[1] - 1])

    clauses = [
        [K1, K2, C1, C2],
        [K1, K2, C1, -C2],
        [K1, K2, -C1, C2],
        [K1, -K2, C1, C2],
        [-K1, K2, C1, C2],
        [K1, -K2, C1, -C2],
        [-K1, K2, -C1, C2]
    ]

    return clauses

def foo_2(i: int, j: int, k: int, side: int) -> list[list[int]]:
    neighbours = get_neighbours(i, j)
    neighbours.pop(side - 1)

    K1, K2, K3 = encode_var(-k, *neighbours[0]), encode_var(-k, *neighbours[1]), encode_var(-k, *neighbours[2])
    C1, C2, C3 = encode_var(k, *neighbours[0]), encode_var(k, *neighbours[1]), encode_var(k, *neighbours[2])

    clauses = [
        [K1, K2, K3, C1, C2, C3],
        [K1, K2, K3, C1, C2, -C3],
        [K1, K2, K3, C1, -C2, C3],
        [K1, K2, K3, -C1, C2, C3],
        [K1, K2, -K3, C1, C2, C3],
        [K1, -K2, K3, C1, C2, C3],
        [-K1, K2, K3, C1, C2, C3],
        [K1, K2, -K3, C1, C2, -C3],
        [K1, -K2, K3, C1, -C2, C3],
        [-K1, K2, K3, -C1, C2, C3],
        [K1, K2, K3, -C1, -C2, -C3],
        [K1, K2, -K3, -C1, -C2, -C3],
        [K1, -K2, K3, -C1, -C2, -C3],
        [-K1, K2, K3, -C1, -C2, -C3],
        [K1, -K2, -K3, -C1, -C2, -C3],
        [-K1, K2, -K3, -C1, -C2, -C3],
        [-K1, -K2, K3, -C1, -C2, -C3],
        [-K1, -K2, -K3, -C1, -C2, -C3],
    ]

    return clauses

def generate_exactly_one_true_for_path(i: int, j: int, k: int, sides: list[int] = None) -> list[list[int]]:
    all_sides = [1, 2, 3, 4]
    sides = list(set(all_sides) - set(sides))

    s = len(sides)

    neighbours = get_neighbours(i, j)

    Ks = [encode_var(-k, *neighbours[side - 1]) for side in sides]
    Cs = [encode_var(k, *neighbours[side - 1]) for side in sides]

    # At least one is true
    clauses = [Ks + Cs]

    for a in range(s):
        clauses += [
            Ks + Cs[:a] + [-Cs[a]] + Cs[a + 1:],
            Ks[:a] + [-Ks[a]] + Ks[a + 1:] + Cs,
            Ks[:a] + [-Ks[a]] + Ks[a + 1:] + Cs[:a] + [-Cs[a]] + Cs[a + 1:]
        ]

    # At most one is true
    expressions = []
    for a in range(s):
        for b in range(a + 1, s):
            expressions.append([-Ks[a], -Ks[b]])
            expressions.append([-Cs[a], -Cs[b]])

    for a in range(s):
        for b in range(s):
            if a != b:
                expressions.append([-Ks[a], -Cs[b]])

    for a in range(len(expressions)):
        for b in range(a + 1, len(expressions)):
            clauses.append(expressions[a] + expressions[b])

    return clauses

def get_top_neighbour(i: int, j: int) -> tuple[int, int]:
    return i - 1, j

def get_left_neighbour(i: int, j: int) -> tuple[int, int]:
    return i, j - 1

def get_bottom_neighbour(i: int, j: int) -> tuple[int, int]:
    return i + 1, j

def get_right_neighbour(i: int, j: int) -> tuple[int, int]:
    return i, j + 1

def get_neighbours(i: int, j: int) -> list[tuple[int, int]]:
    return [get_top_neighbour(i, j), get_left_neighbour(i, j), get_bottom_neighbour(i, j), get_right_neighbour(i, j)]

def main():
    pass


if __name__ == '__main__':
    main()

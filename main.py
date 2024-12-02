import subprocess
from subprocess import CompletedProcess
from argparse import ArgumentParser


def load_instance(input_file_name: str) -> list[list[int]]:
    global K, N, M
    cells = []

    with open(input_file_name, 'r') as file:
        K = int(next(file))
        N, M = map(int, next(file).split())
        for line in file:
            line = line.strip().split()
            if line:
                line = [int(x) if x.isdigit() else 0 for x in line]
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

                if i + 1 > 1: clause.append(encode_var(k, *get_top_neighbour(i + 1, j + 1)))
                if j + 1 > 1: clause.append(encode_var(k, *get_left_neighbour(i + 1, j + 1)))
                if i + 1 < N: clause.append(encode_var(k, *get_bottom_neighbour(i + 1, j + 1)))
                if j + 1 < M: clause.append(encode_var(k, *get_right_neighbour(i + 1, j + 1)))

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
            for k in range(1, K + 1):
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

def generate_exactly_one_true_for_path(i: int, j: int, k: int, sides: list[int] = ()) -> list[list[int]]:
    all_sides = [1, 2, 3, 4]
    sides = list(set(all_sides) - set(sides))

    s = len(sides)

    neighbours = get_neighbours(i, j)

    C = encode_var(k, i, j)

    Ks = [encode_var(-k, *neighbours[side - 1]) for side in sides]
    Cs = [encode_var(k, *neighbours[side - 1]) for side in sides]

    # At least one is true
    clauses = [[-C] + Ks + Cs]

    for a in range(s):
        clauses += [
            [-C] + Ks + Cs[:a] + [-Cs[a]] + Cs[a + 1:],
            [-C] + Ks[:a] + [-Ks[a]] + Ks[a + 1:] + Cs,
            [-C] + Ks[:a] + [-Ks[a]] + Ks[a + 1:] + Cs[:a] + [-Cs[a]] + Cs[a + 1:]
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
            clauses.append([-C] + expressions[a] + expressions[b])

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

def write_cnf(clauses: list[list[int]], number_of_variables: int, output_file_name: str) -> None:
    with open(output_file_name, 'w') as file:
        file.write(f'p cnf {number_of_variables} {len(clauses)}\n')
        for clause in clauses:
            file.write(' '.join(map(str, clause)) + ' 0\n')

def call_solver(cnf_formula_file: str, solver_name: str, verbosity: int) -> CompletedProcess[bytes]:
    return subprocess.run([f"./{solver_name}", '-model', f"-verb={verbosity}", cnf_formula_file],
                          stdout=subprocess.PIPE)

def print_result(result: CompletedProcess[bytes], result_file: str = None) -> None:
    for line in result.stdout.decode('utf-8').split('\n'):
        print(line)

    if result.returncode == 20:
        return

    model = []
    for line in result.stdout.decode('utf-8').split('\n'):
        if line.startswith("v"):
            vars = line.split(" ")
            vars.remove("v")
            model.extend(int(v) for v in vars)
    model.remove(0)

    print()
    print("#################################################")
    print("############[ Human readable result ]############")
    print("#################################################")
    print()

    cells = [[0 for _ in range(M)] for _ in range(N)]

    for var in model:
        if var > 0:
            k, i, j = decode_var(var)
            cells[i - 1][j - 1] = abs(k)

    max_num_len = len(str(K))

    for row in cells:
        for cell in row:
            print(cell, end=' ' * (max_num_len - len(str(cell)) + 1))
        print()

    if result_file:
        with open(result_file, 'w') as output:
            for row in cells:
                for cell in row:
                    print(cell, end=' ' * (max_num_len - len(str(cell)) + 1), file=output)
                print(file=output)


def main():
    parser = ArgumentParser()

    parser.add_argument(
        "-i",
        "--input",
        default="input.in",
        type=str,
        help=(
            "The instance file."
        ),
    )
    parser.add_argument(
        "-o",
        "--output",
        default="formula.cnf",
        type=str,
        help=(
            "Output file for the DIMACS format (i.e. the CNF formula)."
        ),
    )
    parser.add_argument(
        "-s",
        "--solver",
        default="glucose-syrup",
        type=str,
        help=(
            "The SAT solver to be used."
        ),
    )
    parser.add_argument(
        "-v",
        "--verb",
        default=1,
        type=int,
        choices=range(0, 2),
        help=(
            "Verbosity of the SAT solver used."
        ),
    )
    parser.add_argument(
        "-r",
        "--result",
        default=None,
        type=str,
        help=(
            "File for solved puzzle."
        ),
    )
    args = parser.parse_args()

    instance = load_instance(args.input)
    clauses, number_of_variables = encode(instance)
    write_cnf(clauses, number_of_variables, args.output)
    result = call_solver(args.output, args.solver, args.verb)

    print_result(result, args.result)


if __name__ == '__main__':
    main()

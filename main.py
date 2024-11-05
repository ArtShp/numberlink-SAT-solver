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

def main():
    pass


if __name__ == '__main__':
    main()

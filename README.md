# Numberlink SAT Solver

# Problem description

Here is a [link](https://en.wikipedia.org/wiki/Numberlink) to game description.

The player has to pair up all the matching numbers on the grid with single continuous lines (or paths). The lines cannot branch off or cross over each other, and the numbers have to fall at the end of each line (i.e., not in the middle).

It is considered that a problem is well-designed only if it has a unique solution and all the cells in the grid are filled, although some Numberlink designers do not stipulate this.

The field is a $N \times M$ grid. In the cells there are situated $K$ pairs of natural numbers from $1$ to $K$, in each cell at most one number.

## Input file format

Input file is a normal text file. It represents a puzzle field to be solved.

The first row has the only number $K$. The second row has numbers $N$ and $M$, that represent number of rows and columns respectively, separated with a whitespace.

Next $N$ rows consist of $M$ elements each. An element represents a specific cell.
If there's a number in the game field, we copy it in the cell.
If there's an empty cell, we use a dot ('.') symbol instead.

### Example of input file

```text
5
7 7
. . . 4 . . .
. 3 . . 2 5 .
. . . 3 1 . .
. . . 5 . . .
. . . . . . .
. . 1 . . . .
2 . . . 4 . .
```

## Result file format

Result file is a normal text file. It represents a solved puzzle.

It consists of $N$ rows, each with $M$ elements. An element represents a specific cell. Elements are separated with whitespaces.

Each cell is a number from $1$ to $K$, which represents either cell of a path corresponding to specific number or an end point of a path.

### Example of result file

```text
2 2 2 4 4 4 4
2 3 2 2 2 5 4
2 3 3 3 1 5 4
2 5 5 5 1 5 4
2 5 1 1 1 5 4
2 5 1 5 5 5 4
2 5 5 5 4 4 4
```

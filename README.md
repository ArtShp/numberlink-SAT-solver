# Numberlink SAT Solver

## Problem description

Here is a [link](https://en.wikipedia.org/wiki/Numberlink) to game description.

The player has to pair up all the matching numbers on the grid with single continuous lines (or paths). The lines cannot branch off or cross over each other, and the numbers have to fall at the end of each line (i.e., not in the middle).

It is considered that a problem is well-designed only if it has a unique solution and all the cells in the grid are filled, although some Numberlink designers do not stipulate this.

The field is a $N \times M$ grid. In the cells there are situated $K$ pairs of natural numbers from $1$ to $K$, in each cell at most one number.

### Input file format

Input file is a normal text file. It represents a puzzle field to be solved.

The first row has the only number $K$. The second row has numbers $N$ and $M$, that represent number of rows and columns respectively, separated with a whitespace.

Next $N$ rows consist of $M$ elements each. An element represents a specific cell.
If there's a number in the game field, we copy it in the cell.
If there's an empty cell, we use a dot ('.') symbol instead.

#### Example of input file

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

### Result file format

Result file is a normal text file. It represents a solved puzzle.

It consists of $N$ rows, each with $M$ elements. An element represents a specific cell. Elements are separated with whitespaces.

Each cell is a number from $1$ to $K$, which represents either cell of a path corresponding to specific number or an end point of a path.

#### Example of result file

```text
2 2 2 4 4 4 4
2 3 2 2 2 5 4
2 3 3 3 1 5 4
2 5 5 5 1 5 4
2 5 1 1 1 5 4
2 5 1 5 5 5 4
2 5 5 5 4 4 4
```

## Encoding

The problem is encoded using one set of variables.
Variables $P(k, i, j)$ represents whether at position $(i, j)$ is number $k$.
Specifically, $i \in \{1, \dots, N\}$, $j \in \{1, \dots, M\}$ and $k \in \{-K, \dots, -1, 0, 1, \dots, K\}$.

Coordinates $(i, j)$ represents usual matrix coordinates, so $i$ goes top to bottom and $j$ goes left-to-right.

If $k < 0$ (let $k = -c$), then it represents end point number $-k$ (here $c$).
E.g. variable $P(-3, 1, 2)$ represents the fact, that on position $(1, 2)$ there is end point number $3$.

If $k > 0$, then it represents path cell with number $k$.
E.g. variable $P(3, 1, 2)$ represents the fact, that on position $(1, 2)$ there is path cell with number $3$.

If $k = 0$, then it represents empty cell.
E.g. variable $P(0, 1, 2)$ represents the fact, that on position $(1, 2)$ there is an empty cell.

### Axioms

1. Each cell has exactly one label (number), i.e. from $-K$ to $K$.

$$
\forall i, j : \bigvee_{k}{p_{k,i,j}} \\
\forall i, j : \bigwedge_{k_1 \neq k_2}{\neg p_{k_1,i,j} \lor \neg p_{k_2,i,j}}
$$

2. There is no cells with $0$. This actually means that all cells should be filled.

$$
\bigwedge_{i,j}{\neg p_{0,i,j}}
$$

3. Input data are not changed.

$$
\forall i,j; k \in \{1, \dots, K\} : p_{-k, i, j} \iff \text{cell $(i, j)$ has input value $k$} \\
\forall i,j; k \in \{1, \dots, K\} : \neg p_{-k, i, j} \iff \text{cell $(i, j)$ has not input value $k$}
$$

4. Each end point has exactly one neighbor represented as path cell with the same number.
Thus we prohibit to have more or less than one neighbor with the same number, but there're no limitations for neighbors with different numbers.

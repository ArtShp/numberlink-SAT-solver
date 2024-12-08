# Numberlink SAT Solver

This is a solution to homework for Propositional and Predicate Logic (NAIL062), UK MFF.

The provided Python code encodes, solves, and decodes the numberlink puzzle via reduction to SAT (i.e. propositional logic formula).

## Table of Contents

- [Problem Description](#problem-description)
- [Input File Format](#input-file-format)
- [Result File Format](#result-file-format)
- [Encoding](#encoding)
- [Axioms](#axioms)
- [Installation](#installation)
- [User Documentation](#user-documentation)
- [Example Instances](#example-instances)
- [Experiments](#experiments)
- [License](#license)

## Problem description

Here is a [link](https://en.wikipedia.org/wiki/Numberlink) to the game description.

The player has to pair up all the matching numbers on the grid with single continuous lines (or paths). The lines cannot branch off or cross over each other, and the numbers have to fall at the end of each line (i.e., not in the middle).

It is considered that a problem is well-designed only if it has a unique solution and all the cells in the grid are filled, although some Numberlink designers do not stipulate this.

The field is an $N \times M$ grid. In the cells there are situated $K$ pairs of natural numbers from $1$ to $K$, in each cell at most one number.

### Input file format

The input file is a normal text file representing a puzzle field to be solved.

The first row contains the number $K$.
The second row contains the numbers $N$ and $M$, representing number of rows and columns respectively, separated by a whitespace.

The next $N$ rows consist of $M$ elements each, where each element represents a specific cell.
If there is a number in the game field, it is copied into the cell.
If there is an empty cell, a dot ('.') symbol is used instead.

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

The result file is a normal text file representing a solved puzzle.

It consists of two parts: the first part is a matrix of numbers, and the second part is a matrix of paths between nodes representing the solved puzzle.

Each part consists of $N$ rows, each with $M$ elements. Each element represents a specific cell, and elements are separated by whitespaces.

Each cell is a number from $1$ to $K$. In the first part, it represents either a cell of a path corresponding to a specific number or an end point of a path. In the second part, it represents either an end point or a path cell.

#### Example of result file

```text
2 2 2 4 4 4 4
2 3 2 2 2 5 4
2 3 3 3 1 5 4
2 5 5 5 1 5 4
2 5 1 1 1 5 4
2 5 1 5 5 5 4
2 5 5 5 4 4 4

┌ ─ ┐ 4 ─ ─ ┐
| 3 └ ─ 2 5 |
| └ ─ 3 1 | |
| ┌ ─ 5 | | |
| | ┌ ─ ┘ | |
| | 1 ┌ ─ ┘ |
2 └ ─ ┘ 4 ─ ┘
```

## Encoding

The problem is encoded using a single set of variables.
Variables $p_{k,i,j}$ represents whether the number $k$ is at position $(i, j)$.
Specifically, $i \in \{1, \dots, N\}$, $j \in \{1, \dots, M\}$ and $k \in \{-K, \dots, -1, 0, 1, \dots, K\}$.

Coordinates $(i, j)$ represent usual matrix coordinates, so $i$ goes top to bottom and $j$ goes from left to right.

If $k < 0$ (let $k = -c$), then it represents the end point number $-k$ (here $c$).
E.g. variable $p_{-3,1,2}$ represents the fact that at position $(1, 2)$ there is end point number $3$.

If $k > 0$, then it represents path cell with number $k$.
E.g. variable $p_{3,1,2}$ represents the fact that at position $(1, 2)$ there is path cell with number $3$.

If $k = 0$, then it represents empty cell.
E.g. variable $p_{0,1,2}$ represents the fact that at position $(1, 2)$ there is an empty cell.

### Axioms

1. Each cell has exactly one label (number), i.e., from $-K$ to $K$.

$$
\forall i, j : \bigvee_{k}{p_{k,i,j}} \\
\forall i, j : \bigwedge_{k_1 \neq k_2}{\neg p_{k_1,i,j} \lor \neg p_{k_2,i,j}}
$$

2. There are no cells with $0$. This means that all cells should be filled.

$$
\bigwedge_{i,j}{\neg p_{0,i,j}}
$$

3. The input data do not change.

$$
\begin{align*}
\forall i,j; k \in \{1, \dots, K\} : p_{-k, i, j} &\iff \text{cell $(i, j)$ has input value $k$} \\
\forall i,j; k \in \{1, \dots, K\} : \neg p_{-k, i, j} &\iff \text{cell $(i, j)$ has not input value $k$}
\end{align*}
$$

4. Each end point has exactly one neighbour represented as path cell with the same number.
Thus, we prohibit having more or less than one neighbour with the same number, but there are no limitations for neighbours with different numbers.
This condition states that from each end point there is exactly one path.
It's described by two conditions: if there is an end point, then there is at least one and at most one path cell with the same number.

$$
\begin{align*}
\forall k \in \{1, \dots, K\} : \forall i, j : p_{-k,i,j} \Rightarrow \bigvee_{(i',j') \in \text{neighbours}(i,j)}{p_{k,i',j'}} \\
\forall k \in \{1, \dots, K\} : \forall i, j : p_{-k,i,j} \Rightarrow \bigwedge_{(i_1,j_1) \neq (i_2,j_2) \in \text{neighbours}(i,j)}{\neg p_{k,i_1,j_1} \land \neg p_{k,i_2,j_2}}
\end{align*}
$$

5. Each path point has exactly two neighbours with the same number, which can be represented either as an end point or path cell.
Thus, we prohibit having more or less than two neighbour with the same number, but there are no limitations for neighbours with different numbers.
This condition states that each path cell is connected to exactly two other path cells, so the path neither branches nor breaks.
It's described by three conditions: if there is a path cell, then there are at least two and at most two neighbours with the same number.

$$
\begin{align*}
\forall k \in \{1, \dots, K\} : \forall i, j : p_{k,i,j} \Rightarrow \\
\bigvee_{(i_1,j_1) \neq (i_2,j_2) \in \text{neighbours}(i,j)}(
p_{k,i_1,j_1} \land p_{k,i_2,j_2}) \\
\lor (p_{-k,i_1,j_1} \land p_{k,i_2,j_2}) \\
\lor (p_{-k,i_1,j_1} \land p_{-k,i_2,j_2})
\end{align*}
$$

$$
\begin{align*}
\forall k \in \{1, \dots, K\} : \forall i, j : p_{k,i,j} \Rightarrow \\
\bigwedge_{(i_1,j_1) \neq (i_2,j_2) \neq (i_3, j_3) \neq (i_1, j_1) \in \text{neighbours}(i,j)}(
\neg p_{k,i_1,j_1} \land \neg p_{k,i_2,j_2} \land \neg p_{k,i_3,j_3}) \\
\land (\neg p_{-k,i_1,j_1} \land \neg p_{k,i_2,j_2} \land \neg p_{k,i_3,j_3}) \\
\land (\neg p_{-k,i_1,j_1} \land \neg p_{-k,i_2,j_2} \land \neg p_{k,i_3,j_3}) \\
\land (\neg p_{-k,i_1,j_1} \land \neg p_{-k,i_2,j_2} \land \neg p_{-k,i_3,j_3})
\end{align*}
$$

## Installation

The SAT solver used is [Glucose](https://www.labri.fr/perso/lsimon/research/glucose/), specifically [Glucose 4.2.1](https://github.com/audemard/glucose/releases/tag/4.2.1).
The source code can be compiled using the following commands:

```bash
cmake .
make
```

This example includes a compiled UNIX binary of the Glucose solver.
For the best experience, it is recommended that users compile the SAT solver themselves.
Note that the solver and the Python script are assumed to work on UNIX-based systems.
If you prefer using Windows, it is recommended to use WSL.

## User documentation

Basic usage example:

```bash
numberlink.py [-h] [-i INPUT] [-o OUTPUT] [-r RESULT] [-s SOLVER] [-v {0,1}]
```

Available command-line options:

- `-h`, `--help` : Show a help message.
- `-i INPUT`, `--input INPUT` : An instance file. Default: "input.in".
- `-o OUTPUT`, `--output OUTPUT` : Output file for the [DIMACS](https://jix.github.io/varisat/manual/0.2.0/formats/dimacs.html) format (i.e. the CNF formula).
- `-r RESULT`, `--result RESULT` : Solved puzzle file. By default, no result is printed to a file.
- `-s SOLVER`, `--solver SOLVER` : The SAT solver to be used.
- `-v {0,1}`, `--verb {0,1}` :  Verbosity of the SAT solver used.

## Example instances

In the `instances` directory there are several example instances:

- `input-7by7.in` : A $7 \times 7$ easily solvable instance.
- `input-7by7-unsat.in` : A $7 \times 7$ easy unsolvable instance.
- `input-13by13.in` : A $13 \times 13$ moderately solvable instance.
- `input-13by13-unsat.in` : A $13 \times 13$ moderately unsolvable instance.
- `input-10by40.in` : A $10 \times 40$ difficult-to-solve instance.
- `input-20by20.in` : A $20 \times 20$ difficult-to-solve instance.
- `input-20by20-many-nodes.in` : A $20 \times 20$ difficult-to-solve instance with a relatively large $K$.
- `input-30by30.in` : A $30 \times 30$ extremely difficult-to-solve instance, not computable in an adequate time.
- `input-30by30-many-nodes.in` : A $30 \times 30$ moderately solvable instance with a relatively large $K$.
- `input-40by40.in` : A $40 \times 40$ extremely difficult-to-solve instance, not computable in an adequate time.

In the `instances/results` directory the results of the solved instances are presented.

## Experiments

The experiments were run on Intel Core i7-12700H CPU (2.30 GHz, up to 4.70 Ghz) and 8 GB RAM on Ubuntu inside WSL2 (Windows 11).

| Instance    | Time (s) |
|-------------|----------|
| 7x7         | 0.03     |
| 7x7 unsat   | 0.03     |
| 10x40       | 2        |
| 13x13       | 0.07     |
| 13x13 unsat | 0.055    |
| 20x20       | 97       |
| 20x20 many  | 5        |
| 30x30       | \> 10000 |
| 30x30 many  | 321      |
| 40x40       | \> 10000 |

It was discovered that the more nodes (end points) there are, the less time it takes to solve the puzzle.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.

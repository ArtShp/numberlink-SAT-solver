# Numberlink SAT Solver

This is a solution to homework for Propositional and Predicate Logic (NAIL062).
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
- [License](#license)

## Problem description

Here is a [link](https://en.wikipedia.org/wiki/Numberlink) to game description.

The player has to pair up all the matching numbers on the grid with single continuous lines (or paths). The lines cannot branch off or cross over each other, and the numbers have to fall at the end of each line (i.e., not in the middle).

It is considered that a problem is well-designed only if it has a unique solution and all the cells in the grid are filled, although some Numberlink designers do not stipulate this.

The field is an $N \times M$ grid. In the cells there are situated $K$ pairs of natural numbers from $1$ to $K$, in each cell at most one number.

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

It consists of two parts. The first part is a matrix of numbers. The second part is a matrix of paths between nodes, that represents the solved puzzle.

Each part consists of $N$ rows, each with $M$ elements. An element represents a specific cell. Elements are separated with whitespaces.

Each cell is a number from $1$ to $K$, which for the first part represents either cell of a path corresponding to specific number or an end point of a path and for the second part represents either an end point or path cell.

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

3. Input data do not change.

$$
\begin{align*}
\forall i,j; k \in \{1, \dots, K\} : p_{-k, i, j} &\iff \text{cell $(i, j)$ has input value $k$} \\
\forall i,j; k \in \{1, \dots, K\} : \neg p_{-k, i, j} &\iff \text{cell $(i, j)$ has not input value $k$}
\end{align*}
$$

4. Each end point has exactly one neighbor represented as path cell with the same number.
Thus, we prohibit to have more or less than one neighbor with the same number, but there are no limitations for neighbors with different numbers.
This condition says that from each end point there is exactly one path.
It's described by two conditions: if there is an end point, then there is at least one and at most one path cell with the same number.

$$
\begin{align*}
\forall k \in \{1, \dots, K\} : \forall i, j : p_{-k,i,j} \Rightarrow \bigvee_{(i',j') \in \text{neighbours}(i,j)}{p_{k,i',j'}} \\
\forall k \in \{1, \dots, K\} : \forall i, j : p_{-k,i,j} \Rightarrow \bigwedge_{(i_1,j_1) \neq (i_2,j_2) \in \text{neighbours}(i,j)}{\neg p_{k,i_1,j_1} \land \neg p_{k,i_2,j_2}}
\end{align*}
$$

5. Each path point has exactly two neighbors with the same number, which can be represented either as an end point or path cell.
Thus, we prohibit to have more or less than two neighbor with the same number, but there are no limitations for neighbors with different numbers.
This condition says that each path cell is connected to exactly two other path cells, so the path neither branches nor breaks.
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

The SAT solver used is [Glucose](https://www.labri.fr/perso/lsimon/research/glucose/), more specifically [Glucose 4.2.1](https://github.com/audemard/glucose/releases/tag/4.2.1). The source code is compiled using

```bash
cmake .
make
```

This example contains a compiled UNIX binary of the Glucose solver.
For optimal experience, I encourage the user to compile the SAT solver themselves.
Note that the solver, as well as the Python script, are assumed to work on UNIX-based systems.
In case you prefer using Windows, I recommend to use WSL.

## User documentation

Basic usage:

```bash
numberlink.py [-h] [-i INPUT] [-o OUTPUT] [-r RESULT] [-s SOLVER] [-v {0,1}]
```

Command-line options:

- `-h`, `--help` : Show a help message.
- `-i INPUT`, `--input INPUT` : An instance file. Default: "input.in".
- `-o OUTPUT`, `--output OUTPUT` : Output file for the DIMACS format (i.e. the CNF formula).
- `-r RESULT`, `--result RESULT` : Solved puzzle file. By default, no result is printed to a file.
- `-s SOLVER`, `--solver SOLVER` : The SAT solver to be used.
- `-v {0,1}`, `--verb {0,1}` :  Verbosity of the SAT solver used.

## Example instances

- `input-7by7.in` : A $7 \times 7$ easy-solvable instance.
- `input-13by13.in` : A $13 \times 13$ medium-solvable instance.
- `input-10by40.in` : A $10 \times 40$ hardly solvable instance.
- `input-20by20.in` : A $20 \times 20$ hardly solvable instance.
- `input-20by20-many-nodes.in` : A $20 \times 20$ hardly solvable instance with relatively big $K$.
- `input-30by30.in` : A $30 \times 30$ extremely hard solvable instance, not computable in adequate time.
- `input-40by40.in` : A $40 \times 40$ extremely hard solvable instance, not computable in adequate time.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.

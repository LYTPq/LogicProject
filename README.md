# Peaceably Co-existing Armies of Queens

# 1. Problem description

We are given:

- a board size $n$ (the board is $n$ x $n$)
- an army size $m$

We need to place $m$ white queens and $m$ black queens on the board such that:

- every cell holds at most one queen
- no white queen attacks a black queen.

Queens of the same color can attack each other.
A queen attacks along its row, its column and both of its diagonals.

Equivalently (even with blocking, since two consecutive queens of different colors on a line attack each other), no row, column, or diagonal(in either direction) may contain queens of both colors.

Formally: let $P = \{0,\dots,n-1\}^2$ be the set of cells.
We ask whether there exist sets $W, B \subseteq P$ (white and black queens) such that

- $W \cap B = \emptyset$
- $|W| = |B| = m$
- for every line $L$ (row, column, or diagonal): $L \cap W = \emptyset$ or $L \cap B = \emptyset$

The original problem asks for the largest such $m$. This is its decision version: for given $n$ and $m$, is a placement possible?

The input format:

```
n m
```

Where:

- `n` – size of the board
- `m` – number of queens of each color

## 2. Encoding

### Variables

For each cell $(r, c)$, $0 \le r, c < n$:

- variable $w_{r,c}$ represents "a white queen stands on $(r, c)$"
- variable $b_{r,c}$ represents "a black queen stands on $(r, c)$"

They are numbered row by row, white first:

```
w(r, c) = r*n + c + 1          (1 … n²)
b(r, c) = n² + r*n + c + 1     (n²+1 … 2n²)
```

Total number of Boolean variables: $2n^2$, plus helper variables for counting queens.

### Constraints

1. Every cell holds at most one queen

```
¬w(r,c) ∨ ¬b(r,c)          for every cell (r, c)
```

2. No white queen attacks a black queen

```
¬w(r1,c1) ∨ ¬b(r2,c2)      for every two different cells that are on
                           the same row, column or diagonal
```

Two cells are on the same diagonal if $r_1 - c_1 = r_2 - c_2$, and on the same anti-diagonal if $r_1 + c_1 = r_2 + c_2$.

3. At least $m$ queens of each color

It is enough to require at least $m$ queens of each color: removing a queen never creates an attack, so any solution with more than $m$ queens of a color can be reduced to exactly $m$.

We count the queens of one color with a sequential counter. For the cell variables $x_1, \dots, x_L$ of that color ($L = n^2$), helper variable $s_{i,j}$ means "at least $j$ of $x_1, \dots, x_i$ are true", for $1 \le j \le m$:

```
¬s(1,1) ∨ x1
¬s(1,j)                              for j > 1
¬s(i,1) ∨ s(i-1,1) ∨ x_i             for i > 1
¬s(i,j) ∨ s(i-1,j) ∨ x_i             for i > 1, j > 1
¬s(i,j) ∨ s(i-1,j) ∨ s(i-1,j-1)      for i > 1, j > 1
s(L,m)
```

Last clause says "at least $m$ in total". Other clauses make sure this can't be true unless there really are $m$ cells with a queen

This adds $n^2 m$ helper variables and about $2 n^2 m$ clauses per color.

### Alternatives

* **Line coloring.** One variable per line ("this line is white") instead of pairwise attack clauses: $8n^2 - 8$ clauses instead of about $\frac{10}{3}n^3$. It is correct but not faster.
* **Naive counting.** For every group of $n^2 - m + 1$ cells, one clause saying at least one of them has a queen. No helper variables, but too many clauses.
* **Totalizer.** Count each half of the cells recursively and add the counts in a tree. Similar size to the sequential counter.
* **"Exactly m" instead of "at least m".** More clauses, same answers.


## User documentation

Basic usage:
```
peaceable_queens.py [-h] [-i INPUT] [-o OUTPUT] [-s SOLVER] [-v {0,1}]
```

Command-line options:

* `-h`, `--help` : Show a help message and exit.
* `-i INPUT`, `--input INPUT` : The instance file. Default: "instances/input.in".
* `-o OUTPUT`, `--output OUTPUT` : Output file for the DIMACS format (i.e. the CNF formula). Default: "formula.cnf".
* `-s SOLVER`, `--solver SOLVER` : The SAT solver to be used. Default: "./glucose".
* `-v {0,1}`, `--verb {0,1}` : Verbosity of the SAT solver used.


The script prints the whole output of the SAT solver, then the result in a human-readable format: the board with `W` for a white queen, `B` for a black queen and `.` for an empty cell, or a message that no placement exists. After decoding, the placement is checked directly in Python, without the CNF, and the result is printed as `Check: OK` or `Check: FAILED`.


## Example instances

* `small-sat.in` (`3 1`): A small satisfiable instance, 1 white and 1 black queen on a 3x3 board.
* `small-unsat.in` (`3 2`): A small unsatisfiable instance, 2 queens of each color on a 3x3 board.
* `medium-sat.in` (`8 9`): A satisfiable instance on a standard board, at the maximum for n = 8. Solved in under a second.
* `nontrivial-sat.in` (`11 17`): A satisfiable instance at the maximum for n = 11 that takes approximately 25 s on my machine.



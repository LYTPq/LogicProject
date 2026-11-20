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

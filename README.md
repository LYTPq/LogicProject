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

Formally: let $P = \{1,\dots,n\}^2$ be the set of cells.
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

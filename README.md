
## 1. Problem description

Set splitting

We are given:

* a universe of elements
  [
  U = {1, 2, \dots, n}
  ]
* a family of subsets
  [
  S_1, S_2, \dots, S_m \subseteq U
  ]

The task is to assign each element a color:

* A  (interpreted as `True`)
* B  (interpreted as `False`)

such that every set (S_i) contains at least one A-colored element and at least one B-colored element.

Equivalently: No set may be monochromatic.

The input file format:

```
n m
k1 a1 a2 ... ak1
k2 b1 b2 ... bk2
...
```

Where:

* `n` – number of elements
* `m` – number of sets
* each set line contains its size followed by the element indices


## 2. Encoding


For each element (i) (1 ≤ i ≤ n):

* variable `i` represents “element i is colored A”
* negative literal `-i` represents “element i is colored B”

Total number of Boolean variables: n



For each set ( S = {i_1, i_2, \dots, i_k} ):

 1. Forbid all-A set

```
¬x(i1) ∨ ¬x(i2) ∨ ... ∨ ¬x(ik)
```

 2. Forbid all-B set

```
x(i1) ∨ x(i2) ∨ ... ∨ x(ik)
```

This guarantees that each set contains at least one A and one B.


If any set is empty, we insert two empty clauses:

```
0
0
```

which makes the CNF UNSAT.

### Alternatives

Possible encodings:

1. To add cardinality constraints: We can force |A ∩ S| ≥ 1 and |B ∩ S| ≥ 1 using sequential counters.
   This is unnecessary for this splitting problem.

2. Introduce two variables per element: For example A_i and B_i, and enforce XOR.
   This doubles the number of variables without benefit.



## User documentation

Basic usage:

```
setsplit_sat.py [-h] [-i INPUT] [-o OUTPUT] [-s SOLVER] [-v {0,1}]
```

Command-line options:

* `-h`, `--help`
  Show a help message and exit.

* `-i INPUT`, `--input INPUT`
  The instance file.
  Default: `input.in`.

* `-o OUTPUT`, `--output OUTPUT`
  Output file for the DIMACS CNF formula.
  Default: `formula.cnf`.

* `-s SOLVER`, `--solver SOLVER`
  Path to the SAT solver executable.
  Default: `./glucose`.

* `-v {0,1}`, `--verb {0,1}`
  Verbosity level of the SAT solver (0 = silent, 1 = full solver output).
  Default: `1`.

## Example instances

* `small_postive.in`
  A trivially satisfiable small instance.

* `small_negative.in`
  An unsatisfiable instance (e.g. an empty set is present).

* `random_50_20.in`
  Random instance with 50 elements and 20 sets — solved instantly.

## Experiments

Running sat solver on current non trivial instance(-n 100_000 -m 500_000): 

```
$ time python3 setsplit_sat.py -i instances/nontrivial_positive.in \
       -s ./glucose -v 0 > /dev/null

real    0m13.385s
user    0m12.813s
sys     0m0.558s
```

From my perspective, number of sets (m) is the most important parametr. The encoding generates exactly 2 CNF clauses per set, so the CNF grows linearly with m. In case of number of elements (n),
each element produces one SAT variable. Larger n means a larger Boolean search space.
Medium-sized sets (e.g. 3–10) create the hardest satisfiable instances.






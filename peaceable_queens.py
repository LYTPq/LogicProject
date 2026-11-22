import sys
from argparse import ArgumentParser
 
def load_instance(path):
    # read the input instance
    # the instance is a single line n m, the board size and the number of queens of each colour
    with open(path, "r") as file:
        n, m = (int(x) for x in file.read().split())
    return n, m


def w(r, c):
    return r * N + c + 1
 

def b(r, c):
    return (N * N) + (r * N) + c + 1


def attacks(r1, c1, r2, c2):
    # True if cells (r1, c1) and (r2, c2) are on the same row, column or diagonal
    return (r1 == r2                    # same row
            or c1 == c2                 # column
            or r1 - c1 == r2 - c2       # diagonal
            or r1 + c1 == r2 + c2)      # anti-diagonal


def new_var():
    # helper variable
    global NR_VARS
    NR_VARS += 1
    return NR_VARS



def at_least(cnf, xs, k):
    # clauses say that at least k of the variables in xs are true
    # helper variable s[i][j] means "among the first i+1 variables of xs
    if k <= 0:
        return
 

    L = len(xs)
    s = [[new_var() for j in range(k)] for i in range(L)]
 

    cnf.append([-s[0][0], xs[0]])
    for j in range(1, k):
        cnf.append([-s[0][j]])
 

    for i in range(1, L):
        for j in range(k):
            if j == 0:
                # helper variable s[i][j] means "at least j+1 of the first i+1 
                # variables of xs are true"
                cnf.append([-s[i][0], s[i - 1][0], xs[i]])
            else:
                # at least j+1 among the first i+1: already among the first i
                # or x_i is true and at least j among the first i
                cnf.append([-s[i][j], s[i - 1][j], xs[i]])
                cnf.append([-s[i][j], s[i - 1][j], s[i - 1][j - 1]])


    # require at least k among all of them
    cnf.append([s[L - 1][k - 1]])


def encode():
    # given the instance, create a cnf formula, i.e. a list of lists of integers
    # also return the total number of variables used
    global NR_VARS
    NR_VARS = 2 * N * N     
    cnf = []

    # every cell holds at most one queen
    for r in range(N):
        for c in range(N):
            cnf.append([-w(r, c), -b(r, c)])

    # no white queen attacks black queen
    for r1 in range(N):
        for c1 in range(N):
            for r2 in range(N):
                for c2 in range(N):
                    if (r1, c1) != (r2, c2) and attacks(r1, c1, r2, c2):
                        cnf.append([-w(r1, c1), -b(r2, c2)])
    
    # at least M white queens and at least M black queens
    at_least(cnf, [w(r, c) for r in range(N) for c in range(N)], M)
    at_least(cnf, [b(r, c) for r in range(N) for c in range(N)], M)

    return cnf, NR_VARS


def write_dimacs(cnf, nr_vars, path):
    with open(path, "w") as file:
        file.write(f"p cnf {nr_vars} {len(cnf)}\n")
        for clause in cnf:
            file.write(" ".join(str(lit) for lit in clause) + " 0\n")


if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument(
        "-i",
        "--input",
        default="instances/input.in",
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
        default="./glucose",
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
        choices=range(0,2),
        help=(
            "Verbosity of the SAT solver used."
        ),
    )
    args = parser.parse_args()
 
    N, M = load_instance(args.input)

    cnf, nr_vars = encode()
    write_dimacs(cnf, nr_vars, args.output)

    print("n =", N, "m =", M)
    print(nr_vars, "variables,", len(cnf), "clauses")
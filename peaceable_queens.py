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


if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument(
        "-i",
        "--input",
        default="input.in",
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
        default="glucose-syrup",
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
 
    n, m = load_instance(args.input)

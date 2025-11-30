import argparse
import subprocess

Clause = []

def load_instance(path):

    tokens = []

    with open(path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if parts:
                tokens.append(parts)

    n = int(tokens[0][0])       # number of elements
    m = int(tokens[0][1])       # number of sets

    sets = []

    for row in tokens[1:1 + m]:
        k = int(row[0])
        elems = [int(x) for x in row[1:1 + k]]
        sets.append(elems)

    print(n, m)

    return n, sets


def encode_set_splitting(n, sets):

    cnf = []

    # UNSAT if empty set appears
    for s in sets:
        if len(s) == 0:
            cnf.append([])    
            cnf.append([])
            return cnf, n

    for s in sets:
        cnf.append([-i for i in s])   # NOT all A
        cnf.append([ i for i in s])   # NOT all B

    nr_vars = n
    return cnf, nr_vars


def write_dimacs(cnf, nr_vars, output_file):
    with open(output_file, "w") as f:
        f.write(f"p cnf {nr_vars} {len(cnf)}\n")
        for clause in cnf:
            if not clause:
                f.write("0\n")
            else:
                f.write(" ".join(str(l) for l in clause) + " 0\n")



def call_solver(cnf, nr_vars, output_name, solver_name, verbosity):

    write_dimacs(cnf, nr_vars, output_name)

    return subprocess.run(
        ['./' + solver_name, '-model', '-verb=' + str(verbosity), output_name],
        stdout=subprocess.PIPE
    )



def print_result(result, n, sets, nr_vars):

    for line in result.stdout.decode("utf-8").split("\n"):
        print(line)

    if result.returncode == 20:
        print("\nInstance is UNSAT.")
        return

    
    model_lits = []
    for line in result.stdout.decode().split("\n"):
        line = line.strip()
        if line.startswith("v"):
            for tok in line.split()[1:]:
                lit = int(tok)
                if lit != 0:
                    model_lits.append(lit)

   
    assignment = {i: False for i in range(1, nr_vars + 1)}
    for lit in model_lits:
        var = abs(lit)
        assignment[var] = lit > 0

    
    print("\n##################################################################")
    print("##################[ Human readable result ]#######################")
    print("##################################################################\n")

    print("Satisfiable instance.\n")

    print("Element coloring (A=True, B=False):")
    for i in range(1, n + 1):
        color = "A" if assignment[i] else "B"
        print(f"  element {i}: {color}")

    print("\nSets splitting:")
    for idx, s in enumerate(sets, start=1):
        A = [i for i in s if assignment[i]]
        B = [i for i in s if not assignment[i]]
        print(f"  Set {idx}:")
        print(f"    A-part: {A}")
        print(f"    B-part: {B}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        default="input.in",
        type=str,
        help="The instance file.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="formula.cnf",
        type=str,
        help="Output file for the DIMACS format (i.e. the CNF formula).",
    )
    parser.add_argument(
        "-s",
        "--solver",
        default="./glucose",
        type=str,
        help="The SAT solver to be used."
    )
    parser.add_argument(
        "-v",
        "--verb",
        default=1,
        type=int,
        choices=range(0, 2),
        help="Verbosity of the SAT solver used.",
    )

    args = parser.parse_args()

    # get the input instance
    n, sets = load_instance(args.input)

    # encode the problem to create CNF formula
    cnf, nr_vars = encode_set_splitting(n, sets)

    # call the SAT solver
    result = call_solver(cnf, nr_vars, args.output, args.solver, args.verb)

    # interpret the result and print it in a human-readable format
    print_result(result, n, sets, nr_vars)

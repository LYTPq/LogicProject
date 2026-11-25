import subprocess
import sys
import time

sys.path.insert(0, ".")
import peaceable_queens as pq

TIMEOUT = 300  

INSTANCES = [(6, 6), (7, 7), (7, 8), (8, 9), (8, 10), (9, 12), (9, 13),
             (10, 14), (10,15), (11, 16), (11, 17), (11, 18), (12, 21)]

print("| n | m | variables | clauses | result | time |")
print("|---|---|---|---|---|---|")

for n, m in INSTANCES:
    # encode the instance and write the CNF
    pq.N, pq.M = n, m
    cnf, nr_vars = pq.encode()
    pq.write_dimacs(cnf, nr_vars, "/tmp/experiment.cnf")

    # run the solver and measure the time
    start = time.time()
    try:
        r = subprocess.run(["./glucose", "-verb=0", "/tmp/experiment.cnf"],
                           stdout=subprocess.DEVNULL, timeout=TIMEOUT)
        result = "SAT" if r.returncode == 10 else "UNSAT"
        seconds = f"{time.time() - start:.2f} s"
    except subprocess.TimeoutExpired:
        result = "?"
        seconds = f"> {TIMEOUT} s"

    print(f"| {n} | {m} | {nr_vars} | {len(cnf)} | {result} | {seconds} |", flush=True)
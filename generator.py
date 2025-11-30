import argparse
import random


def gen_instance(n, m, k_min, k_max, output_file):
    with open(output_file, "w") as out:
        out.write(f"{n} {m}\n")
        for _ in range(m):
            k = random.randint(k_min, k_max)
            elems = random.sample(range(1, n + 1), k)
            out.write(str(k) + " " + " ".join(str(x) for x in elems) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # n = number of elements
    parser.add_argument("-n", type=int, required=True)

    # m = number of sets
    parser.add_argument("-m", type=int, required=True)

    # output file name
    parser.add_argument("-o", type=str, default="instance.in")

    args = parser.parse_args()

    K_MIN = 3
    K_MAX = 10

    gen_instance(args.n, args.m, K_MIN, K_MAX, args.o)

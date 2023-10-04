import pycosat
from itertools import product
import time


def construct_SAT_problem(N: int) -> list[list[int]]:
    cnf = []
    
    i_j_to_var = dict()
    c = 1
    for i in range(N + 1):
        for j in range(N):
            i_j_to_var[(i, j)] = c
            c += 1
    
    for i in range(N + 1): # at least one hole for every pigeon
        at_least_one_hole = []
        for j in range(N):
            at_least_one_hole.append(i_j_to_var[(i, j)])
        cnf.append(at_least_one_hole)

    # for i in range(N + 1): # at most one hole for every pigeon (redundant)
    #     for j, k in product(range(N), repeat=2):
    #         if j < k:
    #             cnf.append([-1*i_j_to_var[(i, j)], -1*i_j_to_var[(i, k)]])

    for j in range(N): # at most one pigeon for every hole
        for i, k in product(range(N + 1), repeat=2):
            if i < k:
                cnf.append([-1*i_j_to_var[(i, j)], -1*i_j_to_var[(k, j)]])

    return cnf


if __name__ == "__main__":
    elapsed_time = 0.0
    N = 1 # number of holes
    while elapsed_time <= 60.0: # Solverd in under 60 seconds
        cnf_instance = construct_SAT_problem(N)
        print(f"N={N}, n_clauses={len(cnf_instance)}")
        start = time.time()
        print(pycosat.solve(cnf_instance))
        end = time.time()
        elapsed_time = end - start
        print(f"Time: {round(elapsed_time, 3)} s\n")
        N += 1

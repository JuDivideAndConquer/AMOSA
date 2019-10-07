import random
import copy
import numpy as np


def check_dom_pts(x1, x2):
    flag1 = 0
    flag2 = 0
    for i in range(0, len(x1)):
        if x1[i] < x2[i]:
            flag1 = 1
        if x1[i] > x2[i]:
            flag2 = 1
    if flag1 == 1 and flag2 == 0:
        return 1  # 	x1 dominates x2 (for min)
    elif flag2 == 1 and flag1 == 0:
        return -1  # 	x2 dominates x1	(for min)
    else:
        return 0  # 	non-dominated


def approximate_hypervolume(F, r, samples):
    r = np.asarray(r)
    F = np.asarray(F)
    dom_cnt = 0.0
    M = len(F[0])
    l = len(F)
    lb = copy.deepcopy(F[0])
    # print "a"
    for i in range(1, l):
        for j in range(0, M):
            if F[i][j] < lb[j]:
                lb[j] = copy.deepcopy(F[i][j])
    A = np.tile(lb, (samples, 1))
    temp = r - lb
    B = np.tile(temp, (samples, 1))
    rnd = np.random.rand(samples, M)
    F_samples = A + np.multiply(B, rnd)
    # print "a"
    for i in range(0, samples):
        for j in range(0, l):
            if check_dom_pts(F[j], F_samples[i]):
                dom_cnt = dom_cnt + 1.0
                break
            # print i,j
    # print "b"
    prod = 1.0
    for i in range(0, M):
        prod = prod * (r[i] - lb[i])

    hv = (dom_cnt / float(samples)) * prod
    return hv


# entry point ----------------------------------------------------------------
archive = []
with open("./objective_values.txt", "r") as fp:
    lines = fp.readlines()
    for line in lines:
        point = line.split(" ")[:-1]
        for i in range(len(point)):
            point[i] = float(point[i])
        archive.append(point)
archive = np.asfarray(archive)
#print(archive)
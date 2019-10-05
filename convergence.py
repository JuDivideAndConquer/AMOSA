#!/usr/bin/env python3

import numpy as np
from numpy import linalg as LA
import sys


def conv(ref_points, archive):
    d = 0.0
    for i in range(0, len(archive)):
        min_d = LA.norm(archive[i] - ref_points[0][1])
        for j in range(1, len(ref_points)):
            dd = LA.norm(archive[i] - ref_points[j][1])
            if dd < min_d:
                min_d = dd
        d += min_d
    d /= len(archive)
    return d


# main function---------------------------------------------
ref_points = []
with open(sys.argv[1], "r") as fp:
    lines = fp.readlines()
    for line in lines:
        point = line.split(" ")[:-1]
        for i in range(len(point)):
            point[i] = float(point[i])
        ref_points.append(point)

ref_points = np.asfarray(ref_points)
#print(ref_points)

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

print(conv(ref_points,archive))

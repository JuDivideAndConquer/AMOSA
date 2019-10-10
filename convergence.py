#!/usr/bin/env python3

import numpy as np
from numpy import linalg as LA
import sys
import math


def EuclideanDistance(point1,point2):
    if(len(point1)!=len(point2)):
        print("Incorrect dimensions")
        exit(1)
    d = 0.0
    for i in range(len(point1)):
        d = d + (point1[i]-point2[i])**2
    d = d/len(point1)
    return d

def conv(ref_points, archive):
    d_sum = 0.0
    for i in range(len(archive)):
        min_d = math.inf
        for j in range(len(ref_points)):
            d = EuclideanDistance(ref_points[j],archive[i])
            if(d<min_d):
                min_d = d
        d_sum = d_sum + min_d
    return d_sum/len(archive)


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
#print(len(ref_points))
#print(ref_points)

archive = []
with open(sys.argv[2], "r") as fp:
    lines = fp.readlines()
    for line in lines:
        point = line.split(" ")[:-1]
        for i in range(len(point)):
            point[i] = float(point[i])
        archive.append(point)

archive = np.asfarray(archive)
#print(archive)

print(conv(ref_points,archive))

#!/usr/bin/env python3

import sys
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d



archive = []
with open(sys.argv[1], "r") as fp:
    lines = fp.readlines()
    for line in lines:
        point = line.split(" ")[:-1]
        for i in range(len(point)):
            point[i] = float(point[i])
        archive.append(point)


if len(archive[0])>3:
    print("Incorrect Dimensions\n")
    exit(0)


obj1 = []
obj2 = []
obj3 = []

for i in range(len(archive)):
    #if(archive[i][0]<2.5 and archive[i][1]<2.5 and archive[i][2]<2.5 ):#debug
    for h in range(len(archive[0])):
        if h == 0:
            obj1.append(archive[i][h])
        elif h == 1:
            obj2.append(archive[i][h])
        elif h == 2:
            obj3.append(archive[i][h])

if len(archive[0]) == 2:
    plt.plot(obj1, obj2, 'ro')
    plt.show()
elif len(archive[0]) == 3:
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.scatter3D(obj1, obj2, obj3)
    plt.show()
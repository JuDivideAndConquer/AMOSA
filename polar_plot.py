from matplotlib import pyplot as plt
from ref_points_generator import getRefPoints
import random
import math
import copy
import numpy as np
from main_process import calculateD1D2, associateAllPoints


def displat_polar_plot(func_archive, c_problem):
    print("Displaying polar_plot")

    n_obj = len(func_archive[0])

    refPoints,refPointsDistanceMatrix = getRefPoints(n_obj)
    refPointAssociationList = []
    pointAssociationList = []
    refPointAssociationList, pointAssociationList = associateAllPoints(refPointAssociationList, pointAssociationList, refPoints, func_archive)
    
    theta = np.linspace(0, 2*np.pi, len(refPoints))
    x = []
    y = []
    
    for i in range(len(func_archive)):
        point = func_archive[i]
        refPoint = refPoints[pointAssociationList[i]]
        x.append(theta[pointAssociationList[i]])
        if(c_problem == "DTLZ1"):
            y.append(sum(point))
        else:
            y.append(np.linalg.norm(point))
        #print(x[i],y[i])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='polar')
    ax.scatter(x,y)
    plt.show()

#-------------
def test_plot1():
    theta = np.linspace(0, 2*np.pi,10)
    print(theta)
    y = np.sin(theta)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='polar')
    ax.scatter(theta,[1]*len(theta))
    plt.show()

if __name__=="__main__":
    test_plot1()
    

def test_plot():
    n_obj = 8
    refPoints,refPointsDistanceMatrix = getRefPoints(n_obj)
    
    func_archive = []
    #initialize archive
    for i in range(100):
        point = []
        for j in range(n_obj):
            point.append(random.uniform(0,1))
        func_archive.append(point)

    displat_polar_plot(func_archive)

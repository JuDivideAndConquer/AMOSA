import csv
import math

def distance(point1,point2):
    '''function to calculate euclidean distance between 2 points'''
    if(len(point1)!=len(point1)):
        print("Dimension mismatch in euclidean distance calculation")
        exit(0)
    else:
        sqSum = 0
        for i in range(len(point1)):
            sqSum = sqSum + point1[i]**2 + point2[i]**2
        distance = math.sqrt(sqSum)
        return distance

output = []
trueParetoFront = []

#read output objective values form file
with open('objective_values.txt', 'r') as fp:
    lines = fp.readlines()
    for i in range(len(lines)):
        line = lines[i]
        line = line.split()
        for j in range(len(line)):
            line[j] = float(line[j])
        output.append(line)

#read true pareto front values from file
with open('true_pareto_fronts/DTLZ1(3).csv','r') as fp:
    lines = fp.readlines()
    for i in range(len(lines)):
        line = lines[i]
        line = line.split()
        for j in range(len(line)):
            line[j] = float(line[j])
        trueParetoFront.append(line)


minDistance = []
minDistanceSum = 0


for point in output:
    '''for each point in the output values'''

    #finding point in true pareto front with minimum euclidean distance
    minDis = math.inf
    for truePoint in trueParetoFront:
        dis = distance(point,truePoint)
        if (dis<minDis):
            minDis = dis
    minDistance.append(minDis)
    minDistanceSum = minDistanceSum + minDis

convergence = minDistanceSum/len(minDistance)

print(convergence)




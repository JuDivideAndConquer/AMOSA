# Reference point generation for decomposition based approach
# Please use this look-up table for standard values of partitions
# n_obj, p1, p2, n_pts
# 3, 12, 0, 91
# 5, 6, 0, 210
# 8, 3, 2, 156
# 10, 3, 2, 275
# 15, 2, 1, 135

import copy
import numpy as np


class form_ref_pts(object):
    def __init__(self, m, divisions):
        self.M = m - 1
        self.div = divisions
        self.points = []
        self.form()

    def recursive(self, arr, d, l):
        arr_c = copy.deepcopy(arr)
        if d == self.M - 1:
            self.points.append(arr_c)
        else:
            for i in range(0, l):
                node_val = float(i) / float(self.div)
                arr_next = copy.deepcopy(arr_c)
                arr_next.append(node_val)
                self.recursive(arr_next, d + 1, l - i)

    def form(self):
        layer = []
        for i in range(0, self.div + 1):
            layer.append(float(i) / float(self.div))
        for i in range(0, len(layer)):
            l1 = []
            l1.append(layer[i])
            self.recursive(l1, 0, len(layer) - i)
        for i in range(0, len(self.points)):
            s = sum(self.points[i])
            self.points[i].append(1.0 - s)
        self.points = np.asarray(self.points)


def form_refs(dim, outer, inner):
    points = []

    factory = form_ref_pts(dim, outer)
    factory2 = form_ref_pts(dim, inner)
    factory2.points = (factory2.points / 2) + (1.0 / (2.0 * dim))

    for i in range(0, len(factory.points)):
        points.append(factory.points[i])
    for i in range(0, len(factory2.points)):
        points.append(factory2.points[i])

    return np.asarray(points)

class distanceObj(object):
    def __init__(self,r,c,points):
        self.row = r
        self.col = c
        self.dis = self.distance(points[r],points[c])


    def distance(self,refPoint1,refPoint2):
        if(len(refPoint1) != len(refPoint2)):
            print("Reference point dimension mismatch")
            exit(0);
        distance = 0
        for i in range(len(refPoint1)):
            distance = distance + (refPoint1[i]-refPoint2[i])**2
        distance = distance**0.5
        return distance


# Entry point ----------------------------------
def getRefPoints(n_obj):
    '''returns generated reference points'''
    points=[]
    if(n_obj == 3):
        divisions = 12
        refPoints = form_ref_pts(n_obj, divisions)
        points = refPoints.points
    elif(n_obj == 5):
        divisions = 6
        refPoints = form_ref_pts(n_obj, divisions)
        points = refPoints.points
    elif(n_obj == 8):
        outerDivisions = 3
        innerDivisions = 2
        ref_points = form_refs(n_obj, outerDivisions, innerDivisions)
        points = ref_points
    elif(n_obj == 10):
        outerDivisions = 3
        innerDivisions = 2
        ref_points = form_refs(n_obj, outerDivisions, innerDivisions)
        points = ref_points
    elif(n_obj == 15):
        outerDivisions = 2
        innerDivisions = 1
        ref_points = form_refs(n_obj, outerDivisions, innerDivisions)
        points = ref_points

    distanceMatrix = []
    for i in range(len(points)):
        distanceRow = []
        distanceIndexRow = []
        for j in range(len(points)):
            distanceRow.append(distanceObj(i,j,points))
        distanceRow.sort(key=lambda x:x.dis)
        for i in distanceRow:
            distanceIndexRow.append(i.col)
        distanceMatrix.append(distanceIndexRow)

    return points,distanceMatrix

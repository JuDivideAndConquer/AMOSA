from ref_points_generator import getRefPoints
from amosa import AMOSAType
import copy
import math

# 1. Normalize
# 2. Associate
# 3. Compute cost for each vector
# 4. Keep the lowest cost points


def normalize(dd_archive, amosaParams):
    '''Normalization of archive vectors'''

    d_normalize_shift = [0]*amosaParams.i_no_offunc
    d_normalize_scale = [0]*amosaParams.i_no_offunc

    for i in range(amosaParams.i_no_offunc):
        min = -math.inf
        max = math.inf
        for j in range(len(dd_archive)):
            if(min > dd_archive[j][i]):
                min = dd_archive[j][i]
            if(max < dd_archive[j][i]):
                max = dd_archive[j][i]
        d_normalize_scale[i] = max - min
        d_normalize_shift[i] = min

    for i in range(amosaParams.i_no_offunc):
        # Normalize shift
        for j in range(len(dd_archive)):
            dd_archive[j][i] = dd_archive[j][i] - d_normalize_shift[i]
        # Normalize scale
        for j in range(len(dd_archive)):
            dd_archive[j][i] = dd_archive[j][i]/d_normalize_scale[i]

    return d_normalize_shift, d_normalize_scale


def deNormalize(dd_archive, d_normalize_shift, d_normalize_scale, amosaParams):
    '''De-normalization of vectors'''
    for i in range(amosaParams.i_no_offunc):
        # de-normalize scale
        for j in range(len(dd_archive)):
            dd_archive[j][i] = dd_archive[j][i] * d_normalize_scale[i]
        # de-normalize shift
        for j in range(len(dd_archive)):
            dd_archive[j][i] = dd_archive[j][i] + d_normalize_shift[i]


def calculatePBI(point, refPoint):
    ''' Function to calculate distance (cost function) form the associated ref point'''
    # Assuming that the ideal point is origin for all funcions
    theta = 0.5

    # calculate d1
    refPointMod = 0.0
    for x in refPoint:
        refPointMod = refPointMod + x*x
    refPointMod = math.sqrt(refPointMod)

    d1 = 0.0
    for i in range(len(point)):
        d1 = d1 + point[i]*refPoint[i]
    d1 = d1 / refPointMod

    # calculate d2
    pointOnRef = copy.deepcopy(refPoint)
    for i in range(len(pointOnRef)):
        pointOnRef = pointOnRef*d1/refPointMod

    d2Vector = []
    d2 = 0
    for i in range(len(point)):
        d2Vector.append(point[i]-pointOnRef[i])
        d2 = d2 + (point[i]-pointOnRef[i])**2
    d2 = math.sqrt(d2)

    return d1 + theta*d2




def associate(dd_func_archive, refPoints, associationList):
    '''function to associate each point to a reference point'''
    for i in range(len(dd_func_archive)):
        minDistance = math.inf
        minDistanceIndex = 0
        for j in range(len(refPoints)):
            nDistance = calculatePBI(dd_func_archive[i], refPoints[j])
            if(nDistance < minDistance):
                minDistanceIndex = j
        associationList[minDistanceIndex].append(i)


def clustering(amosaParams):

    dd_archive = copy.deepcopy(amosaParams.dd_archive)
    dd_func_archive = copy.deepcopy(amosaParams.dd_func_archive)

    # Normalization
    d_normalize_shift, d_normalize_scale = normalize(
        dd_func_archive, amosaParams)

    # Getting the reference points (later to be genenrated only once)
    refPoints = getRefPoints(amosaParams.i_no_offunc)

    # Associate each point to a reference point
    associationList = [[]] * len(refPoints)
    associate(dd_func_archive, refPoints, associationList)

    # De-normalization
    deNormalize(dd_func_archive, d_normalize_shift,
                d_normalize_scale, amosaParams)

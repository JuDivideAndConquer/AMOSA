from ref_points_generator import getRefPoints
from amosa import AMOSAType
import copy
import math

# 1. Normalize
# 2. Associate
# 3. Compute cost for each vector
# 4. Keep the lowest cost points


def normalize(dd_func_archive, amosaParams):
    '''Normalization of archive vectors'''

    d_normalize_shift = [0]*amosaParams.i_no_offunc
    d_normalize_scale = [0]*amosaParams.i_no_offunc

    for i in range(amosaParams.i_no_offunc):
        min = math.inf
        max = -math.inf
        for j in range(len(dd_func_archive)):
            if(min > dd_func_archive[j][i]):
                min = dd_func_archive[j][i]
            if(max < dd_func_archive[j][i]):
                max = dd_func_archive[j][i]
        d_normalize_scale[i] = max - min
        d_normalize_shift[i] = min

    for i in range(amosaParams.i_no_offunc):
        # Normalize shift
        for j in range(len(dd_func_archive)):
            dd_func_archive[j][i] = dd_func_archive[j][i] - \
                d_normalize_shift[i]
        # Normalize scale
        for j in range(len(dd_func_archive)):
            dd_func_archive[j][i] = dd_func_archive[j][i]/d_normalize_scale[i]

    return d_normalize_shift, d_normalize_scale


def deNormalize(dd_func_archive, d_normalize_shift, d_normalize_scale, amosaParams):
    '''De-normalization of vectors'''
    for i in range(amosaParams.i_no_offunc):
        # de-normalize scale
        for j in range(len(dd_func_archive)):
            dd_func_archive[j][i] = dd_func_archive[j][i] * \
                d_normalize_scale[i]
        # de-normalize shift
        for j in range(len(dd_func_archive)):
            dd_func_archive[j][i] = dd_func_archive[j][i] + \
                d_normalize_shift[i]


def calculateD1D2(point,refPoint):
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
        pointOnRef[i] = pointOnRef[i]*d1/refPointMod

    d2Vector = []
    d2 = 0
    for i in range(len(point)):
        d2Vector.append(point[i]-pointOnRef[i])
        d2 = d2 + (point[i]-pointOnRef[i])**2
    d2 = math.sqrt(d2)

    return d1,d2


def calculatePBI(point, refPoint):
    ''' Function to calculate distance (cost function) form the associated ref point'''
    # Assuming that the ideal point is origin for all funcions
    theta = 5
    d1,d2 = calculateD1D2(point,refPoint)
    return d1 + theta*d2


def associate(normalized_dd_func_archive,dd_func_archive,dd_archive, refPoints, associationList):
    '''function to associate each point to a reference point'''
    for i in range(len(dd_func_archive)):
        minDistance = math.inf
        minDistanceIndex = -1
        for j in range(len(refPoints)):
            d1,d2 = calculateD1D2(normalized_dd_func_archive[i], refPoints[j])
            nDistance = d2
            # print("refpoint ", j, " , point ", i,
            #       " , distance :", nDistance)  # debug
            if(nDistance < minDistance):
                minDistance = nDistance
                minDistanceIndex = j
        associationList[minDistanceIndex].append([normalized_dd_func_archive[i],dd_func_archive[i],dd_archive[i]])
        # print("point ", i, " associated to ref point ", minDistanceIndex)


def cost(point,refPoint):
    return calculatePBI(point, refPoint)


def niching(dd_func_archive, dd_archive, associationList, refPoints, i_hardl):
    '''function to select points form the archive based on their distance and reference point associated to'''

    clustered_dd_func_archive = copy.deepcopy(dd_func_archive)
    clustered_dd_archive = copy.deepcopy(dd_archive)

    while(len(clustered_dd_archive)>=i_hardl):
        # find the subspace with the hightest no of associations
        maxAssocIndex = -1
        maxAssoc = -1
        for i in range(len(associationList)):
            if(len(associationList[i])>maxAssoc):
                maxAssoc = len(associationList[i])
                maxAssocIndex = i

        if(maxAssoc == 1):
            print("Removing singleton subspace point")
            exit(0)
        
        # find the point with the maximum distance(cost) in that subspace
        maxDistanceIndex = -1
        maxDistance = -math.inf
        for i in range(len(associationList[maxAssocIndex])):
            distance = cost(associationList[maxAssocIndex][i][0],refPoints[maxAssocIndex])
            if(distance>maxDistance):
                maxDistance = distance
                maxDistanceIndex = i

        # removing the point
        try:
            clustered_dd_func_archive.remove(associationList[maxAssocIndex][maxDistanceIndex][1])
        except ValueError:
            print(ValueError)
            print("----------")
            print(associationList[maxAssocIndex][maxDistanceIndex])
            exit(0)
        clustered_dd_archive.remove(associationList[maxAssocIndex][maxDistanceIndex][2])
        associationList[maxAssocIndex].pop(maxDistanceIndex)

    return clustered_dd_archive, clustered_dd_func_archive


def clustering(amosaParams):
    # print("clustering called")
    normalized_dd_func_archive = copy.deepcopy(amosaParams.dd_func_archive)
    dd_archive = copy.deepcopy(amosaParams.dd_archive)
    dd_func_archive = copy.deepcopy(amosaParams.dd_func_archive)

    # Normalization
    #d_normalize_shift, d_normalize_scale = normalize(
    #    normalized_dd_func_archive, amosaParams)

    # Getting the reference points (later to be genenrated only once)
    refPoints = amosaParams.refPoints

    # association list[refPoint] contains list of [normalized_func_point,func_point,point]
    associationList = []
    for i in range(len(refPoints)):
        associationList.append([])
    # Associate each point to a reference point
    associate(normalized_dd_func_archive, dd_func_archive, dd_archive, refPoints, associationList)

    # debug
    # print("association list---------------------")
    # for i in range(len(associationList)):
    #     if(len(associationList[i]) != 0):
    #         print("association list ", i, "----------")
    #         for x in associationList[i]:
    #             print(x)
    #         print()

    # perform niching
    clustered_dd_archive, clustered_dd_func_archive = niching(
        dd_func_archive, dd_archive, associationList, refPoints, amosaParams.i_hardl)

    # # De-normalization
    # deNormalize(clustered_dd_func_archive, d_normalize_shift,
    #             d_normalize_scale, amosaParams)

    #updating the real archive
    amosaParams.dd_archive = clustered_dd_archive
    amosaParams.dd_func_archive = clustered_dd_func_archive
    amosaParams.i_archivesize = len(clustered_dd_archive)

    #exit(0)#debug

import math
import copy
import sys

#single linkage clustering---------------------------------------------------------------------------------------------------------------
def clustering1(amosaParams):
    no_clus = amosaParams.i_archivesize
    cluster = []  # size softl+1
    dd_archive2 = []  # size (softl+2)*(softl+2)
    dd_area2 = []  # size (softl+2)*(softl+2)
    point1 = [0]*(amosaParams.i_softl+1)  # size softl+1
    point2 = [0]*(amosaParams.i_softl+1)  # size softl+1
    dist = [0]*(amosaParams.i_softl)  # size softl
    distance = [[0]*(amosaParams.i_archivesize+1)] * \
        (amosaParams.i_archivesize+1)  # size (softl+1)*(softl+1)
    k = amosaParams.i_archivesize
    u = int()
    v = int()
    w = int()

    for i in range(amosaParams.i_archivesize):
        cluster.append(i)

    for i in range(k):
        distance[i][i] = math.inf
        for j in range(i+1, k):
            distance[i][j] = 0.0
            for p in range(amosaParams.i_no_offunc):
                distance[i][j] = distance[i][j] + math.pow(
                    (amosaParams.dd_func_archive[i][p] - amosaParams.dd_func_archive[j][p]), 2)
            distance[j][i] = math.sqrt(distance[i][j])
    '''Initalizing the distance matrix
    for all i,j (i<j) distance[i][j] stores the sqared distance between the solutions
    for all i,j (i>j) distance[i][j] stores the distance between the solutions
    for all i=j distance[i][j] = infinity'''

    flag = []

    while(no_clus > amosaParams.i_hardl):
        '''While loop that runs until 
        no of clusters is reduced to hard limit'''

        min = math.inf
        flag = [0]*amosaParams.i_archivesize

        for i in range(k):
            for j in range(i):  # the sahil factor
                if(i != j):
                    if(min > distance[i][j]):
                        u = i
                        v = j
                        min = distance[i][j]
        '''Finds the points with minimum distance and 
        stores the location of the points in u and v'''

        if(cluster[u] == u and cluster[v] == v):
            cluster[u] = v
            cluster[v] = u
        elif(cluster[u] == u):
            j = cluster[v]
            while(cluster[j] != v):
                j = cluster[j]
            cluster[j] = u
            cluster[u] = v
        elif(cluster[v] == v):
            j = cluster[u]
            while(cluster[j] != u):
                j = cluster[j]
            cluster[j] = v
            cluster[v] = u
        else:
            j = cluster[u]
            while(cluster[j] != u):
                j = cluster[j]
            cluster[j] = v
            p = cluster[v]
            while(cluster[p] != v):
                p = cluster[p]
            cluster[p] = u
        
        no_clus = no_clus - 1
        g = 0
        point1[g] = u
        j = cluster[u]
        while(j != u):
            g = g+1
            point1[g] = j
            j = cluster[j]
        '''point1[] stores all the points that belongs to the cluster 
        that contains point indexed u'''
        
        for i in range(g):
            w = point1[i]
            flag[w] = 1
            '''marking all those points one if they are in a cluster'''
            for j in range(i+1, g+1):
                m = point1[j]
                flag[m] = 1
                distance[m][w] = math.inf
                distance[w][m] = math.inf
                '''Setting the distance between points in the cluster as infinity'''


        for i in range(amosaParams.i_archivesize):
            if(flag[i] == 0):
                '''if ith point is not in the archive'''

                if(cluster[i] == i):
                    '''if point i not in a cluster (cluster of size 1)'''
                    w = point1[0]
                    min = distance[w][i]
                    for j in range(1, g+1):
                        m = point1[j]
                        if(min > distance[m][i]):
                            min = distance[m][i]
                    for j in range(g+1):
                        m = point1[j]
                        distance[m][i] = min
                        distance[i][m] = min  # the sahil factor
                    flag[i] = 1
                    '''setting the distance of all the points in the cluster 
                    with point 1 with the minimum distance'''

                else:
                    '''if point i is in a cluster'''

                    g2 = 0
                    point2[g2] = i
                    j = cluster[i]
                    while(j != i):
                        g2 = g2+1
                        point2[g2] = j
                        j = cluster[j]
                    '''now points2 stores all the points that belongs to the cluster holding point i'''

                    w = point1[0]
                    m = point2[0]
                    min = distance[w][m]
                    for j in range(g+1):
                        w = point1[j]
                        for p in range(g2+1):
                            m = point2[p]
                            if(min > distance[w][m]):
                                min = distance[w][m]
                    '''now min is the minimum distance between the new cluster and the cluster that hold point i'''

                    for j in range(g+1):
                        for p in range(g2+1):
                            w = point1[j]
                            m = point2[p]
                            distance[m][w] = min
                            distance[w][m] = min
                            flag[m] = 1
                    '''setting the distance between the cluster with the minimum distance between them (Single linkage)'''

    dd_archive2 = copy.deepcopy(amosaParams.dd_archive)
    dd_area2 = copy.deepcopy(amosaParams.dd_func_archive)
    flag = [0]*(amosaParams.i_archivesize)

    '''Empty the archive , points to be re-added after clustering'''

    k=0
    for i in range(amosaParams.i_archivesize):
        if(flag[i]==0):
            '''If point i has not been iterated through'''
            if(cluster[i] != i):
                '''If point i doesnot belong to a single point cluster'''
                g=0
                point1[g] = i
                flag[i] = 1
                j = cluster[i]
                while(j != i):
                    g = g +1
                    point1[g] = j
                    flag[j] = 1
                    j = cluster[j]
                '''Iterated through all the points in the cluster
                setting their flags as 1 and storing them in the array point1'''

                for j in range(g+1):
                    dist[j] = 0
                    w = point1[j]
                    for p in range(g+1):
                        if(p != j):
                            m = point1[p]
                            for pp in range(amosaParams.i_no_offunc):
                                dist[j] = dist[j] + math.pow((amosaParams.dd_func_archive[w][pp] - amosaParams.dd_func_archive[m][pp]),2)
                            dist[j] = math.sqrt(dist[j])
                            '''Storing the sum of distance of all the other points in the cluster form point j'''

                min = dist[0]
                w = point1[0]
                for j in range(1,g+1):
                    if(min>dist[j]):
                        min = dist[j]
                        w = point1[j]
                '''The point with the minimum sum of distance form the rest of the points in the cluster is added in the archive'''

                d_archive = copy.deepcopy(dd_archive2[w])
                d_area = copy.deepcopy(dd_area2[w])
                amosaParams.dd_archive.append(d_archive)
                amosaParams.dd_func_archive.append(d_area)
                k = k + 1
            else:
                '''If point belongs to a cluster of size 1 (single point cluster)'''
                d_archive = copy.deepcopy(dd_archive2[i])
                d_area = copy.deepcopy(dd_area2[i])
                amosaParams.dd_archive.append(d_archive)
                amosaParams.dd_func_archive.append(d_area)
                k = k + 1

    amosaParams.i_archivesize = k
    amosaParams.dd_archive = amosaParams.dd_archive[:k]
    amosaParams.dd_func_archive = amosaParams.dd_func_archive[:k]

#decomposition based clustering-------------------------------------------------------------------------------------------------------
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


def associate(dd_func_archive, refPoints, associationList):
    '''function to associate each point to a reference point'''
    for i in range(len(dd_func_archive)):
        minDistance = math.inf
        minDistanceIndex = -1
        for j in range(len(refPoints)):
            d1,d2 = calculateD1D2(dd_func_archive[i], refPoints[j])
            nDistance = d2
            # print("refpoint ", j, " , point ", i,
            #       " , distance :", nDistance)  # debug
            if(nDistance < minDistance):
                minDistance = nDistance
                minDistanceIndex = j
        associationList[minDistanceIndex].append([i, minDistance])
        # print("point ", i, " associated to ref point ", minDistanceIndex)


def niching(dd_func_archive, dd_archive, associationList, i_hardl):
    '''function to select points form the archive based on their distance and reference point associated to'''

    clustered_dd_func_archive = []
    clustered_dd_archive = []

    while(len(clustered_dd_func_archive) < i_hardl):
        # variable to hold the index of reference points which are non-empty and a point is yet to be selected form them
        refPointSelectedList = []
        for i in range(len(associationList)):
            if(len(associationList[i]) != 0):
                refPointSelectedList.append(i)

        while(len(refPointSelectedList) != 0):
            # find the ref point with least no of point associations
            minAssociationIndex = -1
            minAssociation = math.inf
            for i in range(len(refPointSelectedList)):
                if(minAssociation > len(associationList[refPointSelectedList[i]])):
                    minAssociation = len(
                        associationList[refPointSelectedList[i]])
                    minAssociationIndex = refPointSelectedList[i]

            # find the point with the least distance form that reference point
            minDistanceIndex = -1
            minDistance = math.inf
            for i in range(len(associationList[minAssociationIndex])):
                if(minDistance > associationList[minAssociationIndex][i][1]):
                    minDistanceIndex = i
                    minDistance = associationList[minAssociationIndex][i][1]

            pointIndex = associationList[minAssociationIndex][minDistanceIndex][0]
            # print("pointIndex :",pointIndex)#debug

            # add the point to the archives
            clustered_dd_func_archive.append(
                dd_func_archive[pointIndex])
            clustered_dd_archive.append(dd_archive[pointIndex])

            #check the length of the new archive
            if(len(clustered_dd_archive)>= i_hardl):
                return clustered_dd_archive, clustered_dd_func_archive

            # remove the point form the association list
            associationList[minAssociationIndex].pop(minDistanceIndex)

            # remove the ref point from the list
            refPointSelectedList.remove(minAssociationIndex)

    return clustered_dd_archive, clustered_dd_func_archive


def clustering2(amosaParams):
    # print("clustering called")
    dd_archive = copy.deepcopy(amosaParams.dd_archive)
    dd_func_archive = copy.deepcopy(amosaParams.dd_func_archive)

    # Normalization
    d_normalize_shift, d_normalize_scale = normalize(
        dd_func_archive, amosaParams)

    # Getting the reference points (later to be genenrated only once)
    refPoints = getRefPoints(amosaParams.i_no_offunc)

    # association list[refPoint] contains list of [pointIndex, minDistance]
    associationList = []
    for i in range(len(refPoints)):
        associationList.append([])
    # Associate each point to a reference point
    associate(dd_func_archive, refPoints, associationList)

    # debug
    # print("association list---------------------")
    # for i in range(len(associationList)):
    #     if(len(associationList[i]) != 0):
    #         print("association list ", i, "----------")
    #         for x in associationList[i]:
    #             print(x[0], end=" ")
    #         print()

    # perform niching
    clustered_dd_archive, clustered_dd_func_archive = niching(
        dd_func_archive, dd_archive, associationList, amosaParams.i_hardl)

    # De-normalization
    deNormalize(dd_func_archive, d_normalize_shift,
                d_normalize_scale, amosaParams)

    #updating the real archive
    amosaParams.dd_archive = clustered_dd_archive
    amosaParams.dd_func_archive = clustered_dd_func_archive
    amosaParams.i_archivesize = len(clustered_dd_archive)

    #exit(0)#debug


def clustering(amosaParams):
    if(amosaParams.i_clustering_type == "0"):
        clustering1(amosaParams)
    elif(amosaParams.i_clustering_type == "1"):
        clustering2(amosaParams)
    else:
        print("Invalid clustering type")
        exit(0)

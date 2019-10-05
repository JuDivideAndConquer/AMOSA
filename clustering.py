import math
import copy


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


def clustering2(amosaParams):
    pass


def clustering(amosaParams):
    clustering1(amosaParams)
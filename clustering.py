import math
import copy


def clustering(amosaParams):
    '''SINGLE LINKAGE CLUSTERING\n
    If the size of the archive is greater 
    than soft limit (SL) then the clustering 
    process is done to reduce the size of 
    the archive to Hard Limit (HL).'''

    cluster = []
    flag = []
    point1 = [0]*(amosaParams.i_softl + 1)
    point2 = [0]*(amosaParams.i_softl + 1)
    no_clus = amosaParams.i_archivesize
    k = amosaParams.i_archivesize
    u = int()
    v = int()

    for i in range(amosaParams.i_archivesize):
        cluster.append(i)

    # Creating a table dd_distance to store the distances between points
    dd_distance = [[0 for j in range(k)] for i in range(k)]
    for i in range(k):
        dd_distance[i][i] = math.inf
        for j in range(i+1, k):
            dd_distance[i][j] = 0
            for k in range(amosaParams.i_no_offunc):
                dd_distance[i][j] = dd_distance[i][j] + (amosaParams.dd_func_archive[i][k] - amosaParams.dd_func_archive[j][k])*(amosaParams.dd_func_archive[i][k] - amosaParams.dd_func_archive[j][k])
            dd_distance[j][i] = math.sqrt(dd_distance[i][j])

    # finding the pair of points with minimum distances
    while(no_clus > amosaParams.i_hardl):
        min = math.inf
        flag = [0]*(amosaParams.i_archivesize)
        for i in range(k):
            for j in range(k):
                if(j != i):
                    if(min > dd_distance[i][j]):
                        min = dd_distance[i][j]
                        u = i
                        v = j

        j = cluster[u]
        while(cluster[j] != u):
            cluster[j] = v
        p = cluster[v]
        while(cluster[p] != v):
            cluster[p] = u

        no_clus = no_clus - 1
        g = 0
        point1[0] = g = u
        j = cluster[u]

        while(j != u):
            g = g+1
            point1[g] = j
            j = cluster[j]

        for i in range(g+1):
            w = point1[i]
            flag[w] = 1
            for j in range(i+1, g+1):
                m = point1[j]
                flag[m] = 1
                dd_distance[m][w] = dd_distance[w][m] = math.inf

        for i in range(amosaParams.i_archivesize):
            if(flag[i] == 0):

                if(cluster[i] == i):
                    w = point1[0]

                    min = dd_distance[w][i]
                    for j in range(1, g+1):
                        m = point1[j]

                        if(min > dd_distance[m][i]):
                            min = dd_distance[m][i]

                    for j in range(g+1):
                        m = point1[j]
                        dd_distance[m][i] = min

                    flag[i] = 1

            else:
                g2 = 0
                point2[g2] = i
                j = cluster[i]

                while(j != i):
                    g2 = g2+1
                    point2[g2] = j
                    j = cluster[j]

                w = point1[0]
                m = point2[0]
                min = dd_distance[w][m]

                for j in range(g+1):
                    w = point1[j]
                    for p in range(g2+1):
                        m = point2[p]
                        if(min > dd_distance[w][m]):
                            min = dd_distance[w][m]

                for j in range(g+1):
                    for p in range(g2+1):
                        w = point1[j]
                        m = point2[p]
                        dd_distance[m][w] = dd_distance[w][m] = min
                        flag[m] = 1

    archive2 = copy.deepcopy(amosaParams.dd_archive)
    area2 = copy.deepcopy(amosaParams.dd_func_archive)
    flag = [0]*(amosaParams.i_archivesize)

    k = 0
    dist = [0]*(amosaParams.i_softl)
    for i in range(amosaParams.i_archivesize):
        if(flag[i] == 0):
            if(cluster[i] != i):
                g = 0
                point1[g] = i
                flag[i] = 1
                j = cluster[i]

                while(j != i):
                    g = g+1
                    point1[g] = j
                    flag[j] = 1
                    j = cluster[j]

                for j in range(g+1):
                    dist[j] = 0
                    w = point1[j]
                    for p in range(g+1):
                        if(p != j):
                            m = point1[p]
                            for pp in range(amosaParams.i_no_offunc):
                                dist[j] = dist[j] + (amosaParams.dd_func_archive[w]
                                                     [pp] - amosaParams.dd_func_archive[m][pp])**2
                            dist[j] = dist[j]*(0.5)

                min = dist[0]
                w = point1[0]
                for j in range(1, g+1):
                    if(min > dist[j]):
                        min = dist[j]
                        w = point1[j]

                amosaParams.dd_archive[k] = copy.deepcopy(archive2[i])
                amosaParams.dd_archive[k] = copy.deepcopy(archive2[i])
                k = k+1

    amosaParams.i_archivesize = k

def clustering(amosaParams):
    '''SINGLE LINKAGE CLUSTERING\n
    If the size of the archive is greater 
    than soft limit (SL) then the clustering 
    process is done to reduce the size of 
    the archive to Hard Limit (HL).'''

    cluster = []
    flag = []
    no_clus = amosaParams.i_archivesize
    k = amosaParams.i_archivesize
    u = int()
    v = int()

    dd_distance = [[0 for j in range(k)] for i in range(k)]

    for i in range(amosaParams.i_archivesize):
        cluster.append(i)

    for i in range(k):
        dd_distance[i][i] = 2000000
        for j in range(i+1, k):
            dd_distance[i][j] = 0
            for k in range(amosaParams.i_no_offunc):
                dd_distance[i][j] = dd_distance[i][j] + \
                    (amosaParams.dd_func_archive[i][k] -
                     amosaParams.dd_func_archive[j][k]) ^ 2
            dd_distance[j][i] = (dd_distance[i][j]) ^ 0.5

    while(no_clus > amosaParams.i_hardl):
        min = 2000000
        flag = [0]*(amosaParams.i_archivesize)
        for i in range(k):
            for j in range(k):
                if(j!=k): #(j!=i)
                    if(min>dd_distance[i][j]):
                        min = dd_distance[i][j]
                        u=i
                        v=j


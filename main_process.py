from amosa import AMOSAType
import random
import copy
import sys
from math import *
from real_mutate_ind import point_mutate
from test_func import evaluate
from dominance import find_unsign_dom
from dominance import is_dominated
from clustering import clustering,removeDominated
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from real_time_plot import real_time_plot
import math
from ref_points_generator import getRefPoints


# Calculation of d1 and d2 (here it is not adjusted for the skipping of normalization)
def calculateD1D2(point, refPoint):
    # calculate d1
    refPointMod = 0.0
    for x in refPoint:
        refPointMod = refPointMod + x * x
    refPointMod = math.sqrt(refPointMod)

    d1 = 0.0
    for i in range(len(point)):
        d1 = d1 + point[i] * refPoint[i]
    d1 = d1 / refPointMod

    # calculate d2
    pointOnRef = copy.deepcopy(refPoint)
    for i in range(len(pointOnRef)):
        pointOnRef[i] = pointOnRef[i] * d1 / refPointMod

    d2Vector = []
    d2 = 0
    for i in range(len(point)):
        d2Vector.append(point[i] - pointOnRef[i])
        d2 = d2 + (point[i] - pointOnRef[i]) ** 2

    d2 = math.sqrt(d2)

    return d1, d2


# function to assciate points with reference points
# fills up the refPointAssociationList and pointAssociationList


def associateAllPoints(
    refPointAssociationList, pointAssociationList, refPoints, dd_func_archive
):
    pointAssociationList = [-1] * len(dd_func_archive)
    refPointAssociationList = []
    for i in range(len(refPoints)):
        refPointAssociationList.append([])

    for i in range(len(dd_func_archive)):
        minDistance = math.inf
        minDistanceIndex = -1
        for j in range(len(refPoints)):
            d1, d2 = calculateD1D2(dd_func_archive[i], refPoints[j])
            nDistance = d2
            if nDistance < minDistance:
                minDistance = nDistance
                minDistanceIndex = j
        refPointAssociationList[minDistanceIndex].append(i)
        pointAssociationList[i] = minDistanceIndex
    return refPointAssociationList, pointAssociationList


def refPointToAssociate(refPoints, func_point):
    minDistance = math.inf
    minDistanceIndex = -1
    for j in range(len(refPoints)):
        d1, d2 = calculateD1D2(func_point, refPoints[j])
        nDistance = d2
        if nDistance < minDistance:
            minDistance = nDistance
            minDistanceIndex = j
    return minDistanceIndex


def associatePoint(
    refPointAssociationList, pointAssociationList, refPoints, dd_func_archive, pos
):
    minDistance = math.inf
    minDistanceIndex = -1
    for j in range(len(refPoints)):
        d1, d2 = calculateD1D2(dd_func_archive[pos], refPoints[j])
        nDistance = d2
        if nDistance < minDistance:
            minDistance = nDistance
            minDistanceIndex = j
    refPointAssociationList[minDistanceIndex].append(pos)
    if len(pointAssociationList) == pos:
        pointAssociationList.append(-1)
    pointAssociationList[pos] = minDistanceIndex
    return refPointAssociationList, pointAssociationList


def errorcheck(refPointAssociationList, pointAssociationList, amosaParams):
    if len(pointAssociationList) != len(amosaParams.dd_archive):
        print(
            "PointAssociationList length mismatch, list len:",
            len(pointAssociationList),
            " archive length:",
            len(amosaParams.dd_archive),
        )
        return True
    for i in range(len(pointAssociationList)):
        j = pointAssociationList[i]
        if i not in refPointAssociationList[j]:
            print(i, "th point not in ", j, "th refPoint: ", refPointAssociationList[j])
            return True
    return False


def associateRemovePoint(
    refPointAssociationList, pointAssociationList, pos, amosaParams
):
    refPointAssociationList[pointAssociationList[pos]].remove(pos)
    for i in range(pos + 1, len(pointAssociationList)):
        ref_ind = pointAssociationList[i]
        refPointAssociationList[ref_ind].remove(i)
        refPointAssociationList[ref_ind].append(i - 1)
    pointAssociationList.pop(pos)
    return refPointAssociationList, pointAssociationList


def runAMOSA(amosaParams):
    r = int()
    k = int()
    flag = int()
    pos = int()
    deldom = float()
    amount = float()
    p = float()
    count = int()
    current = []
    func_current = []
    func_new = []
    newsol = []
    d_eval = []
    real_time_graph_data = []

    p2 = amosaParams.i_softl + 3
    p1 = amosaParams.i_archivesize - 1
    duplicate = 0

    r = random.randint(0, p1)
    current = copy.deepcopy(amosaParams.dd_archive[r])

    flag = 1
    pos = r
    func_current = copy.deepcopy(amosaParams.dd_func_archive[r])

    t = amosaParams.d_tmax
    tt = 0
    cases = [0, 0, 0]

    # Getting the reference points (later to be genenrated only once)
    amosaParams.refPoints, amosaParams.refPointsDistanceMatrix = getRefPoints(
        amosaParams.i_no_offunc
    )

    # Setting the no of iterations as the multiple of n_dir closest to 500
    n_dir = len(amosaParams.refPoints)
    amosaParams.i_no_ofiter = n_dir * round(500 / n_dir)
    print("n_iter:", amosaParams.i_no_ofiter)

    amosaParams.d_alpha = float(amosaParams.d_tmin/amosaParams.d_tmax)**(float(amosaParams.i_no_ofiter/amosaParams.maxFES))
    print("cooling rate :", amosaParams.d_alpha)
    if(amosaParams.d_alpha >= 1 or amosaParams.d_alpha < 0):
        print('Invalid cooling rate (0 < Cooling rate < 1). Exiting')
        exit()

    # list to maintain the list of visited reference points
    # 0 means unvisited
    # 1 means visited
    visitedRefDir = [0] * n_dir

    # list to store the indices of points associated with each reference point
    refPointAssociationList = []
    for i in range(n_dir):
        refPointAssociationList.append([])
    # list to indicate which reference point the point belongs to
    pointAssociationList = [-1] * amosaParams.i_archivesize

    refPointAssociationList, pointAssociationList = associateAllPoints(
        refPointAssociationList,
        pointAssociationList,
        amosaParams.refPoints,
        amosaParams.dd_func_archive,
    )

    print("No of reference directions: ", n_dir)
    print("No of iterations per temp: ", amosaParams.i_no_ofiter)

    def consoleprint(case, i):
        # print(pos, pointAssociationList)
        # print('case ' + str(case)  + '\t'+ 'archivesize: ' + str(amosaParams.i_archivesize) + '\t' + 'aList:' + str(len(pointAssociationList)))
        # errorcheck(refPointAssociationList, pointAssociationList, amosaParams)
        cases[case - 1] = cases[case - 1] + 1
        non_empty_ref = 0
        for x in refPointAssociationList:
            if len(x) != 0:
                non_empty_ref = non_empty_ref + 1
        spread = non_empty_ref / len(refPointAssociationList) * 100
        print(
            "iteration: "
            + str(i)
            + "_"
            + "case "
            + str(cases)
            + "_"
            + str(tt)
            + "th temp _ Temperature: "
            + "%.10f" % t
            + "_"
            + "archivesize: "
            + str(amosaParams.i_archivesize)
            + " Spread: "
            + str(non_empty_ref)
            + "/"
            + str(len(refPointAssociationList)),
            end="\r",
        )
        pass

    while t >= amosaParams.d_tmin:
        for i in range(amosaParams.i_no_ofiter):

            all_visited = True
            for ref_index in range(len(visitedRefDir)):
                if (
                    visitedRefDir[ref_index] == 0
                    and len(refPointAssociationList[ref_index]) > 0
                ):
                    all_visited = False
                    break

            if i % (n_dir + 1) == 0 or all_visited:
                # set all reference directions as unvisited
                visitedRefDir = [0] * n_dir

            # direction with which current point is associated with
            # cur_ref_index = pointAssociationList[pos]
            cur_ref_index = refPointToAssociate(amosaParams.refPoints, func_new)

            # debug
            # print(visitedRefDir)
            # for i in range(len(refPointAssociationList)):
            #    if(len(refPointAssociationList[i])!=0):
            #        print(i, end=",")
            # print()

            if visitedRefDir[cur_ref_index] == 0:
                visitedRefDir[cur_ref_index] = 1
            else:
                while (
                    visitedRefDir[cur_ref_index] == 1
                    or len(refPointAssociationList[cur_ref_index]) == 0
                ):
                    cur_ref_index = random.randrange(len(visitedRefDir))
                pos = random.choice(refPointAssociationList[cur_ref_index])
                try:
                    current = copy.deepcopy(amosaParams.dd_archive[pos])
                except IndexError as e:
                    print(str(e))
                    print("line 18d0", pos, len(amosaParams.dd_archive))
                    print(refPointAssociationList[cur_ref_index])
                    exit()
                func_current = copy.deepcopy(amosaParams.dd_func_archive[pos])

            duplicate = 0

            if errorcheck(refPointAssociationList, pointAssociationList, amosaParams):
                print("Error before mutation")
                exit(0)
            newsol = copy.deepcopy(current)
            newsol = point_mutate(
                newsol, amosaParams, cur_ref_index, refPointAssociationList, t
            )
            func_new = evaluate(newsol, amosaParams.c_problem, amosaParams.i_no_offunc)

            # debug
            # print(cur_ref_index, refPointToAssociate(amosaParams.refPoints, func_new))

            count1 = 0
            count2 = 0
            for j in range(amosaParams.i_no_offunc):
                # debug
                # print(func_current[j] - func_new[j])
                if func_current[j] <= func_new[j]:
                    count1 = count1 + 1
                if func_current[j] >= func_new[j]:
                    count2 = count2 + 1

            # debug
            # print(count1,count2)
            # exit(0)

            # case 1: If current dominates new-----------------------------------
            if count1 == amosaParams.i_no_offunc:
                consoleprint(1, i)
                deldom = 0.0
                amount = find_unsign_dom(func_current, func_new, amosaParams)
                deldom = deldom + amount
                for j in range(amosaParams.i_archivesize):
                    count = 1
                    if flag == 0 or i != r:
                        isdom = is_dominated(
                            amosaParams.dd_func_archive[j], func_new, amosaParams
                        )
                        if isdom:
                            count = count + 1
                            amount = find_unsign_dom(
                                amosaParams.dd_func_archive[j], func_new, amosaParams
                            )
                            deldom = deldom + amount

                # Probability for case 1
                expp = float()
                try:
                    expp = exp(deldom / t)
                except OverflowError:
                    expp = math.inf
                p = 1.0 / (1.0 + expp)

                # Selecting the new solution with probability p
                ran2 = random.random()
                if p >= ran2:
                    current = copy.deepcopy(newsol)
                    func_current = copy.deepcopy(func_new)
                    flag = 0

                if errorcheck(
                    refPointAssociationList, pointAssociationList, amosaParams
                ):
                    print("Error after case 1")
                    exit(0)

            # case 3: If new solution dominates the current----------------------
            elif count2 == amosaParams.i_no_offunc:
                k = 0
                count = 0
                deldom = math.inf
                consoleprint(3, i)
                for j in range(amosaParams.i_archivesize):
                    isdom = is_dominated(
                        amosaParams.dd_func_archive[j], func_new, amosaParams
                    )
                    if isdom:
                        count = count + 1
                        amount = find_unsign_dom(
                            amosaParams.dd_func_archive[j], func_new, amosaParams
                        )
                if amount < deldom:
                    deldom = amount
                    k = j

                # case 3(a): If new point is dominated by k(k>=1) solutions in the archive
                if count > 0:
                    p = 1 / (1 + exp(-deldom))
                    ran2 = random.random()

                    # case 3(a).1: Set point of the archive corresponding to deldom as current point with probability = p
                    if p >= ran2:
                        current = copy.deepcopy(amosaParams.dd_archive[k])
                        func_current = copy.deepcopy(amosaParams.dd_func_archive[k])
                        flag = 1
                        pos = k

                    # case 3(a).2: Set new point as current point
                    else:
                        current = copy.deepcopy(newsol)
                        func_current = copy.deepcopy(func_new)
                        flag = 0

                # case 3(b): If new point is non-dominating with respect to the point in the archive
                elif count == 0 and duplicate == 0:
                    """
                    # If current point resides in the archive then remove the current point
                    if (flag == 1):
                        amosaParams.dd_archive.pop(pos)
                        amosaParams.dd_func_archive.pop(pos)
                        amosaParams.i_archivesize = amosaParams.i_archivesize - 1
                        refPointAssociationList, pointAssociationList = associateRemovePoint(
                            refPointAssociationList, pointAssociationList, pos, amosaParams)
                        #debug
                        if(len(pointAssociationList) != len(amosaParams.dd_func_archive)):
                            print("length mismatch after line 272", len(
                                pointAssociationList), len(amosaParams.dd_archive))
                            print(pointAssociationList)
                            exit()

                    area2 = copy.deepcopy(amosaParams.dd_func_archive)
                    archive1 = copy.deepcopy(amosaParams.dd_archive)

                    k = 0
                    # If newsol dominates some other sols in archive then remove them all
                    amosaParams.i_archivesize = len(amosaParams.dd_archive)
                    amosaParams.dd_archive = []
                    amosaParams.dd_func_archive = []
                    for j in range(amosaParams.i_archivesize):
                        isdom = is_dominated(func_new, area2[j], amosaParams)
                        #errorcheck(refPointAssociationList, pointAssociationList)
                        if isdom:
                            refPointAssociationList, pointAssociationList = associateRemovePoint(
                                refPointAssociationList, pointAssociationList, j-k, amosaParams)
                            k = k + 1
                        else:
                            amosaParams.dd_archive.append((archive1[j]))
                            amosaParams.dd_func_archive.append(area2[j])
                    if(k > 0):
                        amosaParams.i_archivesize = len(amosaParams.dd_archive)
                    """
                    amosaParams.i_archivesize = len(amosaParams.dd_archive)

                    # debug
                    if len(pointAssociationList) != len(amosaParams.dd_func_archive):
                        print(
                            "length mismatch after line 300",
                            len(pointAssociationList),
                            len(amosaParams.dd_archive),
                        )
                        print(pointAssociationList)
                        exit()
                    # edited position for cluster
                    # Performing clustering if archive size if greater than soft limit
                    # if(amosaParams.i_archivesize > amosaParams.i_softl):
                    # need to modify clustering here
                    #    clustering(amosaParams)
                    #    refPointAssociationList, pointAssociationList = associateAllPoints(
                    #        refPointAssociationList, pointAssociationList, amosaParams.refPoints, amosaParams.dd_func_archive)

                    amosaParams.i_archivesize = amosaParams.i_archivesize + 1
                    m = amosaParams.i_archivesize - 1

                    # Adding the newsol to the archive
                    amosaParams.dd_archive.append(newsol)
                    amosaParams.dd_func_archive.append(func_new)
                    arefPointAssociationList, pointAssociationList = associatePoint(
                        refPointAssociationList,
                        pointAssociationList,
                        amosaParams.refPoints,
                        amosaParams.dd_func_archive,
                        len(amosaParams.dd_func_archive) - 1,
                    )

                    current = copy.deepcopy(newsol)
                    func_current = copy.deepcopy(func_new)

                    flag = 1
                    pos = m

                if errorcheck(
                    refPointAssociationList, pointAssociationList, amosaParams
                ):
                    print("Error after case 3")
                    exit(0)

            # case 2 : Current and newsol are non-dominating to each-other-------
            else:
                count = 0
                deldom = 0.0
                consoleprint(2, i)
                for j in range(amosaParams.i_archivesize):
                    isdom = is_dominated(
                        amosaParams.dd_func_archive[j], func_new, amosaParams
                    )
                    if isdom:
                        count = count + 1
                        amount = find_unsign_dom(
                            amosaParams.dd_func_archive[j], func_new, amosaParams
                        )
                        deldom = deldom + amount

                # case 2(a) : New point is dominated by k(k>=1) points in the archive
                if count > 0:
                    # debug
                    # print("New point is dominated by k(k>=1) points in the archive")
                    # exit(0)
                    expp = float()
                    try:
                        expp = exp(deldom / t)
                    except OverflowError:
                        expp = math.inf
                    p = 1.0 / (1.0 + expp)
                    ran2 = random.random()
                    if p >= ran2:
                        current = copy.deepcopy(newsol)
                        func_current = copy.deepcopy(func_new)
                        flag = 0

                # case 2(b) : New point is non-dominating with respect to all the points in the archive
                elif count == 0:
                    # debug
                    # print("New point is non-dominated")
                    # exit(0)
                    """
                    area2 = copy.deepcopy(amosaParams.dd_func_archive)
                    archive1 = copy.deepcopy(amosaParams.dd_archive)
                    k = 0
                    h = 0

                    amosaParams.i_archivesize = len(amosaParams.dd_archive)
                    amosaParams.dd_archive = []
                    amosaParams.dd_func_archive = []
                    for j in range(amosaParams.i_archivesize):
                        isdom = is_dominated(func_new, area2[j], amosaParams)
                        if(isdom):
                            refPointAssociationList, pointAssociationList = associateRemovePoint(
                                refPointAssociationList, pointAssociationList, j-k, amosaParams)
                            k = k + 1
                        else:
                            d_func_archive = copy.deepcopy(area2[j])
                            amosaParams.dd_func_archive.append(d_func_archive)
                            d_archive = copy.deepcopy(archive1[j])
                            amosaParams.dd_archive.append(d_archive)
                            h = h + 1

                    if(k > 0):
                        amosaParams.i_archivesize = len(amosaParams.dd_archive)
                    """
                    amosaParams.i_archivesize = len(amosaParams.dd_archive)

                    # debug
                    if len(pointAssociationList) != len(amosaParams.dd_func_archive):
                        print(
                            "length mismatch after line 377",
                            len(pointAssociationList),
                            len(amosaParams.dd_archive),
                        )
                        print(pointAssociationList)
                        exit(0)

                    # Re shifted clustering
                    # if(amosaParams.i_archivesize > amosaParams.i_softl):
                    #    clustering(amosaParams)
                    #    refPointAssociationList, pointAssociationList = associateAllPoints(
                    #        refPointAssociationList, pointAssociationList, amosaParams.refPoints, amosaParams.dd_func_archive)

                    m = amosaParams.i_archivesize
                    amosaParams.i_archivesize = amosaParams.i_archivesize + 1
                    d_archive = copy.deepcopy(newsol)
                    amosaParams.dd_archive.append(d_archive)
                    d_func_archive = copy.deepcopy(func_new)
                    amosaParams.dd_func_archive.append(d_func_archive)
                    refPointAssociationList, pointAssociationList = associatePoint(
                        refPointAssociationList,
                        pointAssociationList,
                        amosaParams.refPoints,
                        amosaParams.dd_func_archive,
                        len(amosaParams.dd_func_archive) - 1,
                    )

                    current = copy.deepcopy(newsol)
                    func_current = copy.deepcopy(func_new)
                    flag = 1
                    pos = m

                if errorcheck(
                    refPointAssociationList, pointAssociationList, amosaParams
                ):
                    print("Error after case 1")
                    exit(0)

            if amosaParams.i_archivesize > amosaParams.i_softl:
                clustering(amosaParams,t)
                refPointAssociationList, pointAssociationList = associateAllPoints(
                    refPointAssociationList,
                    pointAssociationList,
                    amosaParams.refPoints,
                    amosaParams.dd_func_archive,
                )

        if amosaParams.i_no_offunc == 3:
            x1 = []
            x2 = []
            x3 = []
            for i in range(len(amosaParams.dd_archive)):
                x1.append(amosaParams.dd_func_archive[i][0])
                x2.append(amosaParams.dd_func_archive[i][1])
                x3.append(amosaParams.dd_func_archive[i][2])
            real_time_graph_data.append([x1, x2, x3])

        t = round(t * amosaParams.d_alpha, 10)
        tt = tt + 1

    # added clustering at end
    print()
    clustering(amosaParams, t)

    # uncomment the following lines to show real time graph
    '''
    if amosaParams.i_no_offunc == 3:
        real_time_plot(real_time_graph_data)
    '''

    # with open('saplot.out','w+') as fp:
    obj1 = []
    obj2 = []
    obj3 = []

    if len(sys.argv) > 6:
        with open(sys.argv[6], "w+") as fp:
            for i in range(amosaParams.i_archivesize):
                for h in range(amosaParams.i_no_offunc):
                    fp.write(str(amosaParams.dd_func_archive[i][h]) + " ")
                fp.write("\n")

    with open("objective_values.txt", "w+") as fp:
        for i in range(amosaParams.i_archivesize):
            fp.write("\n")
            for h in range(amosaParams.i_no_offunc):
                fp.write("\t" + str(amosaParams.dd_func_archive[i][h]))

    with open("decision_values.txt", "w+") as fp:
        for i in range(amosaParams.i_archivesize):
            fp.write("\n")
            for h in range(amosaParams.i_totalno_var):
                fp.write("\t" + str(amosaParams.dd_archive[i][h]))


    removeDominated(amosaParams)
    print(len(amosaParams.dd_archive))

    for i in range(len(amosaParams.dd_archive)):
        for h in range(amosaParams.i_no_offunc):
            # if(amosaParams.dd_func_archive[i][0]<=1 and amosaParams.dd_func_archive[i][1]<=1 and amosaParams.dd_func_archive[i][2]<=1):#debug(filtered graph)
            if h == 0:
                obj1.append(amosaParams.dd_func_archive[i][h])
            elif h == 1:
                obj2.append(amosaParams.dd_func_archive[i][h])
            elif h == 2:
                obj3.append(amosaParams.dd_func_archive[i][h])

    # uncomment the lines below to show graphs
    '''
    if amosaParams.i_no_offunc == 2:
        plt.plot(obj1, obj2, "ro")
        plt.show()
    elif amosaParams.i_no_offunc == 3:
        fig = plt.figure()
        ax = plt.axes(projection="3d")
        ax.scatter3D(obj1, obj2, obj3)
        plt.show()
    else:
        from polar_plot import displat_polar_plot

        displat_polar_plot(amosaParams.dd_func_archive, amosaParams.c_problem)
    '''

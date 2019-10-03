from amosa import AMOSAType
import random
import copy
from math import *
from real_mutate_ind import real_mutate_ind
from test_func import evaluate
from dominance import find_unsign_dom
from dominance import is_dominated
from clustering import clustering
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from real_time_plot import real_time_plot
import math

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
    tt=0

    def consoleprint(case,i):
        print(  'iteration: ' + str(i) +'\t\t'+ 'case ' + str(case) + '\t'+ 'archivesize: ' + str(amosaParams.i_archivesize) + '\t\t\t'+ str(tt) + 'th temp \t Temperature: ' + str(t), end='\r')

    while(t >= amosaParams.d_tmin):
        for i in range(amosaParams.i_no_ofiter):
            duplicate = 0
            newsol = copy.deepcopy(current)
            real_mutate_ind(newsol, amosaParams)
            func_new = evaluate(newsol, amosaParams.c_problem,
                                amosaParams.i_no_offunc)

            count1 = 0
            count2 = 0
            for j in range(amosaParams.i_no_offunc):
                if(func_current[j] <= func_new[j]):
                    count1 = count1+1
                if(func_current[j] >= func_new[j]):
                    count2 = count2+1

            # case 1: If current dominates new-----------------------------------
            if(count1 == amosaParams.i_no_offunc):
                consoleprint(1,i)
                deldom = 0.0
                amount = find_unsign_dom(func_current, func_new, amosaParams)
                deldom = deldom + amount
                for j in range(amosaParams.i_archivesize):
                    count = 1
                    if(flag == 0 or i != r):
                        isdom = is_dominated(
                            amosaParams.dd_func_archive[j], func_new, amosaParams)
                        if(isdom):
                            count = count + 1
                            amount = find_unsign_dom(
                                amosaParams.dd_func_archive[j], func_new, amosaParams)
                            deldom = deldom + amount

                # Probability for case 1
                expp = float()
                try:
                    expp = exp(deldom/t)
                except OverflowError:
                    expp = math.inf
                p = 1.0/(1.0 + expp)

                # Selecting the new solution with probability p
                ran2 = random.random()
                if(p >= ran2):
                    current = copy.deepcopy(newsol)
                    func_current = copy.deepcopy(func_new)
                    flag = 0

            # case 3: If new solution dominates the current----------------------
            elif(count2 == amosaParams.i_no_offunc):
                k = 0
                count = 0
                deldom = math.inf
                consoleprint(3,i)
                for j in range(amosaParams.i_archivesize):
                    isdom = is_dominated(
                        amosaParams.dd_func_archive[j], func_new, amosaParams)
                    if(isdom):
                        count = count+1
                        amount = find_unsign_dom(
                            amosaParams.dd_func_archive[j], func_new, amosaParams)
                if(amount < deldom):
                    deldom = amount
                    k = j

                # case 3(a): If new point is dominated by k(k>=1) solutions in the archive
                if(count > 0):
                    p = 1/(1+exp(-deldom))
                    ran2 = random.random()

                    # case 3(a).1: Set point of the archive corresponding to deldom as current point with probability = p
                    if(p >= ran2):
                        current = copy.deepcopy(amosaParams.dd_archive[k])
                        func_current = copy.deepcopy(
                            amosaParams.dd_func_archive[k])
                        flag = 1
                        pos = k

                    # case 3(a).2: Set new point as current point
                    else:
                        current = copy.deepcopy(newsol)
                        func_current = copy.deepcopy(func_new)
                        flag = 0

                # case 3(b): If new point is non-dominating with respect to the point in the archive
                elif(count == 0 and duplicate == 0):
                    # If current point resides in the archive then remove the current point
                    if (flag == 1):
                        amosaParams.dd_archive.pop(pos)
                        amosaParams.dd_func_archive.pop(pos)
                        amosaParams.i_archivesize = amosaParams.i_archivesize - 1

                    area2 = copy.deepcopy(amosaParams.dd_func_archive)
                    archive1 = copy.deepcopy(amosaParams.dd_archive)

                    k = 0
                    # If newsol dominates some other sols in archive then remove them all
                    amosaParams.i_archivesize = len(amosaParams.dd_archive)
                    amosaParams.dd_archive = []
                    amosaParams.dd_func_archive = []
                    for j in range(amosaParams.i_archivesize):
                        isdom = is_dominated(func_new, area2[j], amosaParams)
                        if isdom:
                            k = k+1
                        else:
                            amosaParams.dd_archive.append((archive1[j]))
                            amosaParams.dd_func_archive.append(area2[j])
                    if(k > 0):
                        amosaParams.i_archivesize = len(amosaParams.dd_archive)

                    # edited position for cluster
                    # Performing clustering if archive size if greater than soft limit
                    if(amosaParams.i_archivesize > amosaParams.i_softl):
                        clustering(amosaParams)

                    amosaParams.i_archivesize = amosaParams.i_archivesize + 1
                    m = amosaParams.i_archivesize - 1

                    # Adding the newsol to the archive
                    amosaParams.dd_archive.append(newsol)
                    amosaParams.dd_func_archive.append(func_new)

                    # actural clustering done

                    current = copy.deepcopy(newsol)
                    func_current = copy.deepcopy(func_new)

                    flag = 1
                    pos = m

            # case 2 : Current and newsol are non-dominating to each-other-------
            else:
                count = 0
                deldom = 0.0
                consoleprint(2,i)
                for j in range(amosaParams.i_archivesize):
                    isdom = is_dominated(
                        amosaParams.dd_func_archive[j], func_new, amosaParams)
                    if(isdom):
                        count = count + 1
                        amount = find_unsign_dom(
                            amosaParams.dd_func_archive[j], func_new, amosaParams)
                        deldom = deldom + amount

                # case 2(a) : New point is dominated by k(k>=1) points in the archive
                if(count > 0):
                    expp = float()
                    try:
                        expp = exp(deldom/t)
                    except OverflowError:
                        expp = math.inf
                    p = 1.0/(1.0 + expp)
                    ran2 = random.random()
                    if(p >= ran2):
                        current = copy.deepcopy(newsol)
                        func_current = copy.deepcopy(func_new)
                        flag = 0

                # case 2(b) : New point is non-dominating with respect to all the points in the archive
                elif(count == 0):
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
                            k = k+1
                        else:
                            d_func_archive = copy.deepcopy(area2[j])
                            amosaParams.dd_func_archive.append(d_func_archive)
                            d_archive = copy.deepcopy(archive1[j])
                            amosaParams.dd_archive.append(d_archive)
                            h = h + 1

                    if(k > 0):
                        amosaParams.i_archivesize = len(amosaParams.dd_archive)

                    # Re shifted clustering
                    if(amosaParams.i_archivesize > amosaParams.i_softl):
                        clustering(amosaParams)

                    m = amosaParams.i_archivesize
                    amosaParams.i_archivesize = amosaParams.i_archivesize + 1
                    d_archive = copy.deepcopy(newsol)
                    amosaParams.dd_archive.append(d_archive)
                    d_func_archive = copy.deepcopy(func_new)
                    amosaParams.dd_func_archive.append(d_func_archive)

                    # actual clustering position

                    current = copy.deepcopy(newsol)
                    func_current = copy.deepcopy(func_new)
                    flag = 1
                    pos = m

        if(amosaParams.i_no_offunc == 3):
            x1 = []
            x2 = []
            x3 = []
            for i in range(len(amosaParams.dd_archive)):
                x1.append(amosaParams.dd_func_archive[i][0])
                x2.append(amosaParams.dd_func_archive[i][1])
                x3.append(amosaParams.dd_func_archive[i][2])
            real_time_graph_data.append([x1, x2, x3])

        t = round(t * amosaParams.d_alpha, 6)
        tt=tt+1

    if(amosaParams.i_no_offunc == 3):
        real_time_plot(real_time_graph_data)

    # with open('saplot.out','w+') as fp:
    obj1 = []
    obj2 = []
    obj3 = []
    with open('objective_values.txt', 'w+') as fp:

        for i in range(amosaParams.i_archivesize):
            fp.write('\n')
            for h in range(amosaParams.i_no_offunc):
                fp.write("\t" + str(amosaParams.dd_func_archive[i][h]))
                #if(amosaParams.dd_func_archive[i][0]<=1 and amosaParams.dd_func_archive[i][1]<=1 and amosaParams.dd_func_archive[i][2]<=1):#debug(filtered graph)
                if h == 0:
                    obj1.append(amosaParams.dd_func_archive[i][h])
                elif h == 1:
                    obj2.append(amosaParams.dd_func_archive[i][h])
                elif h == 2:
                    obj3.append(amosaParams.dd_func_archive[i][h])

    with open('decision_values.txt', 'w+') as fp:
        for i in range(amosaParams.i_archivesize):
            fp.write('\n')
            for h in range(amosaParams.i_totalno_var):
                fp.write("\t" + str(amosaParams.dd_archive[i][h]))

    if amosaParams.i_no_offunc == 2:
        plt.plot(obj1, obj2, 'ro')
        plt.show()
    elif amosaParams.i_no_offunc == 3:
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        ax.scatter3D(obj1, obj2, obj3)
        plt.show()

from amosa import AMOSAType
import random
import copy
from math import *
from real_mutate_ind import real_mutate_ind
from test_func import evaluate
from dominance import find_unsign_dom
from dominance import is_dominated
from clustering import clustering


def runAMOSA(amosaParams):
    r = int()
    k = int()
    flag = int()
    pos = int()
    deldom = float()
    p = float()
    count = int()
    current = []
    func_current = []
    func_new = []
    newsol = []
    d_eval = []

    p2 = amosaParams.i_softl + 3
    p1 = amosaParams.i_archivesize - 1
    duplicate = 0

    r = random.randint(0, p1)
    current = copy.deepcopy(amosaParams.dd_archive[r])

    flag = 1
    pos = r
    func_current = copy.deepcopy(amosaParams.dd_func_archive[r])

    t = amosaParams.d_tmax
    while(t >= amosaParams.d_tmin):
        print('Temperature: ' + str(t))

        '''
        # Setting range of function
        for i in range(amosaParams.i_no_offunc):
            amosaParams.d_func_range.append(
                max(amosaParams.dd_func_archive[i]) - min(amosaParams.dd_func_archive[i]))
        '''

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

                # Probablity for case 1
                p = 1.0/(1.0 + exp(deldom/t))

                # Selecting the new solution with probability p
                ran2 = random.random()
                if(p >= ran2):
                    current = copy.deepcopy(newsol)
                    func_current = copy.deepcopy(func_new)
                    flag = 0

            # case 3: If new solution dominates the current----------------------
            elif(count2 == amosaParams.i_no_offucn):
                k = 0
                count = 0
                deldom = 10000000000000

                for i in range(amosaParams.i_archivesize):
                    isdom = is_dominated(
                        amosaParams.dd_func_archive[i], func_new, amosaParams)
                    if(isdom):
                        count = count+1
                        amount = find_unsign_dom(
                            amosaParams.dd_func_archive[i], func_new, amosaParams)
                if(amount < deldom):
                    deldom = amount
                    k = i

                # case 3(a): If new point is dominated by k(k>=1) solutions in the archive
                if(count > 0):
                    p = 1/(1+exp(-deldom))
                    ran2 = random.random()

                    # case 3(a).1: Set point of the archive corresponding to deldom as current point with probability = p
                    if(p >= r):
                        current = copy.deepcopy(amosaParams.dd_archive[k])
                        func_current = copy.deepcopy()
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
                    archive1 = copy.deep(amosaParams.dd_archive)

                    k = 0
                    # If newsol dominates some other sols in archive then remove them all
                    amosaParams.dd_archive = []
                    amosaParams.dd_func_archive = []

                    for i in range(amosaParams.i_archivesize):
                        isdom = is_dominated(func_new, area2[i], amosaParams)
                        if isdom:
                            k = k+1
                        else:
                            amosaParams.dd_archive.append((archive1[i]))
                            amosaParams.dd_func_archive.append(area2[i])

                    if(k > 0):
                        amosaParams.i_archivesize = len(amosaParams.dd_archive)

                    amosaParams.i_archivesize = amosaParams.i_archivesize + 1
                    m = amosaParams.i_archivesize - 1

                    # Adding the newsol to the archive
                    amosaParams.dd_archive.append(newsol)
                    amosaParams.dd_func_archive.appned(func_new)

                    # Performing clustering if archive size if greater than soft limit
                    clustering(amosaParams)

                    current = copy.deepcopy(newsol)
                    func_current = copy.deepcopy(func_new)

                    flag = 1
                    pos = m

            # case 2 : Current and newsol are non-dominating to each-other-------
            else:
                count = 0
                deldom = 0.0

                for i in range(amosaParams.i_archivesize):
                    isdom = is_dominated(
                        amosaParams.dd_func_archive[i], func_new, amosaParams)
                    if(isdom):
                        count = count + 1
                        amount = find_unsign_dom(
                            amosaParams.dd_func_archive[i], func_new)
                        deldom = deldom + amount

                # case 2(a) : New point is dominated by k(k>=1) points in the archive
                if(count > 0):
                    p = 1.0/(1.0 + exp(deldom / t))
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

                    amosaParams.dd_archive = []
                    amosaParams.dd_func_archive = []
                    for i in range(amosaParams.i_archivesize):
                        isdom = is_dominated(func_new,area2[i],amosaParams)
                        if(isdom):
                            k = k+1
                        else:
                            d_func_archive = copy.deepcopy(area2[i])
                            amosaParams.dd_func_archive.append(d_func_archive)
                            d_archive = copy.deepcopy(archive1[i])
                            amosaParams.dd_archive.append(d_archive)
                            h = h + 1

                    if(k>0):
                        amosaParams.i_archivesize = h

                    m = amosaParams.i_archivesize
                    amosaParams.i_archivesize = amosaParams.i_archivesize + 1
                    d_archive = copy.deepcopy(newsol)
                    amosaParams.dd_archive.append(d_archive)
                    d_func_archive = copy.deepcopy(func_new)
                    amosaParams.dd_func_archive(d_func_archive)

                    if(amosaParams.i_archivesize > amosaParams.i_softl):
                        clustering(amosaParams)
                    
                    current = copy.deepcopy(newsol)
                    func_current = copy.deepcopy(func_new)
                    flag = 1
                    pos = m

        t = round(t - amosaParams.d_alpha, 6)

    with open('saplot.out','w+') as fp:
        for i in range(amosaParams.i_archivesize):
            fp.write('\n')
            for h in range(amosaParams.i_no_offunc):
                fp.write("\t" + str(amosaParams.dd_func_archive[i][h]))

    with open('saplot1.out','w+') as fp:
        for i in range(amosaParams.i_archivesize):
            fp.write('\n')
            for h in range(amosaParams.i_totalno_var):
                fp.write("\t" + str(amosaParams.dd_archive[i][h]))
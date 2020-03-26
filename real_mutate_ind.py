import random
import copy
from math import *


def real_mutate_ind(s, amosaParam, b = 0.25):
    '''Function to perform mutation on individual input vector'''

    i_rand = random.randint(0, amosaParam.i_totalno_var - 1)
    y = s[i_rand]
    y = mutate(y, amosaParam, i_rand, b)
    #y = random.random()*(amosaParam.d_max_real_var[i_rand]-amosaParam.d_min_real_var[i_rand]) + amosaParam.d_min_real_var[i_rand]
    i_count = 0
    while((y < amosaParam.d_min_real_var[i_rand] or y > amosaParam.d_max_real_var[i_rand]) and i_count < amosaParam.i_hillclimb_no):
        y = s[i_rand]
        y = mutate(y, amosaParam, i_rand, b)
        i_count = i_count + 1

    if(y<amosaParam.d_min_real_var[i_rand]):
        y=amosaParam.d_min_real_var[i_rand]
    elif(y>amosaParam.d_max_real_var[i_rand]):
        y=amosaParam.d_max_real_var[i_rand]
        
    # Update input vector element
    s[i_rand] = y
    return s



def distance(point1,point2):
    if(len(point1) != len(point2)):
        print("point dimension mismatch")
        exit(0);
    distance = 0
    for i in range(len(point1)):
        try:
            distance = distance + (point1[i]-point2[i])**2
        except OverflowError:
            print(OverflowError)
            print(point1[i],point2[i])
            exit(0)
    distance = distance**0.5
    return distance

def ref_real_mutate_ind(s, amosaParams, cur_ref_index, refPointAssociationList, temp):
    nNeig = int(0.2*len(amosaParams.refPoints))
    neigs = []
    nonEmp = 0
    for i in range(len(amosaParams.refPoints)):
        if len(refPointAssociationList[i])!=0:
            neigs.append(i)
            nonEmp = nonEmp + 1
            if(nonEmp >= nNeig):
                break
    point1Ind=0
    point2Ind=0
    flag = 0
    if(len(neigs)>1):
        neigRefs = random.sample(neigs,2)
        point1Ind = random.sample(refPointAssociationList[neigRefs[0]],1)
        point2Ind = random.sample(refPointAssociationList[neigRefs[1]],1)
    elif(len(neigs)==1):
        point1Ind = random.sample(refPointAssociationList[cur_ref_index],1)
        point2Ind = random.sample(refPointAssociationList[neigs[0]],1)
    elif(len(refPointAssociationList[cur_ref_index])>1):
        point1Ind = random.sample(refPointAssociationList[cur_ref_index],1)
        point2Ind = random.sample(refPointAssociationList[cur_ref_index],1)
    else:
        flag=1
        b=0.5

    if(flag==0):
        point1 = amosaParams.dd_archive[point1Ind[0]]
        point2 = amosaParams.dd_archive[point2Ind[0]]
        b = distance(point1, point2)
    else:
        b=0.5
    b=b*(10**random.randint(0,3))
    
    #print("b=",b)
    #if(b>100):
    #    print(point1)
    #    print(point2)
    #    exit(0)
    s_new = real_mutate_ind(s,amosaParams,b)
    return s_new

def rand():
    '''Generates a random number with range (-0.5,0,5)'''
    x = random.random()
    while x == 0:
        x = random.random()
    x = x-0.5
    #x = x*(10**random.randint(-5,0))
    return x


def mutate(y, amosaParam, i_rand, b):
    '''Perform mutation on individual vector element'''
    d_rand = rand()

    d_rand_lap = int()
    if(d_rand < 0):
        d_rand_lap = b * log(1-2*fabs(d_rand))
    else:
        d_rand_lap = - b * log(1-2*fabs(d_rand))
    y = y + d_rand_lap
    return y

def point_mutate(s, amosaParams, cur_ref_index, refPointAssociationList, temp):
    #s = ref_real_mutate_ind(s, amosaParams, cur_ref_index, refPointAssociationList, temp)
    #s = polynomial_mutate(s, temp, 100*temp, amosaParams.d_min_real_var, amosaParams.d_max_real_var)
    #s = diff_mut(amosaParams.dd_archive, amosaParams.refPointsDistanceMatrix, refPointAssociationList, cur_ref_index, s, amosaParams.d_min_real_var, amosaParams.d_max_real_var)
    s = SBX_mut(amosaParams.dd_archive, amosaParams.refPointsDistanceMatrix, refPointAssociationList, cur_ref_index, s, amosaParams.d_min_real_var, amosaParams.d_max_real_var)
    return s

# Testing new perturbation schemes------------------------------------------

def getnNeighbours(n_samples, refPointsDistanceMatrix, refPointAssociationList, cur_ref_index): 
    point_samples = []
    count = 0
    ref_nbr_no = 0
    while(count < n_samples):
        ref_nbr_index = refPointsDistanceMatrix[cur_ref_index][ref_nbr_no]
        nbr_index_list = refPointAssociationList[ref_nbr_index]
        samples_left = n_samples - count
        if(len(nbr_index_list) > samples_left):
            point_samples = point_samples + random.sample(nbr_index_list,samples_left)
            count = count + samples_left
        else:
            point_samples = point_samples + nbr_index_list
            count = count + len(nbr_index_list)

        ref_nbr_no = ref_nbr_no + 1
    return point_samples

# GA based reproduction - it needs one more random candidate from the archive
def SBX(parent1, parent2, eta_c, cross_prob, min_x, max_x):
    child1 = copy.deepcopy(parent1)
    child2 = copy.deepcopy(parent2)
    EPS=0.0000000001
    r = random.random()
    if (r < cross_prob):
        for i in range(0, len(parent1)):
            r = random.random()
            if (r <= 0.9):
                if (abs(parent1[i] - parent2[i]) > EPS):
                    y1 = min(parent1[i], parent2[i])
                    y2 = max(parent1[i], parent2[i])
                    yl = min_x[i]
                    yu = max_x[i]
                    r = random.random()
                    beta = 1.0 + (2.0 * (y1 - yl) / (y2 - y1))
                    alpha = 2.0 - (beta ** (-1.0 * (1.0 + eta_c)))
                    betaq = 0.0
                    if (r <= (1.0 / alpha)):
                        betaq = (r * alpha) ** (1.0 / (eta_c + 1.0))
                    else:
                        betaq = (1.0 / (2.0 - (r * alpha))) ** (1.0 / (eta_c + 1.0))
                    child1[i] = 0.5 * (y1 + y2 - (betaq * (y2 - y1)))

                    beta = 1.0 + (2.0 * (yu - y2) / (y2 - y1))
                    alpha = 2.0 - (beta ** (-1.0 * (1.0 + eta_c)))
                    if (r <= (1.0 / alpha)):
                        betaq = (r * alpha) ** (1.0 / (eta_c + 1.0))
                    else:
                        betaq = (1.0 / (2.0 - (r * alpha))) ** (1.0 / (eta_c + 1.0))
                    child2[i] = 0.5 * ((y1 + y2) + (betaq * (y2 - y1)))

                    child1[i] = min(yu, max(yl, child1[i]))
                    child2[i] = min(yu, max(yl, child2[i]))

                    r = random.random()
                    if (r <= 0.5):
                        sw = child1[i]
                        child1[i] = child2[i]
                        child2[i] = sw

    return child1, child2


def SBX_mut(archive, refPointsDistanceMatrix, refPointAssociationList, cur_ref_index, p1, min_x, max_x, eta_c = 30, cross_prob = 1):
    point_samples = getnNeighbours(1, refPointsDistanceMatrix, refPointAssociationList, cur_ref_index)
    p2 = copy.deepcopy(archive[point_samples[0]])

    c1, c2 = SBX(p1, p2, eta_c, cross_prob, min_x, max_x)
    v_new = []
    rnd = random.random()
    if (rnd > 0.5):
        v_new = c1
    else:
        v_new = c2

    return v_new


# DE based reproduction - it needs 3 more random candidates from the archive
def diff_mut(archive, refPointsDistanceMatrix, refPointAssociationList, cur_ref_index, v, min_x, max_x, F = 1, CR = 1):
    size = len(v)

    point_samples = getnNeighbours(3, refPointsDistanceMatrix, refPointAssociationList, cur_ref_index)
    p1 = copy.deepcopy(archive[point_samples[0]])
    p2 = copy.deepcopy(archive[point_samples[1]])
    p3 = copy.deepcopy(archive[point_samples[2]])

    k_rand = random.randint(0, size - 1)
    u = copy.deepcopy(v)
    for k in range(0, size):
        r = random.random()
        if ((r < CR) or (k == k_rand)):
            u[k] = min(max_x[k], max(p1[k] + F * (p2[k] - p3[k]), min_x[k]))
    print(v)
    print(u)
    exit(0)
    return u

# Polynomial mutation - effective to escape local optima - it doesn't need any other candidate except the current candidate
def polynomial_mutate(v, mut_prob, eta_m, min_x, max_x):
    v_new = copy.deepcopy(v)
    for i in range(0, len(v)):
        r = random.random()
        if (r < mut_prob):
            y = v_new[i]
            yl = min_x[i]
            yu = max_x[i]

            delta1 = (y - yl) / (yu - yl)
            delta2 = (yu - y) / (yu - yl)

            mut_pow = 1.0 / (eta_m + 1.0)
            deltaq = 0.0

            rnd = random.random()

            if (rnd <= 0.5):
                xy = 1.0 - delta1
                val = (2.0 * rnd) + ((1.0 - (2.0 * rnd)) * (xy ** (eta_m + 1.0)))
                deltaq = (val ** mut_pow) - 1.0
            else:
                xy = 1.0 - delta2
                val = (2.0 * (1.0 - rnd)) + (2.0 * (rnd - 0.5) * (xy ** (eta_m + 1.0)))
                deltaq = 1.0 - (val ** mut_pow)

            y = y + deltaq * (yu - yl)
            y = min(yu, max(yl, y))
            v_new[i] = y
    return v_new

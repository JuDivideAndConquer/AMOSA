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
    s = ref_real_mutate_ind(s, amosaParams, cur_ref_index, refPointAssociationList, temp)
    s = polynomial_mutate(s, temp, 100*temp, amosaParams.d_min_real_var, amosaParams.d_max_real_var)
    return s

# Testing new perturbation schemes------------------------------------------

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

import random
from math import *


def real_mutate_ind(s, amosaParam):
    '''Function to perform mutation on individual input vector'''

    i_rand = random.randint(0, amosaParam.i_totalno_var - 1)
    y = s[i_rand]
    y = mutate(y, amosaParam, i_rand)
    i_count = 0
    while((y < amosaParam.d_min_real_var[i_rand] or y > amosaParam.d_max_real_var[i_rand]) and i_count < amosaParam.i_hillclimb_no):
        y = s[i_rand]
        y = mutate(y, amosaParam, i_rand)
        i_count = i_count + 1
        
    # Update input vector element
    s[i_rand] = y


def rand():
    '''Generates a random number with range (-0.5,0,5)'''
    x = random.random()
    while x == 0:
        x = random.random()
    x = x-0.5
    return x


def mutate(y, amosaParam, i_rand):
    '''Perform mutation on individual vector element'''
    b = 0.25
    d_rand = rand()

    d_rand_lap = int()
    if(d_rand < 0):
        d_rand_lap = b * log(1-2*fabs(d_rand))
    else:
        d_rand_lap = - b * log(1-2*fabs(d_rand))
    y = y + d_rand_lap
    return y

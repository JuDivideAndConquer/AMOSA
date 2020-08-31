from amosa import AMOSAType
from math import *


def find_unsign_dom(func1, func2, amosaParams):
    '''Returns the amount by which func1 dominates func2'''
    d_dominance = 1.0
    for i in range(amosaParams.i_no_offunc):
        if(func1[i]-func2[i] != 0):
            d_dominance = d_dominance * \
                fabs(func1[i]-func2[i])/amosaParams.d_func_range[i]
    return d_dominance


def is_dominated(func1, func2, amosaParams):
    '''Checks if func1 dominates func2'''
    i_count_less = 0
    i_count_equal = 0
    for i in range(amosaParams.i_no_offunc):
        if(func1[i] < func2[i]):
            i_count_less = i_count_less + 1
        elif(func1[i] == func2[i]):
            i_count_equal = i_count_equal + 1
    if(((i_count_equal+i_count_less) == amosaParams.i_no_offunc) and i_count_less > 0):
        return True
    else:
        return False

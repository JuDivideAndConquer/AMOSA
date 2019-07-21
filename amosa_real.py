#!/usr/bin/env python3

from amosa import AMOSAType
from test_func import VALID_FUNC
from test_func import init_functions
from init_sol import initialize_sol
from creating_archive import creating_archive
from main_process import runAMOSA
import math


def readParameters(amosaParams):
    func = input('Enter the test function name: ')
    if(not (func in VALID_FUNC)):
        print('Invaid function name. Exiting')
        exit()

    # Setting the problem function
    amosaParams.c_problem = str(func)

    # Setting the number of objective functions
    amosaParams.i_no_offunc, amosaParams.i_totalno_var = init_functions(func)

    # Setting hard and soft limits on archive size
    amosaParams.i_hardl = int(input('Enter the hard-limit: '))
    amosaParams.i_softl = int(input('Enter the soft-limit: '))
    if(amosaParams.i_softl < amosaParams.i_hardl):
        print('Invalid soft and hard limits. Exiting')
        exit()

    # Setting the number of iterations per temperature
    amosaParams.i_no_ofiter = 100

    # Setting temperature limits
    amosaParams.d_tmin = 0.000025
    amosaParams.d_tmax = 100

    # Function range according to input variables

    # Setting hill-climb number
    amosaParams.i_hillclimb_no = 20

    # Setting the cooling rate
    amosaParams.d_alpha = float(input('Enter the cooling rate: '))
    if(amosaParams.d_alpha >= 1 or amosaParams.d_alpha < 0):
        print('Invalid cooling rate (0 < Cooling rate < 1). Exiting')
        exit()

    # Setting the range of values of variables
    '''for i in range(amosaParams.i_totalno_var):
        amosaParams.d_min_real_var.append(
            float(input('Enter the minimim value of real-variable '+str(i)+': ')))
        amosaParams.d_max_real_var.append(
            float(input('Enter the maximum value of real-variable '+str(i)+': ')))'''
    for i in range(amosaParams.i_totalno_var):
        amosaParams.d_min_real_var.append(0.0)
        amosaParams.d_max_real_var.append(1.0)
    
    print (amosaParams.d_min_real_var)
    print (amosaParams.d_max_real_var)

    # Initialize the solution
    initialize_sol(amosaParams)

    # Initialize the archive according to the solutions
    creating_archive(amosaParams)

    # Setting range of function
    for i in range(amosaParams.i_no_offunc):
        d_max = - math.inf
        d_min = math.inf
        for j in range(len(amosaParams.dd_func_archive)):
            if(amosaParams.dd_func_archive[j][i]>d_max):
                d_max = amosaParams.dd_func_archive[j][i]
            if(amosaParams.dd_func_archive[j][i]<d_min):
                d_min = amosaParams.dd_func_archive[j][i]
        amosaParams.d_func_range.append(d_max-d_min)


'''Main function (Execution starting point)'''
amosaParams = AMOSAType()
readParameters(amosaParams)

# Calling the main fucntion which runs the algorithm proposed in AMOSA
runAMOSA(amosaParams)

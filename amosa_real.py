#!/usr/bin/env python3

from amosa import AMOSAType
from test_func import VALID_FUNC
from test_func import init_functions
from init_sol import initialize_sol
from creating_archive import creating_archive

def readParameters(amosaParams):
    func = input('Enter the test function name: ')
    if(not (func in VALID_FUNC)):
        print('Invaid function name. Exiting')
        exit()
        
    #Setting the problem function
    amosaParams.c_problem = str(func)
    
    # Setting the number of objective functions
    amosaParams.i_no_offunc,amosaParams.i_totalno_var = init_functions(func)
    
    # Setting hard and soft limits on archive size
    amosaParams.i_hardl = int(input('Enter the hard-limit: '))
    amosaParams.i_softl = int(input('Enter the soft-limit: '))
    if(amosaParams.i_softl < amosaParams.i_hardl):
        print('Invalid soft and hard limits. Exiting')
        exit()
    
    # Setting the number of iterations per temperature
    amosaParams.i_no_ofiter = 500
    
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
    for i in range(amosaParams.i_totalno_var):
        amosaParams.d_min_real_var.append(float(input('Enter the minimim value of real-variable '+str(i)+': ')))
        amosaParams.d_max_real_var.append(float(input('Enter the maximum value of real-variable '+str(i)+': ')))
        
    # Initialize the solution
    initialize_sol(amosaParams)
    
    # Initialize the archive according to the solutions
    creating_archive(amosaParams)


       

'''Main function (Execution starting point)'''
amosaParams = AMOSAType()
readParameters(amosaParams)


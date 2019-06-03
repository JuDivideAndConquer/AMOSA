from amosa import AMOSAType
import random

def initialize_sol(amosaParams):
    '''Function to initialize the solution set'''
    
    #Randomly inializing the softl number of solutions
    for i in range(amosaParams.i_softl):
        solution = []
        for j in range(amosaParams.i_totalno_var):
            solution.append(random.uniform(amosaParams.d_min_real_var[j],amosaParams.d_max_real_var[j]))
        amosaParams.dd_solution.append(solution)
        
    
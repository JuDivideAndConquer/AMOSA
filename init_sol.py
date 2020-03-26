from amosa import AMOSAType
import random
from test_func import evaluate
from real_mutate_ind import real_mutate_ind

def initialize_sol(amosaParams):
    '''Function to initialize the solution set'''
    
    # Randomly inializing the softl number of solutions
    for i in range(amosaParams.i_softl):
        solution = []
        for j in range(amosaParams.i_totalno_var):
            solution.append(random.uniform(amosaParams.d_min_real_var[j],amosaParams.d_max_real_var[j]))
        amosaParams.dd_solution.append(solution)
        
        
    # Performing hill-climbing operation on solution of the archive
    for i in range(amosaParams.i_softl):
        d_eval = []
        d_xnew = []
        d_area1 = []
        d_area2 = []
        for j in range(amosaParams.i_hillclimb_no):
            d_eval = evaluate(amosaParams.dd_solution[i],amosaParams.c_problem,amosaParams.i_no_offunc)

            for k in range(amosaParams.i_no_offunc):
                d_area1.append(d_eval[k])
            
            for k in range(amosaParams.i_totalno_var):
                d_xnew.append(amosaParams.dd_solution[i][k])

            #####
            d_xnew = real_mutate_ind(d_xnew,amosaParams)
            d_eval = evaluate(d_xnew, amosaParams.c_problem,amosaParams.i_no_offunc)
            
            for k in range(amosaParams.i_no_offunc):
                d_area2.append(d_eval[k])
            
            # Checking if all the new solutions are better than the old solutions
            count=0
            for k in range(amosaParams.i_no_offunc):
                if(d_area1[k]>=d_area2[k]):
                    count=count+1
            if(count==amosaParams.i_no_offunc):
                for k in range(amosaParams.i_totalno_var):
                    amosaParams.dd_solution[i][k] = d_xnew[k]

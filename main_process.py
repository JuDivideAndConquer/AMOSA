from amosa import AMOSAType
import random
import copy
from real_mutate_ind import real_mutate_ind
from test_func import evaluate


def runAMOSA(amosaParams):
    r = int()
    flag = int()
    pos = int()
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

        for i in range(amosaParams.i_no_ofider):
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

    		# case 1: If current dominates new
            if(count1 == amosaParams.i_no_offunc):
				print('Temporary statement')

        t = t - amosaParams.d_alpha

from amosa import AMOSAType
import random
import copy
from math import *
from real_mutate_ind import real_mutate_ind
from test_func import evaluate
from dominance import find_unsign_dom
from dominance import is_dominated


def runAMOSA(amosaParams):
	r = int()
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

			# case 1: If current dominates new
			if(count1 == amosaParams.i_no_offunc):
				deldom = 0.0
				amount = find_unsign_dom(func_current, func_new, amosaParams)
				deldom = deldom + amount
				for j in range(amosaParams.i_archivesize):
					count=1
					if(flag == 0 or i!=r):
						isdom = is_dominated(amosaParams.dd_func_archive[j],func_new,amosaParams)
						if(isdom):
							count = count + 1
							amount = find_unsign_dom(amosaParams.dd_func_archive[j],func_new,amosaParams)
							deldom = deldom + amount
				
				# Probablity for case 1
				p = 1.0/(1.0 + exp(deldom/t))

				# Selecting the new solution with probability p
				ran2 = random.random()
				if(p>=ran2):
					current = copy.deepcopy(newsol)
					func_current = copy.deepcopy(func_new)
					flag = 0

		t = round(t - amosaParams.d_alpha,6)

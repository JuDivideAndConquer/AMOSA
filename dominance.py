from amosa import AMOSAType


def find_unsign_dom(func1, func2, amosaParams):
    d_dominance = 1.0
    for i in range(amosaParams.i_no_offunc):
        if(func1[i]-func2[i] != 0):
			d_dominance = d_dominance * fabs(func1[i]-func2[i])/amosaParams.d_func_range[i]
	return d_dominance

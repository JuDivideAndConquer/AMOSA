from test_func import *
from amosa import AMOSAType

def evaluate(input,amosaParams):
    if(amosaParams.c_problem == 'SCH1'):
        amosaParams.d_eval = SCH1(input)
        return
    elif(amosaParams.c_problem == 'SCH2'):
        amosaParams.d_eval = SCH2(input)
        return
    elif(amosaParams.c_problem == 'DTLZ1'):
        amosaParams.d_eval = DTLZ1(input,amosaParams.i_no_offunc)
        return
    elif(amosaParams.c_problem == 'DTLZ2'):
        amosaParams.d_eval = DTLZ2(input,amosaParams.i_no_offunc)
        return
    elif(amosaParams.c_problem == 'DTLZ3'):
        amosaParams.d_eval = DTLZ3(input,amosaParams.i_no_offunc)
        return
    elif(amosaParams.c_problem == 'DTLZ4'):
        amosaParams.d_eval = DTLZ4(input,amosaParams.i_no_offunc)
        return
    else:
        print ('Invalid arguement for amosaParams.c_problem\nExiting.')
        exit()


a = AMOSAType()
a.i_no_offunc = 3
a.c_problem = 'DTLZ4'
input = [0,0,0,0,0,0]
evaluate(input,a)
print (a.d_eval)
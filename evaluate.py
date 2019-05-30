from test_func import *
from amosa import AMOSAType

def evaluate(input,amosaParams):
    if(amosaParams.c_problem == 'SCH1'):
        amosaParams.d_eval = SCH1(input)
        return
    elif(amosaParams.c_problem == 'SCH2'):
        amosaParams.d_eval = SCH2(input)
        return
    else:
        print ('Invalid arguement for amosaParams.c_problem\nExiting.')
        exit()
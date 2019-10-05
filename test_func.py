from math import *
from amosa import AMOSAType

VALID_FUNC = ['SCH1', 'SCH2', 'DTLZ1', 'DTLZ2', 'DTLZ3',
              'DTLZ4', 'ZDT1', 'ZDT2', 'ZDT3', 'ZDT4', 'ZDT5', 'ZDT6']


def init_functions(func):
    '''Sets the number of variables and objectives for the test function'''
    obj = 0
    var = 0
    if(func in ['SCH1', 'SCH2']):
        print("Number of objective functions: 2")
        print("Number of variables: 1")
        obj = 2
        var = 1
    elif(func in ['DTLZ1', 'DTLZ2', 'DTLZ3', 'DTLZ4']):
        #obj = int(input("Enter the number of objective function: "))
        print("Number of objective functions: 3")#debug
        obj = 3
        k = int()
        if(func == 'DTLZ1'):
            k = 5
        elif(func in ['DTLZ2', 'DTLZ3', 'DTLZ4']):
            k = 10
        var = obj + k - 1
        print("Number of variables: " + str(var))
    elif(func in ['ZDT1', 'ZDT2', 'ZDT3', 'ZDT4', 'ZDT5', 'ZDT6']):
        print("Number of objective functions: 2")
        obj = 2
        var = int(input("Enter  the number of variables: "))
    else:
        obj = int(input("Enter the number of objective functions: "))
        var = int(input("Enter  the number of variables: "))
    return obj, var


def evaluate(input, c_problem, i_no_offunc):
    if(c_problem == 'SCH1'):
        d_eval = SCH1(input[0])
        return d_eval
    elif(c_problem == 'SCH2'):
        d_eval = SCH2(input[0])
        return d_eval
    elif(c_problem == 'DTLZ1'):
        d_eval = DTLZ1(input, i_no_offunc)
        return d_eval
    elif(c_problem == 'DTLZ2'):
        d_eval = DTLZ2(input, i_no_offunc)
        return d_eval
    elif(c_problem == 'DTLZ3'):
        d_eval = DTLZ3(input, i_no_offunc)
        return d_eval
    elif(c_problem == 'DTLZ4'):
        d_eval = DTLZ4(input, i_no_offunc)
        return d_eval
    elif(c_problem == 'ZDT1'):
        d_eval = ZDT1(input)
        return d_eval
    elif(c_problem == 'ZDT2'):
        d_eval = ZDT2(input)
        return d_eval
    elif(c_problem == 'ZDT3'):
        d_eval = ZDT3(input)
        return d_eval
    elif(c_problem == 'ZDT4'):
        d_eval = ZDT4(input)
        return d_eval
    # elif(c_problem == 'ZDT5'):
    #     d_eval = ZDT5(input)
        return d_eval
    elif(c_problem == 'ZDT6'):
        d_eval = ZDT6(input)
        return d_eval
    else:
        print('Invalid arguement for amosaParams.c_problem\nExiting.')
        exit()


def ZDT1(input_arr):
    f1 = input_arr[0]
    s = 0.0
    for i in range(1, len(input_arr)):
        s = s + input_arr[i]
    g = 1.0 + ((9.0*s)/(len(input_arr)-1.0))
    f2 = g * (1.0 - sqrt(f1/g))
    return [f1, f2]


def ZDT2(input_arr):
    f1 = input_arr[0]
    s = 0.0
    for i in range(1, len(input_arr)):
        s = s + input_arr[i]
    g = 1.0 + ((9.0*s)/(len(input_arr)-1.0))
    f2 = g*(1.0 - ((f1/g)**2))
    return [f1, f2]


def ZDT3(input_arr):
    f1 = input_arr[0]
    s = 0.0
    for i in range(1, len(input_arr)):
        s = s + input_arr[i]
    g = 1.0 + ((9.0*s)/(len(input_arr)-1.0))
    f2 = g*(1.0 - sqrt(f1/g) - ((f1/g)*sin(10.0*3.14*f1)))
    return [f1, f2]


def ZDT4(input_arr):
    f1 = input_arr[0]
    s = 0.0
    for i in range(1, len(input_arr)):
        s = s + ((input_arr[i]**2) - (10.0*cos(4*3.14*input_arr[i])))
    g = 1.0 + (10.0*(len(input_arr)-1.0)) + s
    f2 = g*(1.0 - ((f1/g)**2))
    return [f1, f2]


def ZDT6(input_arr):
    f1 = 1.0 - (exp(-4.0*input_arr[0])*((sin(6.0*3.14*input_arr[0]))**6))
    s = 0.0
    for i in range(1, len(input_arr)):
        s = s + input_arr[i]
    g = 1.0 + 9.0*((s/(len(input_arr)-1.0))**0.25)
    f2 = 1.0 - ((f1/g)**2)
    return [f1, f2]


def DTLZ1(input_arr, n_obj):
    n_var = len(input_arr)
    k = n_var - n_obj + 1
    out = [0.0]*n_obj
    g = 0.0
    for i in range(n_var-k, n_var):
        g = g + ((input_arr[i] - 0.5)**2) - cos(20*pi*(input_arr[i] - 0.5))
    g = 100*(k+g)
    for i in range(1, n_obj+1):
        s = 0.5 * (1 + g)
        j = n_obj - i
        while j >= 1:
            j = j - 1
            s = s * input_arr[j]
        if i > 1:
            s = s * (1 - input_arr[n_obj - i])
        out[i-1] = s
    return out


def DTLZ2(input_arr, n_obj):
    n_var = len(input_arr)
    k = n_var - n_obj + 1
    out = [0.0]*n_obj
    g = 0.0
    for i in range(n_var-k, n_var):
        g = g + ((input_arr[i] - 0.5)**2)
    for i in range(1, n_obj+1):
        s = (1.0 + g)
        j = n_obj - i
        while j >= 1:
            j = j - 1
            s = s * cos(pi*input_arr[j]*0.5)
        if i > 1:
            s = s * sin(input_arr[n_obj - i]*pi/2)
        out[i-1] = s
    return out


def DTLZ3(input_arr, n_obj):
    n_var = len(input_arr)
    k = n_var - n_obj + 1
    g = 0.0
    for i in range(n_obj-1, n_var):
        g += (((input_arr[i]-0.5)**2) - cos(20.0*pi*(input_arr[i]-0.5)))
    g = (k+g)*100
    out = [0.0]*n_obj
    for m in range(0, n_obj):
        product = (1+g)
        i = 0
        while((i+m) <= n_obj-2):
            product *= cos(input_arr[i]*pi/2)
            i += 1
        if m > 0:
            product *= sin(input_arr[i]*pi/2)
        out[m] = product
    return out


def DTLZ4(input_arr, n_obj, a=100):
    n_var = len(input_arr)
    k = n_var - n_obj + 1
    g = 0.0
    for i in range(n_obj-1, n_var):
        g += ((input_arr[i]-0.5)**2)
    out = [0.0]*n_obj
    for m in range(0, n_obj):
        product = (1+g)
        i = 0
        while((i+m) <= n_obj-2):
            product *= cos((input_arr[i]**a)*pi/2)
            i += 1
        if m > 0:
            product *= sin((input_arr[i]**a)*pi/2)
        out[m] = product
    return out


def SCH1(input):
    func1 = input**2
    func2 = (input-2.0)**2
    out = [func1, func2]
    return out


def SCH2(input):
    func1 = float()
    if(input <= 1):
        func1 = - input
    elif (input > 1 and input <= 3):
        func1 = input - 2
    elif (input > 3 and input <= 4):
        func1 = 4 - input
    else:
        func1 = input - 4
    func2 = (input - 5)**2
    out = [func1, func2]
    return out


# functions left:
# DTLZ5
# DTLZ7
# Dev1
# Dev2
# Dev3
# Dev4
# ZDT1
# ZDT2
# ZDT3
# ZDT6

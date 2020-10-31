from math import *
from amosa import AMOSAType
import sys
import copy
import random
import time
import operator
import csv
from numpy import linalg as LA
from optproblems import wfg

VALID_FUNC = [
    "SCH1",
    "SCH2",
    "DTLZ1",
    "DTLZ2",
    "DTLZ3",
    "DTLZ4",
    "ZDT1",
    "ZDT2",
    "ZDT3",
    "ZDT4",
    "ZDT5",
    "ZDT6",
    "IMB1",
    "IMB2",
    "IMB3",
    "IMB4",
    "IMB5",
    "IMB6",
    "IMB7",
    "IMB8",
    "IMB9",
    "IMB10",
]


def init_functions(func):
    """Sets the number of variables and objectives for the test function"""
    obj = 0
    var = 0
    if func in ["SCH1", "SCH2"]:
        print("Number of objective functions: 2")
        print("Number of variables: 1")
        obj = 2
        var = 1
    elif func in ["DTLZ1", "DTLZ2", "DTLZ3", "DTLZ4"]:
        obj = int(sys.argv[2])
        k = int()
        if func == "DTLZ1":
            k = 5
        elif func in ["DTLZ2", "DTLZ3", "DTLZ4"]:
            k = 10
        var = obj + k - 1
        print("Number of variables: " + str(var))
    elif func in ["ZDT1", "ZDT2", "ZDT3", "ZDT4", "ZDT5", "ZDT6"]:
        print("Number of objective functions: 2")
        obj = 2
        var = 30
    elif func in ["IMB1", "IMB2", "IMB3", "IMB7", "IMB8", "IMB9"]:
        print("Number of objective functions: 2")
        print("Number of variables: 10")
        obj = 2
        var = 10
    elif func in ["IMB4", "IMB5", "IMB6", "IMB10"]:
        print("Number of objective functions: 3")
        print("Number of variables: 10")
        obj = 3
        var = 10
    else:
        # obj = int(sys.argv[2])
        # var = int(input("Enter  the number of variables: "))
        print("Unknown function")
        exit()
    return obj, var


def evaluate(input, c_problem, i_no_offunc):
    if c_problem == "SCH1":
        d_eval = SCH1(input[0])
        return d_eval
    elif c_problem == "SCH2":
        d_eval = SCH2(input[0])
        return d_eval
    elif c_problem == "DTLZ1":
        d_eval = DTLZ1(input, i_no_offunc)
        return d_eval
    elif c_problem == "DTLZ2":
        d_eval = DTLZ2(input, i_no_offunc)
        return d_eval
    elif c_problem == "DTLZ3":
        d_eval = DTLZ3(input, i_no_offunc)
        return d_eval
    elif c_problem == "DTLZ4":
        d_eval = DTLZ4(input, i_no_offunc)
        return d_eval
    elif c_problem == "ZDT1":
        d_eval = ZDT1(input)
        return d_eval
    elif c_problem == "ZDT2":
        d_eval = ZDT2(input)
        return d_eval
    elif c_problem == "ZDT3":
        d_eval = ZDT3(input)
        return d_eval
    elif c_problem == "ZDT4":
        d_eval = ZDT4(input)
        return d_eval
    elif c_problem == "ZDT6":
        d_eval = ZDT6(input)
        return d_eval
    elif c_problem == "IMB1":
        return IMB1(input)
    elif c_problem == "IMB2":
        return IMB2(input)
    elif c_problem == "IMB3":
        return IMB3(input)
    elif c_problem == "IMB4":
        return IMB4(input)
    elif c_problem == "IMB5":
        return IMB5(input)
    elif c_problem == "IMB6":
        return IMB6(input)
    elif c_problem == "IMB7":
        return IMB7(input)
    elif c_problem == "IMB8":
        return IMB8(input)
    elif c_problem == "IMB9":
        return IMB9(input)
    elif c_problem == "IMB10":
        return IMB10(input)
    else:
        print("Invalid arguement for amosaParams.c_problem\nExiting.")
        exit()


def ZDT1(input_arr):
    f1 = input_arr[0]
    s = 0.0
    for i in range(1, len(input_arr)):
        s = s + input_arr[i]
    g = 1.0 + ((9.0 * s) / (len(input_arr) - 1.0))
    f2 = g * (1.0 - sqrt(f1 / g))
    return [f1, f2]


def ZDT2(input_arr):
    f1 = input_arr[0]
    s = 0.0
    for i in range(1, len(input_arr)):
        s = s + input_arr[i]
    g = 1.0 + ((9.0 * s) / (len(input_arr) - 1.0))
    f2 = g * (1.0 - ((f1 / g) ** 2))
    return [f1, f2]


def ZDT3(input_arr):
    f1 = input_arr[0]
    s = 0.0
    for i in range(1, len(input_arr)):
        s = s + input_arr[i]
    g = 1.0 + ((9.0 * s) / (len(input_arr) - 1.0))
    f2 = g * (1.0 - sqrt(f1 / g) - ((f1 / g) * sin(10.0 * 3.14 * f1)))
    return [f1, f2]


def ZDT4(input_arr):
    f1 = input_arr[0]
    s = 0.0
    for i in range(1, len(input_arr)):
        s = s + ((input_arr[i] ** 2) - (10.0 * cos(4 * 3.14 * input_arr[i])))
    g = 1.0 + (10.0 * (len(input_arr) - 1.0)) + s
    f2 = g * (1.0 - ((f1 / g) ** 2))
    return [f1, f2]


def ZDT6(input_arr):
    f1 = 1.0 - (exp(-4.0 * input_arr[0]) * ((sin(6.0 * 3.14 * input_arr[0])) ** 6))
    s = 0.0
    for i in range(1, len(input_arr)):
        s = s + input_arr[i]
    g = 1.0 + 9.0 * ((s / (len(input_arr) - 1.0)) ** 0.25)
    f2 = 1.0 - ((f1 / g) ** 2)
    return [f1, f2]


def DTLZ1(input_arr, n_obj):
    n_var = len(input_arr)
    k = n_var - n_obj + 1
    out = [0.0] * n_obj
    g = 0.0
    for i in range(n_var - k, n_var):
        g = g + ((input_arr[i] - 0.5) ** 2) - cos(20 * pi * (input_arr[i] - 0.5))
    g = 100 * (k + g)
    for i in range(1, n_obj + 1):
        s = 0.5 * (1 + g)
        j = n_obj - i
        while j >= 1:
            j = j - 1
            s = s * input_arr[j]
        if i > 1:
            s = s * (1 - input_arr[n_obj - i])
        out[i - 1] = s
    return out


def DTLZ2(input_arr, n_obj):
    n_var = len(input_arr)
    k = n_var - n_obj + 1
    out = [0.0] * n_obj
    g = 0.0
    for i in range(n_var - k, n_var):
        g = g + ((input_arr[i] - 0.5) ** 2)
    for i in range(1, n_obj + 1):
        s = 1.0 + g
        j = n_obj - i
        while j >= 1:
            j = j - 1
            s = s * cos(pi * input_arr[j] * 0.5)
        if i > 1:
            s = s * sin(input_arr[n_obj - i] * pi / 2)
        out[i - 1] = s
    return out


def DTLZ3(input_arr, n_obj):
    n_var = len(input_arr)
    k = n_var - n_obj + 1
    g = 0.0
    for i in range(n_obj - 1, n_var):
        g += ((input_arr[i] - 0.5) ** 2) - cos(20.0 * pi * (input_arr[i] - 0.5))
    g = (k + g) * 100
    out = [0.0] * n_obj
    for m in range(0, n_obj):
        product = 1 + g
        i = 0
        while (i + m) <= n_obj - 2:
            product *= cos(input_arr[i] * pi / 2)
            i += 1
        if m > 0:
            product *= sin(input_arr[i] * pi / 2)
        out[m] = product
    return out


def DTLZ4(input_arr, n_obj, a=100):
    n_var = len(input_arr)
    k = n_var - n_obj + 1
    g = 0.0
    for i in range(n_obj - 1, n_var):
        g += (input_arr[i] - 0.5) ** 2
    out = [0.0] * n_obj
    for m in range(0, n_obj):
        product = 1 + g
        i = 0
        while (i + m) <= n_obj - 2:
            product *= cos((input_arr[i] ** a) * pi / 2)
            i += 1
        if m > 0:
            product *= sin((input_arr[i] ** a) * pi / 2)
        out[m] = product
    return out


def SCH1(input):
    func1 = input ** 2
    func2 = (input - 2.0) ** 2
    out = [func1, func2]
    return out


def SCH2(input):
    func1 = float()
    if input <= 1:
        func1 = input
    elif input > 1 and input <= 3:
        func1 = input - 2
    elif input > 3 and input <= 4:
        func1 = 4 - input
    else:
        func1 = input - 4
    func2 = (input - 5) ** 2
    out = [func1, func2]
    return out


def IMB1(input_arr):
    n_var = len(input_arr)
    h = 0
    for i in range(1, n_var):
        t = abs(input_arr[i] - sin(0.5 * pi * input_arr[0]))
        h += 0.5 * ((-0.9 * t * t) + (t ** 0.6))
    g = 0
    if input_arr[0] > 0.2:
        g = h
    f1 = (1.0 + g) * input_arr[0]
    f2 = (1.0 + g) * (1 - sqrt(input_arr[0]))
    return [f1, f2]


def IMB2(input_arr):
    n_var = len(input_arr)
    h = 0
    for i in range(1, n_var):
        t = abs(input_arr[i] - sin(0.5 * pi * input_arr[0]))
        h += 0.5 * ((-0.9 * t * t) + (t ** 0.6))
    g = 0
    if (input_arr[0] > 0.6) or (input_arr[0] < 0.4):
        g = h
    f1 = (1.0 + g) * input_arr[0]
    f2 = (1.0 + g) * (1 - input_arr[0])
    return [f1, f2]


def IMB3(input_arr):
    n_var = len(input_arr)
    h = 0
    for i in range(1, n_var):
        t = abs(input_arr[i] - sin(0.5 * pi * input_arr[0]))
        h += 0.5 * ((-0.9 * t * t) + (t ** 0.6))
    g = 0
    if (input_arr[0] > 1.0) or (input_arr[0] < 0.8):
        g = h
    f1 = (1.0 + g) * cos(pi * input_arr[0] * 0.5)
    f2 = (1.0 + g) * sin(pi * input_arr[0] * 0.5)
    return [f1, f2]


def IMB4(input_arr):
    n_var = len(input_arr)
    h = 0
    for i in range(2, n_var):
        t = abs(input_arr[i] - (0.5 * (input_arr[0] + input_arr[1])))
        h += 2.0 * cos(pi * 0.5 * input_arr[0]) * ((-0.9 * t * t) + (t ** 0.6))
    g = 0
    if (input_arr[0] > 1.0) or (input_arr[0] < 2.0 / 3.0):
        g = h
    f1 = (1.0 + g) * input_arr[0] * input_arr[1]
    f2 = (1.0 + g) * input_arr[0] * (1.0 - input_arr[1])
    f3 = (1.0 + g) * (1.0 - input_arr[0])
    return [f1, f2, f3]


def IMB5(input_arr):
    n_var = len(input_arr)
    h = 0
    for i in range(2, n_var):
        t = abs(input_arr[i] - (0.5 * (input_arr[0] + input_arr[1])))
        h += 2.0 * cos(pi * 0.5 * input_arr[0]) * ((-0.9 * t * t) + (t ** 0.6))
    g = 0
    if (input_arr[0] > 0.5) or (input_arr[0] < 0.0):
        g = h
    f1 = (1.0 + g) * cos(pi * 0.5 * input_arr[0]) * cos(pi * 0.5 * input_arr[1])
    f2 = (1.0 + g) * cos(pi * 0.5 * input_arr[0]) * sin(pi * 0.5 * input_arr[1])
    f3 = (1.0 + g) * sin(pi * 0.5 * input_arr[0])
    return [f1, f2, f3]


def IMB6(input_arr):
    n_var = len(input_arr)
    h = 0
    for i in range(2, n_var):
        t = abs(input_arr[i] - (0.5 * (input_arr[0] + input_arr[1])))
        h += 2.0 * cos(pi * 0.5 * input_arr[0]) * ((-0.9 * t * t) + (t ** 0.6))
    g = 0
    if (input_arr[0] > 0.75) or (input_arr[0] < 0.0):
        g = h
    f1 = (1.0 + g) * input_arr[0] * input_arr[1]
    f2 = (1.0 + g) * input_arr[0] * (1.0 - input_arr[1])
    f3 = (1.0 + g) * (1.0 - input_arr[0])
    return [f1, f2, f3]


def IMB7(input_arr):
    n_var = len(input_arr)
    h1 = 0
    h2 = 0
    for i in range(1, n_var):
        s = abs(input_arr[i] - sin(0.5 * pi * input_arr[0]))
        t = abs(input_arr[i] - 0.5)
        h1 += 1.0 * ((-0.9 * s * s) + (s ** 0.6))
        h2 += t ** 0.6
    g = h1
    if (input_arr[0] > 0.8) or (input_arr[0] < 0.5):
        g = h2
    f1 = (1.0 + g) * input_arr[0]
    f2 = (1.0 + g) * (1 - sqrt(input_arr[0]))
    return [f1, f2]


def IMB8(input_arr):
    n_var = len(input_arr)
    h1 = 0
    h2 = 0
    for i in range(1, n_var):
        s = abs(input_arr[i] - sin(0.5 * pi * input_arr[0]))
        t = abs(input_arr[i] - 0.5)
        h1 += 1.0 * ((-0.9 * s * s) + (s ** 0.6))
        h2 += t ** 0.6
    g = h1
    if (input_arr[0] > 0.8) or (input_arr[0] < 0.5):
        g = h2
    f1 = (1.0 + g) * input_arr[0]
    f2 = (1.0 + g) * (1 - input_arr[0])
    return [f1, f2]


def IMB9(input_arr):
    n_var = len(input_arr)
    h1 = 0
    h2 = 0
    for i in range(1, n_var):
        s = abs(input_arr[i] - sin(0.5 * pi * input_arr[0]))
        t = abs(input_arr[i] - 0.5)
        h1 += 1.0 * ((-0.9 * s * s) + (s ** 0.6))
        h2 += t ** 0.6
    g = h1
    if (input_arr[0] > 0.8) or (input_arr[0] < 0.5):
        g = h2
    f1 = (1.0 + g) * cos(pi * 0.5 * input_arr[0])
    f2 = (1.0 + g) * sin(pi * 0.5 * input_arr[0])
    return [f1, f2]


def IMB10(input_arr):
    n_var = len(input_arr)
    h1 = 0
    h2 = 0
    for i in range(2, n_var):
        s = abs(input_arr[i] - (0.5 * (input_arr[0] + input_arr[1])))
        t = abs(input_arr[i] - (input_arr[0] * input_arr[1]))
        h1 += 2.0 * ((-0.9 * s * s) + (s ** 0.6))
        h2 += t ** 0.6
    g = h1
    if ((input_arr[0] > 0.8) or (input_arr[0] < 0.2)) or (
        (input_arr[1] > 0.8) or (input_arr[1] < 0.2)
    ):
        g = h2
    f1 = (1.0 + g) * input_arr[0] * input_arr[1]
    f2 = (1.0 + g) * input_arr[0] * (1.0 - input_arr[1])
    f3 = (1.0 + g) * (1.0 - input_arr[0])
    return [f1, f2, f3]


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

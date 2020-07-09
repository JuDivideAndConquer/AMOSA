import numpy as np
import copy
from math import *
import random
import time
import operator
import csv
from numpy import linalg as LA
from optproblems import wfg


def IMB1(input_arr):
	n_var = len(input_arr)
	h = 0
	for i in range(1,n_var):
		t = abs(input_arr[i] - sin(0.5*pi*input_arr[0]))
		h += (0.5*((-0.9*t*t)+(t**0.6)))
	g = 0
	if input_arr[0] > 0.2 :
		g = h
	f1 = (1.0 + g)*input_arr[0]
	f2 = (1.0 + g)*(1-sqrt(input_arr[0]))
	return np.asarray([f1,f2])

def IMB2(input_arr):
	n_var = len(input_arr)
	h = 0
	for i in range(1,n_var):
		t = abs(input_arr[i] - sin(0.5*pi*input_arr[0]))
		h += (0.5*((-0.9*t*t)+(t**0.6)))
	g = 0
	if (input_arr[0] > 0.6) or (input_arr[0] < 0.4) :
		g = h
	f1 = (1.0 + g)*input_arr[0]
	f2 = (1.0 + g)*(1-input_arr[0])
	return np.asarray([f1,f2])

def IMB3(input_arr):
	n_var = len(input_arr)
	h = 0
	for i in range(1,n_var):
		t = abs(input_arr[i] - sin(0.5*pi*input_arr[0]))
		h += (0.5*((-0.9*t*t)+(t**0.6)))
	g = 0
	if (input_arr[0] > 1.0) or (input_arr[0] < 0.8) :
		g = h
	f1 = (1.0 + g)*cos(pi*input_arr[0]*0.5)
	f2 = (1.0 + g)*sin(pi*input_arr[0]*0.5)
	return np.asarray([f1,f2])

def IMB4(input_arr):
	n_var = len(input_arr)
	h = 0
	for i in range(2,n_var):
		t = abs(input_arr[i] - (0.5*(input_arr[0]+input_arr[1])))
		h += (2.0*cos(pi*0.5*input_arr[0])*((-0.9*t*t)+(t**0.6)))
	g = 0
	if (input_arr[0] > 1.0) or (input_arr[0] < 2.0/3.0) :
		g = h
	f1 = (1.0 + g)*input_arr[0]*input_arr[1]
	f2 = (1.0 + g)*input_arr[0]*(1.0-input_arr[1])
	f3 = (1.0 + g)*(1.0-input_arr[0])
	return np.asarray([f1,f2,f3])

def IMB5(input_arr):
	n_var = len(input_arr)
	h = 0
	for i in range(2,n_var):
		t = abs(input_arr[i] - (0.5*(input_arr[0]+input_arr[1])))
		h += (2.0*cos(pi*0.5*input_arr[0])*((-0.9*t*t)+(t**0.6)))
	g = 0
	if (input_arr[0] > 0.5) or (input_arr[0] < 0.0) :
		g = h
	f1 = (1.0 + g)*cos(pi*0.5*input_arr[0])*cos(pi*0.5*input_arr[1])
	f2 = (1.0 + g)*cos(pi*0.5*input_arr[0])*sin(pi*0.5*input_arr[1])
	f3 = (1.0 + g)*sin(pi*0.5*input_arr[0])
	return np.asarray([f1,f2,f3])

def IMB6(input_arr):
	n_var = len(input_arr)
	h = 0
	for i in range(2,n_var):
		t = abs(input_arr[i] - (0.5*(input_arr[0]+input_arr[1])))
		h += (2.0*cos(pi*0.5*input_arr[0])*((-0.9*t*t)+(t**0.6)))
	g = 0
	if (input_arr[0] > 0.75) or (input_arr[0] < 0.0) :
		g = h
	f1 = (1.0 + g)*input_arr[0]*input_arr[1]
	f2 = (1.0 + g)*input_arr[0]*(1.0-input_arr[1])
	f3 = (1.0 + g)*(1.0-input_arr[0])
	return np.asarray([f1,f2,f3])

def IMB7(input_arr):
	n_var = len(input_arr)
	h1 = 0
	h2 = 0
	for i in range(1,n_var):
		s = abs(input_arr[i] - sin(0.5*pi*input_arr[0]))
		t = abs(input_arr[i] - 0.5)
		h1 += (1.0*((-0.9*s*s)+(s**0.6)))
		h2 += (t**0.6)
	g = h1
	if (input_arr[0] > 0.8) or (input_arr[0] < 0.5):
		g = h2
	f1 = (1.0 + g)*input_arr[0]
	f2 = (1.0 + g)*(1-sqrt(input_arr[0]))
	return np.asarray([f1,f2])

def IMB8(input_arr):
	n_var = len(input_arr)
	h1 = 0
	h2 = 0
	for i in range(1,n_var):
		s = abs(input_arr[i] - sin(0.5*pi*input_arr[0]))
		t = abs(input_arr[i] - 0.5)
		h1 += (1.0*((-0.9*s*s)+(s**0.6)))
		h2 += (t**0.6)
	g = h1
	if (input_arr[0] > 0.8) or (input_arr[0] < 0.5):
		g = h2
	f1 = (1.0 + g)*input_arr[0]
	f2 = (1.0 + g)*(1-input_arr[0])
	return np.asarray([f1,f2])

def IMB9(input_arr):
	n_var = len(input_arr)
	h1 = 0
	h2 = 0
	for i in range(1,n_var):
		s = abs(input_arr[i] - sin(0.5*pi*input_arr[0]))
		t = abs(input_arr[i] - 0.5)
		h1 += (1.0*((-0.9*s*s)+(s**0.6)))
		h2 += (t**0.6)
	g = h1
	if (input_arr[0] > 0.8) or (input_arr[0] < 0.5):
		g = h2
	f1 = (1.0 + g)*cos(pi*0.5*input_arr[0])
	f2 = (1.0 + g)*sin(pi*0.5*input_arr[0])
	return np.asarray([f1,f2])


def IMB10(input_arr):
	n_var = len(input_arr)
	h1 = 0
	h2 = 0
	for i in range(2, n_var):
		s = abs(input_arr[i] - (0.5 * (input_arr[0] + input_arr[1])))
		t = abs(input_arr[i] - (input_arr[0] * input_arr[1]))
		h1 += (2.0 * ((-0.9 * s * s) + (s ** 0.6)))
		h2 += (t ** 0.6)
	g = h1
	if ((input_arr[0] > 0.8) or (input_arr[0] < 0.2)) or ((input_arr[1] > 0.8) or (input_arr[1] < 0.2)):
		g = h2
	f1 = (1.0 + g) * input_arr[0] * input_arr[1]
	f2 = (1.0 + g) * input_arr[0] * (1.0 - input_arr[1])
	f3 = (1.0 + g) * (1.0 - input_arr[0])
	return np.asarray([f1, f2, f3])


def evaluate(func,decision,n_obj):
	if func == "IMB1":
		return IMB1(decision)
	elif func == "IMB2":
		return IMB2(decision)
	elif func == "IMB3":
		return IMB3(decision)
	elif func == "IMB4":
		return IMB4(decision)
	elif func == "IMB5":
		return IMB5(decision)
	elif func == "IMB6":
		return IMB6(decision)
	elif func == "IMB7":
		return IMB7(decision)
	elif func == "IMB8":
		return IMB8(decision)
	elif func == "IMB9":
		return IMB9(decision)
	elif func == "IMB10":
		return IMB10(decision)

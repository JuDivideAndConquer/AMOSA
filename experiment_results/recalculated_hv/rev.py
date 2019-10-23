#!/usr/bin/env python3


import sys

file = sys.argv[1]

list = []

with open(file,"r") as fp:
    list = fp.readlines()

for i in list:
    i = float(i)
    i = 1/i
    print(i,end=" ")
print()
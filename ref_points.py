# Reference point generation for decomposition based approach
# Please use this look-up table for standard values of partitions
# n_obj, p1, p2, n_pts
# 3, 12, 0, 91
# 5, 6, 0, 210
# 8, 3, 2, 156
# 10, 3, 2, 275
# 15, 2, 1, 135

import copy
import numpy as np


class form_ref_pts(object):
    def __init__(self, m, divisions):
        self.M = m - 1
        self.div = divisions
        self.points = []

    def recursive(self, arr, d, l):
        arr_c = copy.deepcopy(arr)
        if d == self.M - 1:
            self.points.append(arr_c)
        else:
            for i in range(0, l):
                node_val = float(i) / float(self.div)
                arr_next = copy.deepcopy(arr_c)
                arr_next.append(node_val)
                self.recursive(arr_next, d + 1, l - i)

    def form(self):
        layer = []
        for i in range(0, self.div + 1):
            layer.append(float(i) / float(self.div))
        for i in range(0, len(layer)):
            l1 = []
            l1.append(layer[i])
            self.recursive(l1, 0, len(layer) - i)
        for i in range(0, len(self.points)):
            s = sum(self.points[i])
            self.points[i].append(1.0 - s)
        self.points = np.asarray(self.points)


def form_refs(dim, outer, inner):
    points = []

    factory = form_ref_pts(dim, outer)
    factory.form()
    factory2 = form_ref_pts(dim, inner)
    factory2.form()
    factory2.points = (factory2.points / 2) + (1.0 / (2.0 * dim))

    for i in range(0, len(factory.points)):
        points.append(factory.points[i])
    for i in range(0, len(factory2.points)):
        points.append(factory2.points[i])

    return np.asarray(points)


n_obj = 15  ### enter number of objectives
if n_obj == 3:
    p1 = 12
    a1 = form_ref_pts(n_obj, p1)
    a1.form()
    b2 = a1.points
elif n_obj == 5:
    p1 = 6
    a1 = form_ref_pts(n_obj, p1)
    a1.form()
    b2 = a1.points
elif n_obj == 8:
    p1 = 3
    p2 = 2
    b2 = form_refs(n_obj, p1, p2)
elif n_obj == 10:
    p1 = 3
    p2 = 2
    b2 = form_refs(n_obj, p1, p2)
elif n_obj == 15:
    p1 = 2
    p2 = 1
    b2 = form_refs(n_obj, p1, p2)


fname = 'Res' + str(n_obj) + '.txt'
f = open(fname, 'w')
for i in range(len(b2)):
    for j in range(len(b2[0])):
        f.write(repr(b2[i][j]))
        f.write('\t')
    f.write('\n')
f.close()

print(len(b2))
print(b2)

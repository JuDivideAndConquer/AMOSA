from ref_points_generator import getRefPoints
from amosa import AMOSAType
import copy
import math

# 1. Normalize
# 2. Associate
# 3. Compute cost for each vector
# 4. Keep the lowest cost points


def normalize(dd_archive,amosaParams):
    '''Normalization of archive vectors'''

    d_normalize_shift = [0]*amosaParams.i_no_offunc
    d_normalize_scale = [0]*amosaParams.i_no_offunc

    for i in range(amosaParams.i_no_offunc):
        min = -math.inf
        max = math.inf
        for j in range(len(dd_archive)):
            if(min>dd_archive[j][i]):
                min = dd_archive[j][i]
            if(max<dd_archive[j][i]):
                max = dd_archive[j][i]
        d_normalize_scale[i] = max - min
        d_normalize_shift[i] = min
        
    for i in range(amosaParams.i_no_offunc):
        #Normalize shift
        for j in range(len(dd_archive)):
            dd_archive[j][i] = dd_archive[j][i] - d_normalize_shift[i]
        #Normalize scale
        for j in range(len(dd_archive)):
            dd_archive[j][i] = dd_archive[j][i]/d_normalize_scale[i]
    
    return d_normalize_shift, d_normalize_scale


def deNormalize(dd_archive, d_normalize_shift, d_normalize_scale, amosaParams):
    for i in range(amosaParams.i_no_offunc):
        #de-normalize scale
        for j in range(len(dd_archive)):
            dd_archive[j][i] = dd_archive[j][i] * d_normalize_scale[i]
        #de-normalize shift
        for j in range(len(dd_archive)):
            dd_archive[j][i] = dd_archive[j][i] + d_normalize_shift[i]


def getRefPoints(amosaParams):

    dd_archive = copy.deepcopy(amosaParams.dd_archive)

    # Normalization
    d_normalize_shift, d_normalize_scale = normalize(dd_archive,amosaParams)


    # De-normalization
    deNormalize(dd_archive, d_normalize_shift, d_normalize_scale, amosaParams)

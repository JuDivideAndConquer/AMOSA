import copy


class form_ref_points(object):
    '''class to hold the reference points'''

    def __init__(self, n_obj, n_div):
        '''arguments: no of objectives, no of divisions'''
        self.m = n_obj
        self.n = n_div
        self.allPoints = []
        self.points = []
        self.form()

    def recursivePointsGenerate(self, layer, point):
        '''Generates the points recursively. Every permutation of values in layer is generated'''
        if(len(point) == self.m):
            # If point is an m dimensional vector
            self.allPoints.append(point)
        else:
            # If point is a <m dimensional vector
            for i in range(len(layer)):
                point_next = copy.deepcopy(point)
                point_next.append(layer[i])
                self.recursivePointsGenerate(layer, copy.deepcopy(point_next))

    def form(self):
        layer = []
        for i in range(0, self.n + 1):
            layer.append(float(i)/float(self.n))
        # layer holds the n+1 division in the range [0,1]

        self.recursivePointsGenerate(layer, [])

        for i in range(0, len(self.allPoints)):
            s = sum(self.allPoints[i])
            if(s == 1):
                self.points.append(self.allPoints[i])

# for higher objectives, partitioning using inner and outer divisions


def form_refs(n_obj, outerDivisions, innerDivisions):
    points = []

    outerPoints = form_ref_points(n_obj, outerDivisions).points
    innerPoints = form_ref_points(n_obj, innerDivisions).points

    for i in range(len(innerPoints)):
        for j in range(n_obj):
            innerPoints[i][j] = (innerPoints[i][j]/2) + (1.0/(2.0*n_obj))

    for i in range(len(outerPoints)):
        points.append(outerPoints[i])
    for i in range(len(innerPoints)):
        points.append(innerPoints[i])

    return points


# Entry point ----------------------------------
def getRefPoints(n_obj):
    '''returns generated reference points'''
    if(n_obj == 3):
        divisions = 12
        refPoints = form_ref_points(n_obj, divisions)
        return refPoints.points
    elif(n_obj == 5):
        divisions = 6
        refPoints = form_ref_points(n_obj, divisions)
        return refPoints.points
    elif(n_obj == 8):
        outerDivisions = 3
        innerDivisions = 2
        ref_points = form_refs(8, outerDivisions, innerDivisions)
        return ref_points
    elif(n_obj == 10):
        outerDivisions = 3
        innerDivisions = 2
        ref_points = form_refs(8, outerDivisions, innerDivisions)
        return ref_points
    elif(n_obj == 15):
        outerDivisions = 2
        innerDivisions = 1
        ref_points = form_refs(8, outerDivisions, innerDivisions)
        return ref_points

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
        print(self.points)
        print(len(self.points))

    def recursivePointsGenerate(self,layer,point):
        '''Generates the points recursively. Every permutation of values in layer is generated'''
        if(len(point)==self.m):
            # If point is an m dimensional vector
            self.allPoints.append(point)
        else:
            # If point is a <m dimensional vector
            for i in range(len(layer)):
                point_next = copy.deepcopy(point)
                point_next.append(layer[i])
                self.recursivePointsGenerate(layer,copy.deepcopy(point_next))

    def form(self):
        layer = []
        for i in range(0, self.n + 1):
            layer.append(float(i)/float(self.n))
        # layer holds the n+1 division in the range [0,1]

        self.recursivePointsGenerate(layer,[])

        for i in range(0,len(self.allPoints)):
            s = sum(self.allPoints[i])
            if(s==1):
                self.points.append(self.allPoints[i])


# Entry point ----------------------------------
def getRefPoints(n_obj,divisions):
    '''returns generated reference points'''
    refPoints = form_ref_points(n_obj,divisions)
    return refPoints.points

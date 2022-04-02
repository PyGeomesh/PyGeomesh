from .geometry import Geometry
from .sampler import Sampler
import numpy as np


class Polygon(Geometry):
    def __init__(self, time_dependent, *pointlist):
        super().__init__(time_dependent)
        self.pointlist = pointlist
        self.ndim = len(pointlist[0])
        self.n = len(pointlist)
        self.l_bounds = np.zeros(self.ndim)
        self.u_bounds = np.zeros(self.ndim)
        for i in range(self.ndim):
            self.l_bounds[i] = min([point[i] for point in pointlist])
            self.u_bounds[i] = max([point[i] for point in pointlist])

    def is_internal(self, x):
        for i in range(self.n):
            if i == self.n - 1:
                if np.cross(x - self.pointlist[i],
                            x - self.pointlist[0])[2] < 0:
                    return False
            else:
                if np.cross(x - self.pointlist[i],
                            x - self.pointlist[i + 1])[2] < 0:
                    return False
        return True

    def is_boundary(self, x):
        for i in range(self.n):
            if i == self.n - 1:
                if np.cross(x - self.pointlist[i],
                            x - self.pointlist[0])[2] == 0:
                    return True
            else:
                if np.cross(x - self.pointlist[i],
                            x - self.pointlist[i + 1])[2] == 0:
                    return True
        return False

    def grid_points(self, n):
        vlist = []
        for i in range(self.ndim):
            vlist.append(
                Sampler(1, n, self.l_bounds[i], self.u_bounds[i], type='grid'))

        points = np.vstack(np.meshgrid(*vlist)).reshape(self.ndim, -1).T
        points = points[self.is_internal(points)]
        self.points = points
        return points


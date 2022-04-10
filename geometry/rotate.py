from .geometry import Geometry
from .sampler import Sampler
import numpy as np


class Rotate(Geometry):
    def __init__(self, geometry, angle):
        self.angle = angle
        self.geometry = geometry
        self.pointlist = geometry.pointlist
        self.min_h = min([point[1] for point in self.pointlist])
        self.max_h = max([point[1] for point in self.pointlist])
        self.max_r = max([np.abs(point[0]) for point in self.pointlist])

    def __str__(self):
        return "Rotate(%s, %f)" % (self.geometry, self.angle)

    def check_alpha(self, x):
        alpha = np.arctan2(x[:, 1], x[:, 0])
        alpha[alpha < 0] += 2 * np.pi
        alpha = alpha - self.angle
        return alpha < 0

    def is_internal(self, x):
        r = np.sqrt(np.square(x[:, 0]) + np.square(x[:, 1]))
        return self.geometry.is_internal(np.array([r, x[:, 2]]).T)

    def is_boundary(self, x):
        return super().is_boundary(x)

    def grid_points(self, n):
        vlist = []
        for i in range(2):
            vlist.append(Sampler(1, n, -self.max_r, self.max_r, type='grid'))
        vlist.append(Sampler(1, n, self.min_h, self.max_h, type='grid'))
        points = np.vstack(np.meshgrid(*vlist)).reshape(3, -1).T
        points = points[self.is_internal(points)]
        points = points[self.check_alpha(points)]
        self.points = points
        return points

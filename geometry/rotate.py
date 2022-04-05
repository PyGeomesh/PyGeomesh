from cmath import sin
import math

from sympy import re
from .geometry import Geometry
from .sampler import Sampler
import numpy as np
import scipy.optimize as opt


class Rotate(Geometry):
    def __init__(self, geometry, angle):
        self.angle = angle
        self.geometry = geometry
        self.pointlist = geometry.pointlist

    def __str__(self):
        return "Rotate(%s, %f)" % (self.geometry, self.angle)

    def _transform(self, x, alpha):
        rotateMatrix = np.array([[np.cos(alpha),
                                  np.sin(alpha), 0],
                                 [-np.sin(alpha),
                                  np.cos(alpha), 0], [0, 0, 1]])
        return np.dot(x, rotateMatrix)

    def _solve_alpha(self, x):
        alpha = np.arctan2(x[:, 1], x[:, 0])
        alpha[alpha < 0] = alpha[alpha < 0] + 2 * np.pi
        return alpha

    def is_internal(self, x):
        alpha = self._solve_alpha(x)
        x_rotated = self._transform(x, -alpha)[:, [0, 2]]
        return self.geometry.is_internal(x_rotated)

    def is_boundary(self, x):
        return super().is_boundary(x)

    def grid_points(self, n):
        vlist = []
        for i in range(3):
            vlist.append(Sampler(1, n, -1, 1, type='grid'))

        points = np.vstack(np.meshgrid(*vlist)).reshape(3, -1).T
        points = points[self.is_internal(points)]
        self.points = points
        return points

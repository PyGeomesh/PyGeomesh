from .sampler import Sampler
from .geometry import Geometry
import numpy as np


class Point(Geometry):
    def __init__(self, time_dependent, center, r, *grometry):
        super().__init__(time_dependent)
        self.center = center
        self.r = r
        self.ndim = len(center)
        self.grometry = grometry

    def is_internal(self, x):
        return np.linalg.norm(x - self.center, axis=1) <= self.r

    def is_boundary(self, x):
        return np.linalg.norm(x - self.center, axis=1) == self.r

    def grid_points(self, n):
        vlist = []
        for i in range(self.ndim):
            vlist.append(
                Sampler(
                    1,
                    n,
                    self.center[i] - self.r,
                    self.center[i] + self.r,
                    type='grid'))

        points = np.vstack(np.meshgrid(*vlist)).reshape(self.ndim, -1).T
        points = points[self.is_internal(points)]
        self.points = points
        return points

    def grid_points_on_boundary(self, n):
        if self.ndim == 2:
            theta = Sampler(1, n, 0, 2 * np.pi, type='grid')
            points = np.vstack((self.center[0] + self.r * np.cos(theta),
                                self.center[1] + self.r * np.sin(theta))).T
            self.boundary_points['0'] = points
            return points
        elif self.ndim == 3:
            i = Sampler(1, n, 0, n, type='grid')
            phi = np.arccos((2 * i - 1) / n - 1)
            theta = np.sqrt(n * np.pi) * phi
            points = np.vstack(
                (self.center[0] + self.r * np.cos(theta) * np.sin(phi),
                 self.center[1] + self.r * np.sin(theta) * np.sin(phi),
                 self.center[2] + self.r * np.cos(phi))).T
            self.boundary_points[0] = points
            return points

    def random_points(self, n, seed=None, type='uniform'):
        # http://extremelearning.com.au/how-to-generate-uniformly-random-points-on-n-spheres-and-n-balls/
        u = Sampler(self.ndim, n, 0, 1, type='normal')
        norm = np.sum(u**2, axis=0)**(0.5)
        r = self.r * np.random.random(n)**(1.0 / self.ndim)
        points = r * u / norm
        points = points.T + self.center
        self.points = points
        return points

    def random_points_on_boundary(self, n, seed=None, type='random'):
        if self.ndim == 2:
            theta = Sampler(1, n, 0, 2 * np.pi, type='random')
            points = np.vstack((self.r * np.cos(theta),
                                self.r * np.sin(theta))).T
            self.boundary_points[0] = points
            return points
        elif self.ndim == 3:
            u = Sampler(1, n, 0, 1, type='normal')
            v = Sampler(1, n, 0, 1, type='normal')
            w = Sampler(1, n, 0, 1, type='normal')

            norm = np.sqrt(u**2 + v**2 + w**2)
            x = u / norm
            y = v / norm
            z = w / norm

            points = np.vstack((x, y, z)).T
            points = points * self.r + self.center
            self.boundary_points[0] = points
            return points

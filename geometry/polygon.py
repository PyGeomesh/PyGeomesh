from .geometry import Geometry
from .sampler import Sampler
import numpy as np
from shapely.geometry import Polygon as ShapelyPolygon
from shapely.geometry import Point as ShapelyPoint


class Polygon(Geometry):
    def __init__(self, time_dependent, *pointlist):
        super().__init__(time_dependent)
        self.shape = ShapelyPolygon(pointlist)
        self.pointlist = pointlist
        self.ndim = len(pointlist[0])
        self.n = len(pointlist)
        self.l_bounds = np.zeros(self.ndim)
        self.u_bounds = np.zeros(self.ndim)
        for i in range(self.ndim):
            self.l_bounds[i] = min([point[i] for point in pointlist])
            self.u_bounds[i] = max([point[i] for point in pointlist])

    def _is_internal(self, x):
        return self.shape.intersects(ShapelyPoint(x))

    def is_internal(self, x):
        return [self._is_internal(point) for point in x]

    def _is_boundary(self, x):
        return self.shape.distance(ShapelyPoint(x)) == 0

    def is_boundary(self, x):
        return [self._is_boundary(point) for point in x]

    def grid_points(self, n):
        vlist = []
        for i in range(self.ndim):
            vlist.append(
                Sampler(1, n, self.l_bounds[i], self.u_bounds[i], type='grid'))

        points = np.vstack(np.meshgrid(*vlist)).reshape(self.ndim, -1).T
        points = points[self.is_internal(points)]
        self.points = points
        return points

    def grid_points_on_boundary(self, n):
        vlist = []
        for i in range(self.n):
            x = Sampler(
                1,
                n,
                self.pointlist[i][0],
                self.pointlist[(i + 1) % self.n][0],
                type='grid')
            y = Sampler(
                1,
                n,
                self.pointlist[i][1],
                self.pointlist[(i + 1) % self.n][1],
                type='grid')

            vlist.append(np.vstack((x, y)).T)
            # every segment will save like this: {'0': [[x1, y1],...], '1': [[x2, y2],...], ...}
            self.boundary_points[i] = np.vstack((x, y)).T
        
        self.boundary_points['num'] = self.n
        # for development
        points = np.vstack(vlist)
        return points

    def random_points(self, n):
        x = Sampler(1, n, self.l_bounds[0], self.u_bounds[0], type='random')
        y = Sampler(1, n, self.l_bounds[1], self.u_bounds[1], type='random')
        points = np.vstack((x, y)).T
        points = points[self.is_internal(points)]
        self.points = points
        return points

    def random_points_on_boundary(self, n, seed=None, type='random'):
        vlist = []
        for i in range(self.n):

            dx = self.pointlist[(i + 1) % self.n][0] - self.pointlist[i][0]
            dy = self.pointlist[(i + 1) % self.n][1] - self.pointlist[i][1]

            if dx == 0:
                y = Sampler(
                    1,
                    n,
                    self.pointlist[i][1],
                    self.pointlist[(i + 1) % self.n][1],
                    type=type)
                x = np.full(n, self.pointlist[i][0])
            elif dy == 0:
                x = Sampler(
                    1,
                    n,
                    self.pointlist[i][0],
                    self.pointlist[(i + 1) % self.n][0],
                    type=type)
                y = np.full(n, self.pointlist[i][1])
            else:
                x = Sampler(
                    1,
                    n,
                    self.pointlist[i][0],
                    self.pointlist[(i + 1) % self.n][0],
                    type=type)
                y = (dy / dx) * (
                    x - self.pointlist[i][0]) + self.pointlist[i][1]
            vlist.append(np.vstack((x, y)).T)
            # every segment will save like this: {'0': [[x1, y1],...], '1': [[x2, y2],...], ...}
            self.boundary_points[i] = np.vstack((x, y)).T

        self.boundary_points['num'] = self.n
        points = np.vstack(vlist)
        return points

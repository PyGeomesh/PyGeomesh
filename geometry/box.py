from matplotlib.pyplot import axis
from .geometry import Geometry
import numpy as np


class Box(Geometry):
    def __init__(self,
                 center,
                 length,
                 width,
                 height,
                 q=[0, 0, 0],
                 time_dependent=False):
        super().__init__(time_dependent)
        self.center = center
        self.q = q
        self.length = length
        self.width = width
        self.height = height
        self.transformationMatrix = self.get_transformationMatrix()

    def __str__(self):
        return "Box: center: {}, q: {}, length: {}, width: {}, height: {}, ".format(
            self.center, self.q, self.length, self.width, self.height)

    def get_transformationMatrix(self):
        """
        Compute the transformation matrix.
        :return: transformation matrix
        """

        # compute the transformation matrix
        # we use the euler angles to rotate the box z-y-x
        gamma = np.array([[np.cos(self.q[0]), -np.sin(self.q[0]), 0],
                          [np.sin(self.q[0]),
                           np.cos(self.q[0]), 0], [0, 0, 1]])
        beta = np.array([[1, 0, 0], [0,
                                     np.cos(self.q[1]), -np.sin(self.q[1])],
                         [0, np.sin(self.q[1]),
                          np.cos(self.q[1])]])
        alpha = np.array([[np.cos(self.q[2]), 0,
                           np.sin(self.q[2])], [0, 1, 0],
                          [-np.sin(self.q[2]), 0,
                           np.cos(self.q[2])]])
        self.transformationMatrix = np.dot(np.dot(gamma, beta), alpha)
        return self.transformationMatrix

    def _is_internal(self, x):
        """
        Check if a point is inside the box.
        :param x: point to check
        :return: True if point is inside the box, False otherwise
        """
        # check if point is inside the box
        if np.all(x >= self.center - self.length / 2) and np.all(
                x <= self.center + self.length / 2):
            return True
        else:
            return False

    def is_internal(self, x):
        return [self._is_internal(i) for i in x]

    def _is_boundary(self, x):
        """
        Check if a point is on the boundary of the box.
        :param x: point to check
        :return: True if point is on the boundary of the box, False otherwise
        """
        # check if point is on the boundary of the box
        if np.all(x == self.center - self.length / 2) or np.all(
                x == self.center + self.length / 2):
            return True
        else:
            return False

    def is_boundary(self, x):
        return [self._is_boundary(i) for i in x]

    def grid_points(self, n):
        """
        Generate a list of points on the box.
        :param n: number of points
        :return: list of points on the box
        """
        # generate a list of points on the box
        x = np.linspace(self.center[0] - self.length / 2,
                        self.center[0] + self.length / 2, n)
        y = np.linspace(self.center[1] - self.width / 2,
                        self.center[1] + self.width / 2, n)
        z = np.linspace(self.center[2], self.center[2] + self.height, n)
        points = np.vstack(np.meshgrid(x, y, z)).reshape(3, -1).T
        points = np.dot(self.transformationMatrix, points.T).T
        self.points = points
        return points

    def grid_points_on_edge(self, n):
        """
        Generate a dict of points on the box edges.
        :param n: number of points
        :return: dict of points on the box edges
        """

        above_point = np.array(
            [[
                self.center[0] - self.length / 2,
                self.center[1] - self.width / 2, self.center[2] + self.height
            ],
             [
                 self.center[0] + self.length / 2,
                 self.center[1] - self.width / 2, self.center[2] + self.height
             ],
             [
                 self.center[0] + self.length / 2,
                 self.center[1] + self.width / 2, self.center[2] + self.height
             ],
             [
                 self.center[0] - self.length / 2,
                 self.center[1] + self.width / 2, self.center[2] + self.height
             ]])
        below_point = np.array(
            [[
                self.center[0] - self.length / 2,
                self.center[1] - self.width / 2, self.center[2]
            ],
             [
                 self.center[0] + self.length / 2,
                 self.center[1] - self.width / 2, self.center[2]
             ],
             [
                 self.center[0] + self.length / 2,
                 self.center[1] + self.width / 2, self.center[2]
             ],
             [
                 self.center[0] - self.length / 2,
                 self.center[1] + self.width / 2, self.center[2]
             ]])
        edge_points = {}
        for i in [0, 2]:
            point = np.arange(
                above_point[i, 0], above_point[(i + 1) % 4, 0], 1 / n *
                (1, -1)[above_point[i, 0] > above_point[(i + 1) % 4, 0]])
            edge_points[i] = np.vstack(
                (point, above_point[i, 1] * np.ones(len(point)),
                 above_point[i, 2] * np.ones(len(point)))).T

            point = np.arange(
                below_point[i, 0], below_point[(i + 1) % 4, 0], 1 / n *
                (1, -1)[below_point[i, 0] > below_point[(i + 1) % 4, 0]])
            edge_points[i + 4] = np.vstack(
                (point, below_point[i, 1] * np.ones(len(point)),
                 below_point[i, 2] * np.ones(len(point)))).T

        for i in [1, 3]:
            point = np.arange(
                above_point[i, 1], above_point[(i + 1) % 4, 1], 1 / n *
                (1, -1)[above_point[i, 1] > above_point[(i + 1) % 4, 1]])
            edge_points[i] = np.vstack(
                (above_point[i, 0] * np.ones(len(point)), point,
                 above_point[i, 2] * np.ones(len(point)))).T

            point = np.arange(
                below_point[i, 1], below_point[(i + 1) % 4, 1], 1 / n *
                (1, -1)[below_point[i, 1] > below_point[(i + 1) % 4, 1]])
            edge_points[i + 4] = np.vstack(
                (below_point[i, 0] * np.ones(len(point)), point,
                 below_point[i, 2] * np.ones(len(point)))).T

        for i in range(4):
            point = np.arange(
                above_point[i, 2], below_point[i, 2],
                1 / n * (1, -1)[above_point[i, 2] > below_point[i, 2]])
            edge_points[i + 8] = np.vstack(
                (above_point[i, 0] * np.ones(len(point)),
                 above_point[i, 1] * np.ones(len(point)), point)).T

        for key in edge_points:
            edge_points[key] = np.dot(self.transformationMatrix,
                                      edge_points[key].T).T

        return edge_points

    def grid_points_on_surface(self, n):
        """
        Generate a list of points on the box surface.
        :param n: number of points
        :return: list of points on the box surface
        """
        surfacepoints = {}
        x = np.arange(
            self.center[0] - self.length / 2, self.center[0] + self.length / 2,
            1 / n * (1, -1)[self.center[0] > self.center[0] + self.length / 2])
        y = np.arange(
            self.center[1] - self.width / 2, self.center[1] + self.width / 2,
            1 / n * (1, -1)[self.center[1] > self.center[1] + self.width / 2])
        z = np.arange(
            self.center[2], self.center[2] + self.height,
            1 / n * (1, -1)[self.center[2] > self.center[2] + self.height])
        point = np.meshgrid(x, self.center[1] - self.width / 2, z)
        surfacepoints[0] = np.vstack((point[0].flatten(), point[1].flatten(),
                                      point[2].flatten())).T
        point = np.meshgrid(x, self.center[1] + self.width / 2, z)
        surfacepoints[1] = np.vstack((point[0].flatten(), point[1].flatten(),
                                      point[2].flatten())).T
        point = np.meshgrid(self.center[0] - self.length / 2, y, z)
        surfacepoints[2] = np.vstack((point[0].flatten(), point[1].flatten(),
                                      point[2].flatten())).T
        point = np.meshgrid(self.center[0] + self.length / 2, y, z)
        surfacepoints[3] = np.vstack((point[0].flatten(), point[1].flatten(),
                                      point[2].flatten())).T
        point = np.meshgrid(x, y, self.center[2])
        surfacepoints[4] = np.vstack((point[0].flatten(), point[1].flatten(),
                                      point[2].flatten())).T
        point = np.meshgrid(x, y, self.center[2] + self.height)
        surfacepoints[5] = np.vstack((point[0].flatten(), point[1].flatten(),
                                      point[2].flatten())).T

        for key in surfacepoints:
            surfacepoints[key] = np.dot(self.transformationMatrix,
                                        surfacepoints[key].T).T

        return surfacepoints

    def grid_points_on_boundary(self, n):
        edge_points = self.grid_points_on_edge(n)
        surfacepoints = self.grid_points_on_surface(n)

        boundary_points = {}
        for i in range(12):
            boundary_points['e' + str(i)] = edge_points[i]
        for i in range(6):
            boundary_points['s' + str(i)] = surfacepoints[i]
        self.boundary_points = boundary_points
        return boundary_points

    def random_points(self, n):
        """
        Generate a list of random points on the box.
        :param n: number of points
        :return: list of random points on the box
        """
        vlist = []
        for i in range(n):
            x = np.random.uniform(self.center[0] - self.length / 2,
                                  self.center[0] + self.length / 2)
            y = np.random.uniform(self.center[1] - self.width / 2,
                                  self.center[1] + self.width / 2)
            z = np.random.uniform(self.center[2], self.center[2] + self.height)
            vlist.append([x, y, z])

        points = np.vstack(vlist, axis=0)
        points = np.dot(self.transformationMatrix, points.T).T
        return points
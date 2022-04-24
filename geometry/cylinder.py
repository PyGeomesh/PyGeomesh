from regex import B
from .geometry import Geometry
import numpy as np
from .box import Box


class Cylinder(Geometry):
    def __init__(self,
                 pos,
                 radius,
                 length,
                 q: list = [0, 0, 0],
                 time_dependent=False):
        super().__init__(time_dependent)
        self.pos = pos
        self.radius = radius
        self.length = length
        self.q = q
        self.transformationMatrix = Box.get_transformationMatrix(self.q)

    def __str__(self):
        return 'Cylinder({}, {}, {})'.format(self.pos, self.radius, self.axis)

    def is_internal(self, x):
        """
        Returns True if the point x is internal to the Geometry.
        ### Args:
        - `x` : A point as like [x, y, z]
        ### Returns:
        - `bool` : True if the point x is internal to the Geometry.
        """
        x = np.array(x)
        x = np.dot(np.linalg.inv(self.transformationMatrix), x.T).T
        x = x - self.pos
        return np.linalg.norm(x[:, :-1], axis=1) < self.radius

    def _is_boundary(self, x):
        """
        Returns True if the point x is on the boundary of the Geometry.
        ### Args:
        - `x` : A point as like [x, y, z]
        ### Returns:
        - `bool` : True if the point x is on the boundary of the Geometry.
        """
        x = np.array(x)
        x = np.dot(np.linalg.inv(self.transformationMatrix), x.T).T
        x = x - self.pos
        return np.linalg.norm(x) == self.radius

    def is_boundary(self, x):
        """
        Returns True if the point x is on the boundary of the Geometry.
        ### Args:
        - `x` : list of points as like [[x, y, z], [x, y, z], ...]
        ### Returns:
        - `bool` : True if the point x is on the boundary of the Geometry.
        """
        if isinstance(x, list):
            return [self._is_boundary(xi) for xi in x]
        else:
            return self._is_boundary(x)

    def grid_points(self, n):
        """
        Returns a list of points on the Geometry.
        ### Args:
        - `n` : Number of points on the Geometry.
        ### Returns:
        - `list` : A list of points on the Geometry.
        """
        x = np.linspace(-self.radius, self.radius, n)
        y = np.linspace(-self.radius, self.radius, n)
        z = np.linspace(0, self.length, n)
        points = np.meshgrid(x, y, z)
        points = np.array(points).reshape(3, -1).T
        point = points[self.is_internal(points)]
        point = point + self.pos
        points = np.dot(self.transformationMatrix, point.T).T
        return points

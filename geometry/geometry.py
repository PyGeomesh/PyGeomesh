import abc


class Geometry(abc.ABC):
    def __init__(self, time_dependent):
        self.time_dependent = time_dependent
        self.points = []
        self.boundary_points = []

    @abc.abstractmethod
    def is_internal(self, x):
        '''
        Returns True if the point x is internal to the geometry.
        '''
        pass
    
    @abc.abstractmethod
    def is_boundary(self, x):
        '''
        Returns True if the point x is on the boundary of the geometry.
        '''
        pass

    def grid_points(self, n):
        '''
        Returns a list of n grid points.
        '''
        pass

    def grid_points_on_boundary(self, n):
        '''
        Returns a list of n grid points on the boundary.
        '''
        pass

    def random_points(self, n, seed=None, type=None):
        '''
        Returns a list of n random points.
        '''
        pass

    def random_points_on_boundary(self, n, seed=None, type=None):
        '''
        Returns a list of n random points on the boundary.
        '''
        pass

    def uniform_time_dependent(self, n, time_start, time_end):
        '''
        Returns a list of n time-dependent points.
        '''
        pass

    def random_time_dependent(self, n, seed=None, type=None):
        '''
        Returns a list of n time-dependent points.
        '''
        pass

    def union(self, other):
        '''
        Returns the union of the two geometries.
        '''
        pass

    def intersection(self, other):
        '''
        Returns the intersection of the two geometries.
        '''
        pass

    def difference(self, other):
        '''
        Returns the difference of the two geometries.
        '''
        pass

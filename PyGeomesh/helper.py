import meshio
from gmsh import model


class model(model):
    pass


def read(filename):
    """Read a mesh from a file"""
    return meshio.read(filename)

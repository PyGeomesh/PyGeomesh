import meshio
from gmsh import model  # noqa


def read(filename):
    """
    Read a mesh from a file.
    """
    return meshio.read(filename)

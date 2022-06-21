import meshio
from gmsh import model as gmsh_model


class model(gmsh_model):
    def __init__(self):
        super().__init__()


def read(filename):
    """
    Read a mesh from a file.
    """
    return meshio.read(filename)


def extract_points():
    """
    Extract the points from a mesh.
    """
    import pygmsh

    return pygmsh.helpers.extract_to_meshio()

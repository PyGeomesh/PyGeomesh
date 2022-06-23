import meshio


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

import gmsh
from meshio._mesh import Mesh


class Geometry(object):
    mesh: Mesh

    def __new__(cls):
        gmsh.model.add(cls.__name__)
        gmsh.model.setCurrent(cls.__name__)
        return super(Geometry, cls).__new__(cls)

    @staticmethod
    def show(mesh: Mesh):
        print(mesh)

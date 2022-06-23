import gmsh
from meshio import Mesh
from pygmsh.occ import Geometry as OccGeometry


class Geometry(OccGeometry):
    mesh: Mesh

    def __new__(cls):
        gmsh.model.add(cls.__name__)
        gmsh.model.setCurrent(cls.__name__)
        return super(Geometry, cls).__new__(cls)

    @staticmethod
    def show(mesh: Mesh):
        print(mesh)

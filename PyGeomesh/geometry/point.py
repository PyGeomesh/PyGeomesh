import gmsh


class Point:
    def __init__(self, x: float, y: float, z: float = 0, meshSize=0, tag=-1):
        self.x = x
        self.y = y
        self.z = z
        self.meshSize = meshSize
        self.tag = tag
        gmsh.model.occ.addPoint(x, y, z, meshSize, tag)

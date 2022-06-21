class _Geometry:
    """
    Class for all geometries.

    Attributes

    model: gmsh.model

    """

    def __call__(self):
        return self


Geometry = _Geometry()

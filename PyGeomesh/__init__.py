import gmsh

from .geometry import Geometry
from .helper import extract_points, model

gmsh.initialize()

__all__ = [
    "Geometry",
    "model",
    "extract_points",
]

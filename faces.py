import copy as cp

import numpy as np

from translations import FaceTranslation, FaceListTranslation


class Copy:

    def copy(self):
        return cp.deepcopy(self)


class FaceRepresentation:

    def __init__(self):
        self.vertice_cnt = 0
        self.corners = []

    def __str__(self):
        to_print = \
            """
            A geometric face with {vertice_cnt} vertices\n
            with following corners :\n""".format(vertice_cnt=self.vertice_cnt)
        n = 1
        for corner in self.corners:
            to_print += "\t \t{n}. ({}, {}, {})\n".format(*corner, n=n)
            n += 1

        return to_print


class FaceListRepresentation:
    def __init__(self):
        self.faces = []

    def __str__(self):
        to_print = \
        """
        The Face list consists of :
        """
        for face in self.faces:
            to_print += face.__str__()

        return to_print


class GeomFaceUtilities(FaceTranslation, Copy, FaceRepresentation):
    pass


class GeomFaceListUtilities(FaceListTranslation, Copy, FaceListRepresentation):
    pass


class GeomFace(GeomFaceUtilities):
    """
    A Class representing a 2D geometrical Object which embodies the Face of a
    3D Objekt.
    We require that one of the corners is located at 0.0, 0.0, 0.0.
    The point have to be a 3D vectorlike shape (numpy array with length 3).

    The corners will be counted as follows (example quadrat) where the corners will be enumerated:

    1 -------- 2
    |          |
    |          |
    |          |
    |          |
    0 -------- 3

    """
    def __init__(self, vertice_cnt, corners, is_fast_cap=True):
        super(GeomFace, self).__init__()
        self.corners = corners
        self.vertice_cnt = vertice_cnt
        self.is_fast_cap = is_fast_cap

        self.validate()

    def validate(self):
        if not self.vertice_cnt == len(self.corners):
            raise ValueError(
                "Not enough corner points provided for a polygon with {n} vertices".format(n=self.vertice_cnt))
        if not (np.array([0.0, 0.0, 0.0]) in self.corners):
            raise ValueError(" The Point (0.0, 0.0, 0.0) is not included in the variable corners.")
        if list(map(lambda x: len(x) == 3, self.corners)).count(False):
            raise ValueError("Not all corners provided are a 3D vector.")
        if list(map(lambda x: isinstance(x, np.ndarray), self.corners)).count(False):
            raise ValueError("Not all corners provided are numpy arrays")
        if self.is_fast_cap:
            if self.vertice_cnt not in (3, 4):
                raise ValueError("For FastCap faces (is_fast_cap=True) only triangles and rectangles are allowed.")

    def prep_export_string(self, cond_name=1):
        shape_indicator = "T"
        base_string = "{shape}  {name}  {} {} {}  {} {} {}  {} {} {}\n"
        if self.vertice_cnt == 4:
            shape_indicator = "Q"
            base_string = "{shape}  {name}  {} {} {}  {} {} {}  {} {} {}  {} {} {}\n"

        return base_string.format(*self.corners.flatten(), shape=shape_indicator, name=cond_name)


class GeomFaceList(GeomFaceListUtilities):
    """
    A Container for multiple Faces.

    """
    def __init__(self, faces):
        super(GeomFaceList, self).__init__()
        self.faces = faces

        self.validate()

    def validate(self):
        if not isinstance(self.faces, list):
            raise ValueError("The profided Value for 'faces' is not a list.")

        for face in self.faces:
            if not isinstance(face, GeomFace):
                raise ValueError("The values of 'faces' aren't GeomFace instances, but {}.".format(face))

    def append(self, face):
        if not isinstance(face, GeomFace):
            raise ValueError("The provided face is not a GeomFace instances.")
        self.faces.append(face)

    def prep_export_string(self, cond_name=1):
        export_string = ""
        for face in self.faces:
            export_string += face.prep_export_string(cond_name=cond_name)
        return export_string

    def __iter__(self):
        return self.faces.__iter__()

    def __next__(self):
        self.faces.__next__()

# Test for Geometric faces
# g = GeomFace(3, np.array([[0.0, 0.0, 0.0], [0.0, 1.0, 0.0], [1.0, 0.0, 0.0]]))
#
# l = g.copy() + np.array([1, 0, 0])
# p = l - np.array([1, 0, 0])
# print("g", g)
# print("p", p)
# print("p == g", p==g)
# print(p.prep_export_string())

# Test for Gemoetricface lists
# list_to_add = [g.copy() + np.array([n, 0.0, 0.0]) for n in range(3)]
#
# geom_list = GeomFaceList(list_to_add)
# print(*g)
# for face in geom_list:
#     print(face)

# tilt = [*geom_list, g.copy() + np.array([1000.0, 0.0, 0.0])]
#
# for i in tilt:
#     print(i)
# other_geom_list = geom_list.copy() + np.array([1000.0, 0.0, 0.0])
#
# print(geom_list)
# print(other_geom_list)

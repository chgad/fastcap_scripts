# Ein Skript um Listfiles für FastCap zu erstellen


import numpy as np
import copy as cp


class GeomFace:
    """
    A Class representing a 2D geomatrical Object which embodies the Face of a
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
            if not self.vertice_cnt in (3, 4):
                raise ValueError("For FastCap faces (is_fast_cap=True) only triangles and rectangles are allowed.")

    def __add__(self, other):
        if not isinstance(other, np.ndarray):
            raise ValueError("__add__ is a translation operation. A Face can only be added with a 3D vectore")
        for vector in self.corners:
            vector += other

        return self

    def __sub__(self, other):
        if not isinstance(other, np.ndarray):
            raise ValueError("__sub__ is a translation operation. A Face can only be added with a 3D vectore")
        for vector in self.corners:
            vector -= other

        return self

    def copy(self):
        return cp.deepcopy(self)

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

    def prep_export_string(self, conductor_name=1):
        shape_indicator = "T"
        base_string = "{shape}  {name}  {} {} {}  {} {} {}  {} {} {}\n"
        if self.vertice_cnt == 4:
            shape_indicator = "Q"
            base_string = "{shape}  {name}  {} {} {}  {} {} {}  {} {} {}  {} {} {}\n"

        return base_string.format(*self.corners.flatten(), shape=shape_indicator, name=conductor_name)


# Test for Geometric faces
# g = GeomFace(3, np.array([[0.0, 0.0, 0.0], [0.0, 1.0, 0.0], [1.0, 0.0, 0.0]]))

# g = g + np.array([1, 0, 0])
# p = g.copy() - np.array([1, 0, 0])
# print(g)
# print(p)
# print(p.prep_export_string())


class ElectrodeStructure:
    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.heigth = height

        self.left_face = None
        self.right_face = None
        self.front_face = None
        self.back_face = None
        self.bottom_face = None
        self.top_face = None

        self.setup_all_faces()

    def validate(self):
        if not self.length > 0.0:
            raise ValueError("length must be non-negative and greater than 0.")

        if not self.width > 0.0:
            raise ValueError("width must be non-negative and greater than 0.")

        if not self.heigth > 0.0:
            raise ValueError("height must be non-negative and greater than 0.")

    def set_left_face(self):
        zero = np.array([0.0, 0.0, 0.0])
        one = np.array([0.0, self.length, 0.0])
        two = np.array([0.0, self.length, self.heigth])
        three = np.array([0.0, 0.0, self.heigth])
        self.left_face = GeomFace(4, np.array([zero, one, two, three]))

    def set_right_face(self):
        self.right_face = self.left_face.copy() + np.array([self.width, 0.0, 0.0])

    def set_front_face(self):
        zero = np.array([0.0, 0.0, 0.0])
        one = np.array([0.0, 0.0, self.heigth])
        two = np.array([self.width, 0.0, self.heigth])
        three = np.array([self.width, 0.0, 0.0])
        self.front_face = GeomFace(4, np.array([zero, one, two, three]))

    def set_back_face(self):
        self.back_face = self.front_face.copy() + np.array([0.0, self.length, 0.0])

    def set_bottom_face(self):
        zero = np.array([0.0, 0.0, 0.0])
        one = np.array([0.0, self.length, 0.0])
        two = np.array([self.width, self.length, 0.0])
        three = np.array([self.width, 0.0, 0.0])
        self.bottom_face = GeomFace(4, np.array([zero, one, two, three]))

    def set_top_face(self):
        self.top_face = self.bottom_face.copy() + np.array([0.0, 0.0, self.heigth])

    def setup_all_faces(self):
        self.set_front_face()
        self.set_back_face()
        self.set_left_face()
        self.set_right_face()
        self.set_bottom_face()
        self.set_top_face()

    def prep_export_string(self,cond_name=1):
        export_string = ""
        for face in [getattr(self, x) for x in self.__dict__ if x.endswith("face") and getattr(self, x)]:
            export_string += face.prep_export_string()

        return export_string

    def export_to_file(self,file_name):
        with open(file_name, "a") as f:
            f.write(self.prep_export_string())
            f.close()


# Test the Electrode Structure


elec = ElectrodeStructure(length=7.0, width=1.5, height=3.7)
print(elec.prep_export_string())
elec.export_to_file("fast_cap_test.txt")

#
# print("Bottom and top Face")
# print(elec.bottom_face)
# print(elec.top_face)
# print("Front and back Face")
# print(elec.front_face)
# print(elec.back_face)
# print("Left and right Face")
# print(elec.left_face)
# print(elec.right_face)

class BaseStructure:
    def __init__(self):
        pass

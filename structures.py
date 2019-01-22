# Ein Skript um Listfiles für FastCap zu erstellen


import copy as cp

import numpy as np

from translations import IdtTranslation
from faces import GeomFace, GeomFaceList


class Cuboid:
    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height

        self.left_face = None
        self.right_face = None
        self.front_face = None
        self.back_face = None
        self.bottom_face = None
        self.top_face = None

        self.setup_all_faces()
        self.all_faces = self.get_all_faces()

    def validate(self):
        if not self.length > 0.0:
            raise ValueError("length must be non-negative and greater than 0.")

        if not self.width > 0.0:
            raise ValueError("width must be non-negative and greater than 0.")

        if not self.height > 0.0:
            raise ValueError("height must be non-negative and greater than 0.")

    def set_left_face(self):
        zero = np.array([0.0, 0.0, 0.0])
        one = np.array([0.0, 0.0, self.height])
        two = np.array([0.0, self.length, self.height])
        three = np.array([0.0, self.length, 0.0])

        self.left_face = GeomFace(4, np.array([zero, one, two, three]))

    def set_right_face(self):
        zero = np.array([0.0, 0.0, 0.0])
        one = np.array([0.0, self.length, 0.0])
        two = np.array([0.0, self.length, self.height])
        three = np.array([0.0, 0.0, self.height])
        self.right_face = GeomFace(4, np.array([zero, one, two, three])) + np.array([self.width, 0.0, 0.0])

    def set_front_face(self):
        zero = np.array([0.0, 0.0, 0.0])
        one = np.array([self.width, 0.0, 0.0])
        two = np.array([self.width, 0.0, self.height])
        three = np.array([0.0, 0.0, self.height])
        self.front_face = GeomFace(4, np.array([zero, one, two, three]))

    def set_back_face(self):
        zero = np.array([0.0, 0.0, 0.0])
        one = np.array([0.0, 0.0, self.height])
        two = np.array([self.width, 0.0, self.height])
        three = np.array([self.width, 0.0, 0.0])
        self.back_face = GeomFace(4, np.array([zero, one, two, three])) + np.array([0.0, self.length, 0.0])

    def set_bottom_face(self):
        zero = np.array([0.0, 0.0, 0.0])
        one = np.array([0.0, self.length, 0.0])
        two = np.array([self.width, self.length, 0.0])
        three = np.array([self.width, 0.0, 0.0])
        self.bottom_face = GeomFace(4, np.array([zero, one, two, three]))

    def set_top_face(self):
        zero = np.array([0.0, 0.0, 0.0])
        one = np.array([self.width, 0.0, 0.0])
        two = np.array([self.width, self.length, 0.0])
        three = np.array([0.0, self.length, 0.0])
        self.top_face = GeomFace(4, np.array([zero, one, two, three])) + np.array([0.0, 0.0, self.height])

    def setup_all_faces(self):
        # ORDER MATTERS HERE
        self.set_front_face()
        self.set_back_face()

        self.set_left_face()
        self.set_right_face()

        self.set_bottom_face()
        self.set_top_face()

    def get_all_faces(self):
        return GeomFaceList([getattr(self, face) for face in self.__dict__
                             if face.endswith("face") and getattr(self, face)])

    def prep_blender_data(self, start_index=0, diff_faces=None):
        if diff_faces:
            faces = diff_faces
        else:
            faces = self.all_faces
        exp_corners = []
        exp_faces = []

        for face in faces:
            corners, fce = face.prep_blender_data(start_index=start_index)
            exp_corners.extend(corners)
            exp_faces.append(fce)
            start_index += face.vertice_cnt

        return exp_corners, exp_faces

    def copy(self):
        return cp.deepcopy(self)

    def __add__(self, other):
        if not isinstance(other, np.ndarray):
            raise ValueError("__add__ is a translation operation. A Face can only be added with a 3D vectore")
        self.all_faces += other

        return self

    def __sub__(self, other):
        if not isinstance(other, np.ndarray):
            raise ValueError("__sub__ is a translation operation. A Face can only be added with a 3D vectore")
        self.all_faces -= other

        return self


class FastCapCuboid(Cuboid):

    def __init__(self, omit_faces=[], *args, **kwargs):
        super(FastCapCuboid, self).__init__(*args, **kwargs)
        self.omit_faces = omit_faces

    def get_all_faces(self):
        """
        In Fast Cap we allow that one 'normal' Cuboid face is splitted into multiple faces, represented by
        a GeomFaceList instance.
        :return:
        """
        final_list = []
        for attr in self.__dict__:
            actual_attr = getattr(self, attr)
            if attr.endswith("face") and actual_attr:
                if isinstance(actual_attr, GeomFaceList):
                    final_list = [*final_list, *actual_attr]
                else:
                    final_list.append(actual_attr)
        return GeomFaceList(final_list)

    def fields_to_export(self):
        """
        In FastCap we allow certain faces to be omitted since the could be replaced by other structures faces.
        """
        final_list = []
        for attr in self.__dict__:
            actual_attr = getattr(self, attr)
            if attr.endswith("face") and actual_attr and attr not in self.omit_faces:
                if isinstance(actual_attr, GeomFaceList):
                    final_list = [*final_list, *actual_attr]
                else:
                    final_list.append(actual_attr)
        return GeomFaceList(final_list)

    def prep_export_string(self,cond_name=1):
        return self.fields_to_export().prep_export_string(cond_name=cond_name)

    def export_to_file(self,file_name):
        with open(file_name, "a") as f:
            f.write(self.prep_export_string())
            f.close()


class ElectrodeStructure(FastCapCuboid):
    pass

# Test the Electrode Structure


# elec = ElectrodeStructure(length=7.0, width=1.5, height=3.7) #omit_faces=["bottom_face"])
# print(elec.prep_export_string())
# elec.export_to_file("fast_cap_test2.txt")

# print("Bottom and top Face")
# print(elec.bottom_face)
# print(elec.top_face)
# print("Front and back Face")
# print(elec.front_face)
# print(elec.back_face)
# print("Left and right Face")
# print(elec.left_face)
# print(elec.right_face)


class LowerBaseStructure(FastCapCuboid):

    """
    The BaseStructure will look like the followning scheme:

                    back

    1eee2-----3eee4-----5eee6-----7eee8-----9eee10
    |   |     |   |     |   |     |   |     |   |
    |   |     |   |     |   |     |   |     |   |
    0-------------------------------------------11
                    front

    in the x-y-plane.

    The marker eee show where no face is defined and an ElectrodeStructure is added
    later on.


    """
    def __init__(self, elec_width, elec_sep, elec_cnt, *args, **kwargs):

        self.elec_width = elec_width    # elec distance in y-direction
        self.elec_sep = elec_sep        # distance between 2 Electrodes
        self.elec_cnt = elec_cnt        # number of electrodes

        super(LowerBaseStructure, self).__init__(*args, **kwargs)

    def set_back_face(self):
        zero = np.array([0.0, 0.0, 0.0])
        one = np.array([0.0, 0.0, self.height])
        two = np.array([2*self.elec_sep + self.elec_width, 0.0, self.height])
        three = np.array([2*self.elec_sep + self.elec_width, 0.0, 0.0])
        base_face = GeomFace(4, np.array([zero, one, two, three]))
        separation = 2 * (self.elec_width + self.elec_sep)
        faces_list = [base_face.copy() + np.array([n * separation + self.elec_width, self.length, 0.0])
                      for n in range(self.elec_cnt-1)]

        self.back_face = GeomFaceList(faces=faces_list)

    def set_top_face(self):
        """
        The Top face gets split up into faces that are, alternating, of electrode width and
        2*electrode separation + electrode width wide. This is depicted in the class Docstring.
        """
        # vertices for the electrode wide top faces (in scheme: faces touching eee sections)
        zero = np.array([0.0, 0.0, 0.0])
        one = np.array([self.elec_width, 0.0, 0.0])
        two = np.array([self.elec_width, self.length, 0.0])
        three = np.array([0.0, self.length, 0.0])
        # For faces on the right of the above faces we need different vertices for one and two
        sec_one = np.array([2*self.elec_sep + self.elec_width, 0.0, 0.0])
        sec_two = np.array([2*self.elec_sep + self.elec_width, self.length, 0.0])

        base_elec_face = GeomFace(4, np.array([zero, one, two, three])) + np.array([0.0, 0.0, self.height])
        base_sep_face = GeomFace(4, np.array([zero, sec_one, sec_two, three])) + np.array([0.0, 0.0, self.height])

        separation = 2 * (self.elec_width + self.elec_sep)

        # Prepare all faces ouching electrodes
        faces_list = [base_elec_face.copy() + np.array([n * separation, 0.0, 0.0])
                      for n in range(self.elec_cnt)]
        # Extend list by Faces in between the above faces
        faces_list.extend([base_sep_face.copy() + np.array([self.elec_width + n * separation, 0.0, 0.0])
                          for n in range(self.elec_cnt-1)])

        self.top_face = GeomFaceList(faces=faces_list)


class UpperBaseStructure(FastCapCuboid):
    """
    The BaseStructure will look like the followning scheme:

                    back

    1-------------------------------------------2
    |                                           |
    |                                           |
    0----+eee*-----9eee8-----7eee6-----5eee4----3
                    front

    in the x-y-plane.

    The marker eee show where no face is defined and an ElectrodeStructure is added
    later on.
    """

    def __init__(self, elec_width, elec_sep, elec_cnt, *args, **kwargs):
        self.elec_width = elec_width  # elec distance in y-direction
        self.elec_sep = elec_sep  # distance between 2 Electrodes
        self.elec_cnt = elec_cnt  # number of electrodes

        super(UpperBaseStructure, self).__init__(*args, **kwargs)

    def set_front_face(self):
        zero = np.array([0.0, 0.0, 0.0])
        one = np.array([2 * self.elec_sep + self.elec_width, 0.0, 0.0])
        two = np.array([2 * self.elec_sep + self.elec_width, 0.0, self.height])
        three = np.array([0.0, 0.0, self.height])
        sec_one = np.array([self.elec_sep + self.elec_width, 0.0, 0.0])
        sec_two = np.array([self.elec_sep + self.elec_width, 0.0, self.height])

        start_end_face = GeomFace(4, np.array([zero, sec_one, sec_two, three]))
        base_face = GeomFace(4, np.array([zero, one, two, three]))

        separation = 2 * (self.elec_width + self.elec_sep)
        faces_list = [base_face.copy() + np.array([n * separation + 2 * self.elec_width + self.elec_sep, 0.0, 0.0])
                      for n in range(self.elec_cnt - 1)]
        faces_list.extend([start_end_face,
                           start_end_face.copy() + np.array(
                               [self.width - (self.elec_sep + self.elec_width), 0.0, 0.0])])
        self.front_face = GeomFaceList(faces_list)

    def set_top_face(self):
        # Coordinates for the firs Top face with Corners 0, +, "", 1
        # This is the Start and End top face
        zero = np.array([0.0, 0.0, 0.0])
        one = np.array([self.elec_width +self.elec_sep, 0.0 , 0.0])
        two = np.array([self.elec_width + self.elec_sep, self.length, 0.0])
        three = np.array([0.0, self.length, 0.0])
        # Coordinates for the Top faces cornering the Electrode's top faces
        sec_one = np.array([self.elec_width, 0.0, 0.0])
        sec_two = np.array([self.elec_width, self.length, 0.0])
        # Coordinates for the Top faces between the Electrodes
        third_one = np.array([self.elec_width + 2*self.elec_sep, 0.0, 0.0])
        third_two = np.array([self.elec_width + 2*self.elec_sep, self.length, 0.0])
        # Faces
        start_end_face = GeomFace(4, corners=np.array([zero, one, two, three])) + np.array([0.0, 0.0, self.height])
        elec_face = GeomFace(4, corners=np.array([zero, sec_one, sec_two, three])) + np.array([0.0, 0.0, self.height])
        middle_face = GeomFace(4, corners=np.array([zero, third_one, third_two, three])) + np.array(
            [0.0, 0.0, self.height])

        separation = 2 * (self.elec_width + self.elec_sep)
        # Start generating all Electrode cornering faces
        faces_list = [elec_face.copy() + np.array([self.elec_width + self.elec_sep + n * separation, 0.0, 0.0])
                      for n in range(self.elec_cnt)]
        # Extend with all Faces in between
        faces_list.extend([middle_face.copy() + np.array([2*self.elec_width + self.elec_sep + n * separation, 0.0, 0.0])
                      for n in range(self.elec_cnt-1)])
        # Finally add start and end faces
        faces_list.extend(
            [start_end_face, start_end_face + np.array([self.width - (self.elec_sep + self.elec_width), 0.0, 0.0])])

        self.top_face = GeomFaceList(faces_list)


class IdtLowerStructure(IdtTranslation):

    def __init__(self, elec_length, elec_width, elec_sep, elec_cnt,
                 base_length, height):
        super(IdtLowerStructure, self).__init__()
        self.elec_length = elec_length
        self.elec_width = elec_width
        self.elec_sep = elec_sep
        self.elec_cnt = elec_cnt

        self.base_length = base_length
        self.base_width = self.set_base_width()

        self.height = height

        self.electrodes = None
        self.base = None

        self.diel_faces = None

        self.setup()

    def setup(self):
        self.set_base()
        self.set_electrodes()
        self.setup_diel_faces()

    def set_base_width(self):
        return self.elec_cnt * self.elec_width + (self.elec_cnt-1)*(self.elec_width+2*self.elec_sep)

    def set_base(self):
        self.base = LowerBaseStructure(elec_width=self.elec_width, elec_sep=self.elec_sep, elec_cnt=self.elec_cnt,
                                       length=self.base_length, width=self.base_width, height=self.height,
                                       omit_faces=["bottom_face"])

    def set_electrodes(self):
        electrode = ElectrodeStructure(length=self.elec_length, width=self.elec_width, height=self.height,
                                       omit_faces=["bottom_face", "front_face"])
        separation = 2 * (self.elec_width + self.elec_sep)
        self.electrodes = [electrode.copy() + np.array([n * separation, self.base_length, 0.0])
                           for n in range(self.elec_cnt)]

    def setup_diel_faces(self):
        self.diel_faces = GeomFaceList([*self.set_diel_short(), *self.set_diel_long()])

    def prep_diel_short(self):
        zero = np.array([0.0, 0.0, 0.0])
        one = np.array([self.elec_width, 0.0, 0.0])
        two = np.array([self.elec_width, self.elec_sep, 0.0])
        three = np.array([0.0, self.elec_sep, 0.0])
        return GeomFace(4, np.array([zero, one, two, three]))

    def prep_diel_long(self):
        zero = np.array([0.0, 0.0, 0.0])
        one = np.array([self.elec_sep, 0.0, 0.0])
        two = np.array([self.elec_sep, self.elec_length + self.elec_sep, 0.0])
        three = np.array([0.0, self.elec_length + self.elec_sep, 0.0])
        return GeomFace(4, np.array([zero, one, two, three]))

    def set_diel_short(self):
        base_face = self.prep_diel_short()

        separation = 2 * (self.elec_width + self.elec_sep)
        final_list = [base_face.copy() + np.array([n * separation, self.elec_length + self.base_length, 0.0])
                      for n in range(self.elec_cnt)]
        return final_list

    def set_diel_long(self):
        base_face = self.prep_diel_long()

        separation = 2 * (self.elec_width + self.elec_sep)
        final_list = [base_face.copy() + np.array([n * separation + self.elec_width, self.base_length, 0.0])
                      for n in range(self.elec_cnt-1)]
        return final_list

    def prep_blender_data(self):
        exp_corners = []
        exp_faces = []
        start_index = 0

        # First prepare elecrodes
        for elec in self.electrodes:
            corners, faces = elec.prep_blender_data(start_index=start_index, diff_faces=elec.fields_to_export())
            exp_corners.extend(corners)
            exp_faces.extend(faces)
            start_index = faces[-1][-1] + 1
        # Now prepare base

        corners, faces = self.base.prep_blender_data(start_index=start_index, diff_faces=self.base.fields_to_export())
        exp_corners.extend(corners)
        exp_faces.extend(faces)
        return exp_corners, exp_faces

    def prep_export_strings(self):

        export_cond_string = ""
        export_diel_string = ""

        export_cond_string += self.base.prep_export_string()
        export_diel_string += self.base.bottom_face.prep_export_string()
        for elec in self.electrodes:
            export_cond_string += elec.prep_export_string()
            export_diel_string += elec.bottom_face.prep_export_string()

        return export_cond_string, export_diel_string

    def export_to_file(self,cond_file_name, diel_file_name):
        cond, diel = self.prep_export_strings()
        with open(cond_file_name, "a") as f:
            f.write(cond)
            f.close()

        with open(diel_file_name, "a")as f:
            f.write(diel)
            f.close()


# Test for IdtLowerStructure
# idt_lower = IdtLowerStructure(elec_length=20, elec_width=2, elec_sep=3, elec_cnt=10, base_length=5, height=7)
#
# idt_lower.export_to_file(cond_file_name="test_cond_file.txt", diel_file_name="test_diel_file.txt")

class IdtUpperStructure(IdtLowerStructure):

    def set_base_width(self):
        # originally self.elec_cnt * self.elec_width + (self.elec_cnt-1)*(self.elec_width+2*self.elec_sep)
        # + 2*(self.elec_width + self.elec_sep
        return (self.elec_cnt+1) * self.elec_width + self.elec_cnt*(self.elec_width+2*self.elec_sep)

    def set_base(self):
        self.base = UpperBaseStructure(elec_width=self.elec_width, elec_sep=self.elec_sep, elec_cnt=self.elec_cnt,
                                       length=self.base_length, width=self.base_width, height=self.height,
                                       omit_faces=["bottom_face"])

    def set_diel_short(self):
        base_face = self.prep_diel_short()

        separation = 2 * (self.elec_width + self.elec_sep)
        final_list = [base_face.copy() + np.array([(n+0.5) * separation, -(self.elec_length+self.elec_sep), 0.0])
                      for n in range(self.elec_cnt)]
        return final_list

    def set_diel_long(self):

        base_face = self.prep_diel_long()

        separation = 2 * (self.elec_width + self.elec_sep)
        final_list = [base_face.copy() + np.array(
            [n * separation + 2 * self.elec_width + self.elec_sep, -(self.elec_length + self.elec_sep), 0.0])
                      for n in range(self.elec_cnt)]
        return final_list

    def set_electrodes(self):
        electrode = ElectrodeStructure(length=self.elec_length, width=self.elec_width, height=self.height,
                                       omit_faces=["bottom_face", "back_face"])
        separation = 2 * (self.elec_width + self.elec_sep)
        self.electrodes = [electrode.copy() + np.array([(n + 0.5) * separation, -self.elec_length, 0.0])
                           for n in range(self.elec_cnt)]


# Test for IdtLowerStructure
# idt_upper = IdtUpperStructure(elec_length=20, elec_width=2, elec_sep=3, elec_cnt=9, base_length=5, height=7)
#
# idt_upper.export_to_file(cond_file_name="test_upper_cond_file.txt", diel_file_name="test_upper_diel_file.txt")

class SiO2Layer(FastCapCuboid):
    def __init__(self,structure_length, structure_width, *args,**kwargs):
        self.structure_length = structure_length
        self.structure_width = structure_width
        super(SiO2Layer, self).__init__(*args, **kwargs)

    def prep_top_longer_part(self):
        y = 0.5*(self.length - self.structure_length)
        zero = np.array([0.0, 0.0, self.height])
        one = np.array([0.0, y, self.height])
        two = np.array([self.width, y, self.height])
        three = np.array([self.width, 0.0, self.height])
        return GeomFace(4, np.array([zero, one, two, three]))

    def prep_top_shorter_part(self):
        x = 0.5 * (self.width - self.structure_width)
        zero = np.array([0.0, 0.0, self.height])
        one = np.array([0.0, self.structure_length, self.height])
        two = np.array([x, self.structure_length, self.height])
        three = np.array([x, 0.0, self.height])
        return GeomFace(4, np.array([zero, one, two, three]))

    def set_top_face(self):
        long_part = self.prep_top_longer_part()
        short_part = self.prep_top_shorter_part() + np.array([0.0, 0.5 * (self.length - self.structure_length), 0.0])
        final_list = [long_part,
                      long_part.copy() + np.array([0.0, 0.5 * (self.length + self.structure_length), 0.0]),
                      short_part.copy(),
                      short_part.copy() + np.array([0.5*(self.width + self.structure_width), 0.0, 0.0])]
        self.top_face = GeomFaceList(final_list)


# Test for SiO2Layer
# si_o_two = SiO2Layer(structure_length=1, structure_width=1, length=10, width=10, height=3)
# si_o_two.export_to_file("si_o_2_diel.txt")

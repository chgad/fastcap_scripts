from structures import IdtLowerStructure, IdtUpperStructure, SiO2Layer, FastCapCuboid
import numpy as np


class BlenderIDTonSiO2struct:
    def __init__(self, elec_length, elec_width, elec_sep, elec_cnt, base_length, idt_height, si_o2_height):

        self.elec_length = elec_length
        self.elec_width = elec_width
        self.elec_sep = elec_sep
        self.elec_cnt = elec_cnt
        self.base_length = base_length
        self.idt_height = idt_height
        self.si_o2_height = si_o2_height

        self.structure_dict = self.create_structure()
        self.blender_dict = self.prepare_visualization_data(self.structure_dict)

    def create_idt_lower(self):
        return IdtLowerStructure(
            elec_length=self.elec_length,
            elec_width=self.elec_width,
            elec_sep=self.elec_sep,
            elec_cnt=self.elec_cnt,
            base_length=self.base_length,
            height=self.idt_height,
        )

    def create_idt_upper(self):
        return IdtUpperStructure(
            elec_length=self.elec_length,
            elec_width=self.elec_width,
            elec_sep=self.elec_sep,
            elec_cnt=self.elec_cnt - 1,
            base_length=self.base_length,
            height=self.idt_height,
        )

    def create_si_o2_layer(self, structure_length, structure_width, substrate_length, substrate_width):
        return SiO2Layer(
            structure_length=structure_length,
            structure_width=structure_width,
            length=substrate_length,
            width=substrate_width,
            height=self.si_o2_height,
        )

    def create_structure(self):
        """
        This Function creates a symmetric IDT structure on a so called SI_O2 substrate.
        The substrate is of factor 1.25 greater than the resulting IDT structure.
        The structure is placed centered on top, touching the substrate.
        :param elec_length:
        :param elec_width:
        :param elec_sep:
        :param elec_cnt:
        :param base_length:
        :param idt_height:
        :param si_o2_height:
        :return: Dict
        """
        idt_lower = self.create_idt_lower()

        idt_upper = self.create_idt_upper()

        structure_length = self.elec_sep + 2 * idt_upper.base_length + self.elec_length
        structure_width = idt_upper.base_width

        # Fix so that Dielectric top Face is not of orders greater than the structure

        substrate_width = 1.25 * structure_width
        substrate_length = 1.25 * structure_length

        si_o2 = self.create_si_o2_layer(
            structure_length=structure_length,
            structure_width=structure_width,
            substrate_length=substrate_length,
            substrate_width=substrate_width,
        )

        idt_structure_length = self.elec_sep + 2 * idt_upper.base_length + self.elec_length
        idt_structure_width = idt_lower.base_width

        # Alignment translation to position the IDT structure in the middle of the Substrate

        align_idt_vector = np.array(
            [
                0.5 * (substrate_width - idt_structure_width),
                0.5 * (substrate_length - idt_structure_length),
                0.0,
            ]
        )

        idt_upper + np.array([0.0, self.elec_length + self.elec_sep + idt_lower.base_length, 0.0])
        idt_lower + align_idt_vector
        idt_upper + align_idt_vector

        si_o2 - np.array([0.0, 0.0, si_o2.height])

        return {"IDT_LOWER": idt_lower, "IDT_UPPER": idt_upper, "SI_O2": si_o2}

    def prepare_visualization_data(self, structure_dict):
        idt_lower = structure_dict.get("IDT_LOWER", None)
        idt_upper = structure_dict.get("IDT_UPPER", None)
        si_o2 = structure_dict.get("SI_O2", None)

        assert idt_lower, "IDT_LOWER must be provided."
        assert idt_upper, "IDT_UPPER must be provided."
        assert si_o2, "SI_O2 must be provided."

        lower_elec_data = list_electrode_prep_blender_data(
            idt_lower.electrodes, "bottom_face"
        )

        upper_elec_data = list_electrode_prep_blender_data(
            idt_upper.electrodes, "bottom_face"
        )

        lower_base_bottom_verts, lower_face = idt_lower.base.bottom_face.prep_blender_data()
        upper_base_bottom_verts, upper_face = idt_upper.base.bottom_face.prep_blender_data()

        upper_base_bottom_data = (upper_base_bottom_verts, [upper_face])
        lower_base_bottom_data = (lower_base_bottom_verts, [lower_face])

        upper_data = idt_upper.prep_blender_data()

        lower_data = idt_lower.prep_blender_data()

        diel_upper_data = idt_upper.diel_faces.prep_blender_data()

        diel_lower_data = idt_lower.diel_faces.prep_blender_data()

        sio2_data = si_o2.top_face.prep_blender_data()

        return {
            "IDT_UPPER": upper_data,
            "IDT_LOWER": lower_data,
            "BASE_BOTTOM_UPPER": upper_base_bottom_data,
            "BASE_BOTTOM_LOWER": lower_base_bottom_data,
            "ELEC_UPPER": upper_elec_data,
            "ELEC_LOWER": lower_elec_data,
            "DIEL_UPPER": diel_upper_data,
            "DIEL_LOWER": diel_lower_data,
            "SI_O2": sio2_data,
        }


class BlenderIDTonSiO2AndSiStruct(BlenderIDTonSiO2struct):

    def __init__(self, si_height, *args, **kwargs):
        self.si_height = si_height
        super(BlenderIDTonSiO2AndSiStruct, self).__init__(*args, **kwargs)

    def create_si_o2_layer(self, structure_length, structure_width, substrate_length, substrate_width):
        si_o2 = super(BlenderIDTonSiO2AndSiStruct, self).create_si_o2_layer(
            structure_length,
            structure_width,
            substrate_length,
            substrate_width
        )
        si_o2.omit_faces = ["bottom_face"]
        return si_o2

    def create_si_layer(self, substrate_length, substrate_width):
        return FastCapCuboid(
            length=substrate_length,
            width=substrate_width,
            height=self.si_height,
            omit_faces=["top_face"]
        )

    def create_structure(self):
        structure_dict = super(BlenderIDTonSiO2AndSiStruct, self).create_structure()
        si_o2 = structure_dict["SI_O2"]
        si_layer = self.create_si_layer(substrate_length=si_o2.length, substrate_width=si_o2.width)
        si_layer - np.array([0.0, 0.0, self.si_o2_height + self.si_height])
        structure_dict["SI"] = si_layer
        return structure_dict

    def prepare_visualization_data(self, structure_dict):
        return_dict = super(BlenderIDTonSiO2AndSiStruct, self).prepare_visualization_data(structure_dict)
        # si_o2 = structure_dict.get("SI_O2", None)
        si_layer = structure_dict.get("SI", None)
        assert si_layer, "SI must be provided."
        # Here we prepare all faces for the SiO2 but the bottom face
        # sio2_data = si_o2.prep_blender_data(diff_faces=si_o2.fields_to_export())
        si_top_corners, si_top_faces = si_layer.top_face.prep_blender_data()
        si_data = si_layer.prep_blender_data(diff_faces=si_layer.fields_to_export())
        # return_dict["SI_O2"] = sio2_data
        return_dict["SI_TOP"] = (si_top_corners, [si_top_faces])
        return_dict["SI"] = si_data
        return return_dict

def list_electrode_prep_blender_data(cuboid_list, face_name):
    """
    this Function Creates the Blender input data for the Python API of a list consisting
    of Cuboid instances.
    :param cuboid_list:
    :param face_name:
    :return:
    """
    exp_vertices = []
    exp_faces = []
    start_index = 0
    for cuboid in cuboid_list:
        face_obj = getattr(cuboid, face_name)
        vertices, face = face_obj.prep_blender_data(start_index)
        exp_vertices.extend(vertices)
        exp_faces.append(face)
        start_index += 4

    return exp_vertices, exp_faces
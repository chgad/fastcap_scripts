from structures import IdtLowerStructure, IdtUpperStructure, SiO2Layer
import numpy as np


def create_idt_structure(
    elec_length, elec_width, elec_sep, elec_cnt, base_length, idt_height, si_o2_height
):
    """
    This Function creates a symmetric IDT structure on a so calld SI_O2 substrate.
    The substrate is of factor 1.25 greater that the resulting IDT structure.
    The structure is placed centered on top, touching thie substrate
    :param elec_length:
    :param elec_width:
    :param elec_sep:
    :param elec_cnt:
    :param base_length:
    :param idt_height:
    :param si_o2_height:
    :return: Dict
    """
    idt_lower = IdtLowerStructure(
        elec_length=elec_length,
        elec_width=elec_width,
        elec_sep=elec_sep,
        elec_cnt=elec_cnt,
        base_length=base_length,
        height=idt_height,
    )

    idt_upper = IdtUpperStructure(
        elec_length=elec_length,
        elec_width=elec_width,
        elec_sep=elec_sep,
        elec_cnt=elec_cnt - 1,
        base_length=base_length,
        height=idt_height,
    )

    si_o2_length = elec_sep + 2 * idt_upper.base_length + elec_length
    si_o2_width = idt_upper.base_width

    # Fix so that Dielectric top Face is not of orders greater than the structure

    substrate_width = 1.25 * si_o2_width
    substrate_length = 1.25 * si_o2_length

    si_o2 = SiO2Layer(
        structure_length=si_o2_length,
        structure_width=si_o2_width,
        length=substrate_length,
        width=substrate_width,
        height=si_o2_height,
    )

    idt_structure_length = elec_sep + 2 * idt_upper.base_length + elec_length
    idt_structure_width = idt_lower.base_width

    # Alignment translation to position the IDT structure in the middle of the Substrate

    align_idt_vector = np.array(
        [
            0.5 * (substrate_width - idt_structure_width),
            0.5 * (substrate_length - idt_structure_length),
            0.0,
        ]
    )

    idt_upper + np.array([0.0, elec_length + elec_sep + idt_lower.base_length, 0.0])
    idt_lower + align_idt_vector
    idt_upper + align_idt_vector

    si_o2 - np.array([0.0, 0.0, si_o2.height])

    return {"IDT_LOWER": idt_lower, "IDT_UPPER": idt_upper, "SI_O2": si_o2}


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


def prepare_visualization_data(structure_dict):
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

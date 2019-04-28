from create_idt_structure_classes import BlenderIDTonSiO2struct, BlenderIDTonSiO2AndSiStruct
import numpy as np
import bpy


def create_materials(file_dict):
    """
    Dynamically creates Blender Material-objects from a provided file dictionary.
    The file dictionary is expected to be :
    {
        "<Material Name>": "<File Name for Interfaces of Material>"
    }

    The Function returns a Dictionary of kind :

    {
        "<Material Name>": Material Object
    }

    :param file_dict:
    :return: Dict
    """
    _dict = {}
    for material in file_dict:
        material_object = bpy.data.materials.new(name=material)
        material_object.diffuse_color = tuple(
            np.random.choice(np.linspace(0, 1, 6), size=3)
        )
        _dict[material] = material_object
    return _dict


def retrieve_current_material(name, material_dict):

    if name.startswith("IDT"):
        if name.endswith("UPPER"):
            return material_dict.get("Conductor Air Upper")
        else:
            return material_dict.get("Conductor Air Lower")

    elif name.startswith("ELEC") or name.startswith("BASE_BOTTOM"):
        if name.endswith("UPPER"):
            return material_dict.get("Conductor Dielectric Upper")
        else:
            return material_dict.get("Conductor Dielectric Lower")
    elif name.startswith("SI"):
        if name.endswith("TOP"):
            return material_dict.get("Si Top")
        elif name == "SI":
            return material_dict.get("Si")
        else:
            return material_dict.get("Dielectric")
    else:
        return material_dict.get("Dielectric")

def load_blender_data(name, verts_face_tuple, material_dict):
    """
    This Function loads the Python data into Blender.

    :param name: Name of the Blender Meshobject
    :param verts_face_tuple: Tuple consisting of Vertices Tuple and Tuple of Facetuples
    :return: None
    """
    mat = retrieve_current_material(name, material_dict)

    mesh_data = bpy.data.meshes.new(name)
    mesh_data.from_pydata(verts_face_tuple[0], [], verts_face_tuple[1])

    obj = bpy.data.objects.new(name, mesh_data)
    obj.data.materials.append(mat)
    bpy.context.scene.objects.link(obj)

    bpy.context.scene.objects.active = obj


def blender_perform_modification(number_insets=0, number_subdivides=0, min_relative_thickness=0, subdivide_all=False):

    """
    Perform modification of the imported Blender objects.
    We perform n insets, k subdivides to the most inner inset.
    If subdivde_all is True we subdivide all faces.
    To prevent resulting overlapping faces after performing insets we need to introduce
    a min_relative_thickness. This enables us to perform 10 insets at most.

    :param number_insets:
    :param number_subdivides:
    :param min_relative_thickness:
    :param subdivide_all:
    :return:
    """
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.join()

    bpy.ops.object.mode_set(mode="EDIT")

    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.remove_doubles()
    assert number_insets <= 10, "No more insets than 10 allowed"

    for i in range(number_insets):
        bpy.ops.mesh.inset(
            use_relative_offset=False,
            thickness=0.1 * min_relative_thickness,
            use_interpolate=True,
            use_individual=True,
        )
    # only the last insets get divided
    if subdivide_all:
        bpy.ops.mesh.select_all(action="SELECT")

    if number_subdivides:
        bpy.ops.mesh.subdivide(number_cuts=number_subdivides)

    bpy.ops.mesh.separate(type="MATERIAL")
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="DESELECT")


def blender_export_to_fastcap(material_filename_dict, title):
    for obj in bpy.context.scene.objects:
        data = obj.data
        assert data, "{}".format(obj)
        exp_str = title
        for face in data.polygons:
            face_verts = face.vertices

            base_str = "Q  1"
            if len(face_verts) == 3:
                base_str = "T  1"
            exp_str += base_str
            for i in face_verts:
                vert = data.vertices[i].co
                exp_str += "  {} {} {}".format(vert.x, vert.y, vert.z)
            exp_str += "\n"

        assert len(data.materials) >= 1
        exp_str += "N  1  {}".format(data.materials[0].name.split(" ")[-1])
        bpy.ops.object.select_pattern(pattern=obj.name)
        bpy.ops.object.delete(use_global=True)

        # we know that the objects only consist of one material
        file_name = material_filename_dict[data.materials[0].name]
        with open(file_name, "a") as f:
            f.write(exp_str)


if __name__ == "__main__":
    dummy = False
    modify = True
    export = True
    subdivide_all = False
    insets = 0
    subdivides = 10

    title = "0  Dummy_Si_O2_cond_Si\n"

    if dummy:
        idt_height = 1

        elec_cnt = 4
        elec_length = 50
        elec_width = 10
        elec_sep = 20

        base_length = 30

        substrate_length = 200
        substrate_width = 200
        si_o2_height = 4
        min_value = idt_height
        si_height = 4

    if not dummy:
        # all entries resemble micrometer scale
        # results must be multiplied by 10^-6 for real values
        idt_height = 0.11

        elec_cnt = 21
        elec_length = 139
        elec_width = 1.35
        elec_sep = 1.65

        base_length = 20.41

        # idt_structure_height = 0.110

        si_o2_height = 2
        min_value = idt_height
        si_height = 10

    data_class = BlenderIDTonSiO2AndSiStruct(
        elec_length=elec_length,
        elec_width=elec_width,
        elec_sep=elec_sep,
        elec_cnt=elec_cnt,
        base_length=base_length,
        idt_height=idt_height,
        si_o2_height=si_o2_height,
        si_height=si_height
    )

    object_data_dict = data_class.blender_dict
    # Material - file_name Dictionary

    mat_file_name_dict = {
        "Conductor Air Upper": "idt_upper_cond_air.txt",
        "Conductor Air Lower": "idt_lower_cond_air.txt",
        "Dielectric": "dielectric.txt",
        "Conductor Dielectric Upper": "idt_upper_cond_diel.txt",
        "Conductor Dielectric Lower": "idt_lower_cond_diel.txt",
        "Si Top": "si_top.txt",
        "Si": "si_rest.txt"
    }

    material_dict = create_materials(mat_file_name_dict)
    for name, tpl in object_data_dict.items():
        load_blender_data(name, tpl, material_dict)

    if modify:
        blender_perform_modification(
            number_subdivides=subdivides,
            number_insets=insets,
            min_relative_thickness=min_value,
            subdivide_all=subdivide_all
        )

    # This should become a function
    if export:
        blender_export_to_fastcap(mat_file_name_dict, title=title)

        exit()

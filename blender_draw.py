from faces import GeomFace, GeomFaceList
from structures import Cuboid, LowerBaseStructure, UpperBaseStructure, IdtLowerStructure, IdtUpperStructure, SiO2Layer
import numpy as np
import bpy
import time

width, length, height = 1.0, 1.0, 1.0

# zero = np.array([0.0, 0.0, 0.0])
# one = np.array([0.0, length, 0.0])
# two = np.array([width, length, 0.0])
# three = np.array([width, 0.0, 0.0])
# obj = GeomFace(vertice_cnt=4, corners=[zero, one, two, three])
#
# dummy_list = []
# for i in range(3):
#     dummy_list.append(obj.copy() + np.array([i * 1.0, 0.0, 0.0]))
#
# assert len(dummy_list) == 3
#
# face_list = GeomFaceList(dummy_list)
#
# vertices, faces = face_list.prep_blender_data()

# cube = Cuboid(length=length, width=width, height=height)
#
# vertices, faces = cube.prep_blender_data()


def list_electrode_prep_blender_data(cuboid_list, face_name):

    exp_vertices =[]
    exp_faces = []
    start_index = 0
    for cuboid in cuboid_list:
        face_obj = getattr(cuboid, face_name)
        vertices, face = face_obj.prep_blender_data(start_index)
        exp_vertices.extend(vertices)
        exp_faces.append(face)
        start_index += 4

    return exp_vertices, exp_faces


elec_width = 1
elec_sep = 2
elec_cnt = 2
length *= 3
elec_length = 5
width = elec_cnt * elec_width + (elec_cnt-1)*(elec_width+2*elec_sep)
height *= 1

modify = True
export = True
subdivide_all = True
insets = 2
subdivides = 2
title = "0  NO_SUB_DIVS\n"

# base_lower = LowerBaseStructure(elec_width=elec_width, elec_sep=elec_sep, elec_cnt=elec_cnt,
#                                 length=length, width=width, height=height,
#                                 omit_faces=["bottom_face"])

# base_upper = UpperBaseStructure(elec_width=elec_width, elec_sep=elec_sep, elec_cnt=elec_cnt-1,
#                                length=length, width=width, height=height,
#                                omit_faces=["bottom_face"])

idt_lower = IdtLowerStructure(elec_length=elec_length, elec_width=elec_width, elec_sep=elec_sep,
                              elec_cnt=elec_cnt, base_length=length, height=height)

idt_upper = IdtUpperStructure(elec_length=elec_length, elec_width=elec_width, elec_sep=elec_sep,
                              elec_cnt=elec_cnt-1, base_length=length, height=height)


si_o2 = SiO2Layer(structure_length=elec_sep + 2* idt_upper.base_length + elec_length,
                  structure_width=idt_upper.base_width,
                  length=20,
                  width=20,
                  height=6)


idt_structure_length = elec_sep + 2 * idt_upper.base_length + elec_length
idt_structure_width = idt_lower.base_width

# Alignment translation to position the IDT structure in the middle of the Substrate

align_idt_vector = np.array([0.5*(20 - idt_structure_width),
                             0.5 * (20 - idt_structure_length),
                             0.0])
idt_upper + np.array([0.0, elec_length + elec_sep + idt_lower.base_length, 0.0])
idt_lower + align_idt_vector
idt_upper + align_idt_vector

si_o2 - np.array([0.0, 0.0, 6.0])

# To be simplified after succesful simulation

lower_elec_data = list_electrode_prep_blender_data(idt_lower.electrodes, "bottom_face")

upper_elec_data = list_electrode_prep_blender_data(idt_upper.electrodes, "bottom_face")

lower_base_bottom_verts, lower_face = idt_lower.base.bottom_face.prep_blender_data()
upper_base_bottom_vaerts, upper_face = idt_upper.base.bottom_face.prep_blender_data()

upper_base_bottom_data = (upper_base_bottom_vaerts, (upper_face,))
lower_base_bottom_data = (lower_base_bottom_verts, (lower_face,))

upper_data = idt_upper.prep_blender_data()

lower_data = idt_lower.prep_blender_data()


diel_upper_data = idt_upper.diel_faces.prep_blender_data()

diel_lower_data = idt_lower.diel_faces.prep_blender_data()

sio2_data = si_o2.prep_blender_data()

objects = {
    "IDT_UPPER": upper_data,
    "IDT_LOWER": lower_data,
    "BASE_BOTTOM_UPPER": upper_base_bottom_data,
    "BASE_BOTTOM_LOWER": lower_base_bottom_data,
    "ELEC_UPPER": upper_elec_data,
    "ELEC_LOWER": lower_elec_data,
    "DIEL_UPPER": diel_upper_data,
    "DIEL_LOWER": diel_lower_data,
    "SI_O2": sio2_data
}

# Material - file_name Dictionary

mat_file_name_dict = {
    "Conductor Air Upper": "idt_upper_cond_air.txt",
    "Conductor Air Lower": "idt_lower_cond_air.txt",
    "Dielectric": "dielectric.txt",
    "Conductor Dielectric Upper": "idt_upper_cond_diel.txt",
    "Conductor Dielectric Lower": "idt_lower_cond_diel.txt"
}

mat_one = bpy.data.materials.new(name="Conductor Air Upper")
mat_one.diffuse_color = (0.0, 0.0, 1.0)  # Blue
mat_two = bpy.data.materials.new(name="Conductor Air Lower")
mat_two.diffuse_color = (0.0, 0.5, 0.5)

mat_three = bpy.data.materials.new(name="Conductor Dielectric Upper")
mat_three.diffuse_color = (1.0, 0.0, 0.0)  # Red
mat_four = bpy.data.materials.new(name="Conductor Dielectric Lower")
mat_four.diffuse_color = (0.5, 0.5, 0.0)

mat_five = bpy.data.materials.new(name="Dielectric")
mat_five.diffuse_color = (0.0, 1.0, 0.0)  # Green

for name, tpl in objects.items():
    mat = mat_two

    if name.startswith("IDT"):
        if name.endswith("UPPER"):
            mat = mat_one
        else:
            mat = mat_two

    elif name.startswith("ELEC") or name.startswith("BASE_BOTTOM"):
        if name.endswith("UPPER"):
            mat = mat_three
        else:
            mat = mat_four
    else:
        mat = mat_five

    mesh_data = bpy.data.meshes.new(name)
    mesh_data.from_pydata(tpl[0], [], tpl[1])

    obj = bpy.data.objects.new(name, mesh_data)
    obj.data.materials.append(mat)
    bpy.context.scene.objects.link(obj)

    bpy.context.scene.objects.active = obj



if modify:
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.join()

    bpy.ops.object.mode_set(mode="EDIT")


    for i in range(insets):
        bpy.ops.mesh.inset()

    # only the las insets get divided

    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.remove_doubles()
    if not subdivide_all:
        bpy.ops.mesh.select_all(action="DESELECT")
    if subdivides:
        bpy.ops.mesh.subdivide(number_cuts=subdivides)

    bpy.ops.mesh.separate(type="MATERIAL")
    bpy.ops.object.mode_set(mode="OBJECT")

bpy.ops.object.select_all(action="DESELECT")

# obj = bpy.context.scene.objects[0].data
#
# print(bpy.context.scene.objects[0].data.materials[0].name)

# This should become a function
# print([(x.name, list(x.data.materials), len(x.data.polygons)) for x in bpy.context.scene.objects])
if export:
    for obj in bpy.context.scene.objects:
        data = obj.data
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

        exp_str += "N  1  {}".format(data.materials[0].name.split(" ")[-1])
        bpy.ops.object.select_pattern(pattern=obj.name)
        bpy.ops.object.delete(use_global=True)

        # we know that the objects only consist of one material
        file_name = mat_file_name_dict[data.materials[0].name]
        with open(file_name, "a") as f:
            f.write(exp_str)

# print([x for x in bpy.context.scene.objects[0].data.polygons[:2]])
# vertices_diel, faces_diel = idt_lower.diel_faces.prep_blender_data()
#
# vertices, faces = idt_lower.prep_blender_data()

# vertices_diel, faces_diel = idt_upper.diel_faces.prep_blender_data()
# vertices, faces = idt_upper.prep_blender_data()


# idt_upper = IdtUpperStructure(elec_length=elec_length, elec_width=elec_width, elec_sep=elec_sep,
#                               elec_cnt=elec_cnt-1, base_length=length, height=height)
#
# vertices, faces = idt_upper.prep_blender_data()

# mesh_data = bpy.data.meshes.new("IDT")
# mesh_data.from_pydata(vertices, [], faces)
#
# obj = bpy.data.objects.new("IDT", mesh_data)
# mat = bpy.data.materials.new(name="Conductor")
# obj.data.materials.append(mat)
# bpy.context.scene.objects.link(obj)

# mesh_data_diel = bpy.data.meshes.new("DIEL")
# mesh_data_diel.from_pydata(vertices_diel, [], faces_diel)
#
# obj_diel = bpy.data.objects.new("DIEL", mesh_data_diel)
# mat = bpy.data.materials.new(name="Dielectric")
# obj_diel.data.materials.append(mat)
# bpy.context.scene.objects.link(obj_diel)


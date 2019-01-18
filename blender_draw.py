from faces import GeomFace, GeomFaceList
from structures import Cuboid, LowerBaseStructure, UpperBaseStructure, IdtLowerStructure
import numpy as np
import bpy

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

elec_width = 1
elec_sep = 3
elec_cnt = 2
length *= 3
elec_length = 5
width = elec_cnt * elec_width + (elec_cnt-1)*(elec_width+2*elec_sep)
height *= 1

# base_lower = LowerBaseStructure(elec_width=elec_width, elec_sep=elec_sep, elec_cnt=elec_cnt,
#                                 length=length, width=width, height=height,
#                                 omit_faces=["bottom_face"])

# base_upper = UpperBaseStructure(elec_width=elec_width, elec_sep=elec_sep, elec_cnt=elec_cnt-1,
#                                length=length, width=width, height=height,
#                                omit_faces=["bottom_face"])

idt_lower = IdtLowerStructure(elec_length=elec_length, elec_width=elec_width, elec_sep=elec_sep,
                              elec_cnt=elec_cnt, base_length=length, height=height)

vertices_diel, faces_diel = idt_lower.diel_faces.prep_blender_data()

vertices, faces = idt_lower.prep_blender_data()

mesh_data = bpy.data.meshes.new("IDT")
mesh_data.from_pydata(vertices, [], faces)

obj = bpy.data.objects.new("IDT", mesh_data)
mat = bpy.data.materials.new(name="Conductor")
obj.data.materials.append(mat)
bpy.context.scene.objects.link(obj)

mesh_data_diel = bpy.data.meshes.new("DIEL")
mesh_data_diel.from_pydata(vertices_diel, [], faces_diel)

obj_diel = bpy.data.objects.new("DIEL", mesh_data_diel)
mat = bpy.data.materials.new(name="Dielectric")
obj_diel.data.materials.append(mat)
bpy.context.scene.objects.link(obj_diel)


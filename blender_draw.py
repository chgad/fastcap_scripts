from faces import GeomFace, GeomFaceList
from structures import Cuboid
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

cube = Cuboid(length=length, width=width, height=height)

vertices, faces = cube.prep_blender_data()

mesh_data = bpy.data.meshes.new("Face 1")
mesh_data.from_pydata(vertices, [], faces)

obj = bpy.data.objects.new("Object 1", mesh_data)
mat = bpy.data.materials.new(name="Material 1")
obj.data.materials.append(mat)
bpy.context.scene.objects.link(obj)

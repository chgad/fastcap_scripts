# This Script creates a simple Platecapacitor
# Usecase of this script : Check if structures.py can reproduce the results provided
# by the FastCap Docs.

from structures import IdtLowerStructure, IdtUpperStructure, SiO2Layer, FastCapCuboid
import numpy as np

import bpy
# All lengths provided in meter

export = False
visualize = True

lower_plate = FastCapCuboid(length=1, width=1, height=0.001, omit_faces=["top_face"])
upper_plate = FastCapCuboid(length=1, width=1, height=0.001, omit_faces=["bottom_face"]) + np.array([0.0, 0.0, 0.101])

dielectric = FastCapCuboid(length=1, width=1, height=0.1, omit_faces=["top_face", "bottom_face"])
dielectric + np.array([0.0, 0.0, 0.001])


# Export to Files
if export:
    upper_plate.export_to_file("upper_plate_capacitor.txt")
    lower_plate.export_to_file("lower_plate_capacitor.txt")

    dielectric.export_to_file("plate_capacitor_dielectric.txt")

    with open("upper_plate_capacitor_diel.txt","a") as f:
        f.write(upper_plate.bottom_face.prep_export_string())

    with open("lower_plate_capacitor_diel.txt","a") as f:
        f.write(lower_plate.top_face.prep_export_string())


if visualize:
    objects = {
        "UPPER PLATE": upper_plate.prep_blender_data(),
        #    "UPPER BOUND": upper_plate.bottom_face.prep_blender_data(),
        "LOWER PLATE": lower_plate.prep_blender_data(),
        #    "LOWER BOUND": lower_plate.prep_blender_data(),
        "DIELECTRIC": dielectric.prep_blender_data()

    }

    mat_one = bpy.data.materials.new(name="Conductor Air Upper")
    mat_one.diffuse_color = (0.0, 0.0, 1.0)

    mat_five = bpy.data.materials.new(name="Dielectric")
    mat_five.diffuse_color = (0.0, 1.0, 0.0)  # Green

    for name, tpl in objects.items():

        mat = mat_one

        if name.startswith("DIELECTRIC"):
            mat = mat_five

        mesh_data = bpy.data.meshes.new(name)
        mesh_data.from_pydata(tpl[0], [], tpl[1])

        obj = bpy.data.objects.new(name, mesh_data)
        obj.data.materials.append(mat)
        bpy.context.scene.objects.link(obj)

        bpy.context.scene.objects.active = obj
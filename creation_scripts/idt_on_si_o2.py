# This Script creates a  IDT-Structure on a Silicon Chips with a Silicondioxide layer between the conducting
# IDT Part and the Conducting Silicon
#
import sys
sys.path.append('../..')
from os.path import isfile
from os import remove
from structures import IdtLowerStructure, IdtUpperStructure, SiO2Layer, FastCapCuboid

import numpy as np

import bpy
# Files to store the IDT-to-Air interfaces

idt_lower_filename = "creation_scripts/list_files/idt_lower_cond_air.txt"
idt_upper_filename = "creation_scripts/list_files/idt_upper_cond_air.txt"

# Files to store the IDT-to-SiO_2 interfaces

idt_lower_diel_filename = "creation_scripts/list_files/idt_lower_cond_diel.txt"
idt_upper_diel_filename = "creation_scripts/list_files/idt_upper_cond_diel.txt"

# Files to store the SiO_2-to-Air interfaces

si_o2_filename = "creation_scripts/list_files/si_o2.txt"

# File to store the Si-to-Air interfaces

si_cond_filename = "creation_scripts/list_files/si_substrate_cond_air.txt"

# File to store the Si-to-SiO_2 interfaces

si_diel_filename = "creation_scripts/list_files/si_substrate_cond_diel.txt"

file_list = [idt_lower_filename,
             idt_upper_filename,
             idt_lower_diel_filename,
             idt_upper_diel_filename,
             si_o2_filename,
             si_cond_filename,
             si_diel_filename]

# Sanitycheck wether any oth the provided Files allready exists and prompt
# user action if so. Existing files will be overwritten, otherwise the script exits.

# if any(map(isfile, file_list)):
#     print("One or more of the provided files allready exist.")
#     answer = input("Do you want to go on (existing files will be overwritten) [Y/n]:")
#     if answer.lower() == "y":
#         for f in file_list:
#             try:
#                 remove(f)
#             except FileNotFoundError:
#                 pass
#
#     else:
#         print("Please check which file allready exists and change the Input")
#         print("Exiting......")
#         exit()
#

# All lengths provided in Micro meters
# All parameters concerning the IDT structure
electrode_count = 41
electrode_length = 139
electrode_width = 1.35
electrode_sep = 1.65

base_length = 20.41

idt_structure_height = 0.110
# idt_structure_length = 0.0
# idt_structure_width = 0.0

# All parameters concerning the overall substrate
substrate_length = 500  # 10000
substrate_width = 500  # 10000

# SiO_2 layer height
si_o2_height = 0.2

# Si layer height
si_height = 600

# Creation of the IDT Structure

idt_lower = IdtLowerStructure(elec_length=electrode_length, elec_width=electrode_width, elec_sep=electrode_sep,
                              elec_cnt=electrode_count, base_length=base_length, height=idt_structure_height)

idt_upper = IdtUpperStructure(elec_length=electrode_length, elec_width=electrode_width, elec_sep=electrode_sep,
                              elec_cnt=electrode_count-1, base_length=base_length, height=idt_structure_height)
idt_upper + np.array([0.0, electrode_length + electrode_sep + base_length, 0.0])

idt_structure_length = 2 * base_length + electrode_length + electrode_sep
idt_structure_width = idt_lower.base_width

# Alignment translation to position the IDT structure in the middle of the Substrate

align_idt_vector = np.array([0.5*(substrate_width - idt_structure_width),
                             0.5 * (substrate_length - idt_structure_length),
                             0.0])

idt_lower + align_idt_vector
idt_upper + align_idt_vector

# Creation of the SiO_2 layer

si_o2_layer = SiO2Layer(structure_length=idt_structure_length, structure_width=idt_structure_width,
                        length=substrate_length, width=substrate_length, height=si_o2_height,
                        omit_faces=[])

# Creation of Si layer

si_layer = FastCapCuboid(length=substrate_length, width=substrate_width, height=si_height, omit_faces=["top_face"])

# Positioning of Si and SiO_2 layer

si_o2_layer - np.array([0.0, 0.0, si_o2_height])
si_layer - np.array([0.0, 0.0, si_o2_height + si_height])

# Export part

# Export IDT structure
idt_lower.export_to_file(cond_file_name=idt_lower_filename, diel_file_name=idt_lower_diel_filename)
idt_upper.export_to_file(cond_file_name=idt_upper_filename, diel_file_name=idt_upper_diel_filename)

# Export SiO_2-to-Air interfaces betwen the Electrodes of the IDT structure

# diel_faces_string = ""
# diel_faces_string += idt_lower.diel_faces.prep_export_string()
# diel_faces_string += idt_upper.diel_faces.prep_export_string()
#
# with open(si_o2_filename, "a") as f:
#     f.write(diel_faces_string)
#
# # Export SiO_2 layer
#
# si_o2_layer.export_to_file(file_name=si_o2_filename)
#
# # Export Si-to-Air interfaces
#
# si_layer.export_to_file(file_name=si_cond_filename)
#
# # Export Si-to-SiO_2 interfaces
#
# with open(si_diel_filename, "a") as f:
#     f.write(si_layer.top_face.prep_export_string())

# Visualization with Blender


upper_data = idt_upper.prep_blender_data()

upper_electrode_data = idt_upper.electrodes[0].prep_blender_data()

lower_data = idt_lower.prep_blender_data()

lower_electrode_data = idt_lower.electrodes[0].prep_blender_data()


diel_upper_data = idt_upper.diel_faces.prep_blender_data()

diel_lower_data = idt_lower.diel_faces.prep_blender_data()

sio2_data = si_o2_layer.prep_blender_data()

objects = {
    # "IDT_UPPER_ELECTRODES": upper_electrode_data,
    # "IDT_LOWER_ELECTRODES": lower_electrode_data,
    "IDT_UPPER": upper_data,
    "IDT_LOWER": lower_data,
    "DIEL_UPPER": diel_upper_data,
    "DIEL_LOWER": diel_lower_data,
    "SI_O2": sio2_data
}

mat_one = bpy.data.materials.new(name="Conductor")
mat_one.diffuse_color = (0.0, 0.0, 1.0)
mat_two = bpy.data.materials.new(name="Dielectric")
mat_two.diffuse_color = (0.0, 1.0, 0.0)

for name, tpl in objects.items():
    mat = mat_two

    if name.startswith("IDT"):
        mat = mat_one

    mesh_data = bpy.data.meshes.new(name)
    mesh_data.from_pydata(tpl[0], [], tpl[1])

    obj = bpy.data.objects.new(name, mesh_data)
    obj.data.materials.append(mat)
    bpy.context.scene.objects.link(obj)

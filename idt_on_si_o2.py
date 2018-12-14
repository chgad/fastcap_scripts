from os.path import isfile
from os import remove
from structures import IdtLowerStructure, IdtUpperStructure, SiO2Layer, FastCapCuboid

import numpy as np

idt_cond_filename = "idt_conductor_air.txt"
cond_diel_filename = "conductor_diel.txt"
si_o2_filename = "si_o2.txt"
si_cond_filename = "si_substrate_conductor.txt"

file_list = [idt_cond_filename, cond_diel_filename, si_o2_filename, si_cond_filename]

if any(map(isfile, file_list)):
    print("One or more of the provided files allready exist.")
    answer = input("Do you want to go on (existing files will be overwritten) [Y/n]:")
    if answer.lower() == "y":
        for f in file_list:
            try:
                remove(f)
            except FileNotFoundError:
                pass

    else:
        print("Please check which file allready exists and change the Input")
        print("Exiting......")
        exit()

electrode_count = 5
electrode_length = 7.0
electrode_width = 1.0
electrode_sep = 2.0

base_length = 5.0

idt_structure_height = 3.0
# idt_structure_length = 0.0
# idt_structure_width = 0.0

substrate_length = 150.0
substrate_width = 150.0

si_o2_height = 2.0

si_height = 5.0

idt_lower = IdtLowerStructure(elec_length=electrode_length, elec_width=electrode_width, elec_sep=electrode_sep,
                              elec_cnt=electrode_count, base_length=base_length, height=idt_structure_height)

idt_upper = IdtUpperStructure(elec_length=electrode_length, elec_width=electrode_width, elec_sep=electrode_sep,
                              elec_cnt=electrode_count-1, base_length=base_length, height=idt_structure_height)
idt_upper + np.array([0.0, electrode_length + electrode_sep + base_length, 0.0])

idt_structure_length = 2 * base_length + electrode_length + electrode_sep
idt_structure_width = idt_lower.base_width

align_idt_vector = np.array([0.5*(substrate_width - idt_structure_width),
                             0.5 * (substrate_length - idt_structure_length),
                             0.0])

idt_lower + align_idt_vector
idt_upper + align_idt_vector

si_o2_layer = SiO2Layer(structure_length=idt_structure_length, structure_width=idt_structure_width,
                        length=substrate_length, width=substrate_length, height=si_o2_height,
                        omit_faces=["bottom_face", ])

si_layer = FastCapCuboid(length=substrate_length, width=substrate_width, height=si_height, omit_faces=["top_face"])

si_o2_layer - np.array([0.0, 0.0, si_o2_height])
si_layer - np.array([0.0, 0.0, si_o2_height + si_height])

idt_lower.export_to_file(cond_file_name=idt_cond_filename, diel_file_name=cond_diel_filename)
idt_upper.export_to_file(cond_file_name=idt_cond_filename, diel_file_name=cond_diel_filename)

diel_faces_string = ""
diel_faces_string += idt_lower.diel_faces.prep_export_string()
diel_faces_string += idt_upper.diel_faces.prep_export_string()
with open(si_o2_filename, "a") as f:
    f.write(diel_faces_string)

si_o2_layer.export_to_file(file_name=si_o2_filename)

si_layer.export_to_file(file_name=si_cond_filename)
with open(cond_diel_filename, "a") as f:
    f.write(si_layer.top_face.prep_export_string())

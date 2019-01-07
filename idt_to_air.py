# This script creates an IDT-structure which is only
# exposed to air sourrounding it
#
#

from os.path import isfile
from os import remove
from structures import IdtLowerStructure, IdtUpperStructure, SiO2Layer, FastCapCuboid
import numpy as np

# All lengths provided in Micro meters
# All parameters concerning the IDT structure

electrode_count = 41
electrode_length = 139
electrode_width = 1.35
electrode_sep = 1.65

base_length = 20.41

idt_structure_height = 0.110

# Creation of the IDT-structure

idt_lower = IdtLowerStructure(elec_length=electrode_length, elec_width=electrode_width, elec_sep=electrode_sep,
                              elec_cnt=electrode_count, base_length=base_length, height=idt_structure_height)

idt_upper = IdtUpperStructure(elec_length=electrode_length, elec_width=electrode_width, elec_sep=electrode_sep,
                              elec_cnt=electrode_count-1, base_length=base_length, height=idt_structure_height)

# Positioning of the upper IDT-part
idt_upper + np.array([0.0, electrode_length + electrode_sep + base_length, 0.0])

# Files for export
dummy_diel_file = "dummy_diel.txt"
file_name_upper = "upper_idt_air.txt"
file_name_lower = "lower_idt_air.txt"

# Normally the Bottom Faces of the IDT-base are omitted for the Conductor-Air exports

idt_lower.base.omit_faces = []
idt_upper.base.omit_faces = []

# Normally the Bottom faces and front-/backfaces of the Electrodes are omitted for the Conductor-Air exports

for elec in idt_lower.electrodes:
    elec.omit_faces = ["front_face"]

for elec in idt_upper.electrodes:
    elec.omit_faces = ["back_face"]

# Export to Files

idt_lower.export_to_file(cond_file_name=file_name_lower, diel_file_name=dummy_diel_file)
idt_upper.export_to_file(cond_file_name=file_name_upper, diel_file_name=dummy_diel_file)



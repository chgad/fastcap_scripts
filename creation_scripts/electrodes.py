# This script Creates the IDT-structure as in idt_on_si_o2.py but only exports
# the electrodes to test if Fastcap produces some reasonable output
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

# Positioning of the Upper IDT-structure
idt_upper + np.array([0.0, electrode_length + electrode_sep + base_length, 0.0])

# Files to export Upper/Lower electrodes
file_name_upper = "upper_electrodes.txt"
file_name_lower = "lower_electrodes.txt"

# Export only electrodes

for elec in idt_upper.electrodes:
    elec.omit_faces = []
    elec.export_to_file(file_name_upper)

for elec in idt_lower.electrodes:
    elec.omit_faces = []
    elec.export_to_file(file_name_lower)

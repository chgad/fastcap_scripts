# This Script creates a simple Platecapacitor
# Usecase of this script : Check if structures.py can reproduce the results provided
# by the FastCap Docs.

from structures import IdtLowerStructure, IdtUpperStructure, SiO2Layer, FastCapCuboid
import numpy as np

# All lengths provided in meter

upper_plate = FastCapCuboid(length=1, width=1, height=0.001)
lower_plate = upper_plate.copy() + np.array([0.0, 0.0, 0.101])

# Export to Files

upper_plate.export_to_file("upper_plate_capacitor.txt")
lower_plate.export_to_file("lower_plate_capacitor.txt")

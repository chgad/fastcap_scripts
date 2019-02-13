# This Script creates a simple Platecapacitor
# Usecase of this script : Check if structures.py can reproduce the results provided
# by the FastCap Docs.

from structures import IdtLowerStructure, IdtUpperStructure, SiO2Layer, FastCapCuboid
import numpy as np

# All lengths provided in meter

lower_plate = FastCapCuboid(length=1, width=1, height=0.001, omit_faces=["top_face"])
upper_plate = FastCapCuboid(length=1, width=1, height=0.001, omit_faces=["bottom_face"])

dielectric = FastCapCuboid(length=1, width=1, height=0.1, omit_faces=["top_face", "bottom_face"])
dielectric + np.array([0.0, 0.0, 0.001])


# Export to Files

upper_plate.export_to_file("upper_plate_capacitor.txt")
lower_plate.export_to_file("lower_plate_capacitor.txt")

dielectric.export_to_file("plate_capacitor_dielectric.txt")

with open("upper_plate_capcaitor_diel.txt","a") as f:
    f.write(upper_plate.bottom_face.prep_export_string())

with open("lowerer_plate_capcaitor_diel.txt","a") as f:
    f.write(lower_plate.top_face.prep_export_string())

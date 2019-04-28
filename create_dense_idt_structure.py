from create_idt_structure_classes import BlenderIDTonSiO2struct
from blender_draw import create_materials, load_blender_data, blender_perform_modification, blender_export_to_fastcap
import argparse
import sys

argv = sys.argv
argv = argv[argv.index("--") + 1:]


elec_cnt = int(argv[0])
subdivides = 15
insets = 0
subdivide_all = False

idt_height = 0.11

elec_length = 139
elec_width = 1.35
elec_sep = 1.65

base_length = 20.41

# idt_structure_height = 0.110

si_o2_height = 2
min_value = idt_height

mat_file_name_dict = {
    "Conductor Air Upper": "approx_capacitance_per_elec/content_files/idt_upper_cond_air.txt",
    "Conductor Air Lower": "approx_capacitance_per_elec/content_files/idt_lower_cond_air.txt",
    "Dielectric": "approx_capacitance_per_elec/content_files/dielectric.txt",
    "Conductor Dielectric Upper": "approx_capacitance_per_elec/content_files/idt_upper_cond_diel.txt",
    "Conductor Dielectric Lower": "approx_capacitance_per_elec/content_files/idt_lower_cond_diel.txt",
}
title = "0  Dummy_Only_top_diel\n"

data_class = BlenderIDTonSiO2struct(
    elec_length=elec_length,
    elec_width=elec_width,
    elec_sep=elec_sep,
    elec_cnt=elec_cnt,
    base_length=base_length,
    idt_height=idt_height,
    si_o2_height=si_o2_height,
)

object_data_dict = data_class.blender_dict

material_dict = create_materials(mat_file_name_dict)

for name, tpl in object_data_dict.items():
    load_blender_data(name, tpl, material_dict)

blender_perform_modification(number_subdivides=subdivides, number_insets=insets, min_relative_thickness=min_value,
                             subdivide_all=subdivide_all)
blender_export_to_fastcap(mat_file_name_dict, title)
exit()
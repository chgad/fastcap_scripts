from create_idt_structure import create_idt_structure, prepare_visualization_data
from blender_draw import create_materials, load_blender_data, blender_perform_modification, blender_export_to_fastcap
import argparse
import sys
argv = sys.argv
argv = argv[argv.index("--") + 1:]

ap = argparse.ArgumentParser()



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
    "Conductor Air Upper": "test_dir/content_files/idt_upper_cond_air.txt",
    "Conductor Air Lower": "test_dir/content_files/idt_lower_cond_air.txt",
    "Dielectric": "test_dir/content_files/dielectric.txt",
    "Conductor Dielectric Upper": "test_dir/content_files/idt_upper_cond_diel.txt",
    "Conductor Dielectric Lower": "test_dir/content_files/idt_lower_cond_diel.txt",
}
title = "0  Dummy_Only_top_diel\n"

idt_structure_dict = create_idt_structure(
    elec_length=elec_length,
    elec_width=elec_width,
    elec_sep=elec_sep,
    elec_cnt=elec_cnt,
    base_length=base_length,
    idt_height=idt_height,
    si_o2_height=si_o2_height,
)

object_data_dict = prepare_visualization_data(idt_structure_dict)

material_dict = create_materials(mat_file_name_dict)

for name, tpl in object_data_dict.items():
    load_blender_data(name, tpl, material_dict)

blender_perform_modification(number_subdivides=subdivides, number_insets=insets, min_relative_thickness=min_value,
                             subdivide_all=subdivide_all)
blender_export_to_fastcap(mat_file_name_dict, title)
exit()

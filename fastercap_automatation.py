import subprocess

elec_cnt_start = 2
elec_cnt_stop = 25


for elec_cnt in range(elec_cnt_start, elec_cnt_stop + 1):
    subprocess.run(["blender", "-b", "--python", "create_dense_idt_structure.py", "--", "{}".format(elec_cnt)])

    subprocess.run(
        [
            "/bin/bash", "-i", "-c",
            "fastercap -b approx_capacitance_per_elec/content_files/idt_on_si_o2.lst -a0.0 > approx_capacitance_per_elec/test_file_elec_cnt{:02d}.txt".format(elec_cnt)
         ]
                   )
    subprocess.run(["rm approx_capacitance_per_elec/content_files/*.txt", ], shell=True)


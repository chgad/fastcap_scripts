import subprocess

elec_cnt_start = 6
elec_cnt_stop = 25
file_number = 1

for elec_cnt in range(elec_cnt_start, elec_cnt_stop + 1):
    subprocess.run(["blender", "-b", "--python", "create_dense_idt_structure.py", "--", "{}".format(elec_cnt)])

    subprocess.run(
        [
            "/bin/bash", "-i", "-c", "fastercap -b test_dir/content_files/idt_on_si_o2.lst > test_dir/test_file_No{:02d}.txt".format(file_number)
         ]
                   )
    subprocess.run(["rm test_dir/content_files/*.txt", ], shell=True)
    file_number += 1

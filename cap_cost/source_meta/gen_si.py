
import os

from os.path import join as pjoin

output_folder = 'docs'
full_text = ""

with open(os.path.join(output_folder,'SI.md'), 'w', encoding='utf-8') as f:

    fp = os.path.join(output_folder, 'SM_type_source_counts.md')
    with open(fp,'r', encoding='utf-8') as f_read:
        r_text = f_read.read()

    f.write("# Storage Medium Type Source Counts\n")
    f.write(r_text)

    # full_text = full_text + r_text

    fp = os.path.join(output_folder, 'README_combined.md')
    with open(fp,'r', encoding='utf-8') as f_read:
        r_text = f_read.read()

    f.write("# Detailed Source Information\n")
    f.write(r_text)
    # full_text = full_text + r_text

    # f.write(full_text)



import os
os.system('pandoc -o {}/SI.docx -f markdown -t docx {}/SI.md'.format(output_folder,output_folder))
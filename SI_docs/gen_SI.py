
from os.path import join as pjoin
import os
import shutil
import re

from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

if not os.path.exists('output'): os.mkdir('output')

def read_md(f_out, fp):
    with open(pjoin(REPO_DIR,fp), 'r', encoding='utf-8') as f:
        SI_text = f.read()

    SI_text = SI_text.replace(r'../../', r'../')
    SI_text = SI_text + "\n\n"
    return SI_text 

with open('output/SI.md', 'w', encoding='utf-8') as f_out:

    SI_text = read_md(f_out, r'SI_docs\md_written\intro.md')
    f_out.write(SI_text)

    SI_text = read_md(f_out, r'SI_docs\md_written\data_flow_desc.md')
    f_out.write(SI_text)

    SI_text = read_md(f_out, r'SI_docs\md_written\calculation_methods.md')
    f_out.write(SI_text)

    SI_text = read_md(f_out, r'SI_docs\md_written\volumetric_costs.md')
    f_out.write(SI_text)

    SI_text = read_md(f_out, r'SI_docs\md_generated\mat_data_vol.md')
    f_out.write(SI_text)

    f_out.write('# Source Information\n\n')
    SI_text = read_md(f_out, r'SI_docs\md_written\source_info_desc.md')
    f_out.write(SI_text)

    SI_text = read_md(f_out, r'SI_docs\md_generated\SM_type_source_counts.md')
    f_out.write(SI_text)

    # f_out.write("## Specific source detailed info\n\n")
    SI_text = read_md(f_out, r'SI_docs\md_generated\README_combined.md')
    SI_text = re.sub(r'(#+)', r'\1#', SI_text)
    f_out.write(SI_text)

    f_out.write("# Viable Storage media\n\n")
    SI_text = read_md(f_out, r'SI_docs\md_written\viable_SM_desc.md')
    f_out.write(SI_text)

    SI_text = read_md(f_out, r'SI_docs\md_generated\SM_viable.md')
    f_out.write(SI_text)

    SI_text = read_md(f_out,     fp =  r'SI_docs\md_written\supp_figures.md')
    f_out.write(SI_text)


# os.system("cd output")
# os.system("pandoc -o output/SI.docx -f markdown -t docx output/SI.md")

output_folder = 'output'
import os
os.system('pandoc -o {}/SI.docx -f markdown -t docx {}/SI.md --reference-doc reference_doc.docx'.format(output_folder,output_folder))


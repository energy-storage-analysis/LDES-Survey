
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

with open('output/SI_md.md', 'w', encoding='utf-8') as f_out:

    SI_text = read_md(f_out, r'SI_docs\md_written\intro.md')
    f_out.write(SI_text)

    SI_text = read_md(f_out, r'SI_docs\md_written\volumetric_costs.md')
    f_out.write(SI_text)

    SI_text = read_md(f_out, r'SI_docs\md_generated\mat_data_vol.md')
    f_out.write(SI_text)

    f_out.write('# Source Information\n\n')
    SI_text = read_md(f_out, r'SI_docs\md_written\source_info_desc.md')
    f_out.write(SI_text)

    SI_text = read_md(f_out, r'SI_docs\md_generated\source_list.md')
    f_out.write(SI_text)

    SI_text = read_md(f_out, r'SI_docs\md_generated\dataset_counts.md')
    f_out.write(SI_text)

    SI_text = read_md(f_out, r'SI_docs\md_generated\SM_type_source_counts.md')
    f_out.write(SI_text)

    # f_out.write("## Specific source detailed info\n\n")
    SI_text = read_md(f_out, r'SI_docs\md_generated\README_combined.md')
    SI_text = re.sub(r'(#+)', r'\1#', SI_text)
    f_out.write(SI_text)

    f_out.write("# Promising Storage media\n\n")
    SI_text = read_md(f_out, r'SI_docs\md_written\promising_SM_desc.md')
    f_out.write(SI_text)

    SI_text = read_md(f_out, r'SI_docs\md_generated\SM_promising.md')
    f_out.write(SI_text)


# os.system("cd output")
# os.system("pandoc -o output/SI.docx -f markdown -t docx output/SI.md")

output_folder = 'output'
import os
os.system('pandoc -o {}/SI_md.docx -f markdown -t docx {}/SI_md.md --reference-doc reference_doc.docx'.format(output_folder,output_folder))

# Error analysis 

error_table_dir = 'md_generated\error'
with open('output/error_analysis_tables.md', 'w', encoding='utf-8') as f_out:

    for fn in os.listdir(error_table_dir):
        fp = os.path.join('SI_docs', error_table_dir, fn)

        SI_text = read_md(f_out, fp)
        f_out.write(SI_text)

os.system('pandoc -o {}/SI_error_table.docx -f markdown -t docx {}/error_analysis_tables.md --reference-doc reference_doc.docx'.format(output_folder,output_folder))
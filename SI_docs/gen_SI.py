
from os.path import join as pjoin
import os
import shutil

from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

sections = {
    'Storage medium type source counts': r'SI_docs\md_generated\SM_type_source_counts.md',
    'Dataset information': r'SI_docs\md_generated\README_combined.md',
    # 'Raw SM data': r'cap_cost\analysis\table_gen\output\individual\SM_type_tables.md'
}


if not os.path.exists('output'): os.mkdir('output')

with open('output/SI.md', 'w', encoding='utf-8') as f_out:


    f_out.write('# Source Information\n\n')

    fp =  r'SI_docs\md_written\source_info_desc.md'
    with open(pjoin(REPO_DIR,fp), 'r', encoding='utf-8') as f:
        SI_text = f.read()

    f_out.write(SI_text)
    f_out.write("\n")


    f_out.write("## Storage medium type source counts\n\n")
    fp =  r'SI_docs\md_generated\SM_type_source_counts.md'
    with open(pjoin(REPO_DIR,fp), 'r', encoding='utf-8') as f:
        SI_text = f.read()
    f_out.write(SI_text)

    f_out.write("## Specific source detailed info\n\n")
    fp =  r'SI_docs\md_generated\README_combined.md'
    with open(pjoin(REPO_DIR,fp), 'r', encoding='utf-8') as f:
        SI_text = f.read()
    f_out.write(SI_text)

    
    f_out.write("# Viable Storage media\n\n")
    

    fp =  r'SI_docs\md_written\viable_SM_desc.md'
    with open(pjoin(REPO_DIR,fp), 'r', encoding='utf-8') as f:
        SI_text = f.read()

    f_out.write(SI_text)
    f_out.write("\n\n")

    fp =  r'SI_docs\md_generated\SM_viable.md'
    with open(pjoin(REPO_DIR,fp), 'r', encoding='utf-8') as f:
        SI_text = f.read()
    f_out.write(SI_text)
    f_out.write("\n\n")

    fp =  r'SI_docs\md_written\supp_figures.md'
    with open(pjoin(REPO_DIR,fp), 'r', encoding='utf-8') as f:
        SI_text = f.read()

    SI_text = SI_text.replace(r'../../', r'../')
    f_out.write(SI_text)
    f_out.write("\n\n")



# os.system("cd output")
# os.system("pandoc -o output/SI.docx -f markdown -t docx output/SI.md")


output_folder = 'output'
import os
os.system('pandoc -o {}/SI.docx -f markdown -t docx {}/SI.md --reference-doc reference_doc.docx'.format(output_folder,output_folder))



from os.path import join as pjoin
import os
import shutil

from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

sections = {
    'Dataset collection overview': r'cap_cost\datasets\README.md',
    'Storage medium type source counts': r'SI_docs\md_generated\SM_type_source_counts.md',
    'Dataset information': r'SI_docs\md_generated\README_combined.md',
    # 'Raw SM data': r'cap_cost\analysis\table_gen\output\individual\SM_type_tables.md'
}


SI_text = ""

for section, fp in sections.items():

    print(fp)

    SI_text = SI_text + "# {}".format(section) + '\n\n'
    with open(pjoin(REPO_DIR,fp), 'r', encoding='utf-8') as f:
        SI_text = SI_text + f.read()
    SI_text = SI_text + "\n\n"

    # fn = os.path.split(fp)[1]
    # shutil.copyfile(
    #     pjoin(REPO_DIR,fp),
    #     pjoin('output',fn)
    # )

if not os.path.exists('output'): os.mkdir('output')

with open('output/SI.md', 'w', encoding='utf-8') as f:
    f.write(SI_text)

# os.system("cd output")
# os.system("pandoc -o output/SI.docx -f markdown -t docx output/SI.md")


output_folder = 'output'
import os
os.system('pandoc -o {}/SI.docx -f markdown -t docx {}/SI.md --reference-doc reference_doc.docx'.format(output_folder,output_folder))
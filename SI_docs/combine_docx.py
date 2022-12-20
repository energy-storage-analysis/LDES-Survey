from docxcompose.composer import Composer
from docx import Document

master = Document("output/SI.docx")
composer = Composer(master)

doc1 = Document("docx_written/LCOS.docx")
composer.append(doc1)


doc2 = Document("docx_written/EnergyForms.docx")
composer.append(doc2)

# doc3 = Document("docx_written/References.docx")
# composer.append(doc3)

composer.save("output/SI_all.docx")
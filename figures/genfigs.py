"""
Script to generate png files from svg files in each figure's folder
"""
#%%

from cairosvg import svg2png
import os

svg_paths =[fn for fn in os.listdir('.') if fn.endswith('.svg')]

#%%

if not os.path.exists('output'): os.mkdir('output')

for fp in svg_paths:
    folder, fn = os.path.split(fp)
    fn_base, ext = os.path.splitext(fn)

    #Passsing in the file object directly causes issues with relative paths in
    #svg files, but passing in bytestring seems to work
    with open(fp, 'rb') as f:
        svg_text = f.read()

    print("Rendering {}".format(fn_base))

    fp_out = os.path.join('output',fn_base +'.png')
    svg2png(bytestring=svg_text, write_to=fp_out, dpi=600)
"""
Script to generate png files from svg files in each figure's folder

#TODO: this script is broken due to cairo seemingly needing to be in the same folder as the component png files...
"""
#%%

from cairosvg import svg2png
import os

svg_paths =[
    r'final\thermal.svg',
    r'final\ec_rhoE.svg',
    r'final\eda_Ckwh.svg',
    r'final\summary.svg'
]

#%%

if not os.path.exists('final/output'): os.mkdir('final/output')

for fp in svg_paths:
    folder, fn = os.path.split(fp)
    fn_base, ext = os.path.splitext(fn)

    fp_out = os.path.join('final','output',fn_base +'.png')
    svg2png(file_obj=open(fp, 'rb'), write_to=fp_out, dpi=600)
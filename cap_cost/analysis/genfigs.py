"""
Script to generate png files from svg files in each figure's folder

#TODO: this script is broken due to cairo seemingly needing to be in the same folder as the component png files...
"""
#%%

from cairosvg import svg2png
import os

svg_paths =[
    r'figures\thermal.svg',
    r'figures\ec_rhoE.svg',
    r'figures\eda_Ckwh.svg'
]

#%%

if not os.path.exists('figures/output'): os.mkdir('figures/output')

for fp in svg_paths:
    folder, fn = os.path.split(fp)
    fn_base, ext = os.path.splitext(fn)

    fp_out = os.path.join('figures','output',fn_base +'.png')
    svg2png(file_obj=open(fp, 'rb'), write_to=fp_out, dpi=600)
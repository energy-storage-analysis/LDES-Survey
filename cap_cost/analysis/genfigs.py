"""
Script to generate png files from svg files in each figure's folder
"""
#%%

from cairosvg import svg2png
import os

svg_paths =[
    r'thermal\fig_thermal.svg',
    r'electrochem\fig_ec_rhoE.svg'
]

#Directory needs to be changed into each folder, so we get the root analysis folder first
analysis_folder = os.getcwd()

#%%

for fp in svg_paths:
    folder, fn = os.path.split(fp)
    fn_base, ext = os.path.splitext(fn)

    os.chdir(os.path.join(analysis_folder, folder))

    svg_code = open(fn, 'r').read()
    
    fp_out = os.path.join('output',fn_base +'.png')
    svg2png(bytestring=svg_code, write_to=fp_out, dpi=600)
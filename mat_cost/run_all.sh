echo "Consolidating Data"
python "consolidate_data.py"


echo "Calculating C_kWh"
python "calc_Ckwh.py"


# echo "Generate Missing Data Info"
# python "missing_data.py"

echo "Generate visualizations"
python "Ckwh_vis.py"
python "separate_Ckwh_vis.py"
python "bokeh_Ckwh.py"
python "eda.py"
python "downselected_vis.py"

echo "Done"

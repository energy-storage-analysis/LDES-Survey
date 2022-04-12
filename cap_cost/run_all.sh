echo "Consolidating Data"
python "consolidate_data.py"

echo "Calculating C_kWh"
python "calc_Ckwh.py"

echo "Generate visualizations"
python "vis_Ckwh_line.py"
python "vis_Ckwh.py"
python "vis_eda.py"
python "vis_singletech.py"

echo "Done"

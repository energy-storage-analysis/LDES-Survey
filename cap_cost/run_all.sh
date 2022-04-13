echo "Consolidating Data"
python "consolidate_data.py"

echo "Calculating C_kWh"
python "calc_Ckwh.py"

echo "Generate visualizations"
cd analysis
python "Ckwh_line.py"
python "Ckwh.py"
python "eda.py"
python "thermal.py"
python "electrochem.py"

echo "Done"

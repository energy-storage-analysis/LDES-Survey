echo "Consolidating Data"
python "consolidate_data.py"

echo "Calculating C_kWh"
python "calc_Ckwh.py"



if [ "$1" == "vis" ]; then
    echo "Generate visualizations"
    cd figure_panels
    ./genvis_all.sh
fi

echo "Done"
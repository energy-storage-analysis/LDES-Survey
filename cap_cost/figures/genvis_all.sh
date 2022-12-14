cwd=$(pwd)

echo "Generating Figure components"

for folder in thermal electrochem Ckwh_strip eda virial rhoE_matprice
do
    cd $cwd
    echo $folder
    cd $folder
    ./genvis.sh
done


echo "Generating final figures from SVG files"
cd $cwd
python genfigs.py
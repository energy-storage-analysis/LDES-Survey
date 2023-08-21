mkdir -p figures

scripts='*.py'

for script in $scripts
do
echo $script
python $script
done
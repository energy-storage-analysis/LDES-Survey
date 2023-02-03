# TODO


# Export the vars in .env into your shell:
# https://gist.github.com/judy2k/7656bfe3b322d669ef75364a46327836
# export $(egrep -v '^#' ../.env | xargs)

# Generate visualizations

cd lcos
echo "Generating LCOS Figure Panels"
python vis_lcos_pub.py
cd ..

cd GESDB
echo "Generating GESDB Figure Panels"
python gesdb_analysis.py
cd ..

cd cap_cost
echo "Generating database and figure panels"
./run_all.sh vis
cd ..

cd figures
echo "Generating final figures from svg files"
python genfigs.py
cd ..

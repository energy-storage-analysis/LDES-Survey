### Main shell script to generate the final figures and supporting information from the raw extracted datasets
### TODO: add ability to only run individual portions from here. 

# Export the vars in .env into your shell:
# https://stackoverflow.com/questions/5228345/how-can-i-reference-a-file-for-variables-using-bash
source .env

# Generate the LCOS analysis data and figures
cd $REPO_DIR/lcos
echo "---Generating LCOS Figure Panels---"
python vis_lcos_pub.py

# Generate the Global Energy Storage Database Figures
cd $REPO_DIR/EIA
echo "---Generating EIA/GESDB Figure Panels---"
python figure_gen.py

if [ "$1" == "process" ]; then
    # Perform the data processing for each individual source. Due to the long processing time, the data extraction is not run by default (see process_all.sh for more info)
    cd $REPO_DIR/cap_cost/datasets
    echo "---Running Process Scripts for each data source---"
    ./process_all.sh
fi

# Once the data from each source is ready, it is consolidated into the final dataset and the corresponding figure panels are generated. 
cd $REPO_DIR/cap_cost
echo "---Generating final database and figure panels---"
./gen_dataset.sh vis

# Final manuscript figure generation temporarily manual export from inkscape

cd $REPO_DIR/figures
echo "---Generating final figures from svg files---"
./gen_figs.sh

# Run a series of scripts to generate metadata about the final dataset, primarily for the supporting information
cd $REPO_DIR/cap_cost/source_meta
echo "---Generating final source metadata---"
./run_all.sh

# Consolidate metadata and source readme files, then generate the supporting information Word document. 

cd $REPO_DIR/SI_docs
echo "---Generating Supporting information---"
./gen_SI.sh



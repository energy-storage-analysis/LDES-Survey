#!/bin/bash
# Purpose: Read Comma Separated CSV File
# Author: Vivek Gite under GPL v2.0+
# ------------------------------------------
INPUT=dataset_index.csv
basepath="$PWD/"
OLDIFS=$IFS
IFS=','
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }

# Due to the long processing time, the data extraction (e.g. extraction from pdfs) is not run by default but can be by setting run_extract to true
run_extract=false
run_processing=true

i=1
while read  -r source folder processing_script extract_script
do
    test $i -eq 1 && ((i=i+1)) && continue
    extract_script=$(echo $extract_script|tr -d '\r')
    processing_script=$(echo $processing_script|tr -d '\r')
	echo "Name : $source"
    DIR=$basepath$folder
    DIR_clean=$(echo $DIR|tr -d '\r')
    # DIR="$(dirname "${full_path_clean}")" ; FILE="$(basename "${full_path_clean}")"
    cd $DIR_clean

    if [ "$extract_script" == "y" ] && [ "$run_extract" == true ] ; then
    echo "Running extraction Script"
    python "extract.py"
    fi

    if [ "$processing_script" == "y" ] && [ "$run_processing" == true ] ; then 
    echo "Running Processing Script"
    python "process.py"
    fi
done < $INPUT
IFS=$OLDIFS
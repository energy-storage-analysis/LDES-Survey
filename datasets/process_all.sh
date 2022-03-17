#!/bin/bash
# Purpose: Read Comma Separated CSV File
# Author: Vivek Gite under GPL v2.0+
# ------------------------------------------
INPUT=dataset_index.csv
basepath="$PWD/"
OLDIFS=$IFS
IFS=','
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }

i=1
while read source folder processing_script
do
    test $i -eq 1 && ((i=i+1)) && continue
    processing_script=$(echo $processing_script|tr -d '\r')
    if [ "$processing_script" == "y" ] 
    then
	    echo "Name : $source"
        DIR=$basepath$folder
        DIR_clean=$(echo $DIR|tr -d '\r')
        # DIR="$(dirname "${full_path_clean}")" ; FILE="$(basename "${full_path_clean}")"
        cd $DIR_clean
        python "process.py"
    fi
done < $INPUT
IFS=$OLDIFS
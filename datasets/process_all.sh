#!/bin/bash
# Purpose: Read Comma Separated CSV File
# Author: Vivek Gite under GPL v2.0+
# ------------------------------------------
INPUT=dataset_index.csv
basepath="$PWD/"
echo "$basepath"
OLDIFS=$IFS
IFS=','
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }

i=1
while read source price_data_path processing_script
do
    test $i -eq 1 && ((i=i+1)) && continue
	echo "Name : $source"
    if [ ${#processing_script} -ge 2 ] 
    then
	    echo "Running : $processing_script"
        full_path=$basepath$processing_script
        full_path_clean=$(echo $full_path|tr -d '\r')
        DIR="$(dirname "${full_path_clean}")" ; FILE="$(basename "${full_path_clean}")"
        cd $DIR
        # echo "$full_path"
        python $FILE
    fi
done < $INPUT
IFS=$OLDIFS
#!/bin/bash

mkdir temp

while read in; do
    x=""
    x=`grep $in mouse_g2r_f`   
    if [ -z "$x" ];
    then
	echo "$in not found"
    else
	echo "${x%%,*},$in" >> temp/list
    fi
    
    
done < $1

python internal_primergen.py $2

rm -rf temp


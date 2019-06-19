#!/usr/bin/env bash

glob_patt="$1"
echo $glob_patt

for f in "$glob_patt"
do
    echo $f
    srun python3 -u /homeappl/home/aliagadi/saltena_2018/wrf_management/wrf_management/modules/compress_cli.py $f
done
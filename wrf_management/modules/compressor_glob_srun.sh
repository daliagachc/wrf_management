#!/usr/bin/env bash
#todo this is still unders construction
glob_patt="$1"
echo $glob_patt

for f in "$glob_patt"
do
    echo $f
    srun -c1 --mem=4000 -t5 python3 -u /homeappl/home/aliagadi/saltena_2018/wrf_management/wrf_management/modules/compress_cli.py $f
done
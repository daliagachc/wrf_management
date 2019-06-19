#!/usr/bin/env bash

conda activate b36

glob_patt=$1

for f in $glob_patt
do
    echo $f
done
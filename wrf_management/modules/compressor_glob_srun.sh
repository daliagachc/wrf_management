#!/usr/bin/env bash

glob_patt=$1
echo $glob_patt

for f in $glob_patt
do
    echo $f
done
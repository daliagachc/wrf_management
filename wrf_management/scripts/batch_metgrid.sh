#!/bin/bash
#SBATCH -e error%j.txt
#SBATCH -o output%j.txt
#SBATCH -n 1
#SBATCH -t 00:25:00
#SBATCH -p serial
#SBATCH --mem-per-cpu=4000
#SBATCH --mail-type=END
#SBATCH --mail-user=diego.aliaga@helsinki.fi

sleep $SLURM_ARRAY_TASK_ID

conda activate b36
python -u metgrid.py


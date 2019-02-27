#!/bin/bash -l
#SBATCH -J array_job
#SBATCH -o array_job_out_%A_%a.txt
#SBATCH -e array_job_err_%A_%a.txt
#SBATCH -t 00:25:00
#SBATCH --mem-per-cpu=4000
#SBATCH --array=1-30
#SBATCH -n 1
#SBATCH -p serial

sleep $SLURM_ARRAY_TASK_ID

conda activate b36
python -u ungrib_avgtsfc.py


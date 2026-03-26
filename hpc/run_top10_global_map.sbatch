#!/bin/bash
#SBATCH --job-name=top10_map
#SBATCH --partition=debug
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --time=00:05:00
#SBATCH --output=%j.out

source /import/home/sshukla2/mambaforge/etc/profile.d/conda.sh
conda activate /import/home/sshukla2/mambaforge/envs/GEOS694

cd /import/home/sshukla2/REPOSITORIES/GEOS694_ICG_fork/hpc

python top10_global_map.py


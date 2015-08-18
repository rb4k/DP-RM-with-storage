#!/bin/bash -login
#PBS -l nodes=1:ppn=1
#PBS -l walltime=50:00:00
#PBS -l mem=20GB
module load ipython/3.2.0
module load numpy/1.9.2
module load scipy/0.14.0
module load matplotlib/1.4.3
module load networkx/1.10

cd DP_N_NG_NV/

# start ipython
ipython DP_N_NG_NV.py
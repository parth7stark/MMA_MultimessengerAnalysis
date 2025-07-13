#!/bin/bash
#SBATCH --mem=8g                              # required number of memory
#SBATCH --nodes=1                               # nodes required for whole simulation

#SBATCH --cpus-per-task=4                       # CPUs for each task
## SBATCH --gpus-per-task=1                      # Uncomment if using gpu
##SBATCH --ntasks-per-node=1                     # Uncomment if using gpu 

#SBATCH --partition=cpu                    # <- or if Delta one of: gpuA100x4 gpuA40x4 gpuA100x8 gpuMI100x8

##SBATCH --gpus-per-node=1      # Uncomment if using gpu         # number of GPUs you want to use on 1 node
##SBATCH --gpu-bind=none        # Uncomment if using gpu


#SBATCH --job-name=MMA_OverlapAnalysis   # job name
#SBATCH --time=00:10:00                         # dd-hh:mm:ss for the job

#SBATCH -e MMA_OverlapAnalysis-err-%j.log
#SBATCH -o MMA_OverlapAnalysis-out-%j.log

#SBATCH --constraint="scratch"

#SBATCH --account=bbjo-delta-cpu
#SBATCH --mail-user=pp32@illinois.edu
#SBATCH --mail-type="BEGIN,END" # See sbatch or srun man pages for more email options


# Load necessary modules
source /sw/external/python/anaconda3_gpu/etc/profile.d/conda.sh
conda deactivate
conda deactivate  # just making sure
module purge
module reset  # load the default Delta modules

module load anaconda3_gpu
module list

# Change directory to the cloned repo
cd /projects/bepl/parthpatel7173/POLARIS_backup/MMA_MultimessengerAnalysis/OverlapAnalysis

apptainer exec --nv \
  MMA_OverlapAnalysis_miniapp.sif \
  python /app/examples/octopus/run_overlap_analysis.py --config /projects/bepl/parthpatel7173/POLARIS_backup/MMA_MultimessengerAnalysis/OverlapAnalysis/examples/configs/filled_overlap_analysis_config.yaml


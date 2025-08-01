#!/bin/bash
#SBATCH --mem=32g                              # required number of memory
#SBATCH --nodes=1                               # nodes required for whole simulation

#SBATCH --cpus-per-task=16                       # CPUs for each task
#SBATCH --gpus-per-task=1                      # Uncomment if using gpu
#SBATCH --ntasks-per-node=1                     # Uncomment if using gpu 

#SBATCH --partition=gpuA40x4                    # <- or if Delta one of: gpuA100x4 gpuA40x4 gpuA100x8 gpuMI100x8

#SBATCH --gpus-per-node=1      # Uncomment if using gpu         # number of GPUs you want to use on 1 node
#SBATCH --gpu-bind=none        # Uncomment if using gpu


#SBATCH --job-name=MMA_ParameterEstimation   # job name
#SBATCH --time=00:10:00                         # dd-hh:mm:ss for the job

#SBATCH -e MMA_ParameterEstimation-err-%j.log
#SBATCH -o MMA_ParameterEstimation-out-%j.log

#SBATCH --constraint="scratch"

#SBATCH --account=<charging account>
#SBATCH --mail-user=<email-id>
#SBATCH --mail-type="BEGIN,END" # See sbatch or srun man pages for more email options


# Load necessary modules
# source /sw/external/python/anaconda3_gpu/etc/profile.d/conda.sh
# conda deactivate
# conda deactivate  # just making sure
# module purge
# module reset  # load the default Delta modules

# module load anaconda3_gpu
# module list

# Change directory to the cloned repo
cd <path to cloned repo>

apptainer exec --nv \
  MMA_ParameterEstimation_miniapp.sif \
  python /app/examples/octopus/run_bns_parameter_estimation.py --config <absolute path to Parameter Estimator config file>/bns_parameter_estimation_config.yaml


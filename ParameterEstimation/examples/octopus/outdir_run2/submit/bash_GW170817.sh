#!/usr/bin/env bash

# GW170817_data0_1187008882-42_generation
# PARENTS 
# CHILDREN GW170817_data0_1187008882-42_sampling GW170817_data0_1187008882-42_importance_sampling
if [[ "GW170817_data0_1187008882-42_generation" == *"$1"* ]]; then
    echo "Running: /home/parthpatel17/.conda/envs/mma_dingo/bin/dingo_pipe_generation outdir_run2/GW170817_config_complete.ini --label GW170817_data0_1187008882-42_generation --idx 0 --trigger-time 1187008882.42 --outdir outdir_run2"
    /home/parthpatel17/.conda/envs/mma_dingo/bin/dingo_pipe_generation outdir_run2/GW170817_config_complete.ini --label GW170817_data0_1187008882-42_generation --idx 0 --trigger-time 1187008882.42 --outdir outdir_run2
fi

# GW170817_data0_1187008882-42_sampling
# PARENTS GW170817_data0_1187008882-42_generation
# CHILDREN GW170817_data0_1187008882-42_importance_sampling
if [[ "GW170817_data0_1187008882-42_sampling" == *"$1"* ]]; then
    echo "Running: /home/parthpatel17/.conda/envs/mma_dingo/bin/dingo_pipe_sampling outdir_run2/GW170817_config_complete.ini --label GW170817_data0_1187008882-42_sampling --event-data-file outdir_run2/data/GW170817_data0_1187008882-42_generation_event_data.hdf5"
    /home/parthpatel17/.conda/envs/mma_dingo/bin/dingo_pipe_sampling outdir_run2/GW170817_config_complete.ini --label GW170817_data0_1187008882-42_sampling --event-data-file outdir_run2/data/GW170817_data0_1187008882-42_generation_event_data.hdf5
fi

# GW170817_data0_1187008882-42_importance_sampling
# PARENTS GW170817_data0_1187008882-42_sampling GW170817_data0_1187008882-42_generation
# CHILDREN GW170817_data0_1187008882-42_importance_sampling_plot
if [[ "GW170817_data0_1187008882-42_importance_sampling" == *"$1"* ]]; then
    echo "Running: /home/parthpatel17/.conda/envs/mma_dingo/bin/dingo_pipe_importance_sampling outdir_run2/GW170817_config_complete.ini --label GW170817_data0_1187008882-42_importance_sampling --proposal-samples-file outdir_run2/result/GW170817_data0_1187008882-42_sampling.hdf5 --event-data-file outdir_run2/data/GW170817_data0_1187008882-42_generation_event_data.hdf5"
    /home/parthpatel17/.conda/envs/mma_dingo/bin/dingo_pipe_importance_sampling outdir_run2/GW170817_config_complete.ini --label GW170817_data0_1187008882-42_importance_sampling --proposal-samples-file outdir_run2/result/GW170817_data0_1187008882-42_sampling.hdf5 --event-data-file outdir_run2/data/GW170817_data0_1187008882-42_generation_event_data.hdf5
fi

# GW170817_data0_1187008882-42_importance_sampling_plot
# PARENTS GW170817_data0_1187008882-42_importance_sampling
# CHILDREN 
if [[ "GW170817_data0_1187008882-42_importance_sampling_plot" == *"$1"* ]]; then
    echo "Running: /home/parthpatel17/.conda/envs/mma_dingo/bin/dingo_pipe_plot --label GW170817_data0_1187008882-42_importance_sampling_plot --result outdir_run2/result/GW170817_data0_1187008882-42_importance_sampling.hdf5 --outdir outdir_run2/result --corner --weights --log_probs"
    /home/parthpatel17/.conda/envs/mma_dingo/bin/dingo_pipe_plot --label GW170817_data0_1187008882-42_importance_sampling_plot --result outdir_run2/result/GW170817_data0_1187008882-42_importance_sampling.hdf5 --outdir outdir_run2/result --corner --weights --log_probs
fi


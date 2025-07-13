#!/usr/bin/env bash

# GW170817_data0_1187008882-42_generation
# PARENTS 
# CHILDREN GW170817_data0_1187008882-42_sampling GW170817_data0_1187008882-42_importance_sampling
if [[ "GW170817_data0_1187008882-42_generation" == *"$1"* ]]; then
    echo "Running: /opt/conda/bin/dingo_pipe_generation examples/outdir_apptainer/GW170817_config_complete.ini --label GW170817_data0_1187008882-42_generation --idx 0 --trigger-time 1187008882.42 --outdir examples/outdir_apptainer"
    /opt/conda/bin/dingo_pipe_generation examples/outdir_apptainer/GW170817_config_complete.ini --label GW170817_data0_1187008882-42_generation --idx 0 --trigger-time 1187008882.42 --outdir examples/outdir_apptainer
fi

# GW170817_data0_1187008882-42_sampling
# PARENTS GW170817_data0_1187008882-42_generation
# CHILDREN GW170817_data0_1187008882-42_importance_sampling
if [[ "GW170817_data0_1187008882-42_sampling" == *"$1"* ]]; then
    echo "Running: /opt/conda/bin/dingo_pipe_sampling examples/outdir_apptainer/GW170817_config_complete.ini --label GW170817_data0_1187008882-42_sampling --event-data-file examples/outdir_apptainer/data/GW170817_data0_1187008882-42_generation_event_data.hdf5"
    /opt/conda/bin/dingo_pipe_sampling examples/outdir_apptainer/GW170817_config_complete.ini --label GW170817_data0_1187008882-42_sampling --event-data-file examples/outdir_apptainer/data/GW170817_data0_1187008882-42_generation_event_data.hdf5
fi

# GW170817_data0_1187008882-42_importance_sampling
# PARENTS GW170817_data0_1187008882-42_sampling GW170817_data0_1187008882-42_generation
# CHILDREN GW170817_data0_1187008882-42_importance_sampling_plot
if [[ "GW170817_data0_1187008882-42_importance_sampling" == *"$1"* ]]; then
    echo "Running: /opt/conda/bin/dingo_pipe_importance_sampling examples/outdir_apptainer/GW170817_config_complete.ini --label GW170817_data0_1187008882-42_importance_sampling --proposal-samples-file examples/outdir_apptainer/result/GW170817_data0_1187008882-42_sampling.hdf5 --event-data-file examples/outdir_apptainer/data/GW170817_data0_1187008882-42_generation_event_data.hdf5"
    /opt/conda/bin/dingo_pipe_importance_sampling examples/outdir_apptainer/GW170817_config_complete.ini --label GW170817_data0_1187008882-42_importance_sampling --proposal-samples-file examples/outdir_apptainer/result/GW170817_data0_1187008882-42_sampling.hdf5 --event-data-file examples/outdir_apptainer/data/GW170817_data0_1187008882-42_generation_event_data.hdf5
fi

# GW170817_data0_1187008882-42_importance_sampling_plot
# PARENTS GW170817_data0_1187008882-42_importance_sampling
# CHILDREN 
if [[ "GW170817_data0_1187008882-42_importance_sampling_plot" == *"$1"* ]]; then
    echo "Running: /opt/conda/bin/dingo_pipe_plot --label GW170817_data0_1187008882-42_importance_sampling_plot --result examples/outdir_apptainer/result/GW170817_data0_1187008882-42_importance_sampling.hdf5 --outdir examples/outdir_apptainer/result --corner --weights --log_probs"
    /opt/conda/bin/dingo_pipe_plot --label GW170817_data0_1187008882-42_importance_sampling_plot --result examples/outdir_apptainer/result/GW170817_data0_1187008882-42_importance_sampling.hdf5 --outdir examples/outdir_apptainer/result --corner --weights --log_probs
fi


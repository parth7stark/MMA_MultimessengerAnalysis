# Multimessenger App - Overlap Analysis

## Overview
This repository is part of a **Multimessenger App** designed to analyze data from different astronomical sources. In multimessenger astronomy, signals from various messengers—such as gravitational waves, radio waves, and electromagnetic waves—are combined to gain a more comprehensive understanding of astrophysical phenomena.

This repo specifically contains files and code related to **Overlap Analysis** module, which performs joint GW–EM inference by integrating outputs from gravitational wave parameter estimation and radio afterglow modeling. It forms one of the core components of the overall multimessenger workflow. The app integrates these data streams with other repositories handling gravitational wave analysis to create a unified event detection and analysis framework.

## Installation and running your first inference

You will need a machine running Linux x86 architecture to build container image. If using ARM64 or other architecture, one need to update Apptainer definition file accordingly. Refer [Usage on Delta AI section](##usage-on-delta-ai)

Please follow these steps:

1.  Clone this repository and `cd` into it.

    ```bash
    git clone https://github.com/parth7stark/MMA_MultimessengerAnalysis.git
    cd ./MMA_MultimessengerAnalysis/OverlapAnalysis
    ```

2. Build the Apptainer image:

    ```bash
    apptainer build MMA_OverlapAnalysis_miniapp.sif apptainer/MMA_OverlapAnalysis_miniapp.def
    ```

3. Setup Octopus Connection

    To allow the Overlap Analysis module to connect to the Octopus event fabric, you need to export the username (user's OpenID) and password (AWS secret key) in the .bashrc file where this component will run.

    * **Note:** You must configure the .bashrc file in the site where the Overlap Analysis module will run.

    You can append these lines to the end of the .bashrc file using the following command:

    ```bash
    cat <<EOL >> ~/.bashrc
    # Kafka Configuration
    export OCTOPUS_AWS_ACCESS_KEY_ID="AKIA4J4XQFUIIB7Y4FG3"
    export OCTOPUS_AWS_SECRET_ACCESS_KEY="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"
    export OCTOPUS_BOOTSTRAP_SERVERS='b-1-public.diaspora.fy49oq.c9.kafka.us-east-1.amazonaws.com:9198,b-2-public.diaspora.fy49oq.c9.kafka.us-east-1.amazonaws.com:9198'
    EOL   
    ```

    After updating the .bashrc, reload it to apply the changes to your current shell session:
    
    ```bash
    source ~/.bashrc
    ```

4. Start Overlap Analysis module


   * Update the config file:

        Open the `examples/configs/overlap_analysis_config.yaml` configuration file and update the following paths with the appropriate ones for your system:

        - **Simulation Data Path:** Specify the location of the downloaded model checkpoint file.

        - **Result Path:** Define where the overlap analysis contour plot will be saved

        - **Logging Output Path:** Define where the logs should be saved.


   * Update the Job script:
      
       The sample job script can be located in the repository under the name `job_scripts/OverlapAnalysis.sh`

        ```bash
        job_scripts/OverlapAnalysis.sh
    
        - Modify the SLURM parameters in the script to suit your computing environment (e.g., partition, time, and resources).
        ```

    * Submit the Job Script
    
        Use the following command to submit the job script:
    
        ```bash
        sbatch job_scripts/OverlapAnalysis.sh
        ```

    Submitting the job script will automatically start the Server.

5.  Once the run begins, two output files will be generated for the Overlap analysis module in your working directory: 
`<job-name>-err-<job_id>.log` (error logs) and `<job-name>-out-<job_id>.log` (output logs). Additionally, the job's output files will be saved in the log output directory specified in your configuration file.

## Usage on Delta AI

Since Delta AI is an **ARM64 architecture machine**, so the Apptainer definition file must be updated to use a base image and install libraries compatible with the ARM64 architecture.

Just use the `MMA_OverlapAnalysis_miniapp_arm64.def` for building the image.
The remaining steps are the same as those for Delta or Linux x86 architecture.


## Usage on Polaris

Polaris compute nodes do not have network access to the event fabric's port. Therefore, an HTTPS proxy is required. While this will be set up in the future, as a workaround, you can run the server or detector on the **login node**.

Modification to above usage steps:

**Step 1:** Clone repo (no change)

**Step 2:** Build the Apptainer image:

To build the Apptainer images, you need to be on the Polaris compute nodes. Follow these steps:

1. **Start an Interactive Session:**
   ```bash
   qsub -I -A <Project> -q debug -l select=1 -l walltime=01:00:00 -l filesystems=home:eagle -l singularity_fakeroot=true
   ```

2. **Set Proxy Environment Variables:**

   ```bash
   export HTTP_PROXY=http://proxy.alcf.anl.gov:3128
   export HTTPS_PROXY=http://proxy.alcf.anl.gov:3128
   export http_proxy=http://proxy.alcf.anl.gov:3128
   export https_proxy=http://proxy.alcf.anl.gov:3128

   export BASE_SCRATCH_DIR=/local/scratch/ # For Polaris
   export APPTAINER_TMPDIR=$BASE_SCRATCH_DIR/apptainer-tmpdir
   mkdir -p $APPTAINER_TMPDIR

   export APPTAINER_CACHEDIR=$BASE_SCRATCH_DIR/ apptainer-cachedir
   mkdir -p $APPTAINER_CACHEDIR
   ```

3. **Load Apptainer Module:**

   ```bash
   ml use /soft/modulefiles
   ml spack-pe-base/0.8.1
   ml use /soft/spack/testing/0.8.1/modulefiles
   ml apptainer/main
   ml load e2fsprogs
   ```

4. **Build Apptainer Images:**
   
    ```bash
    apptainer build --fakeroot MMA_OverlapAnalysis_miniapp.sif apptainer/MMA_OverlapAnalysis_miniapp.def
    ```


**Step 3:** Update configurations

Update the configurations for the Overlap analysis module as described in the previous steps. Ensure the paths in the config files point to the appropriate locations on your system.

**Step 4:** Start container on login node

To start the Overlap Analysis, execute the following commands from the login node.

    * To start module, run:

    ```bash
    apptainer exec --nv \
    MMA_OverlapAnalysis_miniapp.sif \
    python /app/examples/octopus/run_overlap_analysis.py --config <absolute path to cloned repo>/examples/configs/overlap_analysis_config.yaml
    ```



## Related Projects
This repo focuses on performing joint analysis between gravitational and radio wave data. For gravitational wave and radio wave analysis, please visit [Gravitational Wave Analysis Repo](https://github.com/parth7stark/MMA_GravitationalWave/tree/main) and [Radio Wave Analysis Repo](https://github.com/parth7stark/MMA_RadioWave/tree/main). Together, these repositories work within the multimessenger framework to capture and analyze various cosmic events.


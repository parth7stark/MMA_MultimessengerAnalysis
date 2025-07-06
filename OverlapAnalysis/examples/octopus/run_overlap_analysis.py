import argparse
from omegaconf import OmegaConf
from mma_overlap_analysis.agent import OverlapAnalyzerAgent
from mma_overlap_analysis.communicator.octopus import OctopusOverlapCommunicator
import json

argparser = argparse.ArgumentParser()
argparser.add_argument(
    "--config", 
    type=str, 
    default="examples/configs/filled_overlap_analysis_config.yaml",
    help="Path to the configuration file."
)

args = argparser.parse_args()

# Load config from YAML (via OmegaConf)
overlap_analyzer_config = OmegaConf.load(args.config)

# Initialize overlap_analyzer-side modules
overlap_analyzer_agent = OverlapAnalyzerAgent(overlap_analyzer_config=overlap_analyzer_config)

# Create Octopus communicator for publishing events to Radio topic - 
octopuscommunicator = OctopusOverlapCommunicator(
    overlap_analyzer_agent,
    logger=overlap_analyzer_agent.logger,
)

# Commenting as Octopus doesn't work on Polaris compute node
octopuscommunicator.publish_overlap_analyzer_started_event()

# print("[GCN Listener] Started listening for LVK notices and circulars...", flush=True)
overlap_analyzer_agent.logger.info("[Overlap Analysis Module] Started Overlap Analysis Process...")

# Start the overlap analysis process
if overlap_analyzer_config.overlap_analysis_configs.simulate_events == "yes":
    print("[Simulation Mode] Loading Dingo/federated fitting posterior samples from HDF5 file and publishing to Octopus...")
    overlap_analyzer_agent.logger.info("[Simulation Mode] Loading Dingo/federated fitting posterior samples from HDF5 file and publishing to Octopus...")
    
    octopuscommunicator.publish_posteriors_from_files()

print("[Overlap Analyzer] Listening for posterior samples from Dingo and Afterglowpy...")
for msg in octopuscommunicator.consumer:
    topic = msg.topic
    overlap_analyzer_agent.logger.info(f"[octopus msg: {msg}")

    data_str = msg.value.decode("utf-8")  # decode to string
    data = json.loads(data_str)          # parse JSON to dict

    Event_type = data["EventType"]

    if Event_type == "DingoPosteriorSamplesReady":
        dingo_samples, dingo_weights, dingo_samples_received = octopuscommunicator.handle_DingoPosteriorSamplesReady_message(data)
    elif Event_type == "AfterglowPosteriorSamplesReady":
        afterglow_samples, afterglow_samples_received = octopuscommunicator.handle_AfterglowPosteriorSamplesReady_message(data)
    
    elif Event_type == "ServerStarted":
            # Continue listening other events
        continue

    elif dingo_samples_received==True and afterglow_samples_received==True:
        break

    else:
        print(f"[Server] Unknown Event Type in topic ({topic}): {Event_type}", flush=True)
        overlap_analyzer_agent.logger.info(f"[Server] Unknown Event Type in topic ({topic}): {Event_type}")

# Full overlap contour plot
result_dir =  overlap_analyzer_config.overlap_analysis_configs.dingo_configs.result_dir
overlap_analyzer_agent.analyzer.plot_overlap(dingo_samples, dingo_weights, afterglow_samples, output_path=result_dir + "/dingo_fedfit_overlap_contour_plot.png")


import logging
from typing import Optional
from omegaconf import OmegaConf
from mma_overlap_analysis.agent import OverlapAnalyzerAgent
from mma_overlap_analysis.logger import ServerAgentFileLogger
from diaspora_event_sdk import KafkaProducer, KafkaConsumer
from .utils import serialize_tensor_to_base64, deserialize_tensor_from_base64
import torch
from dingo.gw.result import Result
import pandas as pd
import numpy as np
from proxystore.proxy import Proxy, extract


class OctopusOverlapCommunicator:
    """
    Octopus communicator for Overlap analysis module. It contains functions that parse the incoming alerts and publish a message to octopus event fabric
    Contains functions to produce different events
    """

    def __init__(
        self, 
        overlap_analyzer_agent: OverlapAnalyzerAgent,
        logger: Optional[ServerAgentFileLogger] = None,
    ):
        
        self.overlap_analyzer_agent = overlap_analyzer_agent
        self.logger = logger if logger is not None else self._default_logger()
        
        # MMA topic: topic where Estimator publishes posterior samples for overllaped analysis
        self.overlap_analysis_topic = self.overlap_analyzer_agent.overlap_analyzer_config.overlap_analysis_config.comm_configs.octopus_configs.overlap_analysis_topic.topic


        # Kafka producer for control messages and sending Embeddings
        self.producer = KafkaProducer()


        overlap_analyzer_group_id = self.overlap_analyzer_agent.overlap_analyzer_config.overlap_analysis_config.comm_configs.octopus_configs.overlap_analysis_topic.group_id
        # estimator_overlap_analyzer_group_id = self.overlap_analyzer_agent.overlap_analyzer_config.overlap_analysis_config.comm_configs.octopus_configs.afterglow_topic.group_id
        
        self.consumer = KafkaConsumer(
            self.overlap_analysis_topic,
            enable_auto_commit=True,
            auto_offset_reset="earliest",  # This ensures it reads all past messages
            group_id=overlap_analyzer_group_id
        )

        # self.estimator_topic_consumer = KafkaConsumer(
        #     self.estimator_topic,
        #     enable_auto_commit=True,
        #     auto_offset_reset="earliest",  # This ensures it reads all past messages
        #     group_id=estimator_overlap_analyzer_group_id
        # )

    def publish_overlap_analyzer_started_event(self):
        """
        Publishes an event to the control topic indicating that the Merger listener has started listening for Merger events from GW module
        """

        # Now publish "ParameterEstimatorStarted"
        ready_msg = {
            "EventType": "OverlapAnalyzerStarted",
            "details": "[Overlap Analysis Module] Started Overlap Analysis Process...",
        }
        self.producer.send(self.overlap_analysis_topic, ready_msg)
        self.producer.flush()

        print("Published Overlap Analyzer started event.", flush=True)
        self.logger.info("Published Overlap Analyzer started event.")

    def extract_dingo_samples(self, filepath):
        result = Result(file_name=filepath)
        df = pd.DataFrame(result.samples)
        # Extract parameters and convert theta_jn to theta_obs
        theta_obs = np.pi - df["theta_jn"].to_numpy()
        dl = df["luminosity_distance"].to_numpy()
        weights = df["weights"].to_numpy() if "weights" in df.columns else None
        return np.column_stack((theta_obs, dl)), weights

    def extract_afterglowpy_samples(self, filepath):
        samples = np.load(filepath)
        idx_theta_obs = 1  # θ_obs index
        idx_dl = 3         # DL index   
        return samples[:, [idx_theta_obs, idx_dl]]


    def publish_posteriors_from_files(self):
        """
        We need to send the posterior_samples of Observation and lumonisity distance to the OverlapAnalysis Module for overlap analysis
        :param posterior_dict: 
        Sample posterior_dict: Instead of dictionary, sending dataframe
        {
          "theta_jn": [0.4, 0.41, 0.39, 0.42, ...],
          "luminosity_distance": [40.2, 41.0, 39.8, 40.5, ...]
        }
        :return: None for async and if sync communication return Metadata containing the server's acknowledgment status.
        """
        dingo_samples, dingo_weights = self.extract_dingo_samples(self.overlap_analyzer_config.overlap_analysis_configs.dingo_filepath)
        afterglow_samples = self.extract_afterglowpy_samples(self.overlap_analyzer_config.overlap_analysis_configs.fedfit_filepath)


        # param_names = posterior_df.columns.tolist()
        param_names = ["theta_Obs", "D_L"]

        # Step 2: Convert to tensor for transfer
        tensor_dingo_samples = torch.tensor(dingo_samples.to_numpy())  # Shape [N, num_params]
        tensor_dingo_weights = torch.tensor(dingo_weights.to_numpy())  # Shape [N, num_params]

        tensor_afterglow_samples = torch.tensor(afterglow_samples.to_numpy())  # Shape [N, num_params]

        # Step 3: Proxy if needed
        if self.overlap_analyzer_agent.use_proxystore:
            tensor_dingo_samples = self.overlap_analyzer_agent.proxystore.proxy(tensor_dingo_samples)
            tensor_dingo_weights = self.overlap_analyzer_agent.proxystore.proxy(tensor_dingo_weights)

            tensor_afterglow_samples = self.overlap_analyzer_agent.proxystore.proxy(tensor_afterglow_samples)

            self.logger.info(f"Dingo and Federated Fitting Posterior samples proxied via ProxyStore.")

        # Step 4: Serialize tensor to base64
        dingo_payload_b64 = serialize_tensor_to_base64(tensor_dingo_samples)
        dingo_weight_payload_b64 = serialize_tensor_to_base64(tensor_dingo_weights)

        afterglow_payload_b64 = serialize_tensor_to_base64(tensor_afterglow_samples)

        # Step 5: Build the Kafka JSON payload
        dingo_msgdata = {
            "EventType": "DingoPosteriorSamplesReady",
            "parameters": param_names,
            "posterior_samples": dingo_payload_b64,
            "importance_weights": dingo_weight_payload_b64
        }

        afterglow_msgdata = {
            "EventType": "AfterglowPosteriorSamplesReady",
            "parameters": param_names,
            "posterior_samples": afterglow_payload_b64
        }

        self.producer.send(
            self.overlap_analysis_topic,
            value=dingo_msgdata
        )
        self.logger.info(f"Send Dingo Posterior Samples to Overlap Analysis module")

        self.producer.send(
            self.overlap_analysis_topic,
            value=afterglow_msgdata
        )

        self.producer.flush()

        self.logger.info(f"Send Afterglow Posterior Samples to Overlap Analysis module")
        return    

    def handle_DingoPosteriorSamplesReady_message(self, data):

        dingo_samples_b64 = data["posterior_samples"]
        dingo_weights_b64 = data["importance_weights"]
        
        # Deserialize and extract tensor
        tensor_dingo_samples = deserialize_tensor_from_base64(dingo_samples_b64)
        tensor_dingo_weights = deserialize_tensor_from_base64(dingo_weights_b64)

        if isinstance(tensor_dingo_samples, Proxy):
            self.logger.info(" Extracting Dingo posterior tensor from ProxyStore.")

            tensor_dingo_samples = extract(tensor_dingo_samples)

        if isinstance(tensor_dingo_weights, Proxy):
            tensor_dingo_weights = extract(tensor_dingo_weights)

        dingo_samples = tensor_dingo_samples.numpy()  # Get back list for further processing
        dingo_weights = tensor_dingo_weights.numpy()  # Get back list for further processing

        self.logger.info(f"Received Dingo Posterior Samples")

        return dingo_samples, dingo_weights, True
    
    def AfterglowPosteriorSamplesReady(self, data):

        afterglow_samples_b64 = data["posterior_samples"]
        
        # Deserialize and extract tensor
        tensor_afterglow_samples = deserialize_tensor_from_base64(afterglow_samples_b64)

        if isinstance(tensor_afterglow_samples, Proxy):
            self.logger.info(" Extracting Afterglowpy posterior tensor from ProxyStore.")

            tensor_afterglow_samples = extract(tensor_afterglow_samples)

        afterglow_samples = tensor_afterglow_samples.numpy()  # Get back list for further processing
        self.logger.info(f"Received Afterglow Posterior Samples")

        return afterglow_samples, True


    def _default_logger(self):
        """Create a default logger for the server if no logger provided."""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        fmt = logging.Formatter('[%(asctime)s %(levelname)-4s server]: %(message)s')
        s_handler = logging.StreamHandler()
        s_handler.setLevel(logging.INFO)
        s_handler.setFormatter(fmt)
        logger.addHandler(s_handler)
        return logger

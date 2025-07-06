from mma_overlap_analysis.config import ServerAgentConfig
from mma_overlap_analysis.logger import ServerAgentFileLogger
from mma_overlap_analysis.results import AnalyzeResults
from omegaconf import OmegaConf, DictConfig
from proxystore.store import Store

import subprocess
from pathlib import Path

class OverlapAnalyzerAgent:
    """
    Contain functions that Overlap Analyzer performs like
    - Collecting Posterior samples
    - Plotting overlap contour plot
   
    User can overwrite any class method to customize the behavior of the server agent.
    """
    def __init__(
        self,
        overlap_analyzer_config: ServerAgentConfig = ServerAgentConfig()
    ) -> None:

        self.overlap_analyzer_config = overlap_analyzer_config
        self._create_logger()
        self._load_result_analyzer()
        self._load_proxystore()

    def _create_logger(self) -> None:
        kwargs = {}
        if hasattr(self.overlap_analyzer_config.bns_parameter_estimation_configs, "logging_output_dirname"):
            kwargs["file_dir"] = self.overlap_analyzer_config.bns_parameter_estimation_configs.logging_output_dirname
        if hasattr(self.overlap_analyzer_config.bns_parameter_estimation_configs, "logging_output_filename"):
            kwargs["file_name"] = self.overlap_analyzer_config.bns_parameter_estimation_configs.logging_output_filename
        self.logger = ServerAgentFileLogger(**kwargs)


        
    def _load_result_analyzer(self) -> None:
        """
        Load result analyzer object and initialize parameters
        """

        self.analyzer: AnalyzeResults = AnalyzeResults(
            self.overlap_analyzer_config,
            self.logger,
        )
    
    def clean_up(self) -> None:
        """Clean up the client agent."""
        if hasattr(self, "proxystore") and self.proxystore is not None:
            try:
                self.proxystore.close(clear=True)
            except:
                self.proxystore.close()

    def _load_proxystore(self) -> None:
        """
        Create the proxystore for storing and sending the local mcmc posterior samples from each site to the server.
        """
        if hasattr(self, "proxystore") and self.proxystore is not None:
            return
        self.proxystore = None
        self.use_proxystore = False
        if not hasattr(self.overlap_analyzer_config, "comm_configs"):
            return
        if not hasattr(self.overlap_analyzer_config.comm_configs, "proxystore_configs"):
            return
        if getattr(self.overlap_analyzer_config.comm_configs.proxystore_configs, "enable_proxystore", False):
            self.use_proxystore = True
            self.proxystore = Store(
                name="mma-overlap-analyzer-proxystore",
                connector=self.get_proxystore_connector(
                    self.overlap_analyzer_config.comm_configs.proxystore_configs.connector_type,
                    self.overlap_analyzer_config.comm_configs.proxystore_configs.connector_configs,
                ),
            )
            self.logger.info(
                f"Site using proxystore for local MCMC chain transfer with store: {self.overlap_analyzer_config.comm_configs.proxystore_configs.connector_type}."
            )


    def get_proxystore_connector(self,
        connector_name,
        connector_args,
    ):
        assert connector_name in ["RedisConnector", "FileConnector", "EndpointConnector"], (
            f"Invalid connector name: {connector_name}, only RedisConnector, FileConnector, and EndpointConnector are supported"
        )
        if connector_name == "RedisConnector":
            from proxystore.connectors.redis import RedisConnector

            connector = RedisConnector(**connector_args)
        elif connector_name == "FileConnector":
            from proxystore.connectors.file import FileConnector

            connector = FileConnector(**connector_args)
        elif connector_name == "EndpointConnector":
            from proxystore.connectors.endpoint import EndpointConnector

            connector = EndpointConnector(**connector_args)
        return connector

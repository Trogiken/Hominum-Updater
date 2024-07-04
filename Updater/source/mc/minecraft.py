"""
This module contains the main class for handling Minecraft.

Classes:
- MCManager: A class that handles Minecraft.
"""

import logging
import os
from typing import Generator
from source.mc import remote
from portablemc.standard import Context, Environment, Watcher
from portablemc.fabric import FabricVersion

logger = logging.getLogger(__name__)


class MCManager:
    """
    MCManager is a class that handles Minecraft

    Attributes:
    - context (Context): The context for PortableMC.
    - remote_config (dict): The remote configuration.
    - server_ip (str): The server IP.
    - fabric_version (str): The fabric version.
    - loader_version (str): The loader version.

    Methods:
    - provision_version: Provisions a version for PortableMC.
    - provision_environment: Provisions an environment for PortableMC.
    - sync_dir: Syncs mods with the server.
    - sync_file: Syncs the specified file with the server
    """
    def __init__(self, context: Context):
        logger.debug("Initializing MCManager")

        self.context = context
        self.remote_config = remote.get_config()

        self.server_ip: str = self.remote_config.get("client", {}).get("server_ip", "")
        self.fabric_version: str = self.remote_config.get("client", {}).get("fabric_version", "")
        self.loader_version: str = self.remote_config.get("client", {}).get("loader_version", "")

        logger.debug("Context: %s", self.context)
        logger.debug("Remote Config: %s", self.remote_config)
        logger.debug("Server IP: %s", self.server_ip)
        logger.debug("Fabric Version: %s", self.fabric_version)
        logger.debug("Loader Version: %s", self.loader_version)

        logger.debug("MCManager initialized")

    def _create_dir_path(self, remote_dir: str) -> tuple:
        """
        Creates the local and remote directory paths.

        Parameters:
        - remote_dir (str): The remote directory to sync.
            Options: "config", "mods", "resourcepacks", "shaderpacks"

        Exceptions:
        - ValueError: If the remote directory is invalid.
        - ValueError: If the remote directory URL is not set.

        Returns:
        - tuple: The local directory path and the remote directory URL.
        """
        if self.remote_config is None:
            raise ValueError("Remote config is not set")
        if remote not in self.remote_config["urls"]:
            raise ValueError(f"Invalid remote directory: {remote}")
        if remote == "config":
            local_dir = self.context.work_dir / "config"
        elif remote == "mods":
            local_dir = self.context.work_dir / "mods"
        elif remote == "resourcepacks":
            local_dir = self.context.work_dir / "resourcepacks"
        elif remote == "shaderpacks":
            local_dir = self.context.work_dir / "shaderpacks"
        else:
            raise ValueError(f"Unknown valid remote directory: {remote}")

        local_dir.mkdir(parents=True, exist_ok=True)
        remote_dir_url = self.remote_config["urls"][remote_dir]
        logger.debug("Remote directory URL: %s", remote_dir_url)

        return local_dir, remote_dir_url

    def _create_file_path(self, remote_file: str) -> tuple:
        """
        Creates the local and remote file paths.
        
        Parameters:
        - remote_file (str): The remote file to sync.
            Options: "options", "servers"

        Exceptions:
        - ValueError: If the remote file is invalid.
        - ValueError: If the remote file URL is not set.

        Returns:
        - tuple: The local file path and the remote file URL.
        """
        if remote_file not in self.remote_config["urls"]:
            raise ValueError(f"Invalid remote file: {remote_file}")
        if remote_file == "options":
            local_filepath = self.context.work_dir / "options.txt"
        elif remote_file == "servers":
            local_filepath = self.context.work_dir / "servers.dat"
        else:
            raise ValueError(f"Unknown valid remote file: {remote_file}")

        os.makedirs(os.path.dirname(local_filepath), exist_ok=True)
        remote_file_url = self.remote_config["urls"][remote_file]
        logger.debug("Remote file URL: %s", remote_file_url)

        return local_filepath, remote_file_url

    def provision_version(self, vanilla_version: str, loader_version: str=None) -> FabricVersion:
        """
        Provisions a version for PortableMC.

        Parameters:
        - vanilla_version (str): The fabric version.
        - loader_version (str): The loader version. Defaults to latest.

        Returns:
        - FabricVersion: The version for PortableMC.
        """
        return FabricVersion.with_fabric(
            vanilla_version=vanilla_version, loader_version=loader_version, context=self.context
        )

    def provision_environment(self, version: FabricVersion, watcher: Watcher=None) -> Environment:
        """
        Provisions an environment for PortableMC.

        Parameters:
        - version (FabricVersion): The version for PortableMC.
        - watcher (Watcher): The watcher for PortableMC. Defaults to None.

        Returns:
        - Environment: The environment for PortableMC.
        """
        return version.install(watcher=watcher)

    def sync_dir(self, remote_dir: str) -> Generator[tuple, None, None]:
        """
        Syncs mods with the server.

        Parameters:
        - remote_dir (str): The remote directory to sync.
            Options: "config", "mods", "resourcepacks", "shaderpacks"

        Exceptions:
        - Exception: If any other error occurs.

        Returns:
        - Generator[tuple, None, None]: A generator that yields the progress of the sync.
        """
        local_dir, remote_dir_url = self._create_dir_path(remote_dir)
        if remote_dir_url is None:
            logger.warning("Remote directory '%s' is not set", remote_dir)
            return
        server_mods = remote.get_filenames(remote_dir_url)
        if server_mods is None:
            raise ValueError("Server filenames are not set")
        # Remove invalid mods
        for file in os.listdir(local_dir):
            if file not in server_mods:
                file_path = os.path.join(local_dir, file)
                os.remove(file_path)
                logger.info("Invalid mod '%s' removed", file_path)

        # Download mods
        urls_to_download = remote.get_file_downloads(remote_dir_url)
        if urls_to_download is None:
            raise ValueError("URLs to download are not set")
        for count, total, filename, error_occured in remote.download_files(
            urls_to_download, local_dir
        ):
            yield (count, total, filename, error_occured)

    def sync_file(self, remote_file) -> None:
        """
        Syncs the specified file with the server.

        Parameters:
        - remote_file (str): The remote file to sync.
            Options: "options", "servers"

        Returns:
        - None
        """
        local_filepath, remote_file_url = self._create_file_path(remote_file)
        if remote_file_url is None:
            logger.warning("Remote file '%s' is not set", remote_file)
            return
        server_file = remote.get_file_download(remote_file_url)
        if server_file is None:
            raise ValueError("Server file is not set")

        # Remove the local file if it exists
        if os.path.exists(local_filepath):
            os.remove(local_filepath)
            logger.info("Removed existing local file '%s'", local_filepath)

        # Download the file from the server
        remote.download(server_file, local_filepath)
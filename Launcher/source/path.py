"""
This module contains the paths used by the launcher.

Constants:
- PROGRAM_NAME (str): The name of the program.
- PROGRAM_NAME_LONG (str): The long name of the program.
- VERSION (str): The version of the program.
- APPLICATION_DIR (pathlib.Path): The directory of the application.
- ASSETS_DIR (pathlib.Path): The directory of the assets.
- STORE_DIR (pathlib.Path): The directory of the store.
- DOWNLOAD_DIR (pathlib.Path): The directory of the downloads.
- MAIN_DIR (pathlib.Path): The directory of the main data.
- WORK_DIR (pathlib.Path): The directory of the working data.
- CONTEXT (Context): The context of the program.
- GLOBAL_KILL (pathlib.Path): The global kill switch.
"""

import logging
import os
import pathlib
import sys
from portablemc.standard import Context

logger = logging.getLogger(__name__)

PROGRAM_NAME = "Hominum"
PROGRAM_NAME_LONG = "Hominum Launcher"
VERSION = "1.5.10.15"

if getattr(sys, 'frozen', False):
    APPLICATION_DIR = pathlib.Path(sys.executable).parent
else:
    APPLICATION_DIR = pathlib.Path(__file__).parents[1]

ASSETS_DIR = pathlib.Path(os.path.join(APPLICATION_DIR, "assets"))
STORE_DIR = pathlib.Path(os.path.join(APPLICATION_DIR, "Store"))
DOWNLOAD_DIR = pathlib.Path(os.path.join(STORE_DIR, "download"))
MAIN_DIR = pathlib.Path(os.path.join(STORE_DIR, "minecraft"))
WORK_DIR = pathlib.Path(os.path.join(STORE_DIR, "mcdata"))
CONTEXT = Context(MAIN_DIR, WORK_DIR)
GLOBAL_KILL = pathlib.Path(os.path.join(STORE_DIR, "GLOBAL_KILL"))

if GLOBAL_KILL.exists():
    GLOBAL_KILL.unlink()

os.makedirs(STORE_DIR, exist_ok=True)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(MAIN_DIR, exist_ok=True)
os.makedirs(WORK_DIR, exist_ok=True)

if not os.path.exists(ASSETS_DIR):
    raise FileNotFoundError(f"Assets directory not found: {ASSETS_DIR}")

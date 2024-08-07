"""
This module provides utility functions and classes for the application.

Functions:
- get_image: Get the image from the assets directory.
- get_html_resp: Get the HTML response from the assets directory.
- open_path: Open a folder or file on the users computer.
- format_number: Format a float into correct measurement.

Classes:
- Settings: A class that represents the settings for the application.
- WrappingLabel: A custom label that wraps text.
- PropagatingThread: A thread that propagates exceptions to the main thread.

Constants:
- SETTINGS_FILENAME: The name of the settings file.
- SETTINGS_PATH: The path to the settings file.

Variables:
- gui_settings: The default GUI settings.
- user_settings: The default user settings.
- game_settings: The default game settings.
"""

import logging
import os
import subprocess
import threading
import platform
import json
import pathlib
import customtkinter
from PIL import Image
from source import path

logger = logging.getLogger(__name__)

SETTINGS_FILENAME = "settings.json"
SETTINGS_PATH = pathlib.Path(os.path.join(path.STORE_DIR, SETTINGS_FILENAME))

gui_settings = {
        "appearance": "system",
        "main_window_geometry": [1200, 500],
        "main_window_min_size": [1000, 400],
        "font_small": ["Helvetica", 12],
        "font_normal": ["Helvetica", 14],
        "font_large": ["Helvetica", 16],
        "font_title": ["Helvetica", 16, "bold"],
        "image_small": [14, 14],
        "image_normal": [18, 18],
        "image_large": [24, 24],
}

user_settings =  {
        "email": "",
}

game_settings = {
    "autojoin": True,
    "ram_jvm_args": ["-Xms2048M", "-Xmx2048M"],
    "additional_jvm_args": [
    "-XX:+UnlockExperimentalVMOptions",
    "-XX:+UseG1GC",
    "-XX:G1NewSizePercent=20",
    "-XX:G1ReservePercent=20",
    "-XX:MaxGCPauseMillis=50",
    "-XX:G1HeapRegionSize=32M"
    ],
}


class Settings:
    """
    A class that represents the settings for the application.

    Properties:
    - path: The path to the settings file.

    Methods:
    - validate_settings: Validate the settings.
    - load: Reads the settings from a file.
    - save: Writes the settings to a file.
    - reset: Reset the settings to the default values.
    - reset_gui: Reset the GUI settings to the default values.
    - reset_user: Reset the user settings to the default values.
    - reset_game: Reset the game settings to the default values.
    - get_gui: Retrieves a specific GUI setting.
    - get_user: Retrieves a specific user setting.
    - get_game: Retrieves a specific game setting.
    - set_gui: Updates the GUI settings.
    - set_user: Updates the user settings.
    - set_game: Updates the game settings.
    """
    _first_run = True

    def __init__(self):
        self._gui = None
        self._user = None
        self._game = None
        self.load()

    @property
    def path(self) -> pathlib.Path:
        """
        Get the path to the settings file.

        Returns:
        - pathlib.Path: The path to the settings file.
        """
        return SETTINGS_PATH

    def validate_settings(self) -> bool:
        """
        Validate the settings.
        Checks all attributes of classes.

        Returns:
        - bool: True if the settings are valid, False otherwise.
        """
        valid = True
        for key, value in gui_settings.items():
            if key not in self._gui or not isinstance(self._gui[key], type(value)):
                valid = False
                logger.warning("GUI setting '%s' is missing or invalid", key)
        for key, value in user_settings.items():
            if key not in self._user or not isinstance(self._user[key], type(value)):
                valid = False
                logger.warning("User setting '%s' is missing or invalid", key)
        for key, value in game_settings.items():
            if key not in self._game or not isinstance(self._game[key], type(value)):
                valid = False
                logger.warning("Game setting '%s' is missing or invalid", key)
        return valid

    def load(self):
        """
        Reads the settings from a file.
        If the file doesn't exist, default settings are used.
        """
        try:
            with open(SETTINGS_PATH, 'r', encoding="utf-8") as f:
                data = json.load(f)
                self._gui = data['GUISettings']
                self._user = data['UserSettings']
                self._game = data['GameSettings']

            if Settings._first_run:
                if not self.validate_settings():
                    logger.warning("Settings file is corrupted.")
                    self.reset()
                Settings._first_run = False
        except Exception:
            logger.warning("Settings file not found or damaged.")
            self.reset()

    def save(self):
        """
        Writes the settings to a file.
        """
        data = {
            "GUISettings": self._gui,
            "UserSettings": self._user,
            "GameSettings": self._game
        }
        with open(SETTINGS_PATH, 'w', encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        self.load()

    def reset(self):
        """
        Reset the settings to the default values.
        """
        self._gui = gui_settings
        self._user = user_settings
        self._game = game_settings
        self.save()
        logger.debug("Settings reset to default values.")

    def reset_gui(self):
        """
        Reset the GUI settings to the default values.
        """
        self._gui = gui_settings
        self.save()
        logger.info("GUI settings reset to default values.")

    def reset_user(self):
        """
        Reset the user settings to the default values.
        """
        self._user = user_settings
        self.save()
        logger.info("User settings reset to default values.")

    def reset_game(self):
        """
        Reset the game settings to the default values.
        """
        self._game = game_settings
        self.save()
        logger.info("Game settings reset to default values.")

    def get_gui(self, key: str) -> any:
        """
        Retrieves a specific GUI setting.

        Parameters:
        - key (str): The key of the setting to retrieve.

        Returns:
        - Any: The value of the setting.
        """
        self.load()
        # If the value is a list, return a tuple
        value = tuple(self._gui[key]) if isinstance(self._gui[key], list) else self._gui[key]
        logger.debug("GUI setting '%s' retrieved value '%s'", key, value)
        return value

    def get_user(self, key: str) -> any:
        """
        Retrieves a specific user setting.

        Parameters:
        - key (str): The key of the setting to retrieve.

        Returns:
        - Any: The value of the setting.
        """
        self.load()
        value = self._user[key]
        logger.debug("User setting '%s' retrieved value '%s'", key, value)
        return value

    def get_game(self, key: str) -> any:
        """
        Retrieves a specific game setting.

        Parameters:
        - key (str): The key of the setting to retrieve.

        Returns:
        - Any: The value of the setting.
        """
        self.load()
        value = self._game[key]
        logger.debug("Game setting '%s' retrieved value '%s'", key, value)
        return value

    def set_gui(self, **kwargs) -> None:
        """
        Updates the GUI settings.

        Parameters:
        - **kwargs: Keyword arguments representing the settings to update.
        """
        for key, value in kwargs.items():
            # If the value is a tuple, convert it to a list
            self._gui[key] = list(value) if isinstance(value, tuple) else value
            logger.debug("GUI setting '%s' updated to value '%s'", key, value)
        self.save()

    def set_user(self, **kwargs) -> None:
        """
        Updates the user settings.

        Parameters:
        - **kwargs: Keyword arguments representing the settings to update.
        """
        for key, value in kwargs.items():
            self._user[key] = value
            logger.debug("User setting '%s' updated to value '%s'", key, value)
        self.save()

    def set_game(self, **kwargs) -> None:
        """
        Updates the game settings.

        Parameters:
        - **kwargs: Keyword arguments representing the settings to update.
        """
        for key, value in kwargs.items():
            self._game[key] = value
            logger.debug("Game setting '%s' updated to value '%s'", key, value)
        self.save()


class  WrappingLabel(customtkinter.CTkLabel):
    """A custom label that wraps text."""
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<Configure>", lambda _: self.configure(wraplength=self.winfo_width()))


class PropagatingThread(threading.Thread):
    """A thread that propagates exceptions to the main thread."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exc = None
        self.ret = None

    def run(self):
        try:
            self.ret = self._target(*self._args, **self._kwargs)
        except BaseException as e:
            self.exc = e

    def join(self, timeout=None):
        super().join(timeout)
        if self.exc:
            raise self.exc
        return self.ret


def get_image(image_name: str) -> Image.Image:
    """
    Get the image from the assets directory.

    Parameters:
    - image_name (str): The name of the image.

    Returns:
    - Image: The image.
    """
    try:
        image = Image.open(path.ASSETS_DIR / "images" / image_name)
    except FileNotFoundError:
        logger.error("Image '%s' not found", image_name)
        raise
    logger.debug("Image '%s' loaded", image_name)
    return image


def get_html_resp() -> str:
    """
    Get the HTML response from the assets directory.

    Exceptions:
    - FileNotFoundError: If the HTML response is not found.

    Returns:
    - str: The HTML response.
    """
    try:
        with open(path.ASSETS_DIR / "resp.html", "r", encoding="utf-8") as f:
            html_resp = f.read()
    except FileNotFoundError:
        logger.error("HTML response not found")
        raise
    logger.debug("HTML response loaded")
    return html_resp


def open_path(directory_path: str | pathlib.Path):
    """
    Open a folder or file.

    Parameters:
    - directory_path (str | pathlib.Path): The directory to open.
    """
    system_platform = platform.system()

    if system_platform == "Windows":
        os.startfile(directory_path)  # pylint: disable=no-member
    elif system_platform == "Darwin":  # macOS
        with subprocess.Popen(["open", directory_path]) as proc:
            proc.communicate()
    else:  # Linux and other Unix-like systems
        with subprocess.Popen(["xdg-open", directory_path]) as proc:
            proc.communicate()
    logger.debug("Opened path: '%s'", directory_path)


def format_number(number: float) -> str:
    """
    Format a float into correct measurement

    Parameters:
    - number (float): The number to format.

    Returns:
    - str: The formatted number
    """
    if number < 1000:
        return f"{int(number)} "
    if number < 1000000:
        return f"{(int(number / 100) / 10):.1f} k"
    if number < 1000000000:
        return f"{(int(number / 100000) / 10):.1f} M"
    return f"{(int(number / 100000000) / 10):.1f} G"

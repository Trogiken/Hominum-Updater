"""
This module handles things related to the gui

Functions:
- get_settings() -> GUISettings: Get the settings from the settings file.
- save_settings(settings: GUISettings) -> pathlib.Path: Save the settings to the settings file.
- reset_settings() -> GUISettings: Reset the settings to the default values.
- get_image(image_name: str) -> Image: Get the image from the assets directory.

Classes:
- Settings: Stores the settings for the program.

Constants:
- SETTINGS_FILENAME: The name of the settings file.
- SETTINGS_PATH: The path to the settings file.
"""

import os
import pickle
import pathlib
from dataclasses import dataclass, field
from PIL import Image
from source import path


SETTINGS_FILENAME = "settings.pkl"
SETTINGS_PATH = pathlib.Path(os.path.join(path.STORE_DIR, SETTINGS_FILENAME))

# TODO: Turn this into a normal class and put the module functions in it
class Settings:
    """Stores the settings for the program."""

    @dataclass
    class _GUISettings:
        """Stores the settings for the GUI."""
        font_type: str = "Helvetica"
        font_size_small: int = 12
        font_size_normal: int = 14
        font_size_large: int = 16
        font: tuple = (font_type, font_size_normal)
        font_small: tuple = (font_type, font_size_small)
        font_normal: tuple = (font_type, font_size_normal)
        font_large: tuple = (font_type, font_size_large)
        appearance: str = "system"
        image_small: tuple = (14, 14)
        image_normal: tuple = (18, 18)
        image_large: tuple = (24, 24)

    @dataclass
    class _UserSettings:
        """Stores the settings for the user."""
        email: str = ""
        jvm_args: list = field(default_factory=lambda: [
            "-Xmx2G",
            "-XX:+UnlockExperimentalVMOptions",
            "-XX:+UseG1GC",
            "-XX:G1NewSizePercent=20",
            "-XX:G1ReservePercent=20",
            "-XX:MaxGCPauseMillis=50",
            "-XX:G1HeapRegionSize=32M"
        ])
        # TODO: Add whitelist mods here also
    
    @property
    def gui(self) -> _GUISettings:
        pass

    @property
    def user(self) -> _UserSettings:
        pass

    @gui.setter
    def gui(self, value: _GUISettings) -> None:
        pass

    @user.setter
    def user(self, value: _UserSettings) -> None:
        pass

    def reset_settings(self) -> self:
        """
        Reset the settings to the default values.

        Returns:
        - GUISettings: The default settings.
        """
        settings = Settings()
        save_settings(settings)
        return settings


    def load_settings() -> self:
        """
        Get the settings from the settings file.

        Returns:
        - GUISettings: The settings.
        """
        if not os.path.exists(SETTINGS_PATH):
            with open(SETTINGS_PATH, "wb") as f:
                pickle.dump(Settings(), f)
            return Settings()

        with open(SETTINGS_PATH, "rb") as f:
            return pickle.load(f)


    def save_settings(self) -> pathlib.Path:
        """
        Save the settings to the settings file.
        
        Parameters:
        - settings (GUISettings): The settings to save.
        
        Returns:
        - Path: The path to the settings file."""
        with open(SETTINGS_PATH, "wb") as f:
            pickle.dump(settings, f)
        return SETTINGS_PATH


def get_image(image_name: str) -> Image.Image:
    """
    Get the image from the assets directory.

    Parameters:
    - image_name (str): The name of the image.

    Returns:
    - Image: The image.
    """
    return Image.open(path.ASSETS_DIR / "images" / image_name)

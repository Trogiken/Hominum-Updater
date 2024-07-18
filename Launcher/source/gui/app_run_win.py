"""
A module that contains the RunWindow class.

Classes:
- RunWindow: A class that is used to run the game.
"""

import os
import logging
import customtkinter
from portablemc.standard import Environment
from source.mc.minecraft import EnvironmentRunner
from source.gui.popup_win import PopupWindow
from source import utils, path

if os.name != "posix":
    import pygetwindow as pygw

logger = logging.getLogger(__name__)


class RunWindow(customtkinter.CTkToplevel):
    """A class that is used to run the game."""
    def __init__(self, environment: Environment):
        super().__init__()
        logger.debug("Creating game window")

        self.settings = utils.Settings()

        self.title("Run")
        # Used to minimize the main window after the game starts
        self.main_window = None
        if os.name != "posix":
            self.main_window: pygw.Win32Window = pygw.getWindowsWithTitle(path.PROGRAM_NAME)[0]

        if not environment:
            PopupWindow(
                self,
                title="No Environment",
                message="Environment could not be found. "\
                "Make sure the installation completed successfully."
            )
            super().destroy()
            return

        self.environment = environment
        self.kill_process = False  # Used by EnvironmentRunner

        self.protocol("WM_DELETE_WINDOW", self.destroy)  # Prevent the closing of this window
        self.attributes("-topmost", True)  # Always on top
        self.geometry("500x150")
        self.resizable(False, False)
        self.columnconfigure(0, weight=1)  # configure grid system

        self.title_label = customtkinter.CTkLabel(
            self, text="Game Running", font=self.settings.get_gui("font_large")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=20)

        self.message_label = customtkinter.CTkLabel(
            self,
            text="Please wait until the Minecraft window opens",
            font=self.settings.get_gui("font_normal")
        )
        self.message_label.grid(row=1, column=0, padx=20, pady=(0, 20))

        self.after(100, self.run)

        logger.debug("Created game window")

    def destroy(self):
        """Destroy the window. This overrides the default destroy method to stop the game."""
        self.stop_run()

    def stop_run(self):
        """Stop the game."""
        logger.info("Stopping game")
        self.kill_process = True

    def run(self):
        """Provision the environment and run the game."""
        logger.info("Running game")
        if os.name != "posix" and self.main_window:
            if not self.main_window.isMinimized:
                self.after(1000, self.main_window.minimize())
                logger.debug("Main window minimized")
        self.environment.run(EnvironmentRunner(self))

    def update_gui(self):
        """Update the GUI."""
        self.update()
        self.update_idletasks()

    def on_run_complete(self):
        """Close this window."""
        logger.info("Game stopped")
        if os.name != "posix" and self.main_window:
            if self.main_window.isMinimized:
                self.main_window.maximize()
                logger.debug("Main window maximized")
                min_length, min_height = self.settings.get_gui("main_window_min_size")
                self.main_window.resizeTo(min_length, min_height)
                logger.debug("Main window resized to '%s'x'%s'", min_length, min_height)
        super().destroy()
        logger.debug("Run game window destroyed")

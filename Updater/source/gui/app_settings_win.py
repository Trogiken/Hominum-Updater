"""
This module contains the SettingsWindow class,
which represents the settings window of the application.

Classes:
- GUISettingsFrame: A frame for the GUI settings.
- UserSettingsFrame: A frame for the User settings.
- GameSettingsFrame: A frame for the Game settings.
- SettingsWindow: A window for the settings of the application.
"""

import customtkinter
from source import path
from source.utils import Settings
from source.gui.popup_win import PopupWindow
from source.mc.authentication import AuthenticationHandler

SETTINGS = Settings()


class GUISettingsFrame(customtkinter.CTkFrame):
    """A frame for the GUI settings."""
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Frame Title
        self.title_label = customtkinter.CTkLabel(
            self, text="GUI", font=SETTINGS.get_gui("font_title")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="n")

        # Reset GUI Settings Button
        self.reset_gui_settings_button = customtkinter.CTkButton(
            self,
            text="Reset Settings",
            font=SETTINGS.get_gui("font_normal"),
            command=self.reset_gui_settings
        )
        self.reset_gui_settings_button.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="s")

    def reset_gui_settings(self):
        """Reset the GUI settings to the default values."""
        SETTINGS.reset_gui()
        PopupWindow(
            master=self.master,
            title="Settings Reset",
            message="The GUI settings have been reset to default."
        )


class UserSettingsFrame(customtkinter.CTkFrame):
    """A frame for the User settings."""
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Frame Title
        self.title_label = customtkinter.CTkLabel(
            self, text="User", font=SETTINGS.get_gui("font_title")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="n")

        # Reset User Settings Button
        self.reset_user_settings_button = customtkinter.CTkButton(
            self,
            text="Reset Settings",
            font=SETTINGS.get_gui("font_normal"),
            command=self.reset_user_settings
        )
        self.reset_user_settings_button.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="s")

    def reset_user_settings(self):
        """Reset the User settings to the default values."""
        auth_handler = AuthenticationHandler(SETTINGS.get_user("email"), path.CONTEXT)
        auth_handler.remove_session()
        SETTINGS.reset_user()
        PopupWindow(
            master=self.master,
            title="Settings Reset",
            message="The User settings have been reset to default."
        )


class GameSettingsFrame(customtkinter.CTkFrame):
    """A frame for the Game settings."""
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Frame Title
        self.title_label = customtkinter.CTkLabel(
            self, text="Game", font=SETTINGS.get_gui("font_title")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="n")

        # JVM Arguments Entry
        self.jvm_args_button = customtkinter.CTkButton(
            self,
            text="JVM Arguments",
            font=SETTINGS.get_gui("font_normal"),
            command=self.open_jvm_args_dialog_event
        )
        self.jvm_args_button.grid(row=1, column=0, padx=20, pady=10)

        # TODO: Add memory allocation slider

        # Reset Game Settings Button
        self.reset_game_settings_button = customtkinter.CTkButton(
            self,
            text="Reset Settings",
            font=SETTINGS.get_gui("font_normal"),
            command=self.reset_game_settings
        )
        self.reset_game_settings_button.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="s")

    def open_jvm_args_dialog_event(self):
        """Open the JVM Arguments dialog."""
        dialog = customtkinter.CTkInputDialog(
            text=f"{SETTINGS.get_game('jvm_args')}\n\nSeparate Args With Spaces",
            title="JVM Arguments"
        )
        user_input = dialog.get_input()
        if user_input is not None:
            SETTINGS.set_game(jvm_args=user_input.split())

    def reset_game_settings(self):
        """Reset the Game settings to the default values."""
        SETTINGS.reset_game()
        PopupWindow(
            master=self.master,
            title="Settings Reset",
            message="The Game settings have been reset to default."
        )


class SettingsWindow(customtkinter.CTkToplevel):
    """A window for the settings of the application."""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Settings")
        self.geometry("600x250")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # GUI Settings Frame
        self.gui_settings_frame = GUISettingsFrame(self)
        self.gui_settings_frame.grid(row=0, column=0, padx=(20, 0), pady=20)

        # User Settings Frame
        self.user_settings_frame = UserSettingsFrame(self)
        self.user_settings_frame.grid(row=0, column=1, padx=20, pady=20)

        # Game Settings Frame
        self.game_settings_frame = GameSettingsFrame(self)
        self.game_settings_frame.grid(row=0, column=2, padx=(0, 20), pady=20)

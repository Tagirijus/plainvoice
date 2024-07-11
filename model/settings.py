"""The class holding all the settings."""

import os
from click import argument
import yaml


class Settings:
    """
    This class holds certain settings like path to the program
    or program configs.
    """

    CONFIGFILE: str
    """
    The path to the config file for the program.
    """

    DATADIR: str
    """
    The string containing the path to the programs data directory.
    """

    DEFAULT_DUE_DAYS: int
    """
    The default number of days when an invoice is due.
    """

    EDITOR: str
    """
    The string for the shell command for the editor to use when
    editing files or the config.
    """

    PROJECT_PATH: str
    """
    The path to the programs python script path. This won't get stored
    in the config file, since it gets generated on runtime.
    """

    def __init__(self):
        self.DATADIR = os.path.join(os.path.expanduser("~"), '.plainvoice')
        self.CONFIGFILE = os.path.join(self.DATADIR, 'config.yaml')
        self.PROJECT_PATH = os.path.dirname(
            os.path.realpath(__file__)
        ).replace('/model', '')
        self.init_config()

    def default_config(self) -> None:
        """
        Set the default config.
        """
        self.EDITOR = 'vi'
        self.DEFAULT_DUE_DAYS = 14

    def get_config_as_dict(self) -> dict:
        """
        Get the config data as a dict.

        Returns:
            dict: The dictionary containing the config data.
        """
        return {
            'EDITOR': self.EDITOR,
            'DEFAULT_DUE_DAYS': self.DEFAULT_DUE_DAYS
        }

    def init_config(self) -> None:
        """
        Try to get the user set config and fill missing config
        parts with the default_config() output.
        """
        # first set the default config attributes
        self.default_config()

        # now try to load a config file and replace the respecting configs
        if os.path.exists(self.CONFIGFILE):
            with open(self.CONFIGFILE, 'r') as myfile:
                loaded_config_data = yaml.safe_load(myfile)
            self.overwrite_config(loaded_config_data)

    def overwrite_config(self, config_data: dict) -> None:
        """
        Overwrite the config with the given data.

        Args:
            config_data (dict): The new config data as a dict.
        """
        self.EDITOR = config_data.get('EDITOR', self.EDITOR)
        self.DEFAULT_DUE_DAYS = config_data.get(
            'DEFAULT_DUE_DAYS',
            self.DEFAULT_DUE_DAYS
        )

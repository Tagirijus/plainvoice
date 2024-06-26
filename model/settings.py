"""The class holding all the settings."""

import os
import yaml



class Settings:
    """Settings class."""

    def __init__(self):
        """Initialize the class."""
        self.DATADIR = os.path.join(os.path.expanduser("~"), '.plainvoice')
        self.CONFIGFILE = os.path.join(self.DATADIR, 'config.yaml')
        self.init_config()

    def default_config(self):
        """Set the default config."""
        self.EDITOR = 'vi'
        self.DEFAULT_DUE_DAYS = 14

    def overwrite_config(self, config_data):
        self.EDITOR = config_data.get('EDITOR', self.EDITOR)
        self.DEFAULT_DUE_DAYS = config_data.get('DEFAULT_DUE_DAYS', self.DEFAULT_DUE_DAYS)

    def get_config_as_dict(self):
        return {
            'EDITOR': self.EDITOR,
            'DEFAULT_DUE_DAYS': self.DEFAULT_DUE_DAYS
        }

    def init_config(self):
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

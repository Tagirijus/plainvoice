"""The class holding all the settings."""

import os
import yaml


class Settings:
    """
    This class holds certain settings like path to the program
    or program configs.
    """

    ADD_HELP_COMMENT: bool
    """
    If True the helping comment of all the settings parameters will be
    saved into the config.yaml as well. This can get handy, if you
    want to re-check which setting is for what.
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
        # soem base config attributes, which are needed on a
        # plain core basis; thus they are not being in
        # the self.default_config() method
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
        self.ADD_HELP_COMMENT = True
        self.EDITOR = 'vi'
        self.DEFAULT_DUE_DAYS = 14

    def file_exists(self) -> bool:
        """
        Checks if the config file in the programs data dir
        already is saved and exists or not.

        Returns:
            bool: Returns True if the file exists in the hoem data dir.
        """
        return os.path.exists(self.CONFIGFILE)

    def get_config_as_dict(self) -> dict:
        """
        Get the config data as a dict.

        Returns:
            dict: The dictionary containing the config data.
        """
        return {
            'ADD_HELP_COMMENT': self.ADD_HELP_COMMENT,
            'EDITOR': self.EDITOR,
            'DEFAULT_DUE_DAYS': self.DEFAULT_DUE_DAYS
        }

    def get_help_comment(self) -> str:
        """
        Return the help comment as a string. It should
        explain, what are the attributes / variables
        for etc.

        Returns:
            str: The help comment as a string.
        """
        return """
# This is the config file for plainvoice. Below are details
# about the possible settings.
#
#
# ADD_HELP_COMMENT:
#    If True, this text here always will be added to the
#    config.yaml at the beginning of the file.
#
# EDITOR:
#    Sets the terminal command for the editor to use, when
#    editing files. By default it is 'vi'.
#
# DEFAULT_DUE_DAYS:
#    The default due days to use, when calculating the due
#    date for invoices. By default it is '14'.

""".lstrip()

    def init_config(self) -> None:
        """
        Try to get the user set config and fill missing config
        parts with the default_config() output.
        """
        # first set the default config attributes
        self.default_config()

        # now try to load a config file and replace the respecting configs
        if self.file_exists():
            with open(self.CONFIGFILE, 'r') as yaml_file:
                loaded_config_data = yaml.safe_load(yaml_file)
            self.overwrite_config(loaded_config_data)

    def overwrite_config(self, config_data: dict) -> None:
        """
        Overwrite the config with the given data.

        Args:
            config_data (dict): The new config data as a dict.
        """
        self.ADD_HELP_COMMENT = config_data.get(
            'ADD_HELP_COMMENT',
            self.ADD_HELP_COMMENT
        )
        self.EDITOR = config_data.get(
            'EDITOR',
            self.EDITOR
        )
        self.DEFAULT_DUE_DAYS = config_data.get(
            'DEFAULT_DUE_DAYS',
            self.DEFAULT_DUE_DAYS
        )

    def save(self) -> bool:
        """
        Save the config file to the home data dir. Also,
        if enabled, add the help comment to the config.yaml
        file.

        Returns:
            bool: Returns True on success.
        """
        data_saved = self.save_data()
        if self.ADD_HELP_COMMENT:
            help_saved = self.save_add_help_comment()
        else:
            help_saved = True
        return data_saved and help_saved

    def save_add_help_comment(self) -> bool:
        """
        Add the help comment to the config.yaml.

        Returns:
            bool: Returns True on success.
        """
        try:
            with open(self.CONFIGFILE, 'r') as file:
                original_content = file.read()

            new_content = self.get_help_comment() + original_content

            with open(self.CONFIGFILE, 'w') as file:
                file.write(new_content)
            return True
        except Exception as e:
            print(e)
            return False

    def save_data(self) -> bool:
        """
        Save the pure variables / data into the
        config.yaml.

        Returns:
            bool: Returns True on success.
        """
        try:
            directory = os.path.dirname(self.CONFIGFILE)
            if (
                not os.path.exists(directory)
                and directory is not None
                and directory != ''
            ):
                os.makedirs(directory)
            with open(self.CONFIGFILE, 'w') as yaml_file:
                yaml.dump(
                    self.get_config_as_dict(),
                    yaml_file,
                    default_flow_style=False,
                    allow_unicode=True,
                    sort_keys=False
                )
            return True
        except Exception as e:
            print(e)
            return False

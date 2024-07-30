'''The class holding all the settings.'''

import os
import yaml


class Config:
    '''
    This class holds certain settings like path to the program
    or program configs.
    '''

    def __init__(self):
        # soem base config attributes, which are needed on a
        # plain core basis; thus they are not being in
        # the self.default_config() method

        self.datadir = os.path.join(os.path.expanduser('~'), '.plainvoice')
        '''
        The string containing the path to the programs data directory.
        '''

        self.configfile = os.path.join(self.datadir, 'config.yaml')
        '''
        The path to the config file for the program.
        '''

        self.project_path = os.path.dirname(
            os.path.realpath(__file__)
        ).replace('/model', '')
        '''
        The path to the programs python script path. This won't get stored
        in the config file, since it gets generated on runtime.
        '''

        self.init_config()

    def default_config(self) -> None:
        '''
        Set the default config.
        '''
        self.add_help_comment = True
        '''
        If True the helping comment of all the settings parameters will be
        saved into the config.yaml as well. This can get handy, if you
        want to re-check which setting is for what.
        '''

        self.client_filename_pattern = '{code}'
        '''
        The clients filename pattern. Since the Client class is a child of
        Document, yet with a hard-coded DocumentType, there would be no
        other place to define the filename_pattern otherwise.
        '''

        self.client_folder = '{app_dir}/clients'
        '''
        The folder in which the clients are being stored. This path is
        getting parsed by the File class, thus "{app_dir}" is available
        as a replacer to the plainvoices data dir.
        '''

        self.default_due_days = 14
        '''
        The default number of days when an invoice is due.
        '''

        self.editor = 'vi'
        '''
        The string for the shell command for the editor to use when
        editing files or the config.
        '''

        self.posting_folder = '{app_dir}/presets/postings'
        '''
        The folder of the postings. Basically saving a posting
        would mean "saving a preset of it". Thus the default
        folder is in the app dirs preset folder.
        '''

    def file_exists(self) -> bool:
        '''
        Checks if the config file in the programs data dir
        already is saved and exists or not.

        Returns:
            bool: Returns True if the file exists in the hoem data dir.
        '''
        return os.path.exists(self.configfile)

    def get_config_as_dict(self) -> dict:
        '''
        Get the config data as a dict.

        Returns:
            dict: The dictionary containing the config data.
        '''
        return {
            'add_help_comment': self.add_help_comment,
            'client_filename_pattern': self.client_filename_pattern,
            'client_folder': self.client_folder,
            'default_due_days': self.default_due_days,
            'editor': self.editor,
            'posting_folder': self.posting_folder,
        }

    def get_help_comment(self) -> str:
        '''
        Return the help comment as a string. It should
        explain, what are the attributes / variables
        for etc.

        Returns:
            str: The help comment as a string.
        '''
        return '''
# This is the config file for plainvoice. Below are details
# about the possible settings.
#
#
# add_help_comment:
#    If True, this text here always will be added to the
#    config.yaml at the beginning of the file.
#
# client_filename_pattern:
#    The pattern for the client filename in the client folder.
#    This is important for the "get next id" method, which will
#    look at the filenames of the clients and tries to get the
#    next highest id for new clients. By default is simply is
#    '{code}'.
#
# client_folder:
#    The folder in which the clients are being stored. You
#    can use '{app_dir}' as a variable inside the folder-string
#    to point to the programs data dir. By default it is
#    '{app_dir}/clients'.
#
# default_due_days:
#    The default due days to use, when calculating the due
#    date for invoices. By default it is '14'.
#
# editor:
#    Sets the terminal command for the editor to use, when
#    editing files. By default it is 'vi'.
#
# posting_folder:
#    The folder of the postings. Basically saving a posting
#    would mean "saving a preset of it". Thus the default
#    folder is in the app dirs preset folder.
#

'''.lstrip()

    def init_config(self) -> None:
        '''
        Try to get the user set config and fill missing config
        parts with the default_config() output.
        '''
        # first set the default config attributes
        self.default_config()

        # now try to load a config file and replace the respecting configs
        if self.file_exists():
            with open(self.configfile, 'r') as yaml_file:
                loaded_config_data = yaml.safe_load(yaml_file)
            self.overwrite_config(loaded_config_data)

    def overwrite_config(self, config_data: dict) -> None:
        '''
        Overwrite the config with the given data.

        Args:
            config_data (dict): The new config data as a dict.
        '''
        self.add_help_comment = config_data.get(
            'add_help_comment',
            self.add_help_comment
        )
        self.client_filename_pattern = config_data.get(
            'client_filename_pattern',
            self.client_filename_pattern
        )
        self.client_folder = config_data.get(
            'client_folder',
            self.client_folder
        )
        self.default_due_days = config_data.get(
            'default_due_days',
            self.default_due_days
        )
        self.editor = config_data.get(
            'editor',
            self.editor
        )
        self.posting_folder = config_data.get(
            'posting_folder',
            self.posting_folder
        )

    def save(self) -> bool:
        '''
        Save the config file to the home data dir. Also,
        if enabled, add the help comment to the config.yaml
        file.

        Returns:
            bool: Returns True on success.
        '''
        data_saved = self.save_data()
        if self.add_help_comment:
            help_saved = self.save_add_help_comment()
        else:
            help_saved = True
        return data_saved and help_saved

    def save_add_help_comment(self) -> bool:
        '''
        Add the help comment to the config.yaml.

        Returns:
            bool: Returns True on success.
        '''
        try:
            with open(self.configfile, 'r') as file:
                original_content = file.read()

            new_content = self.get_help_comment() + original_content

            with open(self.configfile, 'w') as file:
                file.write(new_content)
            return True
        except Exception as e:
            print(e)
            return False

    def save_data(self) -> bool:
        '''
        Save the pure variables / data into the
        config.yaml.

        Returns:
            bool: Returns True on success.
        '''
        try:
            directory = os.path.dirname(self.configfile)
            if (
                not os.path.exists(directory)
                and directory is not None
                and directory != ''
            ):
                os.makedirs(directory)
            with open(self.configfile, 'w') as yaml_file:
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

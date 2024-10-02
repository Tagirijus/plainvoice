'''
ConfigBase class

This class handles the config. It serves basic methods
for creating or updating the config and also for
loading it, of course.
'''

import os
import yaml


class ConfigBase:
    '''
    The config class, which can modify the config.
    '''

    def __init__(
        self,
        program_name: str = 'PROGRAM',
        data_dir: str = ''
    ):
        '''
        The config base class which serves certain methods
        to modify and gather the config.

        Args:
            program_name (str): \
                The name of the programm, which will be used for \
                creating and loading the config from the home users \
                dot folder with the program name; e.g. "PROGRAM" will \
                create "~/.PROGRAM/config.yaml" as a folder and its \
                config file accordingly.
            data_dir (str): \
                Optionally it is also possible to set a data_dir manually \
                directly. If left blank, the default data_dir will be set, \
                which is at the users home dot folder with the program name \
                as described by the program_name arguments doc string.
        '''
        self.program_name = program_name
        '''
        The Program name.
        '''

        self.data_dir = ''
        '''
        The string containing the path to the programs data directory.
        '''

        self.config_file = ''
        '''
        The path to the config file for the program.
        '''

        self.config_data = {}
        '''
        The config data are stored in this variable. The idea is that this
        class will be inherited on another class, which basically will
        fill the config data defaults and comments. Then this class serves
        methods, which will be able to create or update a config file in
        resective folder and also be able to load config data from it.
        '''

        self.project_path = os.path.dirname(
            os.path.realpath(__file__)
        ).replace('/model', '')
        '''
        The path to the programs python script path. This won't get stored
        in the config file, since it gets generated on runtime.
        '''

        # get the data_dir, which can be defined as a class initiation argument
        # or even as an ENVIRONMENT variable. the latter one will only be used,
        # if it is set and if the argument of the class initiation is not set.
        # the ENVIRONMENT variable to set is the "program name" in upper case
        # plus "_DATA_DIR". E.g. for the program name "app" it would be
        # "APP_DATA_DIR".
        data_dir_env = os.getenv(self.program_name.upper() + '_DATA_DIR')
        if data_dir == '' and data_dir_env is not None:
            data_dir = data_dir_env

        # change the data_dir and all depending internals accordingly
        self.change_data_dir(data_dir)

    def add_comments_on_config(self) -> bool:
        '''
        Add comments to the keys in the config, where comment
        strings exist.

        Returns:
            bool: Returns True on success.
        '''
        try:
            with open(self.config_file, 'r+') as file:
                content = file.readlines()
                file.seek(0)
                first_line = True
                for line in content:
                    for key, data in self.config_data.items():
                        if key + ':' in line:
                            comment = data['comment']
                            default = str(data['default'])
                            if isinstance(comment, str):
                                comment = [comment]
                            if default:
                                comment.append(  # noqa # type: ignore
                                    f'Default is \'{default}\'.'
                                )
                            comment = [com for com in comment if com]
                            comment = '\n# '.join(comment)
                            if not first_line:
                                file.write('\n')
                            file.write(f'# {comment}\n')
                    file.write(line)
                    first_line = False
            return True
        except Exception:
            return False

    def add_config(
        self,
        key: str,
        default: object,
        comment: str | list = ''
    ) -> None:
        '''
        Adds a config value.

        Args:
            key (str): \
                The key of the config entry.
            default (object): \
                The default value of the config entry.
            comment (str): \
                The comment to the config entry. Leave \
                empty for "no comment".
        '''
        self.config_data[key] = {
            'value': None,
            'default': default,
            'comment': comment
        }

    def change_data_dir(self, data_dir: str = '') -> None:
        '''
        Change the internal data_dir. If left blank, the default
        with the program name in the user folder will be used.

        Args:
            data_dir (str): The data dir string with an absolute path.
        '''
        if data_dir != '':
            self.data_dir = data_dir
        else:
            self.data_dir = os.path.join(
                os.path.expanduser('~'),
                '.' + self.program_name
            )

        # and set internals, which depend on the data_dir
        self.config_file = os.path.join(self.data_dir, 'config.yaml')

    def create_or_update_config(self):
        '''
        Load the config, set internal values accordingly
        and maybe update new keys with its defaults ot so.
        Also this method thus would create a new config
        for the programm on its first run.
        '''
        user_config = {}

        # first load user config, if it exists
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as yaml_file:
                user_config = yaml.safe_load(yaml_file)
        if not user_config:
            user_config = {}

        # set user config to the internal values
        for key, value in user_config.items():
            self.set(key, value)

        # set defaults for unset values
        for key, value in self.get_defaults().items():
            if key not in user_config:
                self.set(key, value)

        self.save()

    def get(self, key: str) -> object:
        '''
        Get a config value by its key.

        Args:
            key (str): The key to get the config value.

        Returns:
            object: Returns the value of the key.
        '''
        output = None
        if key in self.config_data:
            output = self.config_data[key]['value']
        return output

    def get_defaults(self) -> dict:
        '''
        Return the defaults as a dict without comments.

        Returns:
            dict: Returns the default dict config.
        '''
        output = {}
        for key, value in self.config_data.items():
            output[key] = value['default']
        return output

    def get_values(self) -> dict:
        '''
        Return the values as a dict without comments.

        Returns:
            dict: Returns the values dict config.
        '''
        output = {}
        for key, value in self.config_data.items():
            output[key] = value['value']
        return output

    def save(self) -> bool:
        '''
        Save the config.

        Returns:
            bool: Returns True on success.
        '''
        try:
            if not os.path.exists(self.data_dir):
                os.makedirs(self.data_dir)

            with open(self.config_file, 'w') as file:
                yaml.dump(
                    self.get_values(),
                    file,
                    default_flow_style=False,
                    allow_unicode=True
                )
            self.add_comments_on_config()
            return True
        except Exception:
            return False

    def set(self, key: str, value: object) -> None:
        '''
        Set a value to the given key. If it is not set internally
        as a config already, create it with the given value as a
        default value.

        Args:
            key (str): The key to set.
            value (str): The value to set for the key.
        '''
        if key in self.config_data:
            tmp = self.config_data[key]
            tmp['value'] = value
            self.config_data[key] = tmp
        else:
            self.add_config(key, value)
            self.set(key, value)

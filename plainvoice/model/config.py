'''
Config class

This class is the final config, which will "fill"
the ConfigBase.
'''

from .config_base import ConfigBase


class Config(ConfigBase):
    def __init__(self):
        super().__init__('plainvoice')

        self.add_config(
            'client_type',
            'client',
            [
                'The document type, which should represent clients.'
            ]
        )

        self.add_config(
            'date_output_format',
            '%d.%m.%Y',
            [
                'The date output format when dates are being printed to',
                'terminal.'
            ]
        )

        self.add_config(
            'editor',
            'vi',
            [
                'Sets the terminal command for the editor to use, when',
                'editing files.'
            ]
        )

        self.add_config(
            'scripts_folder',
            '{app_dir}/scripts',
            [
                'The folder where the scripts are stored. Use \'{app_dir}\'',
                'to use the app dirs folder.'
            ]
        )

        self.add_config(
            'templates_folder',
            '{app_dir}/templates',
            [
                'The folder where the templates are stored. Use \'{app_dir}\'',
                'to use the app dirs folder.'
            ]
        )

        self.add_config(
            'types_folder',
            '{app_dir}/types',
            [
                'The folder where the types are stored. Use \'{app_dir}\'',
                'to use the app dirs folder.'
            ]
        )

        self.add_config(
            'user_default_name',
            '',
            [
                'The defualt user DataModel to load + pass to every template',
                'rendering. Can be overwritten in commandline with the option',
                '--user / -u.'
            ]
        )

        self.add_config(
            'user_type',
            'users',
            [
                'The document type, which should represent clients. This can',
                'be used to e.g. handle multiple people on the same system',
                'using the programm. The user is a DataModel, which could,',
                'for example, get fixed fields for first / last name, etc.,',
                'which will always be passed to the template. Use the conigs',
                'user_default_name key to define the default user name. Leave',
                'empty so that no user will be loaded as a default.'
            ]
        )

        self.create_or_update_config()

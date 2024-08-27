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
            'editor',
            'vi',
            [
                'Sets the terminal command for the editor to use, when',
                'editing files.'
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
            'scripts_folder',
            '{app_dir}/scripts',
            [
                'The folder where the scripts are stored. Use \'{app_dir}\'',
                'to use the app dirs folder.'
            ]
        )

        self.create_or_update_config()

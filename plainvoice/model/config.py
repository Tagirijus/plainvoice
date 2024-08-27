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
                'The document type, which should represent clients.',
                'By default it is \'client\'.'
            ]
        )

        self.add_config(
            'editor',
            'vi',
            [
                'Sets the terminal command for the editor to use, when',
                'editing files. By default it is \'vi\'.'
            ]
        )

        self.create_or_update_config()

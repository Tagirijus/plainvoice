from model.settings import Settings

import os


class Template:
    """Render and posting templates model"""

    def __init__(self):
        """Initialize the class."""
        self.file = None

    def set_by_name(self, name):
        filename = os.path.join(Settings().DATADIR, 'templates', name + '.j2')
        if not os.path.exists(filename):
            return False
        else:
            self.file = filename
            return True

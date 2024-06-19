from model.settings import Settings

import os


class Template:
    """Render and posting templates model"""

    def __init__(self):
        """Initialize the class."""
        self.types = ['render', 'posting', 'invoice', 'quote']
        self.type = 'render'
        self.file = None

    def set_type(self, ttype):
        if ttype not in self.types:
            return False
        else:
            self.type = ttype
            return True

    def set_by_name(self, name):
        filename = os.path.join(Settings().DATADIR, 'templates', self.type, name + '.html')
        if not os.path.exists(filename):
            return False
        else:
            self.file = filename
            return True

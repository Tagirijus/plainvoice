class Templates(object):
    """Render and posting templates model"""

    def __init__(self):
        """Initialize the class."""
        self.types = ['render', 'posting', 'invoice', 'quote']

    def get_types(self):
        return self.types
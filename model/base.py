from controller.file import File


class Base:
    """Base class which implements loading and saving data"""

    def __init__(self):
        # basically set the defaults, due to the empty
        # dict, which is given as a parameter
        self.set_from_dict()

    def folder(self, filename):
        """
        Prepend the subfolder for this class. I am using
        .plainvoice as the folder inside home folder.
        And in this folder I simply use folders like
        "clients/" or "invoices/" as subfolder to
        store the elements / data in. So change this
        string to the correct subfolder then when
        inheriting from this class.
        """
        return 'BASE/' + filename

    def set_from_dict(self, values={}):
        # do stuff like:
        # self.value = values.get('value', '')
        pass

    def get_as_dict(self):
        return {}

    def load(self, filename):
        try:
            data = File().load(self.folder(filename))
            self.set_from_dict(data)
            return True
        except Exception as e:
            # print(e)
            return False

    def save_check(self):
        """
        This method can be used to do internal checkings
        before sacving. E.g. a class attribute may not
        be empty or so.

        Future reminder to myself: for clients previously
        I did not allow to save a client without any
        client_id nor with a client_id, which already
        exists. In this method I maybe could implement
        such a thing, in case I need it. Otherwise this
        method is just unused - no problem. (;
        """
        return True

    def save(self, filename):
        try:
            if self.save_check():
                data = self.get_as_dict()
                return File().save(self.folder(filename), data)
            else:
                return False
        except Exception as e:
            # print(e)
            return False

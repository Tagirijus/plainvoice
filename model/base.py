from datetime import datetime
from model.file import File
from view import error_printing


class Base:
    """Base class which implements loading and saving data"""

    def __init__(self):
        # basically set the defaults, due to the empty
        # dict, which is given as a parameter
        self.set_from_dict()

    def folder(self, filename=''):
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
        """
        Basically this is an empty abstract method.
        It should be fillde with the needed data
        for the dict "import" of the respecting
        class.

        Do stuff like:
        self.value = values.get('value', '')
        """
        pass

    def get_as_dict(self):
        """
        Basically this is an empty abstract method.
        It should be filled with the needed data
        for the dict "export" of the respecting
        class.
        """
        return {}

    def load_from_yaml_file(self, filename, in_data_dir=True):
        """
        With this method you can load the classes attributes
        etc. from a YAML file. By default in_data_dir is set
        to True, which means that the filename can be a
        relative filename from the ~/.plainvoice folder.
        Otherwise when set to false it should either be
        a relative path from where the programm gets started
        or even an absolute file path.
        """
        try:
            if in_data_dir:
                data = File().load_dict_from_yaml_file(self.folder(filename), in_data_dir)
            else:
                data = File().load_dict_from_yaml_file(filename, in_data_dir)
            self.set_from_dict(data)
            return True
        except Exception as e:
            error_printing.print_if_verbose(e)
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

    def save_to_yaml_file(self, filename, in_data_dir=True):
        """
        With this method you simply can save all the class
        attributes to a YAML file. By default in_data_dir
        is set to True, which means that the filename should
        be used as a filename relative to the ~/.plainvoice
        folder. Otherwise when set to False you should use
        a relative filename from where the programm was
        started or even use an absolute filename.
        """
        try:
            if self.save_check():
                data = self.get_as_dict()
                if in_data_dir:
                    return File().save_dict_to_yaml_file(data, self.folder(filename), in_data_dir)
                else:
                    return File().save_dict_to_yaml_file(data, filename, in_data_dir)
            else:
                return False
        except Exception as e:
            error_printing.print_if_verbose(e)
            return False

    def datetime_from_dict_key(self, dic, key, default=None):
        """
        This method tries to get a datetime from the value
        of the dict with the given key. If there is no
        value behind that key, a new datetime will be
        created instead an returned, if "default" is set
        to 'now'. Otherwise None gets returned.

        Well, if there is a datetime behind that dicts key,
        this will get returned, of course.
        """
        if default == 'now':
            date_tmp = dic.get(key, datetime.now())
        else:
            date_tmp = dic.get(key, None)
        if not isinstance(date_tmp, datetime) and date_tmp is not None:
            return datetime.strptime(date_tmp, '%Y-%m-%d')
        else:
            return date_tmp

    def datetime2str(self, value):
        """
        Simply convert a datetime to an ISO 8601 formatted string.
        """
        return value.strftime('%Y-%m-%d') if isinstance(value, datetime) else None

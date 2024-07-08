from datetime import datetime
from model.files import Files
from view import error_printing


class Base:
    """
    Base class which implements loading and saving data.
    """

    FOLDER: str
    """
    The base folder for the child of this parent class.
    """

    def __init__(self):
        self.FOLDER = 'BASE/'
        # basically set the defaults, due to the empty
        # dict, which is given as a parameter
        self.set_from_dict()

    def get_folder(self, filename: str = '') -> str:
        """
        Prepend the subfolder for this class. I am using
        .plainvoice as the folder inside home folder.
        And in this folder I simply use folders like
        "clients/" or "invoices/" as subfolder to
        store the elements / data in. So change this
        string to the correct subfolder then when
        inheriting from this class.

        Args:
            filename (str): The given filename to prepend. (default: `''`)

        Returns:
            str: The new filename with the prepenaded folder of the class.
        """
        return self.FOLDER + filename

    def set_from_dict(self, values: dict = {}) -> None:
        """
        Basically this is an empty abstract method.
        It should be fillde with the needed data
        for the dict "import" of the respecting
        class.

        Do stuff like:
        self.value = values.get('value', '')

        Args:
            values (dict): The values to set. (default: `{}`)
        """
        pass

    def get_as_dict(self) -> dict:
        """
        Basically this is an empty abstract method.
        It should be filled with the needed data
        for the dict "export" of the respecting
        class.

        Returns:
            dict: The dictionary containing the attributes.
        """
        return {}

    def load_from_yaml_file(
        self,
        filename: str,
        in_data_dir: bool = True
    ) -> bool:
        """
        With this method you can load the classes attributes
        etc. from a YAML file. By default in_data_dir is set
        to True, which means that the filename can be a
        relative filename from the ~/.plainvoice folder.
        Otherwise when set to false it should either be
        a relative path from where the programm gets started
        or even an absolute file path.

        Args:
            filename (str): \
                The filename of the yaml file.
            in_data_dir (bool): \
                If True the filename should be relative and points \
                to inside the .plainvoice folder. (default: `True`)

        Returns:
            bool: Returns True if loading succeeded.
        """
        try:
            if in_data_dir:
                data = Files().load_dict_from_yaml_file(
                    self.get_folder(filename),
                    in_data_dir
                )
            else:
                data = Files().load_dict_from_yaml_file(
                    filename,
                    in_data_dir
                )
            self.set_from_dict(data)
            return True
        except Exception as e:
            error_printing.print_if_verbose(e)
            return False

    def save_check(self) -> bool:
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

        Returns:
            bool: Returns True if the check succeeded.
        """
        return True

    def save_to_yaml_file(
        self,
        filename: str,
        in_data_dir: bool = True
    ) -> bool:
        """
        With this method you simply can save all the class
        attributes to a YAML file. By default in_data_dir
        is set to True, which means that the filename should
        be used as a filename relative to the ~/.plainvoice
        folder. Otherwise when set to False you should use
        a relative filename from where the programm was
        started or even use an absolute filename.

        Args:
            filename (str): \
                The filename of the yaml file to save to.
            in_data_dir (bool): \
                If True the filename should be relative and points \
                to inside the .plainvoice folder. (default: `True`)

        Returns:
            bool: Returns True if saving succeeded.
        """
        try:
            if self.save_check():
                data = self.get_as_dict()
                if in_data_dir:
                    return Files().save_dict_to_yaml_file(
                        data,
                        self.get_folder(filename),
                        in_data_dir
                    )
                else:
                    return Files().save_dict_to_yaml_file(
                        data,
                        filename,
                        in_data_dir
                    )
            else:
                return False
        except Exception as e:
            error_printing.print_if_verbose(e)
            return False

    def datetime_from_dict_key(
        self,
        dic: dict,
        key: str,
        default: str = ''
    ):
        """
        This method tries to get a datetime from the value
        of the dict with the given key. If there is no
        value behind that key, a new datetime will be
        created instead an returned, if "default" is set
        to 'now'. Otherwise None gets returned.

        Well, if there is a datetime behind that dicts key,
        this will get returned, of course.

        Args:
            dic (dict): \
                The dict to use this method on.
            key (str): \
                The key containing the datetime.
            default| None ([type]): \
                If the default is 'now', the datetime,
                when not possible to get, will be
                today. (default: ``)
        """
        if default == 'now':
            date_tmp = dic.get(key, datetime.now())
        else:
            date_tmp = dic.get(key, None)
        if not isinstance(date_tmp, datetime) and date_tmp is not None:
            return datetime.strptime(date_tmp, '%Y-%m-%d')
        else:
            return date_tmp

    def datetime2str(self, value: datetime) -> str:
        """
        Simply convert a datetime to an ISO 8601 formatted string.

        Args:
            value (datetime): Must be a datetime to get the date from.

        Returns:
            str: The ISO 8601 date string.
        """
        return (
            value.strftime('%Y-%m-%d') if isinstance(value, datetime) else ''
        )

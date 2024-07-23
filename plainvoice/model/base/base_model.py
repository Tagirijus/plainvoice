'''
BaseModel Class

This class is the base class for any kind of data object of this program. The
idea behind this structure / principle is to have an object, which is savable
into a file automatically with a given name and folder. It's about simple
abstraction based on just a few values (name and folder) to be able to
save, yet also load such a data object.

The Base class has the BaseRepository class as a component for file operations.
With this it can load its data from file or save it to it.

Accordingly there are certain methods for filling this objects attributes from
dict and also convert it back to a dict or even a YAML string. This shall be
the main principle for loading and saving data. New classes, which will inherit
from this class, should probably implement the methods by overwriting the
needed methods and maybe using e.g. 'super().from_dict(values)' inside this
method to still use the parents method. This way it is possible to inherit the
main functions of such methods, while being able to extend them (in case there
are new class attributes to be filled with the from_dict() method, for
example).
'''


from .base_repository import BaseRepository


class BaseModel:
    '''
    Base class for the apps data class.
    '''

    DEFAULT_NAME: str = 'dummy'
    '''
    The default name fo the object, if nothing is set.
    '''

    DEFAULT_FOLDER: str = './'
    '''
    The default folder fo the object, if nothing is set.
    '''

    def __init__(
        self,
        name: str = '',
        folder: str = ''
    ):
        '''
        The base class for the apps data structure.
        '''

        self.id = None
        '''
        The id of the class. For an invoice this could be used as
        an invoice id, for example.
        '''

        self.name = self.DEFAULT_NAME if name == '' else name
        '''
        Basically the filename without the extension.
        '''

        self.repository = BaseRepository(
            self.DEFAULT_FOLDER if folder == '' else folder
        )
        '''
        The BaseRepository for loading and storing data into the object.
        '''

        self.visible = True
        '''
        Sets if the data set should be visible when e.g. listing datas
        and this data would be hidden in such a list then.
        '''

    @classmethod
    def create_instance(cls):
        return cls()

    def from_dict(self, values: dict) -> None:
        '''
        This is basically an abstract method, which
        should be overwritten by the child. It is for
        filling the class attributes from a dict.

        Args:
            values (dict): The dict to load the attributes from.
        '''
        self._from_dict_base(values)

    def _from_dict_base(self, values: dict) -> None:
        '''
        This is basically an abstract method, which
        should be overwritten by the child. It is for
        filling the class attributes from a dict.

        Args:
            values (dict): The dict to load the attributes from.
        '''
        self.id = values.get('id') or self.id
        self.name = values.get('name') or self.name
        self.visible = bool(values.get('visible', True))

    def get(self, key: str) -> object:
        '''
        Get data from this object or its self.data_user dict
        or the self.data_required dict.

        Args:
            key (str): The key of the object or maybe the self.data dict.

        Returns:
            object: Returns the value, if found, or an empty string.
        '''
        return self.to_dict().get(key, None)

    def get_list(self, show_only_visible: bool = True) -> list:
        """
        Get a list with all automatically loaded data objects
        according to the given folder.

        Args:
            show_only_visible (bool): \
                Show only the documents with the attribute set \
                to "self.visivble = True" in the output list. \
                Here it's data['visible'], since they are still \
                dicts, of course.

        Returns:
            list: Returns a list containing the objects of this class.
        """
        final_list = []
        for data_dict in self.repository.get_list(show_only_visible):
            tmp_object = self.create_instance()
            tmp_object.from_dict(data_dict)
            final_list.append(tmp_object)
        return final_list

    def load_from_name(self, name: str) -> None:
        """
        Load the data object from just it's name. The
        method will look into the data objects folder
        in the program's folder automatically.

        Args:
            name (str): The name of the data object.
        """
        self.name = name
        self.from_dict(self.repository.load_from_name(name))

    def rename(self, new_name: str) -> bool:
        """
        This method renames the data object and also
        it's file.

        Args:
            new_name (str): The new name to set.

        Returns:
            bool: Returns True on success.
        """
        old_name = self.name
        self.name = new_name
        # only also rename the file, if there is a file
        if self.repository.file.exists(old_name):
            return self.repository.rename(old_name, new_name)
        else:
            return True

    def save(self) -> bool:
        """
        Save the datas attributes to a file. All the attributes
        form the to_dict() methods are being used here. The
        filename is generated automatically from the datas
        name and the path is used by the BaseRepository
        File class's attribute folder.

        Returns:
            bool: Returns True on success.
        """
        return self.repository.save(self.to_yaml_string(), self.name)

    def set(self, fieldname: str, value) -> bool:
        '''
        Set into the field with the given fieldname the given value.

        Args:
            fieldname (str): The fieldname to set the value for.
            value (object): The value to set.

        Returns:
            bool: Returns True on success.
        '''
        try:
            if fieldname == 'folder':
                self.repository.set_folder(str(value))
            elif fieldname == 'id':
                self.id = str(value)
            elif fieldname == 'visible':
                self.visible = bool(value)
            return True
        except Exception:
            return False

    def to_dict(self) -> dict:
        """
        This method is for exporting all the needed data
        of the object to a dict.

        Returns:
            dict: Returns the data as a dict.
        """
        return {
            'id': self.id,
            'visible': self.visible
        }

    def to_yaml_string(self) -> str:
        '''
        Convert the object to a YAML string, including comments
        for better structuring the file and for it to be better
        human readable.

        Returns:
            str: Return the final YAML string.
        '''
        output = self.repository.file.to_yaml_string(self.to_dict())
        return output

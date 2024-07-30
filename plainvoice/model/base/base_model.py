'''
BaseModel Class

This class is supposed to be the base structure of an object.
Basically it's some kind of interface after all. With this
I want to have some very basic method / technique with which
the programm can convert data to YAML and vice versa.
'''


class BaseModel:
    '''
    Base class for the apps data class.
    '''

    def __init__(self, filename: str):
        '''
        The base class for the apps data structure.
        '''

        self.filename = filename
        '''
        The absolute filename for this data object.
        '''

        self.visible = True
        '''
        Sets if the data set should be visible when e.g. listing datas
        and this data would be hidden in such a list then.
        '''

    @classmethod
    def create_instance(cls, filename: str):
        return cls(filename)

    def from_dict(self, values: dict) -> None:
        '''
        This is basically an abstract method, which
        should be overwritten by the child. It is for
        filling the class attributes from a dict.

        Yet self._from_dict_base(values) can be used,
        or maybe even should be used inside the overwritten
        childs method so that base attributes will also
        be filled on loading from dict.

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
        self.filename = values.get('filename', self.filename)
        self.visible = bool(values.get('visible', self.visible))

    def get_filename(self) -> str:
        '''
        Get the absolute filename of this object.

        Returns:
            str: Returns the absolute filename as a string.
        '''
        return self.filename

    def hide(self) -> None:
        '''
        Hide the object. Set internal visible attribute to False.
        '''
        self.visible = False

    def is_visible(self) -> bool:
        '''
        Return if this object is visible or not.

        Returns:
            bool: Returns True if visible, else False.
        '''
        return self.visible

    def set_filename(self, filename: str) -> None:
        '''
        Set the absolute filename to this data object.

        Args:
            filename (str): The absolute filename to this data object.
        '''
        self.filename = filename

    def show(self) -> None:
        '''
        Show the object. Set internal visible attribute to True.
        '''
        self.visible = True

    def to_dict(self) -> dict:
        '''
        This method is for exporting all the needed data
        of the object to a dict. Like the from_dict()
        method it is some kind of abstract method and should
        be overwritten by the child class. self._to_dict_base()
        should also be used to get the base attributes as well.

        Returns:
            dict: Returns the data as a dict.
        '''
        output = {}
        output.update(self._to_dict_base())
        return output

    def _to_dict_base(self) -> dict:
        '''
        Get the base attributes of this object as a dict.

        Returns:
            dict: Returns base attributes as a dict.
        '''
        return {
            'visible': self.visible
        }

from datetime import datetime
from decimal import Decimal
from plainvoice.utils import date_utils


class Base:
    """
    Base class which implements the flexible data-dict, the
    user can set in the YAML later to have as many fields
    as they want. This class should be inherited by
    Invoice or Client.
    """

    data: dict = {}
    """
    The internal objects dict, which can store all needed additional
    data.
    """

    def get(self, key: str) -> object:
        """
        Get data from this object or its self.data dict.

        Args:
            key (str): The key of the object or maybe the self.data dict.

        Returns:
            object: Returns the value, if found, or an empty string.
        """
        fetched = self.to_dict().get(key, '_NONE')
        if fetched == '_NONE':
            fetched = self.data.get(key, '_NONE')
        return '' if fetched == '_NONE' else fetched

    def to_dict(self) -> dict:
        """
        Convert the object to a dict.

        Returns:
            dict: Class attributes and the self.data as a dict.
        """
        out = {}
        for key in self.__dict__:
            value = self.__dict__[key]
            # store Decimal as float
            if isinstance(value, Decimal):
                out[key] = float(value)
            # datetimes as a YYYY-MM-DD string
            elif isinstance(value, datetime):
                out[key] = date_utils.datetime2str(value)
            # PostingsList as list having Postings
            # being converted to dicts
            elif value.__class__.__name__ == 'PostingsList':
                out[key] = value.to_dicts()
            # convert a single Posting to dict
            elif value.__class__.__name__ == 'Posting':
                out[key] = value.to_dict()
            # fallback: just output the value
            else:
                out[key] = value

        return out

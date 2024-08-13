'''
Document Class

This class is the main document object. It can be anything, due to the
DocumentType class, which is able to describe the fixed fields of an
instance of Document.

The idea is that the program is all about such documents in the end.
That's why I tried to make them as flexible as possible. Sure it
could have been handled all with just a dict, which the user could
define or so. And then just take the dict to be used inside the
Jinja renderer. Yet I wanted to have some kid of intuitive document
handling inside the YAML file. I wanted to have such a file be
structure by certain field types: base, fixed and additional.
These are the main concept points of the DataModel (from which this
class also is inherited).

The base fields are data related attributes. For the document it shall
be the "visible" state, yet additionally also the "document_type" and
(still in dev) the "links" to represent links between other DataModel
objects.

Then there are the fixed fields. The concept behind them is to have
fields, which are "always there", even if no value is given. Then
there should be a default at least. The idea behind this is that
there always shoudl be keys in the YAML for new documents so that
the user knows which fields are supposed to be used for a certain
document. E.g. an invoice should probably have a "date" field.
Then "date" could be added as a fixed field so that for new invoices
there will always be "date" as a key with a default value in the
new YAML file already.

Finally there are the additional fields, which are basically just
keys, which may exist in the YAML and the DataModel assigns them
to the internal additional fields dict. That way a user can even
have additional key+value paris on the fly to be used in the
Jinja template later directly.
'''


from plainvoice.model.data.data_model import DataModel
from plainvoice.model.posting.posting import Posting
from plainvoice.model.posting.postings_list import PostingsList
from plainvoice.model.quantity.quantity import Quantity
from plainvoice.model.quantity.price import Price
from plainvoice.model.quantity.percentage import Percentage

from datetime import datetime, timedelta
from decimal import Decimal


class Document(DataModel):
    '''
    Base class which implements the flexible DataModel system.
    '''

    def __init__(
        self,
        doc_typename: str = '',
        abs_filename: str = ''
    ):
        '''
        The document object, which can be any DocumentType
        and thus will get fields accordingly.

        Args:
            doc_typename (str): \
                The name of the document type to use. \
                The program will load it from the app_folder \
                and use this loaded document type then.
        '''

        super().__init__()

        self.abs_filename: str = abs_filename
        '''
        The absolute filename of the document. Will probably be used
        by the DocumentRepository and the DocumentLink class.
        '''

        self.doc_typename: str = doc_typename
        '''
        The name of the document type.
        '''

        self.links: list[str] = []

        self._init_fixed_fields()

    def add_days_to_date(self, fieldname: str, days: int) -> None:
        '''
        Add days to the date, which is supposed to be on the field
        with the given fieldname.

        Args:
            fieldname (str): The fieldname of the date field type.
            days (int): The days to add (or negative to substract).
        '''
        date = self.get_fixed(fieldname, False)
        if isinstance(date, datetime):
            date = date + timedelta(days=days)
            self.set_fixed(fieldname, date, False)

    def add_link(self, abs_filename: str) -> None:
        '''
        Add an absolute filename of another document to the
        linked documents list.

        Args:
            abs_filename (str): The absolute filename of the other document.
        '''
        if abs_filename not in self.links:
            self.links.append(abs_filename)

    def _from_dict_base(self, values: dict) -> None:
        '''
        Overwrites the DataModel _from_dict_base() method
        and adds own attributes loader.

        Args:
            values (dict): \
                The values to load the base attributes from.
        '''
        super()._from_dict_base(values)
        self.doc_typename = values.get('doc_typename', self.doc_typename)
        self.links = values.get('links', self.links)

    def get_filename(self) -> str:
        '''
        Get the absolute filename of this document. This will be
        used by DocumentRepository and/or DocumentLink mainly. So
        it's not needed for the integrity of the data model itself.
        So it also will not be saved into the YAML later, since ...
        well it's the filename to that YAML after all, probably!

        Returns:
            str: Returns the absolute filename as a string.
        '''
        return self.abs_filename

    def get_document_typename(self) -> str:
        '''
        Get the document type name.

        Returns:
            str: Returns document type name as string.
        '''
        return self.doc_typename

    def get_links(self) -> list[str]:
        '''
        Get the list with the absolute filenames of the
        linked documents.

        Returns:
            str: Returns linked documents filenames list.
        '''
        return self.links

    def _init_fixed_fields(self) -> None:
        '''
        Initialize the fixed fields for this special DataModel child.

        Since this is the universal Document class, which the user
        can define with DocumentType, I already add all possible
        field types here already to make it as flexible as possible.
        '''

        # Python basics
        self.define_fixed_field_type('str', str, str)
        self.define_fixed_field_type('int', int, int)
        self.define_fixed_field_type('dict', dict, dict)
        self.define_fixed_field_type('list', list, list)

        # additional Python modul types
        self.define_fixed_field_type(
            'date',
            lambda x: datetime.strptime(x, '%Y-%m-%d'),
            lambda x: x.strftime('%Y-%m-%d')
        )
        self.define_fixed_field_type(
            'Decimal',
            lambda x: Decimal(str(x)),
            float
        )

        # plainvoice types
        self.define_fixed_field_type(
            'Percentage',
            lambda x: Percentage(str(x)),
            str
        )
        self.define_fixed_field_type(
            'Posting',
            lambda x: Posting().instance_from_dict(x),
            lambda x: x._to_dict_fixed(True)
        )
        self.define_fixed_field_type(
            'PostingsList',
            lambda x: PostingsList().instance_from_list(x),
            lambda x: x.get_postings(True)
        )
        self.define_fixed_field_type(
            'Price',
            lambda x: Price(str(x)),
            str
        )
        self.define_fixed_field_type(
            'Quantity',
            lambda x: Quantity(str(x)),
            str
        )

    def link_exists(self, abs_filename: str) -> bool:
        '''
        Check if the given absolute filename exists in the links;
        so basically it's a check if the link to a document with
        the given absolute filename exists as a link.

        Args:
            abs_filename (str): The absolute filename of the other document.

        Returns:
            bool: Returns True if it exists.
        '''
        return abs_filename in self.links

    def remove_link(self, abs_filename: str) -> None:
        '''
        Remove an absolute filename of another document from the
        linked documents list.

        Args:
            abs_filename (str): The absolute filename of the other document.
        '''
        if abs_filename in self.links:
            self.links.remove(abs_filename)

    def set_filename(self, abs_filename: str) -> None:
        '''
        Set the absolute filename of this document. This will be
        used by DocumentRepository and/or DocumentLink mainly. So
        it's not needed for the integrity of the data model itself.
        So it also will not be saved into the YAML later, since ...
        well it's the filename to that YAML after all, probably!

        Args:
            abs_filename (str): The absolute filename to set.
        '''
        self.abs_filename = abs_filename

    def set_document_typename(self, doc_typename: str = '') -> None:
        '''
        Set the document typename.

        Args:
            doc_typename (str): The name of the document type.
        '''
        self.doc_typename = doc_typename

    def set_links(self, links: list[str] = []) -> None:
        '''
        Set the linked documents filenames list.

        Args:
            links (list): The list containing the absolute document filenames.
        '''
        self.links = links

    def _to_dict_base(self) -> dict:
        '''
        Overwrites the DataModel _to_dict_base() method
        and adds own attributes on top of it.

        Returns:
            dict: Returns the base attributes as a dict.
        '''
        output = super()._to_dict_base()
        output.update({
            'doc_typename': self.get_document_typename(),
            'links': self.get_links()
        })
        return output

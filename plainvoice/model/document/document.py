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
from plainvoice.model.document.document_type import DocumentType
from plainvoice.model.posting.posting import Posting
from plainvoice.model.posting.postings_list import PostingsList
from plainvoice.model.quantity.quantity import Quantity
from plainvoice.model.quantity.price import Price
from plainvoice.model.quantity.percentage import Percentage

from datetime import datetime, timedelta
from decimal import Decimal


def date_to_internal(value: str | None) -> datetime | None:
    '''
    Convert the readable string (or None) for a date
    type to the internal value.

    Args:
        value (str | None): The value to convert.

    Return:
        datetime: Returns the converted datetime object.
    '''
    if value is not None:
        if value.startswith(('+', '-')):
            try:
                days = float(value)
            except Exception:
                # fallback is just "today"
                days = 0
            date = datetime.now()
            date = date + timedelta(days=days)
            return date
        else:
            return datetime.strptime(value, '%Y-%m-%d')
    else:
        return None


class Document(DataModel):
    '''
    Base class which implements the flexible DataModel system.
    '''

    def __init__(
        self,
        doc_typename: str = '',
        name: str = ''
    ):
        '''
        The document object, which can be any DocumentType
        and thus will get fields accordingly.

        Args:
            doc_typename (str): \
                The name of the document type to use. \
                The program will load it from the app_folder \
                and use this loaded document type then.
            name (str): \
                The name of the DataModel, which canbe used \
                to save it with its repository so that there \
                is no need to pass the name to the repository's \
                save method.
        '''

        super().__init__(name)

        self.abs_filename: str = ''
        '''
        The absolute filename of the document. Will probably be used
        by the DocumentRepository and the DocumentLink class.
        '''

        self.date_due_fieldname = ''
        '''
        The field name which will hold the due date. This attribute
        will be set by the DocumentType with the init_internals_with_doctype()
        method later.
        '''

        self.date_done_fieldname = ''
        '''
        The field name which will hold the done / paid date. This attribute
        will be set by the DocumentType with the init_internals_with_doctype()
        method later.
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

    def days_between_dates(
        self,
        fieldname_a: str,
        fieldname_b: str
    ) -> int | None:
        '''
        Calculate the numnber of days between two dates, which are
        supposed to be on the fields a and b. This method is supposed
        to be used as some kind of "calculate the due date" thing.
        E.g. you might want to have an invoice date (fieldname!) as
        fieldname_a and the due_date of an invoice as fieldname_b.
        This method will find the dates and calculate their difference
        in days and return this. If one of the dates is null or if
        the fields do not exist or so, the fallback is always -1.

        Args:
            fieldname_a (str): \
                The fieldname under whcih the first date exists.
            fieldname_b (str): \
                The fieldname under whcih the second date exists.

        Returns:
            int | None: \
                Returns an int representing the day difference of the dates \
                or None.
        '''
        date_a = self.get_fixed(fieldname_a, False)
        date_b = self.get_fixed(fieldname_b, False)
        if (
            not isinstance(date_a, datetime)
            or not isinstance(date_b, datetime)
        ):
            return None
        date_difference = date_a - date_b
        return abs(date_difference.days)

    def days_till_due_date(self, from_date_fieldname: str = '') -> int | None:
        '''
        Get the days as an integer till due. It is the difference
        from either the date of the given fieldname, or if non is given
        from today to the due date. Will return None, if there is no due
        date set or the fieldname for the due date is set incorrectly
        by the DocumentType in the method init_internals_with_doctype().

        Args:
            from_date_fieldname (str): \
                If given, use the date on the fixed field with this \
                name as the from-date.

        Returns:
            int | None: Returns days as integer or None.
        '''
        # get both dates
        from_date = self.get_now_or_date(from_date_fieldname)
        due_date = self.get_fixed(
            self.date_due_fieldname,
            False
        )

        # it has to be both dates
        if (
            not isinstance(from_date, datetime)
            or not isinstance(due_date, datetime)
        ):
            return None

        # calculate and return
        date_difference = due_date - from_date
        return date_difference.days

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

    def get_done_date(self, readable: bool) -> datetime | str | None:
        '''
        Get the done / paid date, while the field on which it is put
        has to be described by the DocumentType, which was
        used in the init_internals_with_doctype() method.

        Args:
            readable (bool): If True get readbale, else internal.

        Returns:
            datetime: Returns the datetime or None.
        '''
        return self.get(self.date_done_fieldname, readable)

    def get_due_date(self, readable: bool) -> datetime | str | None:
        '''
        Get the due date, while the field on which it is put
        has to be described by the DocumentType, which was
        used in the init_internals_with_doctype() method.

        Args:
            readable (bool): If True get readbale, else internal.

        Returns:
            datetime: Returns the datetime or None.
        '''
        return self.get(self.date_due_fieldname, readable)

    def get_links(self) -> list[str]:
        '''
        Get the list with the absolute filenames of the
        linked documents.

        Returns:
            str: Returns linked documents filenames list.
        '''
        return self.links

    def get_now_or_date(
        self,
        date_fieldname: str = ''
    ) -> datetime | None:
        '''
        Get now as a datetime if no field name is given. Otherwise
        try to get the datetime from that field. If no found, return None.
        Also if used now, set the datetime to only use the date by
        setting its time of the day to 0:00:00.000 o'clock.

        Args:
            date_fieldname (str): \
                If given, use the date on the fixed field with this \
                name as the from-date.

        Returns:
            datetime | None: \
                Return either now if no field name is given, or \
                the date on the fixed field. If none found, \
                return None.
        '''
        if date_fieldname == '':
            output = datetime.now()
            # the now date probably contains time of the day,
            # which has to be removed so that the correct days
            # in difference will be calculated
            output = output.replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0
            )
        else:
            output = self.get_fixed(date_fieldname, False)
        return output

    def init_internals_with_doctype(self, document_type: DocumentType) -> None:
        '''
        Init internal attributs etc. with the given DocumentType object.

        Args:
            document_type (DocumentType): \
                The document type object to get some needed \
                variables from. It is also a DataModel.
        '''
        self.set_fixed_fields_descriptor(
            document_type.get_descriptor()
        )
        self.date_due_fieldname = document_type.get_fixed(
            'date_due_fieldname',
            True
        )
        self.date_done_fieldname = document_type.get_fixed(
            'date_done_fieldname',
            True
        )

    def _init_fixed_fields(self) -> None:
        '''
        Initialize the fixed fields for this special DataModel child.

        Since this is the universal Document class, which the user
        can define with DocumentType, I already add all possible
        field types here already to make it as flexible as possible.
        '''

        # Python basics
        self.define_fixed_field_type('bool', bool, bool)
        self.define_fixed_field_type('str', str, str)
        self.define_fixed_field_type('int', int, int)
        self.define_fixed_field_type('dict', dict, dict)
        self.define_fixed_field_type('list', list, list)

        # additional Python modul types
        self.define_fixed_field_type(
            'date',
            lambda x: date_to_internal(x),
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

    def is_done(self) -> bool:
        '''
        Check if the date on the repsective date fixed field
        for "done date" is set.

        Returns:
            bool: Returns True if there is a date on that field.
        '''
        return self.get_fixed(self.date_done_fieldname, False) is not None

    def is_overdue(self, from_date_fieldname: str = '') -> bool:
        '''
        Check if the document is overdue. Do this by using either
        now as the from-date or the date on the given field
        name, which is supposed to be the from-date then. It
        calculates the difference in these dates. If this
        difference is equal or lower than 0, the document is
        overdue. BUT if there is a done-date set it has higher
        priority in this logic and sets the document not
        to oevrdue.

        Args:
            from_date_fieldname (str): \
                If given, use the date on the fixed field with this \
                name as the from-date.

        Returns:
            bool: Returns True if document is overdue.
        '''
        days = self.days_till_due_date(from_date_fieldname)
        if days is None:
            # the logic here is: if there is no date found, which
            # will result in the method returning None, there
            # seem to be noe due date either. This means that
            # the document technically cannot be overdue at all
            return False
        # otherwise it has to be checked if there either is still
        # time reminaing in days, OR if there even already is a
        # done date set
        done_date = self.get_fixed(self.date_done_fieldname, False)
        return days <= 0 and done_date is None

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

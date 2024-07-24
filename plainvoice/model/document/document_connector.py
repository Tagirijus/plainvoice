'''
DocumentConnector Class

This class is supposed to be a component for the Document class.
It is for connecting / linking documents to each other with an
absolute filename.

To be able to use the Document class in this class, I am using the
typing modul to not have circular imports. Yet I am absolutely not
sure, if this is the best way.
'''


from __future__ import annotations
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from plainvoice.model.document.document import Document


class DocumentConnector:
    '''
    The class for connecting Document objects.
    '''

    def __init__(self, document_context):
        self.connections_filepaths = []
        '''
        This list contains only the paths of the connections.
        This is for checking if connections already exist.
        '''

        self.connections = {}
        '''
        This dict holds the finally loaded objects of the
        links / connections. It is used as some kind of cache
        as well: data parsing / loading only happens on
        demand. Unless an object was linked on runtime. Then
        it also will directly get added to this list, of course.
        '''

        self.document_context = document_context
        '''
        The Document class, which is using this DocumentConnector.
        '''

    def add_connection(
        self,
        document: Document,
        add_to_given_document=None
    ) -> None:
        '''
        Add a document to the connections.

        Args:
            document (Document): \
                The document to add to the connections.
            add_to_given_document (Document | None): \
                If this method gets a Document on this parameter, this
                one will be used to add to the linked document as well.
        '''
        if self.connection_exists(document):
            return None

        other_filepath = document.get_absolute_filename()

        if add_to_given_document is not None:
            # here I chose None for the add_to_given_document parameter,
            # because otherwise it would create an infinite loop. not sure
            # how it would be done properly, though ...
            document.document_connector.add_connection(
                add_to_given_document, None
            )
            # also add this document to the cache self.connections
            # attribute already, so that on a save the link to this
            # document itself will be set correctly. otherwise I had
            # the problem that the link was set without initializing
            # the document. and later on save() the method would iterate
            # over all connections and if they would not be in the cache
            # already, it would load it from the file, yet in the file
            # the connection was not set to this point already. this
            # is why I add the document to the cache attribute already
            # so that on adding the connection, there already exists
            # and updated version of the linked document. and this
            # will be used on save() instead of loading it from file.
            self.connections[other_filepath] = document

        self.connections_filepaths.append(other_filepath)

    def connection_exists(self, document) -> bool:
        '''
        Check if the given document already exists in the connections.

        Args:
            document (Document): The document to check for.

        Returns:
            bool: Returns True, if the document is connected already.
        '''
        other_filepath = document.get_absolute_filename()
        if other_filepath in self.connections_filepaths:
            # yet does it also already exist in the cache?
            # just add it / update it to have the updated
            # reference to the object, in case it will
            # change outside this class
            self.connections[other_filepath] = document
            return True
        else:
            return False

    def from_dict(self, values: dict) -> None:
        '''
        Fill the objects attributes / data from the given dict.

        Args:
            values (dict): Argument description
        '''
        self.connections_filepaths = values.get('document_connections', [])
        self.connections = {}

    def get_connection_by_filename(self, filename: str) -> Document:
        '''
        Tries to fetch the document from the connections by its filename.

        Args:
            filename (str): The absolute filename of the document.

        Returns:
            Document | None: Returns the Document or None.
        '''
        output = None
        # basically initialize the Document into the
        # connections cache variable if it's not
        # already in it
        if filename not in self.connections.keys():
            if filename in self.connections_filepaths:
                self.connections[filename] = \
                    self.document_context.create_instance()
                self.connections[filename].load_from_name(filename)
        # now try to load it. yet it can be that the given filename
        # is no connection at all, thus it was not loaded, thus
        # output stays None
        if filename in self.connections.keys():
            output = self.connections[filename]
        return output  # type: ignore

    def get_connections_filepaths(self) -> list:
        '''
        Get the list with the filenames of the connections.

        Returns:
            list: Returns the list with the strings of the filenames.
        '''
        return self.connections_filepaths

    def to_list(self) -> list:
        '''
        Export the document connections to a list, which
        can be used for the YAML saving, for example.

        Returns:
            list: Returns a list, holding the connections.
        '''
        return self.connections_filepaths

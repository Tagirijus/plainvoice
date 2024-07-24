class DocumentConnector:
    """
    The class for connecting Document objects.
    """

    def __init__(self):
        self.connections_paths_only = []
        '''
        This list contains only the paths of the connections.
        This is for checking if connections already exist.
        '''

        self.connections_for_yaml = []
        '''
        Holds the connectios in a raw format, like it is
        saved in the YAML as well. Quite readable, hopefully.
        '''

        self.connections = []
        '''
        This dict holds the somehow 'parsed' objects of the
        links / connections. It is used as some kind of cache
        as well: data parsing / loading only happens on
        demand. Unless an object was linked on runtime. Then
        it also will directly get added to this list, of course.
        '''

    def add_connection(self, document, add_to_given_document=None) -> None:
        """
        Add a document to the connections.

        Args:
            document (Document): \
                The document to add to the connections.
            add_to_given_document (Document | None): \
                If this method gets a Document on this parameter, this
                one will be used to add to the linked document as well.
        """
        if not self._add_connection_prechecks(document):
            return None

        if add_to_given_document is not None:
            # here I chose None for the add_to_given_document parameter,
            # because otherwise it would create an infinite loop. not sure
            # how it would be done properly, though ...
            document.document_connector.add_connection(
                add_to_given_document, None
            )

        other_filepath = document.get_absolute_filename()
        other_document_type = document.get('document_type')
        self.connections_paths_only.append(other_filepath)
        self.connections.append(document)
        self.connections_for_yaml.append({
            other_document_type: other_filepath
        })

    def _add_connection_prechecks(self, document) -> bool:
        """
        Check some things before the connection adding process may
        be executed.

        Args:
            document (Document): The document to add to the connections.

        Returns:
            bool: Returns True on success.
        """
        if document.__class__.__name__ != 'Document':
            raise ValueError(
                f'DocumentConnector.add_connection() did not get Document type'
                + ' as parameter.'
            )

        if document.get_absolute_filename() in self.connections_paths_only:
            return False
        else:
            return True

    def from_dict(self, values: dict) -> None:
        """
        Fill the objects attributes / data from the given dict.

        Args:
            values (dict): Argument description
        """
        document_connections = values.get('document_connections', None)
        if document_connections is not None:
            self.connections = []
            for connection in document_connections:
                self.connections_for_yaml.append(connection)

    def to_list(self) -> list:
        """
        Export the document connections to a dict, which
        can be used for the YAML saving, for example.

        Returns:
            dict: Returns a dict, holding the connections.
        """
        return self.connections_for_yaml

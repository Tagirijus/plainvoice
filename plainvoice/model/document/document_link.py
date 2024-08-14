'''
DocumentLink class

This class represents a single link between two documents. It can
generate a unique id for this link based on the filenames of the
linked documents. Also it can return the name or even the whole
Document object of either of the two linked documents. Also it can
be used to unconnect the documents and thus deleting the link
completely.

The plan is that this class will be used by DocumentLinkManager.
'''

from plainvoice.model.document.document import Document


class DocumentLink:
    '''
    The link between two documents as an object.
    '''

    def __init__(self, document_a: Document, document_b: Document):
        '''
        This object represents a link between the two given documents.

        Args:
            document_a (Document): The one document of the link.
            document_b (Document): The other document of the link.
        '''

        self.document_a: Document = document_a
        '''
        The one document of the link.
        '''

        self.document_b: Document = document_b
        '''
        The other document of the link.
        '''

    def __str__(self):
        return self.generate_link_id(
            self.document_a,
            self.document_b
        )

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def generate_link_id(document_a: Document, document_b: Document) -> str:
        '''
        Generate a link id string with two given documents. It will use
        their absolute filenames, sort them and connect them in a specific
        string. This way for both sites the id would be the same, due to the
        alphabetical sorting of the filenames.

        Args:
            document_a (Document): The one document.
            document_b (Document): The other document.

        Returns:
            str: Returns a string, which shall represent this link.
        '''
        doc_a = document_a.get_filename()
        doc_b = document_b.get_filename()
        both_filenames = [doc_a, doc_b]
        both_filenames.sort()
        return '<->'.join(both_filenames)

    def get_document_a(self) -> Document:
        '''
        Return the one document from the link.

        Returns:
            Docuemnt: Returns a document object.
        '''
        return self.document_a

    def get_document_b(self) -> Document:
        '''
        Return the other document from the link.

        Returns:
            Docuemnt: Returns a document object.
        '''
        return self.document_b

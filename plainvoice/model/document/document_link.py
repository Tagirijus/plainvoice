'''
DocumentLink class

This class represents a single link between two documents. It can
generate a unique id for this link based on the filenames of the
linked documents. Also it can return the name or even the whole
Document object of either of the two linked documents. Also it can
be used to unconnect the documents and thus deleting the link
completely.

The plan is that this class will be used by DocumentRepository.


!!! TODO / WIP !!!


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

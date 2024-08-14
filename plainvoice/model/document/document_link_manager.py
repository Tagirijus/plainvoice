'''
DocumentLinkManager class

The class, which will manage and control links between documents.
It can add, remove or rename documents and links between each other.
'''

from plainvoice.model.document.document import Document
from plainvoice.model.document.document_link import DocumentLink


class DocumentLinkManager:
    '''
    Manager for handling and controlling links between documents.
    '''

    def __init__(self):
        '''
        This object controls links between documents.
        '''
        self.links_by_id: dict[str, DocumentLink] = {}
        '''
        The dict, which holds all the links with their link id string
        as a key.
        '''

        self.links_of_doc: dict[str, list[Document]] = {}
        '''
        The dict, which holds all the links of a specific document. The
        key is the absolute filename of the document and the value is
        a list of documents, which are linked to the document with this
        absolute filename.
        '''

    def add_link(self, document_a: Document, document_b: Document) -> None:
        '''
        Link two documents, if they are not linked already.

        Args:
            document_a (Document): The one document.
            document_b (Document): The other document.
        '''
        # do the linking with the DocumentLink and its id
        link_id = DocumentLink.generate_link_id(document_a, document_b)
        if link_id not in self.links_by_id:
            self.links_by_id[link_id] = DocumentLink(document_a, document_b)

        # also link document b to document a in its list
        filename_a = document_a.get_filename()
        if filename_a not in self.links_of_doc:
            self.links_of_doc[filename_a] = []
        if document_b not in self.links_of_doc[filename_a]:
            self.links_of_doc[filename_a].append(document_b)

        # and also link document a to document b in its list
        filename_b = document_b.get_filename()
        if filename_b not in self.links_of_doc:
            self.links_of_doc[filename_b] = []
        if document_a not in self.links_of_doc[filename_b]:
            self.links_of_doc[filename_b].append(document_a)

        # now also update the documents internal variables as well
        document_a.add_link(filename_b)
        document_b.add_link(filename_a)

    def document_links_loaded(self, document: Document) -> bool:
        '''
        Check if the given document has links and if they are already
        loaded. If it should not have any links, the method will
        also return True, since technically they are loaded (0 are!)

        Args:
            document (Document): The document to check on.

        Returns:
            bool: Returns True if they are loaded or it has no links at all.
        '''
        if len(document.get_links()) == 0:
            return True
        else:
            return document.get_filename() in self.links_of_doc

    def get_links_of_document(self, document: Document) -> list[Document]:
        '''
        Get the list of linked documents for the given document.

        Args:
            document (Document): The document to get its links from.

        Returns:
            list: Returns list containing linked documents.
        '''
        output = []
        filename = document.get_filename()
        if filename in self.links_of_doc:
            output = self.links_of_doc[filename]
        return output

    def remove_link(self, document_a: Document, document_b: Document) -> bool:
        '''
        Remove the link between the two documents and also update the
        documents internal variables accordingly. It won't save the
        documents yet, though. This has to be done outside of this class.

        Args:
            document_a (Document): The one document.
            document_b (Document): The other document.

        Returns:
            bool: Returns True on success and False, if there was no link.
        '''
        # unlink the DocumentLink and its id thingy
        link_id = DocumentLink.generate_link_id(document_a, document_b)
        if link_id in self.links_by_id:
            del self.links_by_id[link_id]
        else:
            # return False already, since there probably is
            # absolutel no link at all; neither in the
            # links_of_doc dict!
            return False

        # also unlink document b from document a in its list
        filename_a = document_a.get_filename()
        if document_b in self.links_of_doc[filename_a]:
            self.links_of_doc[filename_a].remove(document_b)

        # and also unlink document a from document b in its list
        filename_b = document_b.get_filename()
        if document_a in self.links_of_doc[filename_b]:
            self.links_of_doc[filename_b].remove(document_a)

        # now also update the documents internal variables as well
        document_a.remove_link(filename_b)
        document_b.remove_link(filename_a)

        return True

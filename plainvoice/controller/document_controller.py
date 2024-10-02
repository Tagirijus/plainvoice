'''
DocumentController class

Handles Document managing.
'''

from plainvoice.controller.io_facade.io_facade import IOFacade as io
from plainvoice.model.data.data_model_populator import DataModelPopulator
from plainvoice.model.document.document import Document
from plainvoice.model.config import Config
from plainvoice.model.script.script_repository import ScriptRepository
from plainvoice.model.template.template_repository import TemplateRepository
from plainvoice.utils import data_utils
from plainvoice.utils import doc_utils
from plainvoice.utils import file_utils

from datetime import datetime


class DocumentController:
    '''
    Handles Document managing.
    '''

    def __init__(self):
        '''
        Handles Document managing.
        '''
        self.doc_repo = doc_utils.get_doc_repo()

    def change_visibility(
        self,
        doc_typename: str,
        name: str,
        hide: bool = True
    ) -> None:
        '''
        Hide the document with the given type and name.

        Args:
            doc_typename (str): The name of the document type.
            name (str): The name of the document.
            hide (bool): If True, hide the document.
        '''
        doc = self.doc_repo.get_document_by_name_type_combi(name, doc_typename)

        if doc:
            if hide:
                doc.hide()
                io.print(f'Document "{name}" now hidden.', 'success')
            else:
                doc.show()
                io.print(f'Document "{name}" now visible.', 'success')
            self.doc_repo.save(doc)
        else:
            io.print(f'Document "{name}" not found.', 'warning')

    def edit(self, doc_typename: str, name: str) -> None:
        '''
        Edit the document with the given type and name. Also it
        will update the values, if the document type, for example,
        got fixed fields changed or so.

        Args:
            doc_typename (str): The name of the document type.
            name (str): The name of the document.
        '''
        doc = self.doc_repo.get_document_by_name_type_combi(name, doc_typename)

        if doc:
            io.print(f'Found "{doc.get_name()}".', 'success')
            io.print('Re-saving to fill new fields ...', 'info')
            self.doc_repo.save(doc)
            io.print('Opening file in editor ...', 'info')
            file_utils.open_in_editor(
                self.doc_repo.get_filename(doc_typename, name)
            )
        else:
            io.print(f'Document "{name}" not found!', 'warning')

    def link_documents(
        self,
        doc_typename_a: str,
        name_a: str,
        doc_typename_b: str,
        name_b: str
    ) -> None:
        '''
        Link document a with the given type and name to the
        document b with the given type and name. While the type
        can also stay empty, while the name have to be an
        absolute filepath then.

        Args:
            doc_typename_a (str): The name of the document A type.
            name_a (str): The name of the document A.
            doc_typename_b (str): The name of the document B type.
            name_b (str): The name of the document B.
        '''
        doc_a = self.doc_repo.get_document_by_name_type_combi(
            name_a,
            doc_typename_a
        )
        doc_b = self.doc_repo.get_document_by_name_type_combi(
            name_b,
            doc_typename_b
        )

        if not doc_a:
            io.print(f'Document "{name_a}" not found!', 'warning')
        elif not doc_b:
            io.print(f'Document "{name_b}" not found!', 'warning')
        else:
            self.doc_repo.add_link(doc_a, doc_b)
            self.doc_repo.add_link(doc_a, doc_b)
            io.print(f'Linked document "{name_a}" to "{name_b}"!', 'success')
            self.doc_repo.save(doc_a)
            self.doc_repo.save(doc_b)

    def list(self, doc_typename: str, show_all: bool) -> None:
        '''
        List documents of a certain type.

        Args:
            doc_typename (str): The name of the document type.
            show_all (bool): If True, shows also hidden documents.
        '''
        # show_all is on the show_only_visible argument; thus
        # it has to be inverted to act correct
        docs_list = self.doc_repo.get_list_of_docs(doc_typename, not show_all)
        if docs_list:
            io.print_docs_table(docs_list)
        else:
            io.print(
                f'No documents found for type "{doc_typename}".',
                'warning'
            )

    def list_due(
        self,
        doc_typename: str,
        due_only: bool = False,
        overdue_only: bool = False,
        show_all: bool = True
    ) -> None:
        '''
        List all the documents of this type (or all, if undefined),
        which have a due date set and no done date set NOW.

        Args:
            doc_typename (str): \
                The name of the document type.
            due_only (bool): \
                If True, shows only due docs and no overdue.
            overdue_only (bool): \
                If True, shows only overdue docs. \
                If due_only is also set to True, this parameter \
                has priority.
            show_all (bool): \
                If True, shows also hidden documents.
        '''
        # the logic here is that overdue_only will have higher priority
        # over "due_only"
        include_due = overdue_only is False

        # the logic here is that due_only will exclude overdue docs
        # only if overdue_only is not set, since it has higher priority
        include_overdue = not due_only or overdue_only

        # show_all is on the show_only_visible argument; thus
        # it has to be inverted to act correct
        show_only_visible = not show_all

        # get the due docs
        due_docs = self.doc_repo.get_due_docs(
            doc_typename,
            include_due,
            False,
            show_only_visible
        )
        overdue_docs = self.doc_repo.get_due_docs(
            doc_typename,
            False,
            include_overdue,
            show_only_visible
        )

        # print them in tables
        typename = doc_typename if doc_typename else 'document'
        # first due
        if due_docs:
            io.print_doc_due_table(
                due_docs,
                f'[green]Due {typename}:[/green]',
                doc_typename == ''
            )

        # newline seperator if there are due AND overdue
        if due_docs and overdue_docs:
            print()

        # then overdue
        if overdue_docs:
            io.print_doc_due_table(
                overdue_docs,
                f'[red]Overdue {typename}:[/red]',
                doc_typename == ''
            )

    def list_linked_documents(
        self,
        doc_typename: str,
        name: str,
        show_all: bool = True
    ) -> None:
        '''
        List linked documents for the given type and name of the
        document. The type can be an empty string and the name
        has to be an absolute filepath then.

        Args:
            doc_typename (str): The name of the document type.
            name (str): The name of the document.
            show_all (bool): If True, shows also hidden documents.
        '''
        doc = self.doc_repo.get_document_by_name_type_combi(name, doc_typename)

        if not doc:
            io.print(f'Document "{name}" not found!', 'warning')
        else:
            linked_docs = self.doc_repo.get_links_of_document(doc)
            linked_docs = [
                d for d in linked_docs
                if (not show_all and d.is_visible()) or show_all
            ]
            io.print_docs_table(linked_docs, 'Linked documents')

    def new(
        self,
        doc_typename: str,
        name: str = '',
        client: str = '',
        user_name: str = ''
    ) -> None:
        '''
        Create a new document with the given type and name.

        Args:
            doc_typename (str): The name of the document type.
            name (str): The name of the document.
            client (str): Optional client name to link to.
            user_name (str): Optional the user name to use.
        '''
        doc = self.doc_repo.get_document_by_name_type_combi(name, doc_typename)
        user = self.doc_repo.get_user_by_username(user_name)

        if name == '':
            new_name = self.doc_repo.generate_next_name(doc_typename)
        else:
            new_name = name
        if not doc_typename:
            io.print(
                'Please specify a document type with -t/--type!',
                'warning'
            )
        else:
            if not doc:
                io.print(
                    f'Creating new "{doc_typename}": "{new_name}" ...',
                    'success'
                )
                new_doc = self.doc_repo.create_document(doc_typename, name)

                # now the optional direct client linking
                if client:
                    client_type = str(Config().get('client_type'))
                    if not self.doc_repo.exists(client_type, client):
                        io.print(
                            f'Client "{client}" not found!',
                            'warning'
                        )
                    else:
                        client_doc = self.doc_repo.load(client, client_type)
                        self.doc_repo.add_link(new_doc, client_doc)
                        self.doc_repo.save(new_doc)
                        self.doc_repo.save(client_doc)
                        io.print(
                            f'Linked the new doc to client "{client}".',
                            'success'
                        )

                # also populate the document on first creation
                self.populate_document(new_doc, user)
                self.doc_repo.save(new_doc)

            else:
                io.print(f'Found "{new_name}".', 'success')
            io.print('Opening file in editor ...', 'info')
            file_utils.open_in_editor(
                self.doc_repo.get_filename(doc_typename, new_name)
            )

    def populate_document(
        self,
        document: Document,
        user: Document = Document()
    ) -> None:
        '''
        Populate the given document with certain variables.

        Args:
            document (Document): \
                The document to populate.
            user (Document): \
                The user document (DataModel as well) to set \
                optionally so that it can also be accessed in \
                the replacement values of the main document.
        '''
        client = self.doc_repo.get_client_of_document(document)
        populator = DataModelPopulator(
            client=client,
            config=Config(),
            user=user
        )
        populator.populate(document)

    def remove(self, doc_typename: str, name: str) -> None:
        '''
        Remove the document with the given type and name.

        Args:
            doc_typename (str): The name of the document type.
            name (str): The name of the document.
        '''
        doc = self.doc_repo.get_document_by_name_type_combi(name, doc_typename)

        if doc:
            if io.ask_yes_no(f'Remove document "{name}"?'):
                self.doc_repo.remove(doc_typename, name)
                io.print(f'Document "{name}" removed.', 'success')
            else:
                io.print(f'Document "{name}" not removed.', 'warning')
        else:
            io.print(f'Document "{name}" not found.', 'warning')

    def remove_documents_link(
        self,
        doc_typename_a: str,
        name_a: str,
        doc_typename_b: str,
        name_b: str
    ) -> None:
        '''
        Un-link document a with the given type and name from the
        document b with the given type and name. While the type
        can also stay empty, while the name have to be an
        absolute filepath then.

        Args:
            doc_typename_a (str): The name of the document A type.
            name_a (str): The name of the document A.
            doc_typename_b (str): The name of the document B type.
            name_b (str): The name of the document B.
        '''
        doc_a = self.doc_repo.get_document_by_name_type_combi(
            name_a,
            doc_typename_a
        )
        doc_b = self.doc_repo.get_document_by_name_type_combi(
            name_b,
            doc_typename_b
        )

        if not doc_a:
            io.print(f'Document "{name_a}" not found!', 'warning')
        elif not doc_b:
            io.print(f'Document "{name_b}" not found!', 'warning')
        else:
            if self.doc_repo.remove_link(doc_a, doc_b):
                io.print(
                    f'Unlinked document "{name_a}" from "{name_b}"!',
                    'success'
                )
                self.doc_repo.save(doc_a)
                self.doc_repo.save(doc_b)
            else:
                io.print(
                    f'Could not unlink document "{name_a}" from "{name_b}"!',
                    'warning'
                )

    def render(
        self,
        doc_typename: str,
        name: str,
        template_name: str | None,
        user_name: str = '',
        output_file: str = ''
    ) -> None:
        '''
        Render the document with the given type and name and the
        given template name. Optionally out to the given
        output file.

        Args:
            doc_typename (str): The name of the document type.
            name (str): The name of the document.
            template_name (str): The name of the template.
            user_name (str): Optional the user name to use.
            output_file (str): Optional the output filename to save to.
        '''
        doc = self.doc_repo.get_document_by_name_type_combi(name, doc_typename)
        user = self.doc_repo.get_user_by_username(user_name)

        template_repo = TemplateRepository(
            str(Config().get('templates_folder'))
        )
        if template_name is None:
            io.print('Specify a template. Choose one of those:', 'warning')
            io.print_list(sorted(template_repo.get_template_names()))
        else:
            if doc:
                # create the render engine; import only on demand,
                # since weasyprint is slow loading
                from plainvoice.view.render import Render
                render = Render(str(Config().get('templates_folder')))

                # load the document and render it
                self.populate_document(doc, user)
                success, error = render.render(
                    template_name,
                    doc,
                    user,
                    output_file
                )
                if success:
                    io.print(
                        f'Rendered document "{doc.get_name()}" successfully.',
                        'success'
                    )
                else:
                    io.print(
                        f'Rendering document "{doc.get_name()}" went wrong. '
                        + f'Error:\n  {error}',
                        'error'
                    )
            else:
                io.print(f'Document "{name}" not found.', 'warning')

    def set_document_done(
        self,
        doc_typename: str,
        code: str,
        date: str = '',
        force: bool = False
    ) -> None:
        '''
        Set the document with the given CODE to "done". This will
        set the documents "done date" to the given date, or it
        will ask for a date to set it to.

        It is possible to directly set a date to set it to. In that
        case the program will ask to apply the change (in case something
        valid was entered). Otherwise the program will ask for a date
        in an interactive mode.

        Args:
            doc_typename (str): The name of the document type.
            code (str): The document code.
            date (str): Optional set the date directly.
            force (bool): If True, modify will happen without asking.
        '''
        doc = self.doc_repo.get_document_by_code(doc_typename, code)

        if doc:
            io.print(
                f'Found document "{doc.get_name()}'
                + f' [italic]({doc.get_title()})[/italic]".',
                'success'
            )

            # get the new date
            if not date and not force:
                date = io.ask_date()
            elif not date and force:
                date = datetime.now().strftime('%Y-%m-%d')
            date = data_utils.is_valid_date(date)
            if not date:
                io.print(
                    'Use YYYY-MM-DD or DD.MM.YYYY as the date format, please.',
                    'info'
                )
                return None

            # ask to modify (if not forced)
            if not force:
                old_date = doc.get_done_date(True)
                io.print(f'Old done date: {old_date}')
                io.print(f'New done date: {date}')
                do_it = io.ask_yes_no('Modify done-date?')
            else:
                do_it = True

            # modify it
            if do_it:
                doc.set_done_date(date, True)
                self.doc_repo.save(doc)
                io.print(f'Set date "{date}"!', 'success')

        else:
            io.print(f'Nothing found for code "{code}".', 'warning')

    def script(
        self,
        doc_typename: str,
        name: str,
        script_name: str | None,
        user_name: str = '',
        quiet: bool = False
    ) -> None:
        '''
        Execute a script with the document with the given type and name
        and the given script name. You can also set another user_name
        so that some other user instead of the default one will be used
        so that the variable "user" can have different values in the
        script.

        Args:
            doc_typename (str): The name of the document type.
            name (str): The name of the document.
            script_name (str): The name of the script.
            user_name (str): Optional the user name to use.
            quiet (bool): If True no output from plainvoice will come, \
                only from the script itself.
        '''
        doc = self.doc_repo.get_document_by_name_type_combi(name, doc_typename)
        user = self.doc_repo.get_user_by_username(user_name)

        script_repo = ScriptRepository(str(Config().get('scripts_folder')))
        if script_name is None:
            io.print('Specify a script. Choose one of those:', 'warning')
            io.print_list(sorted(script_repo.get_script_names()))
        else:
            if doc:
                # get script
                script_obj = script_repo.load(script_name)

                # load the document and pass it to the script
                doc = self.doc_repo.load(name, doc_typename)
                if not quiet:
                    io.print(
                        f'Running script "{script_name}"'
                        + f' on document "{doc.get_name()}"'
                        + ' ...',
                        'success'
                    )
                self.populate_document(doc, user)
                script_obj.run(doc, user)
            else:
                io.print(f'Document "{name}" not found.', 'warning')

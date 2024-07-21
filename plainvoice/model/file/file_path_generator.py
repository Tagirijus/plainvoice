from plainvoice.model.config import Config

import os


class FilePathGenerator:
    def __init__(
        self,
        folder: str = '.',
        extension: str = 'yaml'
    ):
        '''
        Adds the functionality to the file class for generating
        the path and automatic extension.

        Args:
            folder (str|None): \
                Tells, if the dotfolder of the program in the home folder \
                should be used automatically for storing relatively to it \
                or use a given string. If the string contains '{pv}', this \
                will be replaced by the data dir in the home folder of the \
                program. That way you can still use the data dir in the \
                home folder, by entering a string, yet relatively to the \
                data dir of the program. Default is set with None, which \
                means to use the programs data dir root. (default: `None`)
            extension (str): \
                The extension with which the FileManager should work. \
                (default: `'yaml'`)
        '''
        self.datadir = Config().datadir
        '''
        The path to the data dir of plainvoice. Probably it will be
        ~/.plainvoice by default.
        '''

        self.extension = extension.replace('.', '')
        '''
        The extension with which the FileManager should work. By
        default it is 'yaml'.
        '''

        self.folder = folder
        '''
        Tells, if the dotfolder of the program in the home folder
        should be used automatically for storing relatively to it
        or use a given string. If the string contains '{pv}', this
        will be replaced by the data dir in the home folder of the
        program. That way you can still use the data dir in the
        home folder, by entering a string, yet relatively to the
        data dir of the program.
        '''

    def auto_append_extension(self, filename: str) -> str:
        '''
        With this method you can append a file extension to
        the given filename string. It can contain a dot
        or not, this does not matter. Also if the filename
        already has the extension (lower or upper case), it
        won't be changed.

        The appended file extension, if it does not exist,
        is lower case always.

        Args:
            filename (str): The filename to append the extension to.

        Returns:
            str: The filename including the extension.
        '''
        full_extension_lower = '.' + self.extension.lower()
        full_extension_upper = '.' + self.extension.upper()
        if (
            full_extension_lower not in filename
            and full_extension_upper not in filename
        ):
            return filename + full_extension_lower
        else:
            return filename

    def generate_correct_filename(self, name: str) -> str:
        '''
        Generates the correct filename string by appending the
        file extension and also generating the absolute filename,
        e.g. if the file is supposed to be in the programs data dir.

        Args:
            name (str): \
                The name. Either relative to the programs data dir \
                or with the given self.folder variable as the user set \
                data folder.

        Returns:
            str: Returns the new filename.
        '''
        name = self.auto_append_extension(name)
        # only generate the path automatically if the given
        # filename probably is not absolute
        if name[0] not in ['.', '/']:
            name = os.path.join(self.get_folder(), name)
        return name

    def get_extension(self) -> str:
        '''
        Simply get the extension.

        Returns:
            str: Returns the extension as a string.
        '''
        return self.extension

    def get_folder(self) -> str:
        '''
        Returns the user set folder as the data dir, or the
        programs default data dir if None is set for self.folder.

        Returns:
            str: The folder to work in with saving / loading files.
        '''
        if self.folder is None:
            return self.datadir
        else:
            '''
            The self.folder string can contain '{pv}' or '{pv}',
            which then will be converted to the programs data dir
            like "/home/user/.plainvoice". This way a user given
            folder like '{pv}/clients' can be converted to
            "/home/user/.plainvoice/clients"
            '''
            if '{pv}' in self.folder or '{PV}' in self.folder:
                return os.path.join(
                    self.datadir,
                    self.folder.replace('{pv}/', '').replace('{PV}/', '')
                )
            else:
                return self.folder

    @staticmethod
    def replace_extension_with_pdf(filename: str) -> str:
        '''
        Replace the given input filename extension with .pdf.

        Args:
            filename (str): \
                Can be any filename with any extension in the filename \
                which will be replaced by ".pdf".

        Returns:
            str: The new output filename with .pdf extension.
        '''
        if '.' in filename:
            name, _ = filename.rsplit('.', 1)
            return f'{name}.pdf'
        else:
            return f'{filename}.pdf'

    def set_extension(self, extension: str) -> None:
        """
        Set the file extension.

        Args:
            extension (str): The extension to set.
        """
        self.extension = str(extension)

    def set_folder(self, folder: str) -> None:
        """
        Set the file folder.

        Args:
            folder (str): The folder to set.
        """
        self.folder = str(folder)

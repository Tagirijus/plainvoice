from datetime import datetime
from plainvoice.model.config import Config
from plainvoice.utils import math_utils

import os
import re


class FilePathGenerator:

    PLACEHOLDER_ID: str = '{id}'
    """
    The placehodler for the id. It can fetch the id from
    a filename with this in combination with the pattern
    and also generate a new name with this and replace
    this string with the id of the data type later.
    """

    PLACEHOLDER_YEAR: str = '{year}'
    """
    The placehodler for the year. For more info read the
    doc string of PLACEHOLDER_ID.
    """

    PLACEHOLDER_MONTH: str = '{month}'
    """
    The placehodler for the month. For more info read the
    doc string of PLACEHOLDER_ID.
    """

    PLACEHOLDER_DAY: str = '{day}'
    """
    The placehodler for the day. For more info read the
    doc string of PLACEHOLDER_ID.
    """

    def __init__(
        self,
        folder: str = '.',
        extension: str = 'yaml',
        filename_pattern: str = '{id}'
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

        self.filename_pattern = filename_pattern
        '''
        The filename pattern to be used for generating, yet also for
        fetching info from filenames accordingly.
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

    def _build_regex(self) -> str:
        """
        Builds a regex pattern to match the filenames.

        Args:
            pattern (str): The pattern to be used.

        Returns:
            str: The regex pattern, generated from the pattern.
        """
        regex = re.escape(self.filename_pattern)
        regex = regex.replace(
            re.escape(self.PLACEHOLDER_ID),
            r'(?P<id>.+)'
        )
        regex = regex.replace(
            re.escape(self.PLACEHOLDER_YEAR),
            r'(?P<year>\d{4})'
        )
        regex = regex.replace(
            re.escape(self.PLACEHOLDER_MONTH),
            r'(?P<month>\d{2})'
        )
        regex = regex.replace(
            re.escape(self.PLACEHOLDER_DAY),
            r'(?P<day>\d{2})'
        )
        return regex

    def _build_replacement_dict(self, additional_dict: dict = {}) -> dict:
        """
        Generate a replacement dic to be used in the generate_name()
        method.

        Args:
            additional_dict (dict): \
                Additional dict replacer values.

        Returns:
            dict: Returns a dict.
        """
        today = datetime.now()
        year = today.year
        month = f'{today.month:02}'
        day = f'{today.day:02}'
        output = {
            self.PLACEHOLDER_YEAR.strip('{}'): year,
            self.PLACEHOLDER_MONTH.strip('{}'): month,
            self.PLACEHOLDER_DAY.strip('{}'): day
        }
        output.update(additional_dict)
        return output

    def extract_id_from_filename(self, filename: str) -> str:
        """
        Extracts the id from a filename according to the
        set filename pattern.

        Args:
            filename (str): The filename string.

        Returns:
            str: Returns the extracted id string.
        """
        id_match = re.search(self._build_regex(), filename)
        if id_match:
            return id_match.group('id')
        else:
            return ''

    def extract_name_from_path(
        self,
        path: str,
        remove_folders: bool = False
    ) -> str:
        """
        This method can extract the name of the given filepath
        considering the folder and file extension. E.g. it will
        be able to convert "/home/user/.plainvoice/docs/doc.yaml"
        to "doc", when folder e.g. is set to "{pv}/docs" and the
        extension is "yaml".

        Args:
            path (str): The full path of the file.
            remove_fodlers (bool): \
                If set True, also the leading folder will be removed. E.g. \
                "2024/invoice_2.yaml" will become "incoie_2.yaml". This is \
                needed when extracting the id and when I do need the plain \
                filename only without the folder.

        Returns:
            str: Returns the name string.
        """
        output = path.replace(
            f'{self.get_folder()}/', ''
        ).replace(f'.{self.extension}', '')
        if remove_folders:
            output = output.rsplit('/', 1)[-1]
        return output

    def generate_absolute_filename(self, name: str) -> str:
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
            if '{pv}' in self.folder:
                return os.path.join(
                    self.datadir,
                    self.folder.replace('{pv}/', '')
                )
            else:
                return self.folder

    def get_next_id(self, filenames: list) -> str:
        """
        Get a list with filenames and exttract their ids according
        to the filename pattern and then get the next highest id,
        if possible.

        Args:
            filenames (list): The list containing the filename strings.

        Returns:
            str: Returns the next possible id string.
        """
        ids = []
        for filename in filenames:
            plain_filename = self.extract_name_from_path(filename, True)
            id_only = self.extract_id_from_filename(plain_filename)
            if math_utils.is_convertible_to_int(id_only):
                ids.append(int(id_only))
        return str(max(ids) + 1 if ids else 1)

    def generate_name(self, replace_dict: dict = {'id': None}) -> str:
        """
        Use the replace_dict and the own class variables to
        generate a new name.

        Args:
            replace_dict (dict): The replacement dict.

        Returns:
            str: Returns a name string.
        """
        replace_dict = self._build_replacement_dict(replace_dict)
        return self.filename_pattern.format(**replace_dict)

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

    def set_filename_pattern(self, filename_pattern: str) -> None:
        """
        Set the file filename pattern.

        Args:
            filename_pattern (str): The filename pattern to set.
        """
        self.filename_pattern = str(filename_pattern)

    def set_folder(self, folder: str) -> None:
        """
        Set the file folder.

        Args:
            folder (str): The folder to set.
        """
        self.folder = str(folder)

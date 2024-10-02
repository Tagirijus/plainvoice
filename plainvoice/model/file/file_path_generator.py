from datetime import datetime
from plainvoice.model.config import Config
from plainvoice.utils import math_utils

import os
import re


class FilePathGenerator:

    DEFAULT_EXTENSION: str = 'yaml'
    '''
    The default extension of the object, if nothing is set.
    '''

    DEFAULT_FILENAME_PATTERN: str = '{code}'
    '''
    The default filename pattern.
    '''

    DEFAULT_FOLDER: str = './'
    '''
    The default folder of the object, if nothing is set.
    '''

    PLACEHOLDER_CODE: str = '{code}'
    '''
    The placehodler for the code. It can fetch the code from
    a filename with this in combination with the pattern
    and also generate a new name with this and replace
    this string with the code of the data type later.
    '''

    PLACEHOLDER_YEAR: str = '{year}'
    '''
    The placehodler for the year. For more info read the
    doc string of PLACEHOLDER_CODE.
    '''

    PLACEHOLDER_MONTH: str = '{month}'
    '''
    The placehodler for the month. For more info read the
    doc string of PLACEHOLDER_CODE.
    '''

    PLACEHOLDER_DAY: str = '{day}'
    '''
    The placehodler for the day. For more info read the
    doc string of PLACEHOLDER_CODE.
    '''

    def __init__(
        self, folder: str = '', extension: str = '', filename_pattern: str = ''
    ):
        '''
        Adds the functionality to the file class for generating
        the path and automatic extension.

        Args:
            folder (str|None): \
                Tells, if the dotfolder of the program in the home folder \
                should be used automatically for storing relatively to it \
                or use a given string. If the string contains '{app_dir}', \
                this will be replaced by the data dir in the home folder of \
                the program. That way you can still use the data dir in the \
                home folder, by entering a string, yet relatively to the \
                data dir of the program. Default is set with None, which \
                means to use the programs data dir root. (default: `None`)
            extension (str): \
                The extension with which the FileManager should work. \
                (default: `'yaml'`)
        '''
        self.datadir = Config().data_dir
        '''
        The path to the data dir of plainvoice. Probably it will be
        ~/.plainvoice by default.
        '''

        self.extension = (
            self.DEFAULT_EXTENSION if extension == '' else extension.replace('.', '')
        )
        '''
        The extension with which the FileManager should work. By
        default it is 'yaml'.
        '''

        self.filename_pattern = (
            self.DEFAULT_FILENAME_PATTERN
            if filename_pattern == ''
            else filename_pattern
        )
        '''
        The filename pattern to be used for generating, yet also for
        fetching info from filenames accordingly.
        '''

        self.folder = self.DEFAULT_FOLDER if folder == '' else folder
        '''
        Tells, if the dotfolder of the program in the home folder
        should be used automatically for storing relatively to it
        or use a given string. If the string contains '{app_dir}', this
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
        '''
        Builds a regex pattern to match the filenames.

        Args:
            pattern (str): The pattern to be used.

        Returns:
            str: The regex pattern, generated from the pattern.
        '''
        regex = re.escape(self.filename_pattern)
        regex = regex.replace(re.escape(self.PLACEHOLDER_CODE), r'(?P<code>.+)')
        regex = regex.replace(re.escape(self.PLACEHOLDER_YEAR), r'\d{4}')
        regex = regex.replace(re.escape(self.PLACEHOLDER_MONTH), r'\d{2}')
        regex = regex.replace(re.escape(self.PLACEHOLDER_DAY), r'\d{2}')
        return regex

    def _build_replacement_dict(self, additional_dict: dict = {}) -> dict:
        '''
        Generate a replacement dic to be used in the generate_name()
        method.

        Args:
            additional_dict (dict): \
                Additional dict replacer values.

        Returns:
            dict: Returns a dict.
        '''
        today = datetime.now()
        year = today.year
        month = f'{today.month:02}'
        day = f'{today.day:02}'
        output = {
            self.PLACEHOLDER_YEAR.strip('{}'): year,
            self.PLACEHOLDER_MONTH.strip('{}'): month,
            self.PLACEHOLDER_DAY.strip('{}'): day,
        }
        output.update(additional_dict)
        return output

    def extract_code_from_filename(self, filename: str) -> str:
        '''
        Extracts the code from a filename according to the
        set filename pattern.

        Args:
            filename (str): The filename string.

        Returns:
            str: Returns the extracted code string.
        '''
        id_match = re.search(self._build_regex(), filename)
        if id_match and id_match.groupdict():
            return id_match.group('code')
        else:
            return ''

    def extract_name_from_path(self, path: str, remove_folders: bool = False) -> str:
        '''
        This method can extract the name of the given filepath
        considering the folder and file extension. E.g. it will
        be able to convert "/home/user/.plainvoice/docs/doc.yaml"
        to "doc", when folder e.g. is set to "{app_dir}/docs" and the
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
        '''
        output = path
        if self.get_folder() != '':
            output = output.replace(f'{self.get_folder()}/', '')
        if self.extension != '':
            output = output.replace(f'.{self.extension}', '')
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
        if name == '':
            return ''
        name = self.auto_append_extension(name)
        # only generate the path automatically if the given
        # filename probably is not absolute nor relative
        # to the program execution working dir
        is_absolute = os.path.isabs(name)
        is_relative = name.startswith('./') or name.startswith('..')
        if not is_absolute and not is_relative:
            name = os.path.join(self.get_folder(), name)
        return os.path.abspath(name)

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
            output = self.folder
            '''
            The self.folder string can contain '{app_dir}' or '{app_dir}',
            which then will be converted to the programs data dir
            like "/home/user/.plainvoice". This way a user given
            folder like '{app_dir}/clients' can be converted to
            "/home/user/.plainvoice/clients"
            '''
            if '{app_dir}' in self.folder:
                output = os.path.join(self.datadir, output.replace('{app_dir}/', ''))
            '''
            For the tests the folder can also contain '{test_data_dir}' as
            a placeholder which will be replaced with the correct test
            data folder.
            '''
            if '{test_data_dir}' in self.folder:
                output = os.path.join(
                    os.path.dirname(__file__),
                    '../../../tests/data',
                    output.replace('{test_data_dir}/', ''),
                )
            return os.path.abspath(output)

    def get_next_code(self, filenames: list) -> str:
        '''
        Get a list with filenames and exttract their codes according
        to the filename pattern and then get the next highest code,
        if possible.

        Args:
            filenames (list): The list containing the filename strings.

        Returns:
            str: Returns the next possible id string.
        '''
        ids = []
        for filename in filenames:
            plain_filename = self.extract_name_from_path(filename, False)
            id_only = self.extract_code_from_filename(plain_filename)
            if math_utils.is_convertible_to_int(id_only):
                ids.append(int(id_only))
        return str(max(ids) + 1 if ids else 1)

    def generate_name(self, replace_dict: dict = {'code': None}) -> str:
        '''
        Use the replace_dict and the own class variables to
        generate a new name.

        Args:
            replace_dict (dict): The replacement dict.

        Returns:
            str: Returns a name string.
        '''
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
        '''
        Set the file extension.

        Args:
            extension (str): The extension to set.
        '''
        self.extension = str(extension)

    def set_filename_pattern(self, filename_pattern: str) -> None:
        '''
        Set the file filename pattern.

        Args:
            filename_pattern (str): The filename pattern to set.
        '''
        self.filename_pattern = str(filename_pattern)

    def set_folder(self, folder: str) -> None:
        '''
        Set the file folder.

        Args:
            folder (str): The folder to set.
        '''
        self.folder = str(folder)

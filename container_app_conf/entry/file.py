#  Copyright (c) 2019 Markus Ressel
#  .
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#  .
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#  .
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
import os
import pathlib

from container_app_conf import ConfigEntry


class FileConfigEntry(ConfigEntry):
    _example = "/tmp/temporary"

    def __init__(self, key_path: [str], example: any = None, description: str or None = None, default: any = None,
                 none_allowed: bool = None, check_existence: bool = False):
        """
        See ConfigEntry
        :param check_existence: whether to check for file existence
        """
        super().__init__(key_path, example, description, default, none_allowed)
        self.check_existence = check_existence

    def _value_to_type(self, value: any) -> str or None:
        """
        Tries to permissively convert the given value to a file path.
        :param value: the value to parse
        :return: the parsed file value
        """
        str_value = str(value)
        if isinstance(value, pathlib.Path):
            file = value
        else:
            file = pathlib.Path(str_value)

        if str_value.endswith(os.sep):
            raise AssertionError("File path should not end with '{}' delimiter: {}".format(os.sep, str_value))

        if file.is_dir():
            raise IsADirectoryError("Path is not a file: {}".format(str_value))

        if self.check_existence and not file.exists():
            raise FileNotFoundError("File does not exist: {}".format(value))

        return file


class DirectoryConfigEntry(ConfigEntry):
    _example = "/tmp"

    def __init__(self, key_path: [str], example: any = None, description: str or None = None, default: any = None,
                 none_allowed: bool = None, check_existence: bool = False):
        """
        See ConfigEntry
        :param check_existence: whether to check for folder existence
        """
        super().__init__(key_path, example, description, default, none_allowed)
        self.check_existence = check_existence

    def _value_to_type(self, value: any) -> str or None:
        """
        Tries to permissively convert the given value to a folder path.
        :param value: the value to parse
        :return: the parsed folder value
        """
        str_value = str(value)
        if isinstance(value, pathlib.Path):
            str_value += "/"
            directory = value
        else:
            directory = pathlib.Path(str_value)

        if not str_value.endswith(os.sep):
            raise AssertionError("Directory path should end with '{}' delimiter: {}".format(os.sep, str_value))

        if directory.is_file():
            raise NotADirectoryError("Path is not a directory: {}".format(str_value))

        if self.check_existence and not directory.exists():
            raise FileNotFoundError("directory does not exist: {}".format(value))

        return directory

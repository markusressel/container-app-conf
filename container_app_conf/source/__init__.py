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
import logging
import os
from typing import List

from container_app_conf import ConfigEntry

LOGGER = logging.getLogger(__name__)


class DataSource:

    def has(self, entry: ConfigEntry) -> bool:
        """
        Checks whether the data source has a value for the given config entry
        :param entry: the config entry to check
        :return: True if the source contains a value for the given entry, False otherwise
        """
        raise NotImplementedError()

    def get(self, entry: ConfigEntry) -> any:
        """
        Retrieve the value of the given key
        :param entry: config entry
        :return: value
        """
        raise NotImplementedError()

    def write_reference(self, reference: dict):
        """
        Writes a reference configuration (if implemented)
        :param reference: the reference config as in tree form
        """
        pass


class FilesystemSource(DataSource):
    DEFAULT_FILE_EXTENSIONS = []

    def __init__(self, file_name: str or List[str],
                 path: str or List[str] = None,
                 file_extension: str or List[str] = None):
        """
        :param path: allowed config file path(s)
        :param file_name: allowed config file name(s)
        :param file_extension: allowed config file extension(s)
        """
        self.root = {}
        if path is None:
            from container_app_conf import DEFAULT_CONFIG_FILE_PATHS
            self.paths = DEFAULT_CONFIG_FILE_PATHS
        else:
            self.paths = path if isinstance(path, list) else [path]
        self.file_names = file_name if isinstance(file_name, list) else [file_name]
        if file_extension is None:
            self.file_extensions = self.DEFAULT_FILE_EXTENSIONS
        else:
            self.file_extensions = file_extension if isinstance(file_extension, list) else [file_extension]

    def load(self):
        """
        Loads the config file content into memory
        """
        file_path = self._find_config_file()
        if file_path is None:
            LOGGER.debug("No config file found in paths: {}".format(self.paths))
            return

        self.root = self._load(file_path)

    def _load(self, file_path: str) -> dict:
        """
        Parses the file content into memory
        :param file_path: the path of the file to parse
        :return: file content as a dictionary
        """
        raise NotImplementedError()

    def has(self, entry: ConfigEntry) -> bool:
        value = self.root
        if value is None:
            return False

        for key in entry.key_path:
            value = value.get(key)
            if value is None:
                return False

        return True

    def get(self, entry: ConfigEntry) -> any:
        value = self.root
        if value is None:
            return None

        for key in entry.key_path:
            value = value.get(key)
            if value is None:
                return entry.value

        return value

    def write_reference(self, reference: dict):
        """
        Writes a reference config file
        """
        folder = self.paths[0]
        file_name = "{}_reference.{}".format(self.file_names[0], self.file_extensions[0])
        file_path = os.path.join(self.paths[0], file_name)

        os.makedirs(folder, exist_ok=True)

        self._write_reference(reference, file_path)

    def _write_reference(self, reference: dict, file_path: str):
        """
        Writes a reference config file
        :param reference: the data to write
        :param file_path: the file path to write to
        """
        pass

    def _find_config_file(self) -> str or None:
        """
        Tries to find a usable config file
        :return: file path or None
        """
        import os

        for path in self.paths:
            path = os.path.expanduser(path)
            for extension in self.file_extensions:
                for file_name in self.file_names:
                    file_path = os.path.join(path, "{}.{}".format(file_name, extension))
                    if os.path.isfile(file_path):
                        return file_path

        return None

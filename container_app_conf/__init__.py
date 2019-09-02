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

import yaml

from container_app_conf.const import DEFAULT_CONFIG_FILE_PATHS
from container_app_conf.entry import ConfigEntry
from container_app_conf.util import find_duplicates

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


class Config:
    """
    Config base class.
    Extend this in your application.
    """

    _instances = {}

    def __new__(cls, validate: bool = True):
        """
        Creates a config object and reads configuration.
        :param validate: if validation should be run (can be disabled for tests)
        """
        if cls._instances.get(cls, None) is None:
            cls._instances[cls] = super(Config, cls).__new__(cls)

        self = cls._instances[cls]
        self._config_entries = self._find_config_entries()
        self.load_config(validate)

        if self._find_config_file() is None:
            self.write_reference_yaml()

        return Config._instances[cls]

    def load_config(self, validate: bool):
        """
        Loads the configuration from all available sources
        """
        self._read_yaml()
        self._read_env()
        if validate:
            self.validate()

    @property
    def config_file_names(self) -> [str]:
        """
        :return: List of allowed config file names
        """
        raise NotImplementedError()

    @property
    def config_file_extensions(self) -> [str]:
        """
        :return: List of allowed config file extensions
        """
        return ['yaml', 'yml']

    @property
    def config_file_paths(self) -> [str]:
        """
        :return: List of allowed config file paths
        """
        return DEFAULT_CONFIG_FILE_PATHS

    def validate(self):
        """
        Validates the current configuration and throws an exception if something is wrong
        """
        return

    def write_reference_yaml(self):
        """
        Writes a reference config file
        :return:
        """
        reference = self.generate_reference_config()
        text = yaml.dump(reference)

        folder = self.config_file_paths[0]
        file_name = "{}_reference.{}".format(self.config_file_names[0], self.config_file_extensions[0])
        file_path = os.path.join(self.config_file_paths[0], file_name)

        os.makedirs(folder, exist_ok=True)
        with open(file_path, "w") as file:
            file.write(text)

    def generate_reference_config(self) -> {}:
        """
        Generates a dictionary containing the expected config tree filled with default and example values
        :return: a dictionary containing the expected config tree
        """
        entries = self._find_config_entries()

        config_tree = {}
        for entry in entries:
            current_level = config_tree
            for path in entry.yaml_path[:-1]:
                if path not in current_level:
                    current_level[path] = {}
                current_level = current_level[path]

            current_level[entry.yaml_path[-1]] = entry._type_to_value(entry.example)

        return config_tree

    def _find_config_entries(self) -> [ConfigEntry]:
        """
        Detects config entry constants in this class
        :return: list of config entries
        """
        entries = set()
        for attribute in map(lambda x: getattr(self, x), dir(self)):
            if isinstance(attribute, ConfigEntry):
                entries.add(attribute)

        entry_env_keys = list(map(lambda x: x.env_key, entries))
        duplicates = find_duplicates(entry_env_keys)
        if len(duplicates) > 0:
            clashing = ", ".join(duplicates.keys())
            raise ValueError("YAML paths must be unique! Clashing paths: {}".format(clashing))

        return list(entries)

    def _find_config_file(self) -> str or None:
        """
        Tries to find a usable config file
        :return: file path or None
        """
        import os

        for path in self.config_file_paths:
            path = os.path.expanduser(path)
            for extension in self.config_file_extensions:
                for file_name in self.config_file_names:
                    file_path = os.path.join(path, "{}.{}".format(file_name, extension))
                    if os.path.isfile(file_path):
                        return file_path

        return None

    def _read_yaml(self) -> None:
        """
        Reads configuration parameters from a yaml config file (if it exists)
        """

        def _get_value(root: {}, config_entry: ConfigEntry) -> any or None:
            """
            Helper function to read the value of a given config entry
            :param root: the yaml root node dictionary
            :param config_entry: the config entry to search for
            :return: the found value or the config entry's current value
            """
            value = root
            for key in config_entry.yaml_path:
                value = value.get(key)
                if value is None:
                    return config_entry.value

            return value

        file_path = self._find_config_file()
        if file_path is None:
            LOGGER.debug("No config file found for path: {}".format(file_path))
            return

        with open(file_path, 'r') as ymlfile:
            import yaml
            cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
            if not cfg:
                return

            for config_entry in self._config_entries:
                config_entry.value = _get_value(cfg, config_entry)

    def _read_env(self) -> None:
        """
        Reads configuration parameters from environment variables
        """
        import os

        for entry in self._config_entries:
            entry.value = os.environ.get(entry.env_key, entry.value)

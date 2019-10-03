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
import copy
import logging
from typing import Dict, List

from container_app_conf.const import DEFAULT_CONFIG_FILE_PATHS
from container_app_conf.entry import ConfigEntry
from container_app_conf.source import DataSource
from container_app_conf.util import find_duplicates, generate_reference_config

LOGGER = logging.getLogger(__name__)


class ConfigBase:
    """
    Config base class.
    Extend this in your application.
    """

    _instances = {}

    def __new__(cls, data_sources: List[DataSource] = None,
                validate: bool = True,
                singleton: bool = True,
                write_reference: bool = True):
        """
        Creates a config object and reads configuration.
        :param data_sources: list of data sources to use. The first value that holds a value for a specific
                             config entry overshadows other data sources.
        :param validate: if validation should be run (can be disabled for tests)
        :param singleton: if the returned instance should be a singleton
        :param write_reference: Whether to write a reference configuration for all used data sources
        """
        if singleton:
            if cls._instances.get(cls, None) is None:
                instance = super(ConfigBase, cls).__new__(cls)
                cls._instances[cls] = instance
            else:
                instance = cls._instances[cls]
        else:
            instance = super(ConfigBase, cls).__new__(cls)

        self = instance
        self._config_entries = self._find_config_entries()

        if not singleton:
            # copy class attribute to instance to overshadow class attributes
            instance_attributes = {}
            for name, attribute in self._config_entries.items():
                attribute_copy = copy.deepcopy(attribute)
                self.__dict__.setdefault(name, attribute_copy)
                key = "_".join(attribute.key_path)
                instance_attributes[key] = attribute_copy
            # update config_entries list to reflect instance attributes
            self._config_entries = instance_attributes

        if data_sources is None:
            # set default data sources
            from container_app_conf.source.env_source import EnvSource
            from container_app_conf.source.yaml_source import YamlSource

            self.data_sources = [
                EnvSource(),
                YamlSource(cls.__name__)
            ]
        else:
            self.data_sources = data_sources

        if write_reference:
            reference_config = generate_reference_config(list(self._config_entries.values()))
            for data_source in self.data_sources:
                data_source.write_reference(reference_config)

        self.load_config(validate)

        return instance

    def load_config(self, validate: bool):
        """
        Loads the configuration from all available sources
        """
        for source in reversed(self.data_sources):
            for entry in self._config_entries.values():
                if source.has(entry):
                    entry.value = source.get(entry)

        if validate:
            self.validate()

    def validate(self):
        """
        Validates the current configuration and throws an exception if something is wrong
        """
        # reset all entries to make sure None constraints are fulfilled
        for entry in self._config_entries.values():
            entry.value = entry.value

    def _find_config_entries(self) -> Dict[str, ConfigEntry]:
        """
        Detects config entry constants in this class
        :return: list of config entries
        """
        entries = {}
        for name, attribute in dict(map(lambda x: (x, getattr(self, x)), dir(self))).items():
            if isinstance(attribute, ConfigEntry):
                entries[name] = attribute

        entry_env_keys = list(map(lambda x: "->".join(x.key_path), entries.values()))
        duplicates = find_duplicates(entry_env_keys)
        if len(duplicates) > 0:
            clashing = ", ".join(duplicates.keys())
            raise ValueError("Key paths must be unique! Clashing paths: {}".format(clashing))

        return entries

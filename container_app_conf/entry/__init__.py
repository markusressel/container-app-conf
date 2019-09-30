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
import re

from container_app_conf.const import KEY_PATH_REGEX


class ConfigEntry:
    _example = None

    def __init__(self, key_path: [str], example: any = None, description: str or None = None, default: any = None,
                 none_allowed: bool = None):
        """
        Creates a config entry
        :param key_path: list of strings representing f.ex. the yaml tree path
        :param example: example str value
        :param description: a description of this entry
        :param default: the default value
        :param none_allowed: Set to True if a 'None' value may be allowed, False if not,
                             otherwise it will be True if the default value is not None.
        """
        if len(key_path) <= 0:
            raise ValueError("{}: key_path must contain at least one node".format(self.__class__.__name__))
        for item in key_path:
            if not re.match(KEY_PATH_REGEX, item):
                raise ValueError("Key path item '{}' contains invalid characters, please "
                                 "restrict yourself to: {}".format(item, KEY_PATH_REGEX))

        self.key_path = key_path

        self.description = description
        if example is not None:
            self._example = example

        if none_allowed is None:
            none_allowed = default is None
        self._none_allowed = none_allowed

        if default is not None or self._none_allowed:
            self.default = self._parse_value(default)
        else:
            self.default = None
        self._value = default

    @property
    def example(self) -> any:
        return self.default if self.default is not None else self._example

    @property
    def value(self) -> any:
        """
        :return: the value of this config entry
        """
        return self._value

    @value.setter
    def value(self, new_value) -> None:
        """
        :param new_value: the new value to set
        """
        self._value = self._parse_value(new_value)

    def _parse_value(self, value: any) -> any or None:
        """
        Tries to permissively convert the given value to the expected value type.
        :param value: the value to parse
        :return: the parsed value
        """
        if value is None:
            if self._none_allowed:
                return None
            else:
                self._raise_invalid_value(value)

        try:
            return self._value_to_type(value)
        except Exception as ex:
            logging.exception(ex)
            self._raise_invalid_value(value)

    def _value_to_type(self, value: any) -> any:
        """
        Converts the given value to the expected value type of this entry
        :param value: the yaml value
        :return: parsed value
        """
        raise NotImplementedError()

    def _type_to_value(self, type: any) -> any:
        """
        Converts a value of the expected entry type to a valid representation in the config file.
        This is the inverse function of _value_to_type
        :param type: value of expected entry type
        :return: config file value
        """
        return str(type)

    def _raise_invalid_value(self, value: any):
        raise ValueError("Invalid value '{}' for config option `{}`".format(value, ">".join(self.key_path)))

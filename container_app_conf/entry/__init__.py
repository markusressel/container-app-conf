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


class ConfigEntry:

    def __init__(self, yaml_path: [str], default: any = None, none_allowed: bool = None):
        """
        Creates a config entry
        :param yaml_path: list of strings representing the yaml tree path for this entry
        :param default: the default value
        :param none_allowed: Set to True if a 'None' value may be allowed, False if not,
                             otherwise it will be True if the default value is not None.
        """
        self.yaml_path = yaml_path
        self.env_key = "_".join(yaml_path).upper()

        if none_allowed is None:
            none_allowed = default is None
        self._none_allowed = none_allowed

        self.default = self._parse_value(default)
        self._value = default

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
        except:
            self._raise_invalid_value(value)

    def _value_to_type(self, value: any) -> any:
        """
        Converts the given type to the expected type
        :param value: the yaml value
        :return: parsed value
        """
        raise NotImplementedError()

    def _raise_invalid_value(self, value: any):
        raise ValueError("Invalid value '{}' for config option {}".format(value, self.env_key))

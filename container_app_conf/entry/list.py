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

from typing import Type

from container_app_conf import ConfigEntry


class ListConfigEntry(ConfigEntry):
    """
    Config entry allowing to specify a list of items of specified type
    """

    def __init__(self, item_type: Type[ConfigEntry], yaml_path: [str], default: any = None, none_allowed: bool = None):
        """

        :param item_type: the type of individual list items
        :param yaml_path: list of yaml tree entries
        :param default: default value
        :param none_allowed: if None is allowed for this config entry
        """
        self._item_type = item_type
        super().__init__(yaml_path, default, none_allowed)

    def _value_to_type(self, value: any) -> [any] or None:
        """
        Tries to permissively convert the given value to a list of values.
        :param value: the value to parse
        :return: the parsed list
        """
        if not isinstance(value, list):
            value = str(value).split(',')

        return list(map(lambda x: self._item_type._value_to_type(self, x), filter(lambda x: x, value)))

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
import re
from typing import Pattern

from container_app_conf import ConfigEntry

# workaround for deepcopy bug in python<=3.6
# see: https://stackoverflow.com/questions/6279305/typeerror-cannot-deepcopy-this-pattern-object/56935186#56935186
copy._deepcopy_dispatch[type(re.compile(''))] = lambda r, _: r


class RegexConfigEntry(ConfigEntry):
    _example = r"^[a-zA-z0-9]*$"

    def __init__(self, key_path: [str], example: any = None, description: str or None = None, default: any = None,
                 required: bool = None, flags: int or None = None):
        """
        :param flags: Regex flags to mandate or None if no flag restrictions should be made
        """
        self.flags = flags | re.UNICODE if flags is not None else None
        super().__init__(key_path, example, description, default, required)

    def _value_to_type(self, value: any) -> Pattern or None:
        if value is None and self._required:
            return None

        if isinstance(value, Pattern) and self.flags is not None:
            if value.flags == int(self.flags):
                return value
            else:
                raise ValueError("Value does not match expected flags: {}".format(self.flags))

        value = str(value)
        return re.compile(value, flags=self.flags if self.flags is not None else 0)

    def _type_to_value(self, type: any) -> str:
        return type.pattern

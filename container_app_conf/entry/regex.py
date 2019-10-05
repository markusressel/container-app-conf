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

from container_app_conf.entry.string import StringConfigEntry

# workaround for deepcopy bug in python<=3.6
# see: https://stackoverflow.com/questions/6279305/typeerror-cannot-deepcopy-this-pattern-object/56935186#56935186
copy._deepcopy_dispatch[type(re.compile(''))] = lambda r, _: r


class RegexConfigEntry(StringConfigEntry):
    _example = r"^[a-zA-z0-9]*$"

    def _value_to_type(self, value: any) -> str or None:
        s = super()._value_to_type(value)
        if s is None and self._none_allowed:
            return None
        return re.compile(s)

    def _type_to_value(self, type: any) -> str:
        return type.pattern

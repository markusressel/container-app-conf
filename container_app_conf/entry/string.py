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
import re

from container_app_conf import ConfigEntry


class StringConfigEntry(ConfigEntry):
    _example = "text"

    def __init__(self, key_path: [str], example: any = None, description: str or None = None, default: any = None,
                 none_allowed: bool = None, regex: str = None):
        self.regex = re.compile(regex) if regex is not None else None
        super().__init__(key_path, example, description, default, none_allowed)

    def _value_to_type(self, value: any) -> str or None:
        """
        Converts the given type to the expected type
        :param value: the yaml value
        :return: parsed value
        """
        s = str(value)
        if self._none_allowed:
            if s.lower() in ['none', 'null', 'nil']:
                return None

        if self.regex is not None:
            if not self.regex.match(s):
                self._raise_invalid_value(s)

        return s

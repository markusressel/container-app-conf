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
from datetime import timedelta

from pytimeparse import parse

from container_app_conf import ConfigEntry


class TimeDeltaConfigEntry(ConfigEntry):
    _example = "4h32m1s"

    def _value_to_type(self, value: any) -> timedelta or None:
        """
        Tries to permissively convert the given value to a timedelta.
        :param value: the value to parse
        :return: the parsed date value
        """
        if isinstance(value, timedelta):
            return value
        elif isinstance(value, str):
            parsed = parse(value)
            if parsed is None:
                raise ValueError("Cannot parse the given timedelta format: {}".format(value))
            return timedelta(seconds=parsed)
        else:
            self._raise_invalid_value(value)

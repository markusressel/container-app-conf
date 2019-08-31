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

from container_app_conf import ConfigEntry


class BoolConfigEntry(ConfigEntry):
    _example = "true"

    def _value_to_type(self, value: any) -> bool or None:
        """
        Tries to permissively convert the given value to a boolean.
        :param value: the value to parse
        :return: the parsed boolean value
        """
        if type(value) == bool:
            return value
        else:
            s = str(value).lower()

            if s in ['y', 'yes', 'true', 't', '1']:
                return True
            elif s in ['n', 'no', 'false', 'f', '0']:
                return False
            else:
                self._raise_invalid_value(value)

    def _type_to_value(self, type: any) -> any:
        return bool(type)

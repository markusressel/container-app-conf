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


class DataSource:

    def has(self, entry: ConfigEntry) -> bool:
        """
        Checks whether the data source has a value for the given config entry
        :param entry: the config entry to check
        :return: True if the source contains a value for the given entry, False otherwise
        """
        raise NotImplementedError()

    def get(self, entry: ConfigEntry) -> any:
        """
        Retrieve the value of the given key
        :param entry: config entry
        :return: value
        """
        raise NotImplementedError()

    def write_reference(self, reference: dict):
        """
        Writes a reference configuration (if implemented)
        :param reference: the reference config as in tree form
        """
        pass

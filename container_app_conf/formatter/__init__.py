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


class ConfigFormatter:
    """
    Allows config entries to be formatted into a string
    """

    def format(self, data: dict) -> str:
        """
        Formats the given entry data
        :param data: entries to format
        :return: formatted string
        """
        raise NotImplementedError()


class SimpleFormatter(ConfigFormatter):
    """
    Prints all config entries in a human readable manner
    """

    def format(self, data: dict) -> str:
        return "\n".join(self._format(data)).strip()

    def _format(self, data: dict, prefix: str = "") -> [str]:
        """
        Recursively formats the dictionary
        :param data:
        :return:
        """
        lines = []
        for key, value in data.items():
            output = prefix + key
            if isinstance(value, dict):
                lines.extend(self._format(value, "{}->".format(output)))
            else:
                lines.append(output + ": {}".format(value))
        return lines

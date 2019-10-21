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
from typing import List

from container_app_conf import ConfigEntry
from container_app_conf.source.env_source import EnvSource


class ConfigFormatter:
    """
    Allows config entries to be formatted into a string
    """

    def format(self, config) -> str:
        """
        Formats the given configuration
        :param config: config to format
        :return: formatted string
        """
        lines = list(map(self.format_entries, config._config_entries.values()))
        output = "\n".join(lines)
        return output

    def format_entries(self, entries: List[ConfigEntry] or ConfigEntry) -> str:
        """
        Formats the given entries
        :param entries: entries to format
        :return: formatted string
        """
        entries = entries if isinstance(entries, list) else [entries]
        output = "\n".join(list(map(self.format_entry, entries)))
        return output

    def format_entry(self, entry: ConfigEntry) -> str:
        """
        Formats the given entry
        :param entry: entry to format
        :return: formatted string
        """
        if entry.secret:
            value = "*****"
        else:
            value = entry._type_to_value(entry.value)

        return "{}: {}".format(EnvSource.env_key(entry), value)

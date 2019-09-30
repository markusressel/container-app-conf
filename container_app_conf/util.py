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


def find_duplicates(l: list) -> []:
    """
    Finds duplicate entries in the given list
    :param l: the list to check
    :return: map of (value -> list of indexes)
    """
    if not len(l) != len(set(l)):
        return []

    # remember indexes of items with equal hash
    tmp = {}
    for i, v in enumerate(l):
        if v in tmp.keys():
            tmp[v].append(i)
        else:
            tmp[v] = [i]

    result = {}
    for k, v in tmp.items():
        if len(v) > 1:
            result[k] = v

    return result


def generate_reference_config(config_entries: List[ConfigEntry]) -> {}:
    """
    Generates a dictionary containing the expected config tree filled with default and example values
    :return: a dictionary containing the expected config tree
    """
    config_tree = {}
    for entry in config_entries:
        current_level = config_tree
        for path in entry.key_path[:-1]:
            if path not in current_level:
                current_level[path] = {}
            current_level = current_level[path]

        current_level[entry.key_path[-1]] = entry._type_to_value(entry.example)

    return config_tree

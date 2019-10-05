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

import unittest
from datetime import datetime, timedelta

from py_range_parse import Range

from container_app_conf import ConfigBase, ConfigEntry
from container_app_conf.entry.bool import BoolConfigEntry
from container_app_conf.entry.date import DateConfigEntry
from container_app_conf.entry.file import FileConfigEntry, DirectoryConfigEntry
from container_app_conf.entry.float import FloatConfigEntry
from container_app_conf.entry.int import IntConfigEntry
from container_app_conf.entry.list import ListConfigEntry
from container_app_conf.entry.range import RangeConfigEntry
from container_app_conf.entry.regex import RegexConfigEntry
from container_app_conf.entry.string import StringConfigEntry
from container_app_conf.entry.timedelta import TimeDeltaConfigEntry


class TestConfigBase2(ConfigBase):
    BOOL = BoolConfigEntry(
        key_path=["test", "bool"],
        # default=False,
        example=True
    )


class TestConfigBase(ConfigBase):
    BOOL = BoolConfigEntry(
        key_path=["test", "bool"],
        default=False
    )
    STRING = StringConfigEntry(
        key_path=["test", "string"],
        default="default value"
    )
    REGEX = RegexConfigEntry(
        key_path=["test", "regex"],
        default="^[a-zA-Z0-9]$"
    )
    INT = IntConfigEntry(
        key_path=["test", "int"],
        default=100
    )
    FLOAT = FloatConfigEntry(
        key_path=["test", "float"],
        default=1.23
    )
    DATE = DateConfigEntry(
        key_path=["test", "this", "date", "is", "nested", "deep"],
        default=datetime.now()
    )
    TIMEDELTA = TimeDeltaConfigEntry(
        key_path=["test", "this", "timediff", "is", "in", "this", "branch"],
        default=timedelta(seconds=10)
    )
    FILE = FileConfigEntry(
        key_path=["test", "file"],
    )
    DIRECTORY = DirectoryConfigEntry(
        key_path=["test", "directory"],
    )
    RANGE = RangeConfigEntry(
        key_path=["test", "this", "is", "a", "range"],
        default=Range(0, 100)
    )
    STRING_LIST = ListConfigEntry(
        item_type=StringConfigEntry,
        key_path=["test", "this", "is", "a", "list"],
        example=[
            "these",
            "are",
            "test",
            "values"
        ]
    )


class TestBase(unittest.TestCase):
    under_test = TestConfigBase()


class EntryTestBase(TestBase):

    def assert_input_output(self, entry: ConfigEntry, list_of_tuples: [()]):
        for item in list_of_tuples:
            assert len(item) == 2

            input = item[0]
            result = item[1]

            if (type(result) == type) and issubclass(result, BaseException):
                try:
                    entry._parse_value(input)
                    assert False
                except:
                    assert True
            else:
                self.assertEqual(entry._parse_value(input), result)

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

from container_app_conf import Config
from container_app_conf.entry.bool import BoolConfigEntry
from container_app_conf.entry.date import DateConfigEntry
from container_app_conf.entry.float import FloatConfigEntry
from container_app_conf.entry.int import IntConfigEntry
from container_app_conf.entry.list import ListConfigEntry
from container_app_conf.entry.string import StringConfigEntry
from container_app_conf.entry.timedelta import TimeDeltaConfigEntry


class TestConfig2(Config):
    @property
    def config_file_names(self) -> [str]:
        return ["testing"]

    BOOL = BoolConfigEntry(
        yaml_path=["test", "bool"],
        # default=False,
        example=True
    )


class TestConfig(Config):
    @property
    def config_file_names(self) -> [str]:
        return ["testing"]

    BOOL = BoolConfigEntry(
        yaml_path=["test", "bool"],
        default=False
    )
    STRING = StringConfigEntry(
        yaml_path=["test", "string"],
        default="default value"
    )
    INT = IntConfigEntry(
        yaml_path=["test", "int"],
        default=100
    )
    FLOAT = FloatConfigEntry(
        yaml_path=["test", "float"],
        default=1.23
    )
    DATE = DateConfigEntry(
        yaml_path=["test", "this", "date", "is", "nested", "deep"],
        default=datetime.now()
    )
    TIMEDELTA = TimeDeltaConfigEntry(
        yaml_path=["test", "this", "timediff", "is", "in", "this", "branch"],
        default=timedelta(seconds=10)
    )
    STRING_LIST = ListConfigEntry(
        item_type=StringConfigEntry,
        yaml_path=["test", "this", "is", "a", "list"],
        example=[
            "these",
            "are",
            "test",
            "values"
        ]
    )


class TestBase(unittest.TestCase):
    under_test = TestConfig()

    def test_singleton(self):
        assert not TestConfig() == TestConfig2()
        assert TestConfig() == TestConfig()
        assert TestConfig2() == TestConfig2()

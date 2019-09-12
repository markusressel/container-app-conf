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

import os

from py_range_parse import Range

from container_app_conf.entry.bool import BoolConfigEntry
from container_app_conf.entry.date import DateConfigEntry
from container_app_conf.entry.file import FileConfigEntry, DirectoryConfigEntry
from container_app_conf.entry.float import FloatConfigEntry
from container_app_conf.entry.int import IntConfigEntry
from container_app_conf.entry.range import RangeConfigEntry
from container_app_conf.entry.timedelta import TimeDeltaConfigEntry
from tests import EntryTestBase


class EntryTest(EntryTestBase):

    @staticmethod
    def test_bool_entry():
        config_entry = BoolConfigEntry(yaml_path=["bool"])

        true_values = ["y", "yes", "true", "t", 1, True]
        false_values = ["n", "no", "false", "f", 0, False]
        invalid_values = ["hello", 2, 0.1]

        input_output = []

        for tv in true_values:
            input_output.append((tv, True))
        for fv in false_values:
            input_output.append((fv, False))
        for iv in invalid_values:
            input_output.append((iv, ValueError))

        EntryTestBase.assert_input_output(config_entry, input_output)

    @staticmethod
    def test_int_entry():
        config_entry = IntConfigEntry(yaml_path=["int"])
        input_output = [
            ("5", 5),
            (5, 5),
            ("-3", -3),
            (-3, -3)
        ]

        EntryTestBase.assert_input_output(config_entry, input_output)

    @staticmethod
    def test_float_entry():
        config_entry = FloatConfigEntry(yaml_path=["float"])
        input_output = [
            ("5", 5.0),
            (5, 5.0),
            ("-3.0", -3.0),
            (-3.0, -3.0),
            (1.2, 1.2),
            ("1.2", 1.2),
            ("3%", 0.03)
        ]

        EntryTestBase.assert_input_output(config_entry, input_output)

    @staticmethod
    def test_date_entry():
        from datetime import datetime
        from dateutil.tz import tzutc

        config_entry = DateConfigEntry(yaml_path=["date"])
        input_output = [
            ("2008-09-03T20:56:35.450686Z", datetime(2008, 9, 3, 20, 56, 35, 450686, tzinfo=tzutc())),
            ("2008-09-03", datetime(2008, 9, 3, 0, 0, 0, 0)),
        ]

        EntryTestBase.assert_input_output(config_entry, input_output)

    @staticmethod
    def test_timedelta_entry():
        from datetime import timedelta

        config_entry = TimeDeltaConfigEntry(yaml_path=["timedelta"])
        input_output = [
            ("20:56:35", timedelta(hours=20, minutes=56, seconds=35)),
            ("32m", timedelta(minutes=32)),
            ("4h0m3s", timedelta(hours=4, minutes=0, seconds=3)),
            ("4h3s", timedelta(hours=4, minutes=0, seconds=3)),
            ("4:13", timedelta(hours=0, minutes=4, seconds=13)),
        ]

        EntryTestBase.assert_input_output(config_entry, input_output)

    @staticmethod
    def test_file_entry():
        config_entry = FileConfigEntry(yaml_path=["file"])
        input_output = [
            ("/tmp/test", "/tmp/test"),
            ("./test", os.path.abspath("./test")),
            ("/something/", AssertionError),
        ]

        EntryTestBase.assert_input_output(config_entry, input_output)

        config_entry = FileConfigEntry(yaml_path=["file"],
                                       check_existence=True)
        input_output = [
            ("/tmp/test", FileNotFoundError),
        ]

        EntryTestBase.assert_input_output(config_entry, input_output)

    @staticmethod
    def test_directory_entry():
        config_entry = DirectoryConfigEntry(yaml_path=["directory"])
        input_output = [
            ("/tmp", "/tmp"),
            ("./test", os.path.abspath("./test")),
            ("/something/", "/something"),
        ]

        EntryTestBase.assert_input_output(config_entry, input_output)

        config_entry = DirectoryConfigEntry(yaml_path=["directory"],
                                            check_existence=True)

        input_output = [
            ("./", os.path.abspath("./")),
        ]

        EntryTestBase.assert_input_output(config_entry, input_output)

    @staticmethod
    def test_range_entry():
        config_entry = RangeConfigEntry(yaml_path=["range"])
        input_output = [
            ("[-5..5]", Range(-5, 5)),
        ]

        EntryTestBase.assert_input_output(config_entry, input_output)

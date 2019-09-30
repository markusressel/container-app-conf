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
from datetime import datetime
from datetime import timedelta
from pathlib import Path

from dateutil.tz import tzutc

from container_app_conf.entry.date import DateConfigEntry
from container_app_conf.entry.file import FileConfigEntry
from container_app_conf.entry.float import FloatConfigEntry
from container_app_conf.entry.int import IntConfigEntry
from container_app_conf.entry.list import ListConfigEntry
from container_app_conf.entry.timedelta import TimeDeltaConfigEntry
from tests import EntryTestBase


class ListEntryTest(EntryTestBase):

    def test_str_list_entry_custom_delimiter(self):
        config_entry = ListConfigEntry(item_type=IntConfigEntry,
                                       key_path=["int_list"],
                                       delimiter="::")
        input_output = [
            ("1::2::3", [1, 2, 3])
        ]

        self.assert_input_output(config_entry, input_output)

    def test_int_list_entry(self):
        config_entry = ListConfigEntry(item_type=IntConfigEntry,
                                       key_path=["int_list"])
        input_output = [
            ("", []),
            ("5", [5]),
            ("1,2,3", [1, 2, 3])
        ]

        self.assert_input_output(config_entry, input_output)

    def test_float_list_entry(self):
        config_entry = ListConfigEntry(item_type=FloatConfigEntry,
                                       key_path=["float_list"])
        input_output = [
            ("", []),
            ("5", [5.0]),
            ("", []),
            ("1,2.5,3", [1.0, 2.5, 3.0])
        ]

        self.assert_input_output(config_entry, input_output)

    def test_date_list_entry(self):
        config_entry = ListConfigEntry(item_type=DateConfigEntry,
                                       key_path=["date_list"])

        input_example_1 = ["2008-09-03T20:56:35.450686Z", "2008-09-03"]
        output_example_1 = [datetime(2008, 9, 3, 20, 56, 35, 450686, tzinfo=tzutc()),
                            datetime(2008, 9, 3, 0, 0, 0, 0)]
        input_output = [
            (None, None),
            (input_example_1, output_example_1),
            (",".join(input_example_1), output_example_1)
        ]

        self.assert_input_output(config_entry, input_output)

    def test_timedelta_entry(self):
        config_entry = ListConfigEntry(item_type=TimeDeltaConfigEntry,
                                       key_path=["timedelta_list"])
        input_output = [
            (None, None),
            (
                ["20:56:35", "32m", "4h0m3s", "4h3s", "4:13"],
                [timedelta(hours=20, minutes=56, seconds=35),
                 timedelta(minutes=32),
                 timedelta(hours=4, minutes=0, seconds=3),
                 timedelta(hours=4, minutes=0, seconds=3),
                 timedelta(hours=0, minutes=4, seconds=13)]
            )
        ]

        self.assert_input_output(config_entry, input_output)

    def test_file_entry(self):
        config_entry = ListConfigEntry(item_type=FileConfigEntry,
                                       item_args={
                                           "check_existence": False
                                       },
                                       key_path=["file_list"])
        example1 = "/tmp/file"
        example2 = "./file"
        example3 = [example1, example2]
        input_output = [
            (None, None),
            ("/tmp/", AssertionError),
            (example1, [Path(example1)]),
            (example2, [Path(example2)]),
            (",".join(example3), [Path(example1), Path(example2)]),
        ]

        self.assert_input_output(config_entry, input_output)

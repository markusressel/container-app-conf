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

from container_app_conf.entry.bool import BoolConfigEntry
from container_app_conf.entry.float import FloatConfigEntry
from container_app_conf.entry.int import IntConfigEntry
from container_app_conf.entry.list import ListConfigEntry
from tests import TestBase


class EntryTest(TestBase):

    @staticmethod
    def test_bool_entry():
        bool_config_entry = BoolConfigEntry(yaml_path=["bool"])

        true_values = ["y", "yes", "true", "t", 1, True]
        false_values = ["n", "no", "false", "f", 0, False]
        invalid_values = ["hello", 2, 0.1]

        for v in true_values:
            assert bool_config_entry._parse_value(v)

        for v in false_values:
            assert not bool_config_entry._parse_value(v)

        for v in invalid_values:
            try:
                bool_config_entry._parse_value(v)
                assert False
            except ValueError as ex:
                assert ex is not None

    @staticmethod
    def test_int_entry():
        int_config_entry = IntConfigEntry(yaml_path=["int"])

        input_result_map = {
            "5": 5,
            5: 5,
            "-3": -3,
            -3: -3
        }

        for k, v in input_result_map.items():
            assert int_config_entry._parse_value(k) == v

    @staticmethod
    def test_float_entry():
        float_config_entry = FloatConfigEntry(yaml_path=["float"])

        input_result_map = {
            "5": 5.0,
            5: 5.0,
            "-3.0": -3.0,
            -3.0: -3.0,
            1.2: 1.2,
            "1.2": 1.2,
            "3%": 0.03
        }

        for k, v in input_result_map.items():
            assert float_config_entry._parse_value(k) == v

    @staticmethod
    def test_int_list_entry():
        int_list_config_entry = ListConfigEntry(item_type=IntConfigEntry, yaml_path=["int_list"])

        input_result_map = {
            "5": [5],
            "": [],
            "1,2,3": [1, 2, 3]
        }

        for k, v in input_result_map.items():
            assert int_list_config_entry._parse_value(k) == v

    @staticmethod
    def test_float_list_entry():
        int_list_config_entry = ListConfigEntry(item_type=FloatConfigEntry, yaml_path=["float_list"])

        input_result_map = {
            "5": [5.0],
            "": [],
            "1,2.5,3": [1.0, 2.5, 3.0]
        }

        for k, v in input_result_map.items():
            assert int_list_config_entry._parse_value(k) == v

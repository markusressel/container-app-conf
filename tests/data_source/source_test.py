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
from typing import Dict
from unittest import mock

from container_app_conf import ConfigEntry
from container_app_conf.entry.int import IntConfigEntry
from container_app_conf.entry.string import StringConfigEntry
from container_app_conf.source.env_source import EnvSource
from container_app_conf.source.json_source import JsonSource
from container_app_conf.source.toml_source import TomlSource
from container_app_conf.source.yaml_source import YamlSource
from tests import TestBase
from tests.data_source import MemoryDataSource
from tests.singleton_test import TestConfigBase2


class MemoryDataSource1(MemoryDataSource):

    def items(self) -> Dict[ConfigEntry, any]:
        return {
            TestConfigBase2.BOOL: True
        }


class MemoryDataSource2(MemoryDataSource):

    def items(self) -> Dict[ConfigEntry, any]:
        return {
            TestConfigBase2.BOOL: False
        }


class TestDataSource(TestBase):

    def test_priority(self):
        conf = TestConfigBase2(data_sources=[
            MemoryDataSource1(),
            MemoryDataSource2()
        ], singleton=False)

        self.assertTrue(conf.BOOL.value)

        conf2 = TestConfigBase2(data_sources=[
            MemoryDataSource2(),
            MemoryDataSource1()
        ], singleton=False)

        self.assertFalse(conf2.BOOL.value)

    def test_toml(self):
        str_entry = StringConfigEntry(
            key_path=["testing", "key1"],
            default="value"
        )
        int_entry = IntConfigEntry(
            key_path=["testing", "key2"],
            default=2
        )
        source = TomlSource("test", ["./", "./tests"])
        source.load()
        self.assertTrue(source.has(str_entry))
        self.assertEqual(source.get(str_entry), "value")
        self.assertTrue(source.has(int_entry))
        self.assertEqual(source.get(int_entry), 2)

    def test_yaml(self):
        str_entry = StringConfigEntry(
            key_path=["testing", "key1"],
            default="value"
        )
        int_entry = IntConfigEntry(
            key_path=["testing", "key2"],
            default=2
        )
        source = YamlSource("test", ["./", "./tests"])
        source.load()
        self.assertTrue(source.has(str_entry))
        self.assertEqual(source.get(str_entry), "value")
        self.assertTrue(source.has(int_entry))
        self.assertEqual(source.get(int_entry), 2)

    def test_json(self):
        str_entry = StringConfigEntry(
            key_path=["testing", "key1"],
            default="value"
        )
        int_entry = IntConfigEntry(
            key_path=["testing", "key2"],
            default=2
        )
        source = JsonSource("test", ["./", "./tests"])
        source.load()
        self.assertTrue(source.has(str_entry))
        self.assertEqual(source.get(str_entry), "value")
        self.assertTrue(source.has(int_entry))
        self.assertEqual(source.get(int_entry), 2)

    def test_env(self):
        str_entry = StringConfigEntry(
            key_path=["test-ing", "key1"],
            default="value"
        )
        int_entry = IntConfigEntry(
            key_path=["testing", "key2"],
            default=2
        )

        source = EnvSource()
        original_key = EnvSource.env_key(str_entry)
        expected = "expected"
        with mock.patch.dict(os.environ, {original_key: expected}, clear=True):
            source.load()

        self.assertTrue(source.has(str_entry))
        self.assertEqual(source.get(str_entry), expected)
        self.assertFalse(source.has(int_entry))

        normalized_env_key = original_key.replace('-', '_')
        self.assertNotEqual(original_key, normalized_env_key)
        with mock.patch.dict(os.environ, {normalized_env_key: expected + '2'}, clear=True):
            source.load()

        self.assertTrue(source.has(str_entry))
        self.assertEqual(source.get(str_entry), expected + '2')
        self.assertFalse(source.has(int_entry))

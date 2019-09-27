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
from container_app_conf import DataSource, ConfigEntry
from tests import TestBase
from tests.singleton_test import TestConfigBase2


class MemoryDataSource(DataSource):
    data = {
        TestConfigBase2.BOOL.env_key: True
    }

    def has(self, entry: ConfigEntry) -> bool:
        return entry.env_key in self.data.keys()

    def get(self, entry: ConfigEntry) -> any:
        return self.data[entry.env_key]


class MemoryDataSource2(MemoryDataSource):
    data = {
        TestConfigBase2.BOOL.env_key: False
    }


class TestDataSource(TestBase):

    def test_yaml_env_priority(self):
        conf = TestConfigBase2(data_sources=[
            MemoryDataSource(),
            MemoryDataSource2()
        ], singleton=False)

        self.assertTrue(conf.BOOL.value)

        conf2 = TestConfigBase2(data_sources=[
            MemoryDataSource2(),
            MemoryDataSource()
        ], singleton=False)

        self.assertFalse(conf2.BOOL.value)

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
from container_app_conf import ConfigBase
from container_app_conf.entry.bool import BoolConfigEntry
from tests import TestBase, TestConfigBase


class TestConfigBase2(ConfigBase):
    BOOL = BoolConfigEntry(
        key_path=["test", "bool"],
        # default=False,
        example=True
    )


class TestSingleton(TestBase):

    def test_singleton(self):
        assert not TestConfigBase() == TestConfigBase2()
        assert TestConfigBase() == TestConfigBase()
        assert TestConfigBase2() == TestConfigBase2()

    def test_singleton_config_entry(self):
        conf1 = TestConfigBase()
        conf2 = TestConfigBase()

        conf1.INT.value = 1
        conf2.INT.value = 2

        self.assertEqual(conf1.INT.value, conf2.INT.value)

    def test_instance_config_entry(self):
        conf1 = TestConfigBase()
        conf2 = TestConfigBase(singleton=False)
        conf3 = TestConfigBase(singleton=False)

        conf1.INT.value = 1
        conf2.INT.value = 2
        conf3.INT.value = 3

        self.assertNotEqual(conf1.INT.value, conf2.INT.value)
        self.assertNotEqual(conf1.INT.value, conf3.INT.value)
        self.assertNotEqual(conf2.INT.value, conf3.INT.value)

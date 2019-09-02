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
from container_app_conf import Config
from container_app_conf.entry.bool import BoolConfigEntry
from container_app_conf.entry.string import StringConfigEntry
from tests import TestBase


class TestConfigClashing(Config):
    clashing_yaml_path = ["test", "bool"]

    @property
    def config_file_names(self) -> [str]:
        return ["clashing_keys"]

    BOOL = BoolConfigEntry(
        yaml_path=clashing_yaml_path,
        default=False)

    STRING = StringConfigEntry(
        yaml_path=clashing_yaml_path,
        default="test"
    )


class TestClashingKeys(TestBase):

    def test_clashing_keys(self):
        with self.assertRaises(ValueError):
            TestConfigClashing()

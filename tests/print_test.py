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

from tests import EntryTestBase, TestConfigBase


class PrintTest(EntryTestBase):

    def test_print_simple(self):
        config = TestConfigBase()
        output = config.print()
        self.assertIsNotNone(output)

    def test_print_yaml(self):
        config = TestConfigBase()
        from container_app_conf.formatter.yaml import YamlFormatter
        output = config.print(YamlFormatter())
        self.assertIsNotNone(output)

    def test_print_toml(self):
        config = TestConfigBase()
        from container_app_conf.formatter.toml import TomlFormatter
        output = config.print(TomlFormatter())
        self.assertIsNotNone(output)

    def test_print_json(self):
        config = TestConfigBase()
        from container_app_conf.formatter.json import JsonFormatter
        output = config.print(JsonFormatter())
        self.assertIsNotNone(output)

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
import copy
import os

from container_app_conf import ConfigEntry
from container_app_conf.source import DataSource


class EnvSource(DataSource):
    """
    Data source utilizing environment variables
    """
    KEY_SPLIT_CHAR = "_"

    def has(self, entry: ConfigEntry) -> bool:
        original_key = self.env_key(entry)
        normalized_key = original_key.replace('-', '_')
        return original_key in self.root.keys() or normalized_key in self.root.keys()

    def get(self, entry: ConfigEntry) -> str or None:
        original_key = self.env_key(entry)
        normalized_key = original_key.replace('-', '_')
        return self.root.get(original_key, self.root.get(normalized_key, None))

    @staticmethod
    def env_key(entry: ConfigEntry) -> str:
        return EnvSource.KEY_SPLIT_CHAR.join(entry.key_path).upper()

    def _load(self) -> dict:
        return copy.deepcopy(os.environ)

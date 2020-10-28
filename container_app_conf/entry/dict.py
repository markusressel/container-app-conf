#  Copyright (c) 2020 Markus Ressel
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
import ast
import json

from voluptuous import Schema

from container_app_conf import ConfigEntry


class DictConfigEntry(ConfigEntry):

    def __init__(self, key_path: [str], example: any = None, description: str or None = None, default: any = None,
                 required: bool = None, secret: bool = None, schema: Schema = None):
        self.schema = schema
        super().__init__(key_path, example, description, default, required, secret)

    def _value_to_type(self, value: any) -> any:
        if isinstance(value, str):
            try:
                value = ast.literal_eval(value)
            except Exception as ex:
                self._raise_invalid_value(value, f"Cannot parse string to dictionary: {ex}")

        if self.schema is not None:
            try:
                value = self.schema(value)
            except Exception as ex:
                self._raise_invalid_value(value, f"Schema validation failed: {ex}")

        return value

    def _type_to_value(self, type: any) -> any:
        if type is None:
            return None
        return json.dumps(type)

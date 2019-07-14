# container-app-conf

This is a library to easily read application values
from multiple places like a yaml file and environment variables
while providing type validation.

The initial purpose of this library was to have an easy way to configure
applications running inside some kind of container (Docker in this case)
using environment variables while still provide the possibility to use
a more simple form of configuration like a yaml file.

# How to use

```shell
pip install container-app-conf
```

## Extend `Config` base

```python
from container_app_conf import Config
from container_app_conf.entry.string import StringConfigEntry

class AppConfig(Config):

    @property
    def config_file_names(self) -> [str]:
        return ["my_app_config_file_name"]
        
    MY_CONFIG = StringConfigEntry(
        yaml_path=[
            "my_app_config_file_name",
            "example"
        ],
        none_allowed=False)

```

## Config Types

### Bool

```python
from container_app_conf.entry.bool import BoolConfigEntry
ALIVE = BoolConfigEntry(
        yaml_path=[
            "my_app_config_file_name",
            "alive"
        ],
        default=True)
```

### Int

```python
from container_app_conf.entry.int import IntConfigEntry
AGE = IntConfigEntry(
        yaml_path=[
            "my_app_config_file_name",
            "age"
        ],
        default=16)
```

### Float

```python
from container_app_conf.entry.float import FloatConfigEntry
CHILDREN = FloatConfigEntry(
        yaml_path=[
            "my_app_config_file_name",
            "children"
        ],
        none_allowed=True,
        default=1.58)
```

### String

```python
from container_app_conf.entry.string import StringConfigEntry
NAME = StringConfigEntry(
        yaml_path=[
            "my_app_config_file_name",
            "name"
        ])
```

### StringList

```python
from container_app_conf.entry.list import StringListConfigEntry
FRIENDS = StringListConfigEntry(
        yaml_path=[
            "my_app_config_file_name",
            "friends"
        ],
        default=[])
```

## Default Values

A default value can be specified for every `ConfigEntry` by using the
`default` constructor parameter.

## Allow `None` 

By default a `None` value is only allowed if the default value is `None`.
This means it is not possible to set the `MY_CONFIG` entry in the example
at the top to `None` even after initial parsing. Specifying an empty text
in the yaml or corresponding environment variable will result in an
exception. If you want to allow setting a `None` value you can use the
`none_allowed` constructor parameter.


# Contributing

GitHub is for social coding: if you want to write code, I encourage contributions through pull requests from forks
of this repository. Create GitHub tickets for bugs and new features and comment on the ones that you are interested in.


# License
```text
container-app-conf
Copyright (c) 2019 Markus Ressel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

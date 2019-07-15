# container-app-conf ![https://badge.fury.io/py/container-app-conf](https://badge.fury.io/py/container-app-conf.svg) [![Build Status](https://travis-ci.org/markusressel/container-app-conf.svg?branch=master)](https://travis-ci.org/markusressel/container-app-conf)

**container-app-conf** is a library to easily read application values
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

| Name                     | Description                              | Type     |
|--------------------------|------------------------------------------|----------|
| `BoolConfigEntry`        | Parses `bool`, `int` (`0` and `1`) and `str` values (`yes`, `no` etc.) to a boolean value | `bool` |
| `IntConfigEntry`         | Parses input to an integer | `int` |
| `FloatConfigEntry`       | Parses input to a floating number | `float` |
| `StringConfigEntry`      | Takes the raw string input | `str` |
| `ListConfigEntry`        | Parses a comma separated string to a list of items specified in another `ConfigEntry` (in yaml it can also be specified as a yaml list) | `[]` |

If none of the existing types suit your needs you can easily create your 
own by extending the `ConfigEntry` base class.

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

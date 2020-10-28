# container-app-conf [![Contributors](https://img.shields.io/github/contributors/markusressel/container-app-conf.svg)](https://github.com/markusressel/container-app-conf/graphs/contributors) [![MIT License](https://img.shields.io/github/license/markusressel/container-app-conf.svg)](/LICENSE) [![Code Climate](https://codeclimate.com/github/markusressel/container-app-conf.svg)](https://codeclimate.com/github/markusressel/container-app-conf) ![Code Size](https://img.shields.io/github/languages/code-size/markusressel/container-app-conf.svg) ![https://badge.fury.io/py/container-app-conf](https://badge.fury.io/py/container-app-conf.svg) [![Build Status](https://travis-ci.org/markusressel/container-app-conf.svg?branch=master)](https://travis-ci.org/markusressel/container-app-conf)

**container-app-conf** is a library to easily read application configuration values
from multiple sources (YAML, env) while providing type validation.

The initial purpose of this library was to have an easy way to configure
an application running inside of a container using environment variables 
(Docker in this case) and still provide the possibility to use a more simple 
form of configuration like a YAML file.

**container-app-conf is used by**
* [python-n26](https://github.com/femueller/python-n26)
* [InfiniteWisdom](https://github.com/ekeih/InfiniteWisdom)
* [DeineMudda](https://github.com/markusressel/DeineMudda)
* [py-image-dedup](https://github.com/markusressel/py-image-dedup)

and hopefully many others :)

# How to use


## Install dependency

```shell
pip install container-app-conf
```

## Extend `ConfigBase` base

Create a custom configuration class and define your config entries:

```python
from container_app_conf import ConfigBase
from container_app_conf.entry.string import StringConfigEntry

class AppConfig(ConfigBase):

    MY_CONFIG = StringConfigEntry(
        description="This is just a demo text config entry",
        example="example",
        key_path=[
            "my_app",
            "example"
        ],
        required=True)
```

## Use configuration values

```python
config = AppConfig()

value = config.MY_CONFIG.value
```

## Print current config

Oftentimes it can be useful to print the current configuration of an
application. To do this you can use

```python
config = AppConfig()
config.print()
```

which will result in an output similar to this:

```text
test->bool: _REDACTED_
test->this->date->is->nested->deep: 2019-10-22T04:21:02.316907
test->this->is->a->range: [0..100]
test->this->is->a->list: None
test->this->timediff->is->in->this->branch: 0:00:10
test->directory: None
test->file: None
test->float: 1.23
test->int: 100
test->regex: ^[a-zA-Z0-9]$
test->string: default value
secret->list: _REDACTED_
secret->regex: _REDACTED_
```

If you don't like the style you can specify a custom `ConfigFormatter`
like this:

```python
from container_app_conf.formatter.toml import TomlFormatter
config = AppConfig()
config.print(TomlFormatter())
```

Which would output the same config like this:

```text
[test]
bool = "_REDACTED_"
float = 1.23
int = 100
regex = "^[a-zA-Z0-9]$"
string = "default value"

[secret]
list = "_REDACTED_"
regex = "_REDACTED_"

[test.this.is.a]
range = "[0..100]"

[test.this.date.is.nested]
deep = "2019-10-22T04:26:10.654541"

[test.this.timediff.is.in.this]
branch = "0:00:10"
```

## Generate reference config

You can generate a reference configuration from a config object.
This reference contains **all** available configuration options. 
If a **default** was specified for an entry it will be used, 
otherwise the **example** value.

```python
from container_app_conf.util import generate_reference_config
config = AppConfig()
reference_config = generate_reference_config(config._config_entries.values())
```

This will return a dictionary representing the config entry tree.
You can also specify a formatter and write a reference config to a 
file using:

```python
from container_app_conf.util import write_reference
from container_app_conf.formatter.yaml import YamlFormatter
config = AppConfig()
write_reference(config, "/home/markus/.config/example.yaml", YamlFormatter())
```

If the generated reference contains values that do not make sense 
because of application constraints, specify your own **example** 
or better yet **default** value using the respective config entry 
constructor parameter.

## Config Types

| Name                     | Description                              | Type     |
|--------------------------|------------------------------------------|----------|
| `BoolConfigEntry`        | Parses `bool`, `int` (`0` and `1`) and `str` values (`yes`, `no` etc.) to a boolean value | `bool` |
| `IntConfigEntry`         | Parses input to an integer | `int` |
| `FloatConfigEntry`       | Parses input to a floating number | `float` |
| `RangeConfigEntry`       | Parses input to a range (see [py-range-parse](https://github.com/markusressel/py-range-parse)) | `Range` |
| `StringConfigEntry`      | Takes the raw string input | `str` |
| `RegexConfigEntry`       | Parses and compiles regular expressions | `re.pattern` |
| `DateConfigEntry`        | Parses various datetime formats (see [python-dateutil](https://github.com/dateutil/dateutil/)) | `datetime` |
| `TimeDeltaConfigEntry`   | Parses various timedelta formats (see [pytimeparse](https://github.com/wroberts/pytimeparse)) | `timedelta` |
| `FileConfigEntry`        | Parses a file path | `Path` |
| `DirectoryConfigEntry`   | Parses a directory path | `Path` |
| `DictConfigEntry`        | Parses a dictionary | `dict` |
| `ListConfigEntry`        | Parses a comma separated string to a list of items specified in another `ConfigEntry` (in yaml it can also be specified as a yaml list) | `[]` |

If none of the existing types suit your needs you can easily create your 
own by extending the `ConfigEntry` base class.

## Default Values

A default value can be specified for every `ConfigEntry` by using the
`default` constructor parameter.

## Required values

By default config entries with a default different from `None` are 
required. A `None` value is only allowed for an entry if it has no 
default (or it is set to `None` explicitly).

For required entries it is not possible to set its value `None` even 
after initial parsing. Omitting a value for this entry in all data 
sources will result in an exception.

If an entry requires a value and has no default, set the `required`
constructor parameter to `True`.

If you want to allow setting a `None` value even if the default value 
is **not** `None`, you have to explicitly set `required=False`.

## Secret values

If your config contains secret values like passwords you can mark them
as such using the `secret=True` constructor parameter. That way their 
value will be redacted when [printing the current configuration](#print-current-config).

## Data sources

**container-app-conf** supports the simultaneous use of multiple data 
sources to determine configuration values. The following 
implementations are available:

| Name                     | Description                              |
|--------------------------|------------------------------------------|
| `EnvSource`              | Reads environment variables |
| `YamlSource`             | Parses `YAML` files |
| `TomlSource`             | Parses `TOML` files |
| `JsonSource`             | Parses `JSON` files |

### EnvSource

#### ENV Key

Since you only specify the key path of a config entry the ENV
key is generated automatically by concatenating all key path items 
using an underscore and converting to uppercase:

```python
key_path = ["my_app", "example"]
env_key = "_".join(key_path).upper()
```

yields `MY_APP_EXAMPLE`.


### Filesystem Source

Multiple data sources using the filesystem are available:

* YamlSource
* TomlSource
* JsonSource

#### File paths

By default config files are searched for in multiple 
directories that are commonly used for configuration files which include:

- `./`
- `~/.config/`
- `~/`

This can be customized using the `path` constructor parameter: 

```python
from container_app_conf.source.yaml_source import YamlSource
yaml_source = YamlSource(file_name="myapp", path=["/my/path", "/my/other/path"])
```

## Singleton

By default every `Config` subclass instance will behave like a 
singleton. This means if you change the config value in one instance it 
will also affect all other instances of the same `__class__`.

To be able to create multiple instances of a config that are independent 
of one another this behaviour can be disabled using the `singleton` 
constructor parameter:

```python
config1 = AppConfig(singleton=False)
config2 = AppConfig(singleton=False)
```

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

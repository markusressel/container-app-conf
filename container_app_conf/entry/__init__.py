class ConfigEntry:

    def __init__(self, yaml_path: [str], default: any = None, none_allowed: bool = None):
        """
        Creates a config entry
        :param yaml_path: list of strings representing the yaml tree path for this entry
        :param default: the default value
        :param none_allowed: Set to True if a 'None' value may be allowed, False if not,
                             otherwise it will be True if the default value is not None.
        """
        self.yaml_path = yaml_path
        self.env_key = "_".join(yaml_path).upper()

        if none_allowed is None:
            none_allowed = default is None
        self._none_allowed = none_allowed

        self.default = self._parse_value(default)
        self._value = default

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = self._parse_value(new_value)

    def _parse_value(self, value: any) -> any:
        """
        Tries to permissively convert the given value to the expected value type.
        :param value: the value to parse
        :return: the parsed value
        """
        if value is None:
            if self._none_allowed:
                return None
            else:
                self._raise_invalid_value(value)

        try:
            return self._value_to_type(value)
        except:
            self._raise_invalid_value(value)

    def _value_to_type(self, value: any) -> any:
        raise NotImplementedError()

    def _raise_invalid_value(self, value: any):
        raise ValueError("Invalid value '{}' for config option {}".format(value, self.env_key))

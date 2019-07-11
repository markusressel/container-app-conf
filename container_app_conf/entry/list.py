from container_app_conf.entry.string import StringConfigEntry


class StringListConfigEntry(StringConfigEntry):

    def _value_to_type(self, value: any) -> any:
        if not isinstance(value, list):
            value = str(value).split(',')

        return list(map(lambda x: StringConfigEntry._value_to_type(self, x), value))

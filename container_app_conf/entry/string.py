from container_app_conf import ConfigEntry


class StringConfigEntry(ConfigEntry):

    def _value_to_type(self, value: any) -> any:
        s = str(value)
        if self._none_allowed:
            if s.lower() in ['none', 'null', 'nil']:
                return None

        return s

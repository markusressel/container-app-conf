from container_app_conf import ConfigEntry


class FloatConfigEntry(ConfigEntry):

    def _value_to_type(self, value: any) -> any:
        return float(value)

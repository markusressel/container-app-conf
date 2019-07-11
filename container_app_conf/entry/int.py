from container_app_conf import ConfigEntry


class IntConfigEntry(ConfigEntry):

    def _value_to_type(self, value: any) -> any:
        return int(value)

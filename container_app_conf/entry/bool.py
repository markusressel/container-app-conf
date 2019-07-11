from container_app_conf import ConfigEntry


class BoolConfigEntry(ConfigEntry):

    def _value_to_type(self, value: any) -> any:
        if type(value) == bool:
            return value
        else:
            s = str(value).lower()

            if s in ['y', 'yes', 'true', 't', '1']:
                return True
            elif s in ['n', 'no', 'false', 'f', '0']:
                return False
            else:
                self._raise_invalid_value(value)

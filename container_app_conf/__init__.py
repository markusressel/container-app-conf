import logging

from container_app_conf.const import DEFAULT_CONFIG_FILE_PATHS
from container_app_conf.entry import ConfigEntry

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


class Config:

    def __init__(self, validate: bool = True):
        """
        Creates a config object and reads configuration.
        """
        self._config_entries = self._find_config_entries()
        self._read_yaml()
        self._read_env()
        if validate:
            self.validate()

    @property
    def config_file_names(self) -> [str]:
        raise NotImplementedError()

    @property
    def config_file_extensions(self) -> [str]:
        return ['yaml', 'yml']

    @property
    def config_file_paths(self) -> [str]:
        return DEFAULT_CONFIG_FILE_PATHS

    def validate(self):
        """
        Validates the current configuration and throws an exception if something is wrong
        """
        return

    def _find_config_entries(self) -> [ConfigEntry]:
        """
        Detects config entry constants in this class
        :return: list of config entries
        """

        entries = set()
        for attribute in map(lambda x: getattr(self, x), dir(self)):
            if isinstance(attribute, ConfigEntry):
                entries.add(attribute)

        return list(entries)

    def _read_yaml(self) -> None:
        """
        Reads configuration parameters from a yaml config file (if it exists)
        """

        def _get_value(root: {}, config_entry: ConfigEntry):
            value = root
            for key in config_entry.yaml_path:
                value = value.get(key)
                if value is None:
                    return config_entry.value

            return value

        file_path = self._find_config_file()
        if file_path is None:
            LOGGER.debug("No config file found, skipping.")
            return

        with open(file_path, 'r') as ymlfile:
            import yaml
            cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
            if not cfg:
                return

            for config_entry in self._config_entries:
                config_entry.value = _get_value(cfg, config_entry)

    def _find_config_file(self) -> str or None:
        """
        Tries to find a usable config file
        :return: file path or None
        """
        import os

        for path in self.config_file_paths:
            path = os.path.expanduser(path)
            for extension in self.config_file_extensions:
                for file_name in self.config_file_names:
                    file_path = os.path.join(path, "{}.{}".format(file_name, extension))
                    if os.path.isfile(file_path):
                        return file_path

        return None

    def _read_env(self):
        """
        Reads configuration parameters from environment variables
        """
        import os

        for entry in self._config_entries:
            entry.value = os.environ.get(entry.env_key, entry.value)

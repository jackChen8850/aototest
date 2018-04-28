"""
Some auxiliary functions
"""
import os
import json
from ..conf import settings
from .exception import ConfigNotExistError,ConfigParseError


def _config():
    config_path = os.path.join(settings.BASE_DIR, "project.config")
    if not os.path.exists(config_path):
        raise ConfigNotExistError("config not exist")

    with open(config_path, encoding="utf-8") as f:
        c = f.read()
    try:
        c = json.loads(c)
        return c
    except Exception as e:
        raise ConfigParseError(e)

class Variable(dict):
    def __init__(self, *args, **kwargs):
        super(Variable, self).__init__(*args, **kwargs)
        if "config" in kwargs:
            self.config = kwargs["config"]
        else:
            self.config=_config()

    def __getattr__(self, name):
        if not name in self.config:
            raise Exception('config has no attr "{}"'.format(name))
        value = self.config[name]
        if isinstance(value, dict):
            value = Variable(config=value)
        return value


VAR = Variable()

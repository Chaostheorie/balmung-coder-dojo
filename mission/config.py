from os import path
from json import load, loads, dump
from aiofile import AIOFile
from mission.errors import ConfigError


def load_config(instance=None):
    """Loads config and can use instance for only selecting
       'instance' from config"""
    if not path.exists("config.json"):
        raise ConfigError("config.json was not found in local directory")
    try:
        with open("config.json") as f:
            if instance is None:
                return load(f)
            else:
                return load(f)[instance]
    except ValueError as e:
        raise ConfigError(f"config.json is not proper JSON ({e})")
    except KeyError:
        raise ConfigError(f"instance {instance} was not found in config.json")


async def aioload_config(instance=None):
    """Loads config from config.json with aiofile.AIOFile"""
    if not path.exists("config.json"):
        raise ConfigError("config.json was not found in local directory")
    try:
        async with AIOFile("config.json", "r") as afp:
            if instance is None:
                return loads(await afp.read())
            else:
                return loads(await afp.read())[instance]
    except ValueError as e:
        raise ConfigError(f"config.json is not proper JSON ({e})")
    except KeyError:
        raise ConfigError(f"instance {instance} was not found in config.json")


def write_config(config, instance=None):
    """writes config and can use instance for only selecting
       'instance' to write to config"""
    if not path.exists("config.json"):
        raise ConfigError("config.json was not found in local directory")
    try:
        with open("config.json", "w") as f:
            if instance is None:
                return dump(f, config)
            else:
                conf = load_config()
                conf["instance"] = config
                return dump(f, conf)
    except ValueError as e:
        raise ConfigError(f"config.json is not proper JSON ({e})")

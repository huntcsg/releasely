import copy
import functools
import logging

from pip._vendor import pytoml

logger = logging.getLogger(__name__)

default_config = {
    "filepaths": {"release_spec": "release.rst", "changelog": "docs/changes.rst"}
}


@functools.lru_cache()
def load_project_config():
    try:
        with open("pyproject.toml") as f:
            conf = pytoml.load(f).get("tool", {}).get("releasely", default_config)
            for category in default_config:
                conf.setdefault(category, type(default_config[category]))
                if isinstance(default_config[category], dict):
                    for key, value in default_config[category].items():
                        if key not in conf[category]:
                            logger.debug(
                                "Setting default config: conf[{!r}][{!r}] to {!r}".format(
                                    category, key, value
                                )
                            )
                            conf[category][key] = value
    except FileNotFoundError:
        conf = copy.deepcopy(default_config)

    return conf

import toml
import os
import copy

default_config = {
    'release_filepath': 'release.rst',
    'changelog_filepath': 'docs/changes.rst',
}


def load_project_config():
    try:
        with open('pyproject.toml') as f:
            conf = toml.load(f).get('tool', {}).get('releasely', default_config)
            for key, value in default_config.items():
                if key not in conf:
                    conf[key] = value
    except FileNotFoundError:
        conf = copy.deepcopy(default_config)

    return conf

try:
    from pip._vendor import pytoml

    toml_load = pytoml.load
except ImportError:
    from pip._vendor import toml

    toml_load = toml.load

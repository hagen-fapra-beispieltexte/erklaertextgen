import toml

CONFIG_PATH = "./config/config.toml"


def read_config():
    with open(CONFIG_PATH, "r") as f:
        return toml.load(f)

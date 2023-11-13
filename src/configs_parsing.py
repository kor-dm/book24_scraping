from json import load

def parse_configs(name: str) -> dict:
    """
    Read configuration from .json file in /configs folder
    """
    name = "./configs/" + name + ".json"
    with open(name, "r") as conf:
        conf_data = load(conf)
        return conf_data
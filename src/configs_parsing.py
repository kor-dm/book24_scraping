from json import load

def parse_configs(name: str) -> dict:
    name = "./configs/" + name + ".json"
    with open(name, "r") as conf:
        conf_data = load(conf)
        return conf_data
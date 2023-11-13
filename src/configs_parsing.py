import json

def parse_configs(name):
    name = "./configs/" + name + ".json"
    with open(name, "r") as conf:
        conf_data = json.load(conf)
        return conf_data
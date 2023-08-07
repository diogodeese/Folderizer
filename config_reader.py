import json

def read_config():
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    return config
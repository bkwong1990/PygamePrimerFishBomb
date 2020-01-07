import json
import copy

config_file_name = "config.json"

default_config_info = {
  "fullscreen": False,
  "missile_maxspeed": 20,
  "max_tank_count": 2
}

def get_config_info():
    config_info = copy.deepcopy(default_config_info)

    try:
        with open(config_file_name, "r") as json_file:
            config_info = json.load(json_file)
            print("Successfully read from " + config_file_name)

    except:
        print("Couldn't read " + config_file_name)
        print("Using default config instead")

    return config_info

def save_config(config_info):
    try:
        with open(config_file_name, "w") as json_file:
            json.dump(config_info, json_file, indent=2, separators=(", ", " : "))
            print("Successfully wrote to " + config_file_name)
    except:
        print("Couldn't save " + config_file_name)

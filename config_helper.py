import json
import copy

#Speed limits

MISSILE_SPEED_UPPER_CAP = 30
MISSILE_SPEED_LOWER_CAP = 10

# Tank count limits
TANK_UPPER_CAP = 3
TANK_LOWER_CAP = 1

config_file_name = "config.json"

default_config_info = {
  "fullscreen": False,
  "missile_maxspeed": MISSILE_SPEED_UPPER_CAP,
  "max_tank_count": TANK_UPPER_CAP
}

config_info = copy.deepcopy(default_config_info)

def is_on_hardest_setting():
    return (config_info["missile_maxspeed"] == MISSILE_SPEED_UPPER_CAP) and (config_info["max_tank_count"] == TANK_UPPER_CAP)

def correct_missile_speed(missile_speed):
    return max( min( missile_speed, MISSILE_SPEED_UPPER_CAP ), MISSILE_SPEED_LOWER_CAP )

def correct_tank_count(tank_count):
    return max( min( tank_count, TANK_UPPER_CAP ), TANK_LOWER_CAP  )

def load_config_info():
    #config_info = copy.deepcopy(default_config_info)
    global config_info
    try:
        with open(config_file_name, "r") as json_file:
            config_info = json.load(json_file)
            print("Successfully read from " + config_file_name)
        config_info["missile_maxspeed"] = correct_missile_speed(config_info["missile_maxspeed"])
        config_info["max_tank_count"] = correct_tank_count(config_info["max_tank_count"])

    except:
        print("Couldn't read " + config_file_name)
        print("Using default config instead")

def save_config():
    try:
        with open(config_file_name, "w") as json_file:
            json.dump(config_info, json_file, indent=2, separators=(", ", " : "))
            print("Successfully wrote to " + config_file_name)
    except:
        print("Couldn't save " + config_file_name)

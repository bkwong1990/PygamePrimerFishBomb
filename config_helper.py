import json
import copy

#Speed limits

MISSILE_SPEED_UPPER_CAP = 30
MISSILE_SPEED_LOWER_CAP = 10

# Tank count limits
TANK_UPPER_CAP = 3
TANK_LOWER_CAP = 1

config_file_name = "config.json"

# Keeping default config in a separate variable just in case
default_config_info = {
  "fullscreen": False,
  "missile_maxspeed": MISSILE_SPEED_UPPER_CAP,
  "max_tank_count": TANK_UPPER_CAP
}

# A deep copy is needed to prevent changes to the default config
config_info = copy.deepcopy(default_config_info)

'''
Checks if the game is currently on the hardest gameplay settings
'''
def is_on_hardest_setting():
    return (config_info["missile_maxspeed"] == MISSILE_SPEED_UPPER_CAP) and (config_info["max_tank_count"] == TANK_UPPER_CAP)

'''
Forces a given missile speed to be within the allowed limits
Parameters:
    missile_speed: the given missile speed to be checked for limits
'''
def correct_missile_speed(missile_speed):
    return max( min( missile_speed, MISSILE_SPEED_UPPER_CAP ), MISSILE_SPEED_LOWER_CAP )

'''
Forces a given tank count to be within the allowed limits
Parameters:
    missile_speed: the given tank count to be checked for limits
'''
def correct_tank_count(tank_count):
    return max( min( tank_count, TANK_UPPER_CAP ), TANK_LOWER_CAP  )

'''
Loads the configuration information from a file. If the file cannot be read into JSON
then the default config is used instead. Gameplay values will be corrected to be within limits
'''
def load_config_info():
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

'''
Saves the current configuration to the JSON file 
'''
def save_config():
    try:
        with open(config_file_name, "w") as json_file:
            # The optional arguments can organize the JSON to be more readable.
            json.dump(config_info, json_file, indent=2, separators=(", ", " : "))
            print("Successfully wrote to " + config_file_name)
    except:
        print("Couldn't save " + config_file_name)

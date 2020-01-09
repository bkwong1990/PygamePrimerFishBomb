import json

ENEMY_SCORES = {
"missile": 1000,
"tank": 10000,
"laser": 100000
}

SCORE_PER_LIVING_TANK = 10

SCORE_COUNT = 5

NAME_CHAR_LIMIT = 10

score_file_name = "scores.json"

# Defaults to an empty list
scores = []

'''
Loads scores from a JSON file
'''
def load_scores():
    global scores
    try:
        with open(score_file_name, "r") as json_file:
            scores = json.load(json_file)
            print("Successfully read from " + score_file_name)
    except:
        print("Couldn't read " + score_file_name)
'''
Saves scores to a JSON file
'''
def save_scores():
    try:
        with open(score_file_name, "w") as json_file:
            # use optional args to prettify the JSON text
            json.dump(scores, json_file, indent=2, separators=(", ", " : "))
            print("Successfully wrote to " + score_file_name)
    except:
        print("Couldn't save " + score_file_name)

'''
Checks if the given score is high enough to be added. Will be added anyways if
there aren't enough scores.
Parameters:
    new_score: the score to be tested
'''
def is_score_high_enough(new_score):
    if len(scores) < SCORE_COUNT:
        return True
    else:
        lowest_score = min( [ entry["score"] for entry in scores ] )
        if new_score > lowest_score:
            return True
    return False

'''
Adds a new score and removes old scores if necessary
Parameters:
    name: the name of the scorer
    score: the score
'''
def add_score(name, new_score):
    global scores
    # Prevent overly long names from being used
    if len(name) > NAME_CHAR_LIMIT:
        name = name[:NAME_CHAR_LIMIT]

    scores.append({
    "name": name,
    "score": new_score
    })


    def sort_fun(entry):
        return entry["score"]
    #It'd be more efficient to insert, but there aren't many scores to work with.
    scores.sort(key = sort_fun,reverse = True)
    #If necessary, cut out the lowest score
    if len(scores) > SCORE_COUNT:
        scores = scores[0:SCORE_COUNT]

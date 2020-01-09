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

scores = []

def load_scores():
    global scores
    try:
        with open(score_file_name, "r") as json_file:
            scores = json.load(json_file)
            print("Successfully read from " + score_file_name)
            #print(scores)

    except:
        print("Couldn't read " + score_file_name)

def save_scores():
    try:
        with open(score_file_name, "w") as json_file:
            json.dump(scores, json_file, indent=2, separators=(", ", " : "))
            print("Successfully wrote to " + score_file_name)
    except:
        print("Couldn't save " + score_file_name)

def can_add_score(new_score):
    if len(scores) < SCORE_COUNT:
        return True
    else:
        lowest_score = min( [ entry["score"] for entry in scores ] )
        if new_score > lowest_score:
            return True
    return False

def add_score(name, new_score):
    global scores
    if len(name) > NAME_CHAR_LIMIT:
        name = name[:NAME_CHAR_LIMIT]

    scores.append({
    "name": name,
    "score": new_score
    })

    def sort_fun(entry):
        return entry["score"]

    scores.sort(key = sort_fun,reverse = True)
    if len(scores) > SCORE_COUNT:
        scores = scores[0:SCORE_COUNT]

'''
Importing the json module, as we are using json for storing the recipes.

Defining the save_recipes function.
    It opens(or creates if it does not exist) the recipes.json file in write mode. 'f' is the file object that is obtained from opening the file. 
    Use json.dump to serialize the 'recipes' dictionary and write it to the 'recipes.json' file.
    The 'recipes' parameter is expected to be a dictionary where the keys are recipe names and the values are their corresponding details.

Defining the load_recipes function.
    It tries to open the recipes.json file in read mode, placed in an try-except block in case it does not exist.
    Deserialize the json data from the file, and returning the resulting dictionary.

'''
import json

def save_recipes(recipes):
    with open('recipes.json', 'w') as f:
        json.dump(recipes, f)

def load_recipes():
    try:
        with open('recipes.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Return an empty dictionary if the file does not exist
        return {}
    except json.JSONDecodeError:
        # Handle the case where the file exists but does not contain valid JSON data
        # Return an empty dictionary as a fallback
        return {}

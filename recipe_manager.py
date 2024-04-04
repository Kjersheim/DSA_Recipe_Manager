'''
Importing the save_recipes and load_recipes from the storage module/file.

Defining a class RecipeManager. This class will be responsible for managing the recipes, with methods for adding, deleting, getting and listing recipes.

class RecipeManager:
    The constructor method is called when a new instance of RecipeManager is created.
    Load the existing recipes from 'recipes.json' into the 'recipes' dictionary upon initialization of the RecipeManager.
    If 'recipes.json' doesn't exist, load_recipes will return an empty dictionary.

    Method for adding new recipes:
        Check if the recipe name already exists in the dictionary. If it does, return False to indicate failure.
        If the recipe name does not exist, add the new recipe to the 'recipes' dictionary.
        The recipe is stored as a dictionary itself, with keys 'ingredients' and 'instructions'.
        Saves the updated 'recipes' dictionary to 'recipes.json'.
        Returns 'True' to indicate a successful add.
    
    Method for deleting recipes:
        Check if the recipe name exists in the 'recipes' dictionary. If so, deleting it.
        Save the updated 'recipes' dictionary to 'recipes.json'
        Returns 'True' to indicate a successful delete.
        Returns 'False' if the recipe name does not exist.
    
    Method for getting a recipe by name:
        Using the dictionary .get() method to return the recipe if it exists, or None if it doesn't.

    Method for listing recipe names:
        Using the dictionary.keys() method to return a list of all recipe names.

    Finally, methods for doing the same functions but using a list instead of the dictionary. These are not used in the actual recipe management application -
    but for the testing section of the application in the performance_test.py module used from the performance testing button.
'''
from storage import load_recipes, save_recipes

class RecipeManager:
    def __init__(self):
        # Main dictionary storage
        self.recipes_dict = load_recipes()  
        # Convert to list of tuples (name, {details}) for comparison in performance test section
        self.recipes_list = [(name, details) for name, details in self.recipes_dict.items()]

    def add_recipe_dict(self, name, ingredients, instructions):
        if name in self.recipes_dict:
            return False
        self.recipes_dict[name] = {
            'ingredients': ingredients,
            'instructions': instructions
        }
        save_recipes(self.recipes_dict)
        return True

    def delete_recipe_dict(self, name):
        if name in self.recipes_dict:
            del self.recipes_dict[name]
            save_recipes(self.recipes_dict)
            return True
        return False

    def get_recipe(self, name):
        return self.recipes_dict.get(name, None)

    def list_recipes(self):
        return list(self.recipes_dict.keys())
    
    # List-based operations for comparison
    def add_recipe_list(self, name, ingredients, instructions):
        for recipe in self.recipes_list:
            # Recipe already exists
            if recipe[0] == name:  
                return False
        self.recipes_list.append((name, {'ingredients': ingredients, 'instructions': instructions}))
        return True

    def delete_recipe_list(self, name):
        for i, recipe in enumerate(self.recipes_list):
            if recipe[0] == name:
                del self.recipes_list[i]
                return True
        return False

    def get_recipe_list(self, name):
        for recipe in self.recipes_list:
            if recipe[0] == name:
                return recipe[1]
        return None
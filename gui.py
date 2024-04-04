'''
In this gui file/module handles the users interaction of the buttons in the RecipeGUI main window, where one can choose to view add or delete recipes. 
The AddRecipeDialog is used for input when adding a new recipe, and the RecipeViewDialog is used to display a recipe details. 

Importing tkinter library for creating the gui. from the recipe_manager file I am importing the RecipeManager class to handle the recipe management logic. 

RecipeGUI Class - This class is the main application window, showing the recipe list and buttons for interacting with the application.
    Setup main application window
    Initializing RecipeManager to handle recipe data
    Creating a listbox for displaying recipe names
    Creating buttons for refreshing the list, adding, viewing, and deleting recipes
    Automatically refresh the listbox with current recipes on startup

AddRecipeDialog Class - This class creates a dialog for adding new recipes, to input a recipes name, ingredients, and instructions.
    Initializing dialog components
    Creating and layout input fields(or widgets as it seems to be more precicely called using Tkinter) for name, ingredients, instructions
    Return the input field for name as the initial focus point
    On dialog completion, process and store input data

RecipeViewDialog Class - This class provides a window to view the detailed information of a recipe(ingredients and instructions).
    Display a new window with the selected recipe's details
    Layout components to show ingredients and instructions in a read-only format using the text widgets.


'''
import tkinter as tk
from tkinter import simpledialog, messagebox
from recipe_manager import RecipeManager
from performance_test import PerformanceDialog


class RecipeGUI:
    def __init__(self, master):
        # Initialize the window of the main application
        self.master = master
        master.title("Recipe Manager")
        # Setting the size of the dialog window initially, but does not restrict resizing.
        master.geometry("300x300") 
        master.resizable(True, True)

        # Creating an instance based on the recipe manager class. 
        self.recipe_manager = RecipeManager()
        

        # The listbox, where the recipe-names will be displayed
        self.listbox = tk.Listbox(master)
        self.listbox.pack()

        # Adding buttons for the different functions, setting relief to flat to not 'pop out'.
        self.refresh_button = tk.Button(master, text="Refresh", command=self.refresh, relief=tk.FLAT, bg='#f0f0f0')
        self.refresh_button.pack()

        self.add_button = tk.Button(master, text="Add Recipe", command=self.add_recipe, relief=tk.FLAT, bg='#f0f0f0')
        self.add_button.pack()

        self.view_button = tk.Button(master, text="View Recipe", command=self.view_recipe, relief=tk.FLAT, bg='#f0f0f0')
        self.view_button.pack()

        self.view_button = tk.Button(master, text="Delete Recipe", command=self.delete_recipe, relief=tk.FLAT, bg='#f0f0f0')
        self.view_button.pack()

        self.performance_button = tk.Button(master, text="Performance testing", command=self.show_performance, relief=tk.FLAT, bg='#f0f0f0')
        self.performance_button.pack()

        self.refresh()

    # Clearing the listbox, then loading and displaying recipe names from the recipe manager
    def refresh(self):
        self.listbox.delete(0, tk.END)
        for recipe_name in self.recipe_manager.list_recipes():
            self.listbox.insert(tk.END, recipe_name)

    # Opening a dialog window for adding a recipe. Processes the result, adding the recipe and then refreshing the listbox again.
    def add_recipe(self):
        dialog = AddRecipeDialog(self.master)
        if dialog.result:
            name, ingredients, instructions = dialog.result
            added = self.recipe_manager.add_recipe_dict(name, ingredients, instructions)
            if added:
                self.refresh()
            else:
                messagebox.showerror("Error", "Recipe could not be added. It may already exist.")

    # Opening a dialog window for viewing a recipe that is selected in the listbox above. Display the details of the selected recipes. 
    def view_recipe(self):
        try:
            selection = self.listbox.curselection()[0]
            recipe_name = self.listbox.get(selection)
            recipe = self.recipe_manager.get_recipe(recipe_name)
            ingredients = "\n".join(recipe["ingredients"])  
            instructions = recipe["instructions"]
            RecipeViewDialog(self.master, recipe_name, ingredients, instructions)
        except IndexError:
            messagebox.showerror("Error", "No recipe selected.")
    
    # When a recipe name is selected in the listbox, the delete function is called from the delete button. Using the recipe manager to delete the the recipe, and refreshing the list again.
    def delete_recipe(self):
        try:
            selection = self.listbox.curselection()[0]
            recipe_name = self.listbox.get(selection)
            deleted = self.recipe_manager.delete_recipe_dict(recipe_name)
            if deleted:
                self.refresh()
            else:
                messagebox.showerror("Error", "Recipe could not be deleted. It may not exist.")
        except IndexError:
            messagebox.showerror("Error", "No recipe selected.")
    
    def show_performance(self):
        PerformanceDialog(self.master)


class AddRecipeDialog(simpledialog.Dialog):
    def body(self, master):
        # Adding labels for the textboxes, and placing them in a grid. Sticky='w' sets the alignment of the labels to the left. 
        # Adding some padding and font changes for readability.
        tk.Label(master, text="Name:", font=('Arial', 12)).grid(row=0, sticky='w', padx=10, pady=5)
        tk.Label(master, text="Ingredients:", font=('Arial', 12)).grid(row=1, sticky='w', padx=10, pady=5)
        tk.Label(master, text="Instructions:", font=('Arial', 12)).grid(row=2, sticky='w', padx=10, pady=5)

        # Entry widgets for the user input
        self.e1 = tk.Entry(master)
        self.e2 = tk.Entry(master)
        self.e3 = tk.Entry(master)

        # Position of the entry fields in the grid
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)

        # Setting the initial focus to the first field
        return self.e1  

    # Retrieving inputs from the entry fields defined in the body function. Splits the ingredients into a list by splitting on commas, and strips the whitespace from the ingredients. Stores the results.
    def apply(self):
        name = self.e1.get()
        ingredients = [i.strip() for i in self.e2.get().split(',')]
        instructions = self.e3.get()
        self.result = (name, ingredients, instructions)

class RecipeViewDialog(tk.Toplevel):
    def __init__(self, master, title, ingredients, instructions):
        super().__init__(master)
        # Setup window title, size, and disable resizing
        self.title(title)
        self.geometry("400x300")
        self.resizable(False, False)

        # Create and layout labels and text boxes for displaying the ingredients
        tk.Label(self, text="Ingredients:", font=('Arial', 14, 'bold')).pack(pady=(10, 0))
        ingredients_text = tk.Text(self, height=5, wrap=tk.WORD)
        ingredients_text.pack(padx=10, pady=(0,10))
        ingredients_text.insert(tk.END, ingredients)
        # Read-only
        ingredients_text.config(state=tk.DISABLED)

        # And similarily for the instructions
        tk.Label(self, text="Instructions:", font=('Arial', 14, 'bold')).pack()
        instructions_text = tk.Text(self, height=10, wrap=tk.WORD)
        instructions_text.pack(padx=10, pady=(0,10))
        instructions_text.insert(tk.END, instructions)
        # Read-only
        instructions_text.config(state=tk.DISABLED)  


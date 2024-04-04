'''
Importing tkinter library for creating a graphical user interface(GUI) for the application. From the gui module/script, I am importing the RecipeGUI class.
The RecipeGUI class defines the gui and the logics for the application.

Continuing, the main function is defined. This is the entry point of the application. The main function creates a root window and passes it to the RecipeGUI class.
When that is done, filling/incorporating the RecipeGUI class with the main window (root) as its parent. This sets up the application's GUI within the main window.

Starting the tkinter event loop. This call is blocking and will wait for user interactions with the GUI, like clicks or typing.
The application will remain open and responsive until the main window is closed.

Finally, checking if the script is the main program being started. It ensures that the GUI application starts only when the script is run directly, 
allowing gui.py (where RecipeGUI is defined) to be imported in other scripts without automatically launching the GUI. Setting up the application in this way as it is suggested to improve easier development in modules. 

If the check is true, then it runs directly by calling the main function.
'''
import tkinter as tk
from gui import RecipeGUI

def main():
    root = tk.Tk()
    app = RecipeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

'''
Performance Testing Module

This module handles the performance testing of dictionary hashmaps vs list of tuples implementations
in managing recipes. The tests are designed to measure and compare the efficiency
of add, get, and delete operations between the two data structures. It demonstrates
the application of time complexity concepts in a practical scenario, using the
RecipeManager class as a test case - while keeping the originally added and saved recipes 'unharmed'.

I used GPT for testing and optimizing the calculations and visualizations, trying to fine tune the matplotlib as I have used it in previous courses.
GPT's guidance helped in structuring and finding suitable test code snippets, as well as analyzing & checking the results of the 
the tests to try to reflect real-world usage patterns.

Key Components:
- PerformanceDialog: A Tkinter dialog window that provides a user interface for
  initiating performance tests and displaying results, where the user can manually add the amount of tests per check. 
- test_add, test_delete, test_get: Functions to measure the performance of respective operations for dictionary 
  and list data structures.
- display_big_o_graph: Visualizes the performance results, highlighting the time complexity differences between 
  dictionary and list operations through bar graphs.

Usage:
- The GUI allows users to input the number of test cases for the performance tests.
- Upon executing the tests, average times for each operation are displayed, followed by a graph illustrating
  the total time taken for each operation in both data structures.

'''

# Importing tkinter for gui, timeit for timing, numpy is used for a couple caluclations and matplotlib as the graphing tools. 
# Also adding the RecipeManager as the idea is to use the functions from there.
import tkinter as tk
import timeit
import numpy as np
import matplotlib.pyplot as plt
from recipe_manager import RecipeManager
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PerformanceDialog(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Performance Comparison - Dictionary vs list of tuples")
        self.geometry("800x600")
        self.resizable(True, True)

        # User interface components for input and initiating tests
        self.input_label = tk.Label(self, text="Enter number of tests:")
        self.input_label.pack(pady=5)

        self.tests_entry = tk.Entry(self)
        self.tests_entry.pack(pady=5)
        # Default value, but can be changed
        self.tests_entry.insert(0, "1000")  

        self.test_button = tk.Button(self, text="Test", command=self.perform_tests)
        self.test_button.pack(pady=5)

        # Frames for displaying results and graphs
        self.result_label_frame = tk.LabelFrame(self, text="Results - Average time per operation")
        self.result_label_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas_frame = tk.Frame(self)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        # Create a separate instance of RecipeManager for testing
        self.recipe_manager = RecipeManager()

    def perform_tests(self):
        # Validates input and initiates performance tests
        try:
            num_tests = int(self.tests_entry.get())
            if num_tests <= 0:
                raise ValueError("Number of tests must be a positive integer")
        except ValueError as e:
            tk.messagebox.showerror("Error", str(e))
            return

        # Clearing previous results and performing new tests
        self.clear_results()
        self.measure_operations(num_tests)

    def clear_results(self):
        # Clearing result labels and graph canvas for new test results. Widget is the input box in Tkinter.
        for widget in self.result_label_frame.winfo_children():
            widget.destroy()

        # Destroy all widgets in the canvas frame
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

    def measure_operations(self, num_tests):
        # Core test function to measure operation times and display results
        operations = ['Add', 'Get', 'Delete']
        times_dict = {op: [] for op in operations}
        times_list = {op: [] for op in operations}
        
        for i in range(num_tests):
            name = f'TestRecipe{i}'
            ingredients = ['Ingredient1', 'Ingredient2']
            instructions = 'Mix well & serve hot.. or cold.'
            # Using a fresh instance for each measurement
            recipe_manager = RecipeManager()  
            
            # Reinitializing the RecipeManagers data structures before each test
            recipe_manager.recipes_dict = self.recipe_manager.recipes_dict.copy()
            recipe_manager.recipes_list = self.recipe_manager.recipes_list.copy()
            
            # Measuring Add operation
            add_dict_time = min(timeit.repeat(lambda: recipe_manager.add_recipe_dict(name, ingredients, instructions), repeat=5, number=10))
            times_dict['Add'].append(add_dict_time)

            add_list_time = min(timeit.repeat(lambda: recipe_manager.add_recipe_list(name, ingredients, instructions), repeat=5, number=10))
            times_list['Add'].append(add_list_time)
            
            # Using the add recipe dict and list methods from recipe manager, add the recipes to the data structures
            recipe_manager.add_recipe_dict(name, ingredients, instructions)
            recipe_manager.add_recipe_list(name, ingredients, instructions)

            # Measuring Get operation
            get_dict_time = min(timeit.repeat(lambda: recipe_manager.get_recipe(name), repeat=5, number=10))
            times_dict['Get'].append(get_dict_time)

            get_list_time = min(timeit.repeat(lambda: recipe_manager.get_recipe_list(name), repeat=5, number=10))
            times_list['Get'].append(get_list_time)

            # Measuring Delete operation
            delete_dict_time = min(timeit.repeat(lambda: recipe_manager.delete_recipe_dict(name), repeat=5, number=10))
            times_dict['Delete'].append(delete_dict_time)

            delete_list_time = min(timeit.repeat(lambda: recipe_manager.delete_recipe_list(name), repeat=5, number=10))
            times_list['Delete'].append(delete_list_time)

        # Calculating and displaying average times
        self.display_average_times(times_dict, times_list)

        # Displaying the Big O notation graph
        self.display_big_o_graph(times_dict, times_list)

    def display_average_times(self, times_dict, times_list):
        # Displaying average times for operations in the result label frame
        for operation in times_dict:
            avg_time_dict = np.mean(times_dict[operation]) * 1000  # Convert to milliseconds
            avg_time_list = np.mean(times_list[operation]) * 1000  # Convert to milliseconds
            tk.Label(self.result_label_frame, text=f"{operation} Operation - Dict: {avg_time_dict:.6f} ms, List: {avg_time_list:.6f} ms").pack()

    def display_big_o_graph(self, times_dict, times_list):
        # Creating and displaying Big O notation graphs for dict vs list of tuples comparisons
        fig, ax = plt.subplots(figsize=(10, 4))
        
        # Summing up the times for each operation for both data structures
        sum_times_dict = {op: sum(times_dict[op]) for op in times_dict}
        sum_times_list = {op: sum(times_list[op]) for op in times_list}
        
        # Creating lists of summed times and labels for plotting
        operations = ['Add', 'Get', 'Delete']
        dict_times = [sum_times_dict[op] for op in operations]
        list_times = [sum_times_list[op] for op in operations]
        colors = ['blue', 'green', 'red', 'orange']
        
        # Plotting the times for each operation
        bar_width = 0.35
        index = np.arange(len(operations))
        
        bars1 = ax.bar(index, dict_times, bar_width, color=colors[0], label='Dict Operations')
        bars2 = ax.bar(index + bar_width, list_times, bar_width, color=colors[1], label='List Operations')
        
        # Adding labels and title
        ax.set_xlabel('Operations')
        ax.set_ylabel('Total Time (s)')
        ax.set_title('Total Time for Operations - Dict vs List')
        ax.set_xticks(index + bar_width / 2)
        ax.set_xticklabels(operations)
        ax.legend()

        # Adding the total time above each bar for better visibility
        for bar in bars1 + bars2:
            height = bar.get_height()
            ax.annotate(f'{height:.4f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
        
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


if __name__ == "__main__":
    root = tk.Tk()
    app = PerformanceDialog(root)
    root.mainloop()

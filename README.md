# Habit-Tracker


You are required to have MYSQL to use this habit tracker (https://www.mysql.com/de/downloads/). In the beginning you will be asked for your username and password.


The habit tracker comes with 7 modules: habitTracker.py, habit_class.py, predefined_habits.py, check_habits.py, analyses.py, test_predefined_habits.py, and test_analyses.py.

The habitTracker.py file is the main file of the program, running it will give access to the main menu of the program, which uses a simple and straight forward CLI design. It will ask what you want to do and give you the key words to use to guide you through the program. Further, this file accesses all the other modules, translates the stored data from the MySQL table into a dictionary for easy access, and saves all the data changed during the use of the program into the SQL table at the end.
The habit_class.py module is the class of the habits and is crucial for habit creation, It is therefore accessed by  habit.Tracker.py, predefined_habits.py, and test_analyses.py modules.
predefined_habits.py creates five predefined habits of which three are daily habits and two are weekly habits and is accessed in the beginning of the main module. This modules also serves a template, should one want to artificially create more habits. The habit creation functions for the predefined habits are tested in the test_predefined_habits.py module.
The check_habits.py module checks whether a habit was checked off often enough. While daily habits are checked every day, weekly habits are checked after seven days, given that the user opens the program. The functionality of the check_habits function is also tested in the test_predefined_habits.py file. 
The analyses.py module includes all the analyses functions. This one also has its own test file, test_analyses.py.

To execute the test modules use the command: pytest test_predefined_habits.py
For more information check: https://docs.pytest.org/en/7.3.x/


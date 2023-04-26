# use datetime to measure time periods

from datetime import date
from datetime import timedelta

# save data in a mysql table 
from getpass import getpass
import mysql.connector

# my modules
from habit_class import Habit
from analyses import print_all
from analyses import print_same_periodicity
from analyses import l_s_specific
from analyses import l_s_all_daily
from analyses import l_s_all_weekly
from analyses import failure
from predefined_habits import create_predefined_habits
from check_habits import check_if_checked_off


sql_user=input("Enter username: ")
pw = getpass("Enter password: ")

db = mysql.connector.connect(host="localhost", user = sql_user, password = pw)

mycursor = db.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS sarabase")
db.close()
db2 = mysql.connector.connect(host="localhost", user = sql_user, password = pw, database = "sarabase")
mycursor = db2.cursor(buffered=True)
mycursor.execute("CREATE TABLE IF NOT EXISTS habits (task varchar(200), periodicity int, begin_date date, fulfilled int, current_streak int, longest_streak int, last_check_date date, fails int)")
db2.commit()

# A dictionary of the objects facilitates the access to the tasks that are saved in the habit tracker
# Every time the code is executed the object dictionary is updated 
com = "SELECT * FROM habits"
mycursor.execute(com)
com = mycursor.fetchall()


object_dict = {}
for i in com:
    object_dict[i[0]] = Habit(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])



#the habit tracker comes with 5 pre-defined tasks

create_predefined_habits(object_dict)

   
# it is checked if the user has checked off their habits sufficiently
for i in object_dict.values():
    check_if_checked_off(object_dict, i.name)


# this menu is the one the user sees whenever they start the program, the program loops through this menu until the user exits the while loop with the command 'quit' 
menu_choice = ""

while menu_choice != "quit":
    print ("\n Hello, this is Sara's habit tracker!")
    menu_choice = input("If you want to see your habits write 'see', if you want to create a new habit write 'new', if you want to check off a task write 'check off', if you want to delete a habit write 'delete', if you want to analyse your progress write 'analyse', and if you want to end the program write 'quit'. ")

    if menu_choice == "new":
        new_habit = input("\n Please name your new habit ")
        gate = True
        if new_habit in object_dict.values():
            gate = False
            print("You already have a task with that name, plese choose a different name or delete this task first.")
        else:
            while gate == True:
                try:
                    periodicity = int(input("\n How often would you like to repeat your new habit per week? Write a number from 1 (once a week) to 7 (daily) "))
                    gate = False
                except ValueError:
                    gate == True
                    print("\n Please write a number. Try again!")
            print("\n You have created a new task :)")
            d = date.today()
            begin_fulfilled = 0
            begin_current_streak = 0
            begin_longest_streak = 0
            begin_last_check_date = date.today()
            begin_fails = 0
            object_dict.update({new_habit:Habit(new_habit,periodicity, d, begin_fulfilled, begin_current_streak, begin_longest_streak, begin_last_check_date, begin_fails)})
    elif menu_choice == "see":
        see_choice = input("\n If you would like to see all your habits write 'all', if you would only like to see those habits of a specific periodicity write 'specific'. ")
        if see_choice == "all":
            print_all(object_dict)
        elif see_choice == "specific":
            gate = True
            while gate == True:
                try:
                    chosen_periodicity = int(input("\n For which periodicity would you like to see all your habits? "))
                    gate = False
                except ValueError:
                    gate == True
                    print("\n Please write a number. Try again!")
            print_same_periodicity(object_dict, chosen_periodicity)
        else:
            print("\n That is not a valid choice.")   
   
    elif menu_choice == "check off":
        for i in object_dict.values():
            print(i.name)
        gate = True
        while gate == True:
            checkedoff_task = input("\n Which task would you like to check off? ")
            if checkedoff_task in object_dict:
                gate = False
            if gate == True:
                print("\n You do not have a task of that name, try again.")  
        print("\n Thank you, your task was checked off. Well done!")
        object_dict[checkedoff_task].fulfilled += 1
        if object_dict[checkedoff_task].periodicity == 7:
            current_s = int(object_dict[checkedoff_task].current_streak+1)
            if  current_s % 7 == 0:
                weeks = int(current_s / 7)
                print ("\n Congratulations! You have managed to complete this task for {y} week(s). Keep it up!".format(y=weeks))
        else:
            if object_dict[checkedoff_task].periodicity == object_dict[checkedoff_task].fulfilled:
                weeks = object_dict[checkedoff_task].current_streak + 1
                if weeks%4 == 0:
                    print ("\n Congratulations! You have managed to complete this task for {y} week(s). Keep it up!".format(y=weeks))

    elif menu_choice == "delete":
        for i in object_dict.values():
            print(i.name)
        if not object_dict:
            print("You have no tasks, please create one first.")
        else:
            gate = True
            while gate == True:
                deleted_task = input("\n Which task would you like to delete? ")
                if deleted_task in object_dict:
                    gate = False
                if gate == True:
                    print("\n You do not have a task of that name, try again.")
            del object_dict[deleted_task]
            print("\n Your task was deleted!")
    elif menu_choice == "analyse":
        analyse_choice = input("\n If you want to see your longest run streak write 'longest streak', if you want to see with which task you are struggling most write 'failure'. ")
        if analyse_choice == "longest streak":
            streak_choice = input("\n If you like to see the longest run streak of all daily tasks write 'all daily', if you like to see the longest run streak of all weekly tasks write 'all weekly', or if you want to see the longest run streak of a specific task write 'specific'. ")
            if streak_choice == "specific":
                for i in object_dict.values():
                    print(i.name)
                gate = True
                while gate == True:
                    next_choice=input("\n For which task would you like to see your longest streak? ")
                    for i in object_dict.values():
                        if next_choice == i.name:
                            gate = False
                    if gate == True:
                        print("\n You do not have a task of that name, try again.")               
                l_s_specific(object_dict, next_choice)
            elif streak_choice == "all daily":
                l_s_all_daily(object_dict)
            elif streak_choice == "all weekly":
                l_s_all_weekly(object_dict)
            else:
                print("\n That is an invalid choice!")
        elif analyse_choice == "failure":
            failure(object_dict)
        else:
                print("\n That is an invalid choice!")

    elif menu_choice == "quit":
        print("End of program")

    else :
        print ("\n You have to choose between 'see', 'new', 'check off', 'delete', 'analyse', and 'quit'. Try again!")



delete_table = "TRUNCATE TABLE habits"
mycursor.execute(delete_table)
db2.commit()


for i in object_dict.values():
    sql = "INSERT INTO habits (task, periodicity, begin_date, fulfilled, current_streak, longest_streak, last_check_date, fails) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (i.name, i.periodicity, i.begin_date, i.fulfilled, i.current_streak, i.longest_streak, i.last_check_date, i.fails)
    mycursor.execute(sql, val)
    db2.commit()



db2.close()
 
# use datetime to measure time periods
from datetime import datetime
from datetime import date
from datetime import timedelta

# save data in a mysql table 
from getpass import getpass
import mysql.connector


# a table is created with the columns task name, periodicity, begin date, number of ticks (fulfilled), the cuurent run streak, the longest run streak, the last check date and the number of fails
sql_user=input("Enter username: ")
pw = getpass("Enter password: ")

db = mysql.connector.connect(host="localhost", user = sql_user, password = pw)

mycursor = db.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS sarabase")
db.close()
db2 = mysql.connector.connect(host="localhost", user = sql_user, password = pw, database = "sarabase")
mycursor = db2.cursor(buffered=True)
mycursor.execute("CREATE TABLE IF NOT EXISTS habits (task varchar(200), periodicity int, begin_date date, fulfilled int, current_streak int, longest_streak int, last_check_date date, fails int)")
#new_column = "ALTER TABLE habits ADD begin_date int, \ fulfilled int"
#mycursor.execute(new_column)
db2.commit()




# defining a habit class
# every object within that class should have the same properties as the my MySQL table has columns

class Habit:
    def __init__(task, name, periodicity, begin_date, fulfilled, current_streak, longest_streak, last_check_date, fails):
        task.name = name
        task.periodicity = periodicity
        task.begin_date = begin_date
        task.fulfilled = fulfilled
        task.longest_streak = longest_streak
        task.current_streak = current_streak
        task.last_check_date = last_check_date
        task.fails = fails

# A list of objects facilitates the access to the tasks that are saved in the habit tracker
# Every time the code is executed the object list is updated 
com = "SELECT * FROM habits"
mycursor.execute(com)
com = mycursor.fetchall()

object_list= []
for i in com :
    object_list.append(Habit(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]))
    




#the habit tracker comes with 5 pre-defined tasks: do yoga, bake a cake, get out of bed, read a book, and shower

def check_if_exists(new_habit):
    for i in object_list:
        if i.name == new_habit:
            return True
        
        
def create_habit(new_habit, periodicity, begin_fulfilled, current_streak, longest_streak, last_check_date, fails):
    s=date.today()
    intervall = timedelta(days=30)
    last_month = s - intervall
    d = last_month
    sql = "INSERT INTO habits (task, periodicity, begin_date, fulfilled, current_streak, longest_streak, last_check_date, fails) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (new_habit, periodicity, d, begin_fulfilled, current_streak, longest_streak, last_check_date, fails)
    mycursor.execute(sql, val)
    db2.commit()
    object_list.append(Habit(new_habit,periodicity, d, begin_fulfilled, current_streak, longest_streak, last_check_date, fails))


if not check_if_exists("do push ups"):
    s = date.today()
    intervall2 = timedelta(days=1)
    yesterday = s - intervall2
    create_habit("do push ups", 7, 1, 7, 14, yesterday, 3)
    
if not check_if_exists("call your mum"):
    s = date.today()
    intervall2 = timedelta(days=2)
    l_c_d = s - intervall2
    create_habit("call your mum", 1, 4, 4, 4, l_c_d, 0)

if not check_if_exists("get out of bed"):
    s = date.today()
    intervall2 = timedelta(days=1)
    l_c_d = s - intervall2
    create_habit("get out of bed", 7, 1, 5, 12, l_c_d, 5)

if not check_if_exists("follow your dreams"):
    s = date.today()
    intervall2 = timedelta(days=8)
    l_c_d = s - intervall2
    create_habit("follow your dreams", 1, 0, 0, 1, l_c_d, 2)

if not check_if_exists("shower"):
    s = date.today()
    intervall2 = timedelta(days=1)
    l_c_d = s - intervall2
    create_habit("shower", 7, 0, 6, 20, l_c_d, 3)



# this function checks wether the daily tasks have been checked off often enough
# it first checks what day it is today and how much time has passed since this function has been called last time, then it compares this number with the number of times the task was checked off
def check_daily_habits(habitname):
    day_today = date.today()
    my_last_check_date = i.last_check_date
    intervall= day_today - my_last_check_date
    intervall=int(intervall.days)
    my_fulfilled = i.fulfilled
    if intervall > my_fulfilled:
        # if the user has not checked off their task often enough they will see a complaint message
        bad_news = ("You broke your habit! You have missed to \'{v}\'").format(v=habitname)
        print(bad_news)
        #if the current run streak is longer than the longest run streak by then it becomes the new longest run streak 
        my_current_streak= i.current_streak
        my_longest_streak= i.longest_streak
        if my_current_streak > my_longest_streak:
            update_longest_streak = "UPDATE habits SET longest_streak = {z} WHERE task = \'{v}\'".format(z=my_current_streak, v=habitname)
            mycursor.execute(update_longest_streak)
            db2.commit()
        # the current run streak is set 0 and the number of fails is increased by 1
        update_current_streak = "UPDATE habits SET current_streak = 0 WHERE task = \'{v}\'".format(v=habitname)
        mycursor.execute(update_current_streak)
        db2.commit()
        update_fails = "UPDATE habits SET fails = fails +1 WHERE task = \'{v}\'".format(v=habitname)
        mycursor.execute(update_fails)
        db2.commit()

    # if the user managed to check off their task often enough the current run streak is increased     
    if my_last_check_date != day_today:
        if intervall <= my_fulfilled:
            update_current_streak = "UPDATE habits SET current_streak = current_streak + {y} WHERE task = \'{v}\'".format(y=my_fulfilled, v=habitname)
            mycursor.execute(update_current_streak)
            db2.commit()
        # the number of ticks is set 0 again
        update_fulfilled = "UPDATE habits SET fulfilled = 0 WHERE task = \'{v}\'".format(v=habitname)
        mycursor.execute(update_fulfilled)
        db2.commit()    

    # after all daily habits have been checked the date of today is set as the new last check date
    today = date.today()
    update_last_check_date = "UPDATE habits SET last_check_date = \'{w}\' WHERE periodicity = 7".format(w=today)
    mycursor.execute(update_last_check_date)
    db2.commit()
            


for i in object_list:
    if i.periodicity == 7:
        check_daily_habits(i.name)



# this function checks wether the weekly tasks have been checked off often enough
# it first checks what day it is today and how much time has passed since this function has been called last time, if at least 7 days have passed, it compares the periodicity with the number of times the task was checked off
def check_weekly_habits(habitname):
    day_today = date.today()
    my_last_check_date= i.last_check_date
    intervall= day_today - my_last_check_date
    intervall=int(intervall.days)
    if intervall >= 7:
        my_fulfilled = i.fulfilled
        my_periodicity = i.periodicity
        if my_periodicity > my_fulfilled:
            # if the user has not checked off their task often enough they will see a complaint message
            bad_news = ("You broke your habit! You have missed to \'{v}\'").format(v=habitname)
            print(bad_news)
            my_current_streak=i.current_streak
            my_longest_streak=i.longest_streak
            # the current run streak might be saved as the new longest run streak
            if my_current_streak > my_longest_streak:
                update_longest_streak = "UPDATE habits SET longest_streak = {z} WHERE task = \'{v}\'".format(z=my_current_streak, v=habitname)
                mycursor.execute(update_longest_streak)
                db2.commit()
            # the current run streak is set 0 and the number of fails increased by 1
            update_current_streak= "UPDATE habits SET current_streak = 0 WHERE task = \'{v}\'".format(v=habitname)
            mycursor.execute(update_current_streak)
            db2.commit()
            update_fails = "UPDATE habits SET fails = fails +1 WHERE task = \'{v}\'".format(v=habitname)
            mycursor.execute(update_fails)
            db2.commit()
        # if the user, however, managed to complete their task their current run streak is increased by 1
        if my_periodicity <= my_fulfilled:
            update_current_streak = "UPDATE habits SET current_streak = current_streak + 1 WHERE task = \'{v}\'".format(v=habitname)
            mycursor.execute(update_current_streak)
            db2.commit()
        # the last check date is updated to a week later, which is from when on the user has to fulfill their tasks again         
        one_week = my_last_check_date + timedelta(days=7)
        update_last_check_date = "UPDATE habits SET last_check_date = \'{w}\' WHERE task = \'{v}\'".format(w=one_week, v=habitname)
        mycursor.execute(update_last_check_date)
        db2.commit()

        # the number of ticks is reduced to 0 again
        update_fulfilled = "UPDATE habits SET fulfilled = 0 WHERE task = \'{v}\'".format(v=habitname)
        mycursor.execute(update_fulfilled)
        db2.commit()





for i in object_list:
    if i.periodicity != 7:
        check_weekly_habits(i.name)




# analyse part:

# this function prints all task names of a chosen periodicity
def print_same_periodicity(chosen_periodicity):
    p_list = []
    for i in object_list:
        if i.periodicity == chosen_periodicity:
            print("task:{name}, periodicity: {periodicity}, begin date: {begindate}, current run streak: {crs}, longest run streak: {lrs}, number of fails: {failure}".format(name=i.name, periodicity=i.periodicity, begindate=i.begin_date, crs = i.current_streak, lrs = i.longest_streak, failure=i.fails)) 
            p_list.append(i.name)
    if len(p_list) == 0:
                print("You do not have any tasks of that periodicity")
            
# this function prints the longest run streak of a chosen task
def l_s_specific(next_choice):
    for i in object_list:
        if i.name == next_choice:
            if i.periodicity == 7:
                day_week = "days"
            else:
                day_week = "weeks"
            print("Your longest streak of {x} is {y} {z}.".format(x=next_choice, y=i.longest_streak, z=day_week))

# this function prints the longest run streak of all daily habits
def l_s_all_daily():
    current_longest_streak_daily = 0
    for i in object_list:
        if i.periodicity == 7:
            if i.longest_streak > current_longest_streak_daily:
                current_longest_streak_daily = i.longest_streak
                name_current_longest_streak_daily = i.name
    if current_longest_streak_daily != 0:
        print("Your longest daily run streak is {x} with {y} days in a row. Well done!".format(x = name_current_longest_streak_daily, y = current_longest_streak_daily))
    if current_longest_streak_daily == 0:
        print("You do not have a longest run streak yet. Get started!")    

# this function prints the longest run streak of all the weekly habits
def l_s_all_weekly():
    current_longest_streak_weekly = 0
    for i in object_list:
        if i.periodicity != 7:            
            if i.longest_streak > current_longest_streak_weekly:
                current_longest_streak_weekly = i.longest_streak
                name_current_longest_streak_weekly = i.name
    if current_longest_streak_weekly != 0:
        print("Your longest weekly run streak is {x} with {y} weeks in a row. Well done!".format(x = name_current_longest_streak_weekly, y = current_longest_streak_weekly))    
    if current_longest_streak_weekly == 0:
        print("You do not have a longest run streak yet. Get started!")    


# this function prints the task that has received the most fails so far
def failure():
    failing_most = 0
    for i in object_list:
        if i.fails > failing_most:
            failing_most = i.fails
            name_failing_most = i.name
    if failing_most != 0:
        print("You are struggling most with {x}. You have failed to reach your goals {y} time(s), you can do better!".format(x=name_failing_most, y = failing_most))
    else:
        print("You have not yet missed to do your tasks! Well done!")




# this menu is the one the user sees whenever they start the program, the program loops through this menu until the user exits the while loop with the command 'quit' 
menu_choice = ""

while menu_choice != "quit":
    print ("\n Hello, this is Sara's habit tracker!")
    menu_choice = input("If you want to see your habits write 'see', if you want to create a new habit write 'new', if you want to check off a task write 'check off', if you want to delete a habit write 'delete', if you want to analyse your progress write 'analyse', and if you want to end the program write 'quit'. ")

    # if the user writes new, they can create a new habit, they have to give it a name and a periodicity
    if menu_choice == "new":
        new_habit = input("\n Please name your new habit ")
        for i in object_list:
                if new_habit == i.name:
                    gate = False
        if gate == False:
            print("You already have a task with that name, plese choose a different name or delete this task first.")
        else:
            gate = True
            while gate == True:
                try:
                    periodicity = int(input("\n How often would you like to repeat your new habit per week? Write a number from 1 (once a week) to 7 (daily) "))
                    gate = False
                except ValueError:
                    gate == True
                    print("\n Please write a number. Try again!")
            print("\n You have created a new task :)")
            # name and periodicity are then saved in the database while all the other properties are set 0 
            d = date.today()
            begin_fulfilled = 0
            begin_current_streak = 0
            begin_longest_streak = 0
            begin_last_check_date = date.today()
            begin_fails = 0
            sql = "INSERT INTO habits (task, periodicity, begin_date, fulfilled, current_streak, longest_streak, last_check_date, fails) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (new_habit, periodicity, d, begin_fulfilled, begin_current_streak, begin_longest_streak, begin_last_check_date, begin_fails)
            mycursor.execute(sql, val)
            db2.commit()
            # the new habit is alse directly inserted into the object list so that the user can see the new task directly and does not have to restart the program
            object_list.append(Habit(new_habit,periodicity, d, begin_fulfilled, begin_current_streak, begin_longest_streak, begin_last_check_date, begin_fails))
    # when 'see' is chosen the user can either see all their habits or only those of a chosen periodicity 
    elif menu_choice == "see":
        see_choice = input("\n If you would like to see all your habits write 'all', if you would only like to see those habits of a specific periodicity write 'specific'. ")
        if see_choice == "all":
            for i in object_list:
                print("task:{name}, periodicity: {periodicity}, begin date: {begindate}, current run streak: {crs}, longest run streak: {lrs}, number of fails: {failure}".format(name=i.name, periodicity=i.periodicity, begindate=i.begin_date, crs = i.current_streak, lrs = i.longest_streak, failure=i.fails)) 
        elif see_choice == "specific":
            gate = True
            while gate == True:
                try:
                    chosen_periodicity = int(input("\n For which periodicity would you like to see all your habits? "))
                    gate = False
                except ValueError:
                    gate == True
                    print("\n Please write a number. Try again!")
            print_same_periodicity(chosen_periodicity)
        else:
            print("\n That is not a valid choice.")   
    # 'quit' exits the while loop  
    elif menu_choice == "quit":
        quit()
    elif menu_choice == "check off":
        # the user should first see all their habits and then get the opportunity to check one off
        for i in object_list:
            print(i.name)
        gate = True
        while gate == True:
            checkedoff_task = input("\n Which task would you like to check off? ")
            for i in object_list:
                if checkedoff_task == i.name:
                    gate = False
            if gate == True:
                print("\n You do not have a task of that name, try again.")
        # checking off a task increases the number in the fulfilled column by 1   
        check_off = "UPDATE habits SET fulfilled = fulfilled + 1 WHERE task = \'{p}\'".format(p = checkedoff_task)
        print("\n Thank you, your task was checked off. Well done!")
        mycursor.execute(check_off)
        db2.commit()
        # if the user has completed their daily tasks for a whole week they should receive a congratulation message
        # for weekly habits they should receive this message every month
        fff = "SELECT fulfilled FROM habits WHERE task = \'{k}\'".format(k=checkedoff_task)
        mycursor.execute(fff)
        fff = mycursor.fetchone()[0]
        ppp = "SELECT periodicity FROM habits WHERE task = \'{k}\'".format(k=checkedoff_task)
        mycursor.execute(ppp)
        ppp = mycursor.fetchone()[0]
        ccc = "SELECT current_streak FROM habits WHERE task = \'{k}\'".format(k=checkedoff_task)
        mycursor.execute(ccc)
        ccc = mycursor.fetchone()[0]
        if ppp == 7:
            current_s = int(ccc+1)
            if fff == 1 and current_s%7 == 0:
                weeks = int(current_s/7)
                print ("\n Congratulations! You have managed to complete this task for {y} week(s). Keep it up!".format(y=weeks))
        else:
            if ppp == fff:
                weeks = ccc + 1
                if weeks%4 == 0:
                    print ("\n Congratulations! You have managed to complete this task for {y} week(s). Keep it up!".format(y=weeks))
    elif menu_choice == "delete":
        # when the user wants to delete a habit they should first see a list of all their habits and the pick one
        for i in object_list:
            print(i.name)
        if not object_list:
            print("You have no tasks, please create one first.")
        else:
            gate = True
            while gate == True:
                deleted_task = input("\n Which task would you like to delete? ")
                for i in object_list:
                    if deleted_task == i.name:
                        gate = False
                if gate == True:
                    print("\n You do not have a task of that name, try again.")
            # the chosen habit is then deleted from the database
            delete = "DELETE FROM habits WHERE task = \'{d}\' ".format(d=deleted_task)
            mycursor.execute(delete)
            db2.commit()
            for i in object_list:
                if i.name == deleted_task:
                    object_list.remove(i)
            print("\n Your task was deleted!")
    # if a user wants to see the analysis of their habits they can either see their longest streaks or their most failures
    elif menu_choice == "analyse":
        analyse_choice = input("\n If you want to see your longest run streak write 'longest streak', if you want to see with which task you are struggling most write 'failure'. ")
        if analyse_choice == "longest streak":
            streak_choice = input("\n If you like to see the longest run streak of all daily tasks write 'all daily', if you like to see the longest run streak of all weekly tasks write 'all weekly', or if you want to see the longest run streak of a specific task write 'specific'. ")
            if streak_choice == "specific":
                for i in object_list:
                    print(i.name)
                gate = True
                while gate == True:
                    next_choice=input("\n For which task would you like to see your longest streak? ")
                    for i in object_list:
                        if next_choice == i.name:
                            gate = False
                    if gate == True:
                        print("\n You do not have a task of that name, try again.")               
                l_s_specific(next_choice)
            elif streak_choice == "all daily":
                l_s_all_daily()
            elif streak_choice == "all weekly":
                l_s_all_weekly()
            else:
                print("\n That is an invalid choice!")
        elif analyse_choice == "failure":
            failure()
        else:
                print("\n That is an invalid choice!")


    else :
        print ("\n You have to choose between 'see', 'new', 'check off', 'delete', 'analyse', and 'quit'. Try again!")



db2.close()
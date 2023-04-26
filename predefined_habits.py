# use datetime to measure time periods

from datetime import date
from datetime import timedelta

from habit_class import Habit

#the habit tracker comes with 5 pre-defined tasks: do push ups, call your mum, get out of bed, follow your dreams, and shower



def check_if_exists(object_dict, new_habit):
    if new_habit in object_dict:
        return True
        
        
def create_habit(object_dict,new_habit, periodicity, begin_fulfilled, current_streak, longest_streak, last_check_date, fails):
    s=date.today()
    intervall = timedelta(days=30)
    last_month = s - intervall
    d = last_month
    object_dict.update({new_habit: Habit(new_habit, periodicity, d, begin_fulfilled, current_streak, longest_streak, last_check_date, fails)})




def create_predefined_habits(object_dict):

    if not check_if_exists(object_dict, "do push ups"):
        s = date.today()
        intervall2 = timedelta(days=1)
        yesterday = s - intervall2
        create_habit(object_dict, "do push ups", 7, 1, 7, 14, yesterday, 3)
        
    if not check_if_exists(object_dict, "call your mum"):
        s = date.today()
        intervall2 = timedelta(days=2)
        l_c_d = s - intervall2
        create_habit(object_dict, "call your mum", 1, 4, 4, 4, l_c_d, 0)

    if not check_if_exists(object_dict, "get out of bed"):
        s = date.today()
        intervall2 = timedelta(days=1)
        l_c_d = s - intervall2
        create_habit(object_dict, "get out of bed", 7, 1, 5, 12, l_c_d, 5)

    if not check_if_exists(object_dict, "follow your dreams"):
        s = date.today()
        intervall2 = timedelta(days=8)
        l_c_d = s - intervall2
        create_habit(object_dict, "follow your dreams", 1, 0, 0, 1, l_c_d, 2)

    if not check_if_exists(object_dict, "shower"):
        s = date.today()
        intervall2 = timedelta(days=1)
        l_c_d = s - intervall2
        create_habit(object_dict, "shower", 7, 0, 6, 20, l_c_d, 3)


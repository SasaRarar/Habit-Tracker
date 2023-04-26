
from datetime import date
from datetime import timedelta


def set_fulfilled_zero (object_dict, habitname):
   object_dict[habitname].fulfilled = 0


# this function checks wether the tasks have been checked off often enough
def check_if_checked_off(object_dict, habitname):
    day_today = date.today()
    my_last_check_date= object_dict[habitname].last_check_date
    intervall= day_today - my_last_check_date
    intervall=int(intervall.days)
    my_fulfilled = object_dict[habitname].fulfilled
    Fail=False
    if object_dict[habitname].periodicity != 7:
        if intervall >= 7:
            my_periodicity = object_dict[habitname].periodicity
            if my_periodicity > my_fulfilled:
                Fail=True
            else:
                object_dict[habitname].current_streak += 1       
            one_week = my_last_check_date + timedelta(days=7)
            object_dict[habitname].last_check_date = one_week
            set_fulfilled_zero
    else:
        if my_last_check_date != day_today:
            if intervall > my_fulfilled:
                Fail=True
            else:
                object_dict[habitname].current_streak += my_fulfilled
            set_fulfilled_zero
            today = date.today()
            if object_dict[habitname].periodicity ==7:
                object_dict[habitname].last_check_date = day_today
            
           
    if Fail==True:
        # if the user has not checked off their task often enough they will see a complaint message
        bad_news = ("You broke your habit! You have missed to \'{v}\'").format(v=habitname)
        print(bad_news)
        my_current_streak= object_dict[habitname].current_streak
        my_longest_streak= object_dict[habitname].longest_streak
        if my_current_streak > my_longest_streak:
            object_dict[habitname].longest_streak = my_current_streak
        object_dict[habitname].current_streak = 0
        object_dict[habitname].fails += 1
        


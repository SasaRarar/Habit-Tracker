
def print_all(object_dict):
    for i in object_dict.values():
                print("task:{name}, periodicity: {periodicity}, begin date: {begindate}, current run streak: {crs}, longest run streak: {lrs}, number of fails: {failure}".format(name=i.name, periodicity=i.periodicity, begindate=i.begin_date, crs = i.current_streak, lrs = i.longest_streak, failure=i.fails)) 


# this function prints all habits of a chosen periodicity
def print_same_periodicity(object_dict, chosen_periodicity):
    p_list = []
    for i in object_dict.values():
        if i.periodicity == chosen_periodicity:
            print("task:{name}, periodicity: {periodicity}, begin date: {begindate}, current run streak: {crs}, longest run streak: {lrs}, number of fails: {failure}".format(name=i.name, periodicity=i.periodicity, begindate=i.begin_date, crs = i.current_streak, lrs = i.longest_streak, failure=i.fails)) 
            p_list.append(i.name)
        if len(p_list) == 0:
            print("You do not have any tasks of that periodicity")
        
                
# this function prints the longest run streak of a chosen task
def l_s_specific(object_dict, next_choice):
    if next_choice in object_dict:
        if object_dict[next_choice].periodicity == 7:
            day_week = "days"
        else:
            day_week = "weeks"
        print("Your longest streak of {x} is {y} {z}.".format(x=next_choice, y=object_dict[next_choice].longest_streak, z=day_week))

# this function prints the longest run streak of all daily habits
def l_s_all_daily(object_dict):
    current_longest_streak_daily = 0
    for i in object_dict.values():
        if i.periodicity == 7:
            if i.longest_streak > current_longest_streak_daily:
                current_longest_streak_daily = i.longest_streak
                name_current_longest_streak_daily = i.name
    if current_longest_streak_daily != 0:
        print("Your longest daily run streak is {x} with {y} days in a row. Well done!".format(x = name_current_longest_streak_daily, y = current_longest_streak_daily))
    if current_longest_streak_daily == 0:
        print("You do not have a longest run streak yet. Get started!")    

# this function prints the longest run streak of all the weekly habits
def l_s_all_weekly(object_dict):
    current_longest_streak_weekly = 0
    for i in object_dict.values():
        if i.periodicity != 7:            
            if i.longest_streak > current_longest_streak_weekly:
                current_longest_streak_weekly = i.longest_streak
                name_current_longest_streak_weekly = i.name
    if current_longest_streak_weekly != 0:
        print("Your longest weekly run streak is {x} with {y} weeks in a row. Well done!".format(x = name_current_longest_streak_weekly, y = current_longest_streak_weekly))    
    if current_longest_streak_weekly == 0:
        print("You do not have a longest run streak yet. Get started!")    


# this function prints the task that has received the most fails so far
def failure(object_dict):
    failing_most = 0
    for i in object_dict.values():
        if i.fails > failing_most:
            failing_most = i.fails
            name_failing_most = i.name
    if failing_most != 0:
        print("You are struggling most with {x}. You have failed to reach your goals {y} time(s), you can do better!".format(x=name_failing_most, y = failing_most))
    else:
        print("You have not yet missed to do your tasks! Well done!")

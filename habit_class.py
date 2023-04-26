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
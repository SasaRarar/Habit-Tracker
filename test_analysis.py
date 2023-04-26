import datetime
from habit_class import Habit
from analyses import print_all
from analyses import print_same_periodicity
from analyses import l_s_specific
from analyses import l_s_all_daily
from analyses import l_s_all_weekly
from analyses import failure

# a test dictionary is created to test the analysis functions on it

test_habit = [Habit("task1", 3, datetime.date(2023, 4, 10), 5, 5, 7, datetime.date(2023, 4, 18), 0), Habit("task2", 3, datetime.date(2023, 4, 12), 1, 1, 4, datetime.date(2023, 4, 15), 2), Habit("task3", 5, datetime.date(2023, 4, 12), 1, 1, 4, datetime.date(2023, 4, 15), 1)]


test_dict = {}
for i in test_habit:
    test_dict[i.name] = i

# this function should print all habits in the test dictionary
def test_print_all(capsys):
    print_all(test_dict)
    captured = capsys.readouterr()
    assert captured.out == "task:task1, periodicity: 3, begin date: 2023-04-10, current run streak: 5, longest run streak: 7, number of fails: 0\ntask:task2, periodicity: 3, begin date: 2023-04-12, current run streak: 1, longest run streak: 4, number of fails: 2\ntask:task3, periodicity: 5, begin date: 2023-04-12, current run streak: 1, longest run streak: 4, number of fails: 1\n"

# this test checks if the functions prints all tasks with the periodicity 3
def test_print_same_periodicity(capsys):
    print_same_periodicity(test_dict, 3)
    captured = capsys.readouterr()         
    assert captured.out == "task:task1, periodicity: 3, begin date: 2023-04-10, current run streak: 5, longest run streak: 7, number of fails: 0\ntask:task2, periodicity: 3, begin date: 2023-04-12, current run streak: 1, longest run streak: 4, number of fails: 2\n"

# this test checks whether the function can determine the longest run streak of task 3
def test_l_s_specific(capsys):
    l_s_specific(test_dict, "task3")
    captured = capsys.readouterr()
    assert captured.out == "Your longest streak of task3 is 4 weeks.\n"

# since there are no daily tasks in the test dictionary the print thes daily task with the longest run streak should say so
def test_l_s_all_daily(capsys):
    l_s_all_daily(test_dict)
    captured = capsys.readouterr()
    assert captured.out == "You do not have a longest run streak yet. Get started!\n"

# when checking for the longest weekly run streak the function should give out task 1
def test_l_s_all_weekly(capsys):
    l_s_all_weekly(test_dict)
    captured = capsys.readouterr()
    assert captured.out == "Your longest weekly run streak is task1 with 7 weeks in a row. Well done!\n"

# this tests whether the failure function gives out the task fith most failures, which should be task 2
def test_failure(capsys):
    failure(test_dict)
    captured = capsys.readouterr()
    assert captured.out == "You are struggling most with task2. You have failed to reach your goals 2 time(s), you can do better!\n"




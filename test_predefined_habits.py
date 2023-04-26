
from predefined_habits import create_predefined_habits
from check_habits import check_if_checked_off



# a test dictionary is created to test the create_predefined_habits function and check_if_checked_off function on it
test_dict = {}



# this test tests whether, after creating the 5 predefined habits, there are actually 5 habits in the dictionary now
def test_creste_predefined_habits():
    create_predefined_habits(test_dict)
    result = len(test_dict.keys())
    assert result == 5

# this test checks whether the function can determine that the task 'shower' was actually not checked off often enough
def test_check_if_checked_off(capsys):
    check_if_checked_off(test_dict, "shower")
    captured = capsys.readouterr()
    assert captured.out == "You broke your habit! You have missed to 'shower'\n"


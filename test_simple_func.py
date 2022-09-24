import pytest

from rich.prompt import Prompt

from datetime import datetime

import main

# from main import BackToChooseEditMethod, BackToMain, BackToChooseList, exit_app, exit_main_check, back_to_upper_menu_check, back_to_edit_menu_check, list_name_duplicate_check, item_duplicate_check, date_convert_format, obtain_list_name, obtain_due_date

inputs = iter(['2', 'M', 'X', 'secondlist', 'Firstlist', '1', 'firstList', 'x', 'm', 'walk dog', 'shopping', 'shopping', 'Shopping', 'x', 'm', '2/2/22', '03/03/33', '2', '2/', 's', 'x', 'm'])

def fake_input(prompt):
    return next(inputs)

# test exit app function
class TestExitApp:
    # valid input
    def test_exit(self):
        with pytest.raises(KeyboardInterrupt):
            main.exit_app('x')

    # invalid input
    def test_not_exit(self):
        assert main.exit_app('a') is None
        assert main.exit_app(1) is None
        assert main.exit_app(1.2) is None

# test Back to main menu and exit the app function
class TestExitMain:
    # valid input - back to main menu
    def test_to_main(self):
        with pytest.raises(main.BackToMain):
            main.exit_main_check('m')
    
    # invalid input
    def test_not_to_main(self):
        assert main.exit_main_check('a') is None
        assert main.exit_main_check(1) is None

    # valid input - exit the app
    def test_exit(self):
        with pytest.raises(KeyboardInterrupt):
            main.exit_main_check('x')

# test back to choose another edit method function
class TestToUpper:
    # valid input
    def test_to_upper(self):
        with pytest.raises(main.BackToChooseEditMethod):
            main.back_to_upper_menu_check('q')
    
    # invalid input
    def test_not_to_upper(self):
        assert main.back_to_upper_menu_check('m') is None

# test back to choose another list function
class TestToEdit:
    # valid input
    def test_to_edit(self):
        with pytest.raises(main.BackToChooseList):
            main.back_to_edit_menu_check('l')
    
    # invalid input
    def test_not_to_edit(self):
        assert main.back_to_edit_menu_check('m') is None

# test back to choose another element function
class TestChooseAnotherElement:
    # valid input
    def test_choose_another_one(self):
        with pytest.raises(main.BackToChooseElement):
            main.select_another_element('e')
    
    # invalid input
    def test_not_to_choose(self):
        assert main.select_another_element('m') is None

# test the function which is used to check if user's input has been used as a list name already
class TestListNameDuplicate:
    # valid input
    def test_valid(self):
        assert main.list_name_duplicate_check('a', ['b', 'c']) is True

    # invalid input (been used already)
    def test_duplicate(self):
        assert main.list_name_duplicate_check('a', ['a', 'b']) is False

    # invalid input (case insensitive)
    def test_case_insensitive(self):
        assert main.list_name_duplicate_check('AB', ['b', 'ab']) is False

# test the function which is used to obtain and return a valid list name
class TestObtainListName:
    # valid input
    def test_valid_name(self, monkeypatch):
        monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['2', 'M', 'X', 'secondlist']
        assert main.obtain_list_name(all_list_names = ['firstlist', '1'], running_time_for_test = 1) == '2'
        assert main.obtain_list_name(all_list_names = ['firstlist', '1'], running_time_for_test = 1) == 'm'
        assert main.obtain_list_name(all_list_names = ['firstlist', '1'], running_time_for_test = 1) == 'x'
        assert main.obtain_list_name(all_list_names = ['firstlist', '1'], running_time_for_test = 1) == 'secondlist'

    # invalid input - duplicates(case insensitive)
    def test_invalid_name(self, monkeypatch):
        monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['Firstlist', '1', 'firstList']
        assert main.obtain_list_name(all_list_names = ['firstlist', '1'], running_time_for_test = 1) is False
        assert main.obtain_list_name(all_list_names = ['firstlist', '1'], running_time_for_test = 1) is False
        assert main.obtain_list_name(all_list_names = ['firstlist', '1'], running_time_for_test = 1) is False

    # quit the function - exit the app
    def test_exit(self, monkeypatch):
        with pytest.raises(KeyboardInterrupt):
            monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['x']
            main.obtain_list_name(all_list_names = ['firstlist', '1'], running_time_for_test = 1)

    # quit the function - back to main menu
    def test_quit(self, monkeypatch):
        with pytest.raises(main.BackToMain):
            monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['m']
            main.obtain_list_name(all_list_names = ['firstlist', '1'], running_time_for_test = 1)

# test the function which is used to check if user's input has been used as an item name already
class TestItemDuplicate:
    # valid input
    def test_valid(self):
        assert main.item_duplicate_check('shopping', ['dishwashing', 'walk dog', 'do laundry']) is True

    # invalid input - duplicates
    def test_duplicate(self):
        assert main.item_duplicate_check('walk dog', ['dishwashing', 'walk dog', 'do laundry']) is False

# test the function which is used to obtain and return a valid item name
class TestObtainItemName:
    # valid input
    def test_valid_name(self, monkeypatch):
        monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['walk dog', 'shopping']
        assert main.obtain_item_name(all_item_names = ['do laundry'], running_time_for_test = 1) == 'walk dog'
        assert main.obtain_item_name(all_item_names = ['do laundry'], running_time_for_test = 1) == 'shopping'

    # invalid input - duplicates (case insensitive)
    def test_invalid_name(self, monkeypatch):
        monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['shopping', 'Shopping']
        assert main.obtain_item_name(all_item_names = ['shopping'], running_time_for_test = 1) is False
        assert main.obtain_item_name(all_item_names = ['shopping'], running_time_for_test = 1) is False

    # quite the function - exit the app
    def test_exit(self, monkeypatch):
        with pytest.raises(KeyboardInterrupt):
            monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['x']
            main.obtain_item_name(all_item_names = ['shopping'], running_time_for_test = 1)

    # quite the function - back to main menu
    def test_quit(self, monkeypatch):
        with pytest.raises(main.BackToMain):
            monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['m']
            main.obtain_item_name(all_item_names = ['shopping'], running_time_for_test = 1)

# test the function which is used to check if user's input is in a valid format
class TestDateFormat:
    # valid input
    def test_valid(self):
        assert main.date_convert_format('2/2/22') == datetime(2022, 2, 2).date()
        assert main.date_convert_format('02/02/22') == datetime(2022, 2, 2).date()

    # invalid input
    def test_invalid(self):
        assert main.date_convert_format('2/2') is None
        assert main.date_convert_format('0.2/2') is None

# test the function which is used to obtain and return a valid due date
class TestObtainDueDate:
    # valid input
    def test_valid_date(self, monkeypatch):
        monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['2/2/22', '03/03/33']
        assert main.obtain_due_date(running_time_for_test = 1) 
        assert main.obtain_due_date(running_time_for_test = 1)

    # invalid input
    def test_invalid_date(self, monkeypatch):
        monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['2', '2/', 's']
        assert main.obtain_due_date(running_time_for_test = 1) is False
        assert main.obtain_due_date(running_time_for_test = 1) is False
        assert main.obtain_due_date(running_time_for_test = 1) is False

    # quite the function - exit the app
    def test_exit(self, monkeypatch):
        with pytest.raises(KeyboardInterrupt):
            monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['x']
            main.obtain_due_date(running_time_for_test = 1)

    # quite the function - back to main menu
    def test_quit(self, monkeypatch):
        with pytest.raises(main.BackToMain):
            monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['m']
            main.obtain_due_date(running_time_for_test = 1)
















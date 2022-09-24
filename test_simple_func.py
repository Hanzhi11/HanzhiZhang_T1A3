import pytest

from rich.prompt import Prompt

import main

# from main import BackToChooseEditMethod, BackToMain, BackToChooseList, exit_app, exit_main_check, back_to_upper_menu_check, back_to_edit_menu_check, list_name_duplicate_check, item_duplicate_check, date_convert_format, obtain_list_name, obtain_due_date

inputs = iter(['2', 'M', 'X', 'secondlist', 'x', 'm', 'shopping', 'walk dog', 'x', 'm', '2/2/22', '03/03/33', 'x', 'm'])

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
        assert main.list_name_duplicate_check('a', ['b', 'c'])

    # invalid input (been used already)
    def test_duplicate(self):
        assert main.list_name_duplicate_check('a', ['a', 'b']) is False

    # invalid input (case insensitive)
    def test_case_insensitive(self):
        assert main.list_name_duplicate_check('AB', ['b', 'ab']) is False

# test the function which is used to obtain return a valid list name
class TestObtainListName:
    # functional test using a valid input
    def test_valid_name(self, monkeypatch):
        monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['2', 'M', 'X', 'secondlist']
        assert main.obtain_list_name({'firstlist': [], '1': []})
        assert main.obtain_list_name({'firstlist': [], '1': []})
        assert main.obtain_list_name({'firstlist': [], '1': []})
        assert main.obtain_list_name({'firstlist': [], '1': []})

    # quit the function - exit the app
    def test_exit(self, monkeypatch):
        with pytest.raises(KeyboardInterrupt):
            monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['x']
            assert main.obtain_list_name({'firstlist': [], '1': []})

    # quit the function - back to main menu
    def test_quit(self, monkeypatch):
        with pytest.raises(main.BackToMain):
            monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['m']
            assert main.obtain_list_name({'firstlist': [], '1': []})

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
    # functional test using a valid input
    def test_valid_name(self, monkeypatch):
        monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['shopping', 'walk dog']
        assert main.obtain_item_name(['do laundry'])
        assert main.obtain_item_name(['dishwashing'])

    # quite the function - exit the app
    def test_exit(self, monkeypatch):
        with pytest.raises(KeyboardInterrupt):
            monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['x']
            assert main.obtain_item_name({'firstlist': [], '1': []})

    # quite the function - back to main menu
    def test_quit(self, monkeypatch):
        with pytest.raises(main.BackToMain):
            monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['m']
            assert main.obtain_item_name({'firstlist': [], '1': []})

# test the function which is used to check if user's input is in a valid format
class TestDateFormat:
    # valid input
    def test_valid(self):
        assert main.date_convert_format('2/2/22')
        assert main.date_convert_format('02/02/22')

    # invalid input
    def test_invalid(self):
        assert main.date_convert_format('2/2') is None
        assert main.date_convert_format('0.2/2') is None

# test the function which is used to obtain and return a valid due date
class TestObtainDueDate:
    # functional test using a valid input
    def test_valid_date(self, monkeypatch):
        monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['2/2/22', '03/03/33']
        assert main.obtain_due_date()
        assert main.obtain_due_date()

    # quite the function - exit the app
    def test_exit(self, monkeypatch):
        with pytest.raises(KeyboardInterrupt):
            monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['x']
            assert main.obtain_due_date()

    # quite the function - back to main menu
    def test_quit(self, monkeypatch):
        with pytest.raises(main.BackToMain):
            monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['m']
            assert main.obtain_due_date()
















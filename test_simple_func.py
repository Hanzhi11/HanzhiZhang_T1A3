import pytest

from rich.prompt import Prompt

import main

# from main import BackToChooseEditMethod, BackToMain, BackToChooseList, exit_app, exit_main_check, back_to_upper_menu_check, back_to_edit_menu_check, list_name_duplicate_check, item_duplicate_check, date_convert_format, obtain_list_name, obtain_due_date

inputs = iter(['2', 'M', 'X', 'secondlist', 'x', 'm', 'shopping', 'walk dog', 'x', 'm', '2/2/22', '03/03/33'])

def fake_input(prompt):
    return next(inputs)

class TestExitApp:
    def test_exit(self):
        with pytest.raises(KeyboardInterrupt):
            main.exit_app('x')

    def test_not_exit(self):
        assert main.exit_app('a') is None
        assert main.exit_app(1) is None
        assert main.exit_app(1.2) is None

class TestExitMain:
    def test_to_main(self):
        with pytest.raises(main.BackToMain):
            main.exit_main_check('m')
    
    def test_not_to_main(self):
        assert main.exit_main_check('a') is None
        assert main.exit_main_check(1) is None


    def test_exit(self):
        with pytest.raises(KeyboardInterrupt):
            main.exit_main_check('x')

class TestToUpper:
    def test_to_upper(self):
        with pytest.raises(main.BackToChooseEditMethod):
            main.back_to_upper_menu_check('q')
    
    def test_not_to_upper(self):
        assert main.back_to_upper_menu_check('m') is None

class TestToEdit:
    def test_to_edit(self):
        with pytest.raises(main.BackToChooseList):
            main.back_to_edit_menu_check('l')
    
    def test_not_to_edit(self):
        assert main.back_to_edit_menu_check('m') is None

class TestListNameDuplicate:
    def test_valid(self):
        assert main.list_name_duplicate_check('a', ['b', 'c'])

    def test_duplicate(self):
        assert main.list_name_duplicate_check('a', ['a', 'b']) is False

    def test_case_insensitive(self):
        assert main.list_name_duplicate_check('AB', ['b', 'ab']) is False

class TestObtainListName:
    def test_valid_name(self, monkeypatch):
        monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['2', 'M', 'X', 'secondlist']
        assert main.obtain_list_name({'firstlist': [], '1': []})
        assert main.obtain_list_name({'firstlist': [], '1': []})
        assert main.obtain_list_name({'firstlist': [], '1': []})
        assert main.obtain_list_name({'firstlist': [], '1': []})

    def test_exit(self, monkeypatch):
        with pytest.raises(KeyboardInterrupt):
            monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['x']
            assert main.obtain_list_name({'firstlist': [], '1': []})

    def test_quit(self, monkeypatch):
        with pytest.raises(main.BackToMain):
            monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['m']
            assert main.obtain_list_name({'firstlist': [], '1': []})

class TestItemDuplicate:
    def test_valid(self):
        assert main.item_duplicate_check('shopping', ['dishwashing', 'walk dog', 'do laundry']) is True

    def test_duplicate(self):
        assert main.item_duplicate_check('walk dog', ['dishwashing', 'walk dog', 'do laundry']) is False

class TestObtainItemName:
    def test_valid_name(self, monkeypatch):
        monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['shopping', 'walk dog']
        assert main.obtain_item_name(['do laundry'])
        assert main.obtain_item_name(['dishwashing'])

    def test_exit(self, monkeypatch):
        with pytest.raises(KeyboardInterrupt):
            monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['x']
            assert main.obtain_item_name({'firstlist': [], '1': []})

    def test_quit(self, monkeypatch):
        with pytest.raises(main.BackToMain):
            monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['m']
            assert main.obtain_item_name({'firstlist': [], '1': []})

class TestDateFormat:
    def test_valid(self):
        assert main.date_convert_format('2/2/22')
        assert main.date_convert_format('02/02/22')

    def test_invalid(self):
        assert main.date_convert_format('2/2') is None

class TestObtainDueDate:
    def test_valid_date(self, monkeypatch):
        monkeypatch.setattr(Prompt, 'ask', fake_input) # test case ['2/2/22', '03/03/33']
        assert main.obtain_due_date()
        assert main.obtain_due_date()
















import pytest

from main import BackToChooseEditMethod, BackToMain, BackToChooseList, exit_app, exit_main_check, back_to_upper_menu_check, back_to_edit_menu_check, list_name_duplicate_check, item_duplicate_check, date_format_check
inputs = iter([])

def fake_input(prompt):
    return next(inputs)

class TestExitApp:
    def test_exit(self):
        with pytest.raises(KeyboardInterrupt):
            exit_app('x')

    def test_not_exit(self):
        assert exit_app('a') == None
        assert exit_app(1) == None
        assert exit_app(1.2) == None

class TestExitMain:
    def test_to_main(self):
        with pytest.raises(BackToMain):
            exit_main_check('m')
    
    def test_not_to_main(self):
        assert exit_main_check('a') == None
        assert exit_main_check(1) == None


    def test_exit(self):
        with pytest.raises(KeyboardInterrupt):
            exit_main_check('x')

class TestToUpper:
    def test_to_upper(self):
        with pytest.raises(BackToChooseEditMethod):
            back_to_upper_menu_check('q')
    
    def test_not_to_upper(self):
        assert back_to_upper_menu_check('m') == None

class TestToEdit:
    def test_to_edit(self):
        with pytest.raises(BackToChooseList):
            back_to_edit_menu_check('l')
    
    def test_not_to_edit(self):
        assert back_to_edit_menu_check('m') == None

class TestListNameDuplicate:
    def test_valid(self):
        assert list_name_duplicate_check('a', ['b', 'c'])

    def test_duplicate(self):
        assert list_name_duplicate_check('a', ['a', 'b']) == False
        assert list_name_duplicate_check('A', ['b', 'a']) == False

class TestItemDuplicate:
    def test_valid(self):
        assert item_duplicate_check('shopping', ['dishwashing', 'walk dog', 'do laundry']) == True

    def test_duplicate(self):
        assert item_duplicate_check('walk dog', ['dishwashing', 'walk dog', 'do laundry']) == False

class TestDateFormat:
    def test_valid(self):
        assert date_format_check('2/2/22') == None
        assert date_format_check('02/02/22') == None

    def test_invalid(self):
        with pytest.raises(ValueError):
            date_format_check('2/2')
            date_format_check('2')
            date_format_check('2/')
            date_format_check('2/2/2')
            date_format_check('2/2/')














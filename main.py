from datetime import date, timedelta, datetime
from typing import ItemsView

from simple_term_menu import TerminalMenu

list_collection = {}
class ItemContent:
    def __init__(self, name, priority, due_date):
        self.name = name
        self.priority = priority
        self.due_date = due_date

    def __repr__(self):
        return f'Item name: {self.name}, Priority: {self.priority}, Due on: {self.due_date}'

class PriorityError(Exception):
    def __init__(self):
        super().__init__('Wrong priority level!')

class InvalidInputError(Exception):
    def __init__(self):
        super().__init__('Invalid input (element missing)')

class BackToMain(Exception):
    def __init__(self):
        super().__init__('Back to Main menu!')

class BackToUpper(Exception):
    def __init__(self):
        super().__init__('Back to the upper level menu!')

class BackToListSelection(Exception):
    def __init__(self):
        super().__init__('Back to List Selection menu!')

class BackToEdit(Exception):
    def __init__(self):
        super().__init__('Back to Edit menu!')

class EmptyListCollection(Exception):
    def __init__(self):
        super().__init__('No lists available. Please create one first.')

class ListNotExist(Exception):
    def __init__(self, list_name):
        super().__init__(f'The list \'{list_name}\' does not exist! Try another one!')
        

def quit_app(input):
    if input == 'X':
        raise KeyboardInterrupt

def quit_check_main(input):
    if input == 'Q':
        raise BackToMain
    else:
        quit_app(input)

def quit_check_sub(input):
    if input == 'q':
        raise BackToUpper
    else:
        quit_check_main(input)



def add_item(list_name, item):
    item_content = item.split(',')
    item_name = item_content[0].lower()
    item_priority_level = item_content[1].lower()
    item_due_date = item_content[2]
    default_due_date= date.today() + timedelta(days = 1)

    if len(item_due_date) == 0:
        if len(item_priority_level) == 0:
            item_content_details = ItemContent(item_name, '2', default_due_date)
        else:
            item_content_details = ItemContent(item_name, item_priority_level, default_due_date)
    else:
        converted_due_date = datetime.strptime(item_due_date, '%d/%m/%y').date()
        if len(item_priority_level) == 0:
            item_content_details = ItemContent(item_name, '2', converted_due_date)
        else:
            item_content_details = ItemContent(item_name, item_priority_level, converted_due_date)

    item_details = {'Name': item_content_details.name, 'Priority': item_content_details.priority, 'Due date':item_content_details.due_date}
    print(item_details)

    items.append(item_details)
    sort_items(list_name, items)

def sort_items(selected_list_name, items):
    sorted_item_list = sorted(items, key = lambda item: (item['Priority'], item['Due date']), reverse = True )
    new_list = {selected_list_name: sorted_item_list}
    list_collection.update(new_list)
    print(list_collection)


def name_and_priority_check(item):
    item_content = item.split(',')
    if item.count(',') == 2 and len(item_content[0]) != 0:
        if len(item_content[1]) != 0 and item_content[1] not in ['1', '2', '3']:
            raise PriorityError
        else:
            return item
    else:
        raise InvalidInputError


def validate_and_add(list_name):
    input_is_valid = False
    while not input_is_valid:
        item = input('Enter the item\'s name, priority and due date DD/MM/YY (X to exit the app or Q to back to Main Menu): ')
        quit_check_main(item)
        try:
            name_and_priority_check(item)
            add_item(list_name, item)
            input_is_valid = True
        except PriorityError as err:
            print(err)
        except InvalidInputError as err:
            print(err)
        except ValueError:
            print('Invalid date!')

def validate_and_add_edit(list_name):
    input_is_valid = False
    while not input_is_valid:
        item = input('Enter the item\'s name, priority and due date DD/MM/YY (X to exit the app, Q to back to Main Menu, q to back to the upper level menu): ')
        quit_check_sub(item)
        try:
            name_and_priority_check(item)
            add_item(list_name, item)
            input_is_valid = True
        except PriorityError as err:
            print(err)
        except InvalidInputError as err:
            print(err)
        except ValueError:
            print('Invalid date!')

def date_format_check(new_due_date):
    datetime.strptime(new_due_date, '%d/%m/%y').date()


def list_collection_check():
    if len(list_collection) == 0:
        raise EmptyListCollection
    
def list_check(list_name):
    if list_name.lower() not in list_collection.keys():
        raise ListNotExist(list_name)

def main_menu_selection():
    options = ['Create a new list', 'Edit an existing list', 'Delete an existing list', 'View an existing list', 'Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    print(f"You have selected \'{options[menu_entry_index]}\'!")
    if menu_entry_index == len(options) - 1:
        raise KeyboardInterrupt
    else:
        return options[menu_entry_index]

def add_more_decision():
    options = ['Yes', 'Back to Main menu', 'Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    print(f"You have selected \'{options[menu_entry_index]}\'!")
    if menu_entry_index == len(options) - 1:
        raise KeyboardInterrupt
    elif menu_entry_index == len(options) - 2:
        raise BackToMain
    else:
        return options[menu_entry_index]

def yes_upper_main_decision():
    options = ['Yes', 'Back to the upper level menu', 'Back to Main menu', 'Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    print(f"You have selected \'{options[menu_entry_index]}\'!")
    if menu_entry_index == len(options) - 1:
        raise KeyboardInterrupt
    elif menu_entry_index == len(options) - 2:
        raise BackToMain
    elif menu_entry_index == len(options) - 3:
        raise BackToUpper
    else:
        return options[menu_entry_index]

def list_selection(list_names):
    options = [*list_names, 'Back to Main menu', 'Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    print(f"You have selected the \'{options[menu_entry_index]}\' list!")
    if menu_entry_index == len(options) - 1:
        raise KeyboardInterrupt
    elif menu_entry_index == len(options) - 2:
        raise BackToMain
    else:
        return options[menu_entry_index]

def item_selection(item_name_list):
    options = [*item_name_list, 'Back to the upper level menu', 'Back to Main menu', 'Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    print(f"You have selected the \'{options[menu_entry_index]}\' item!")
    if menu_entry_index == len(options) - 1:
        raise KeyboardInterrupt
    elif menu_entry_index == len(options) - 2:
        raise BackToMain
    elif menu_entry_index == len(options) - 3:
        raise BackToUpper
    else:
        return menu_entry_index

def how_to_edit_selection():
    options = ['Add a new item', 'Modify an existing item', 'Remove an existing item', 'Back to the upper level menu', 'Back to Main menu', 'Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    print(f"You have selected: \'{options[menu_entry_index]}\'!")
    if menu_entry_index == len(options) - 1:
        raise KeyboardInterrupt
    elif menu_entry_index == len(options) - 2:
        raise BackToMain
    elif menu_entry_index == len(options) - 3:
        raise BackToUpper
    else:
        return options[menu_entry_index]

def element_selection():
    options = ['Name', 'Priority', 'Due date', 'Back to the upper level menu', 'Back to Main menu', 'Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    print(f"You have selected the \'{options[menu_entry_index]}\' element to edit!")
    if menu_entry_index == len(options) - 1:
        raise KeyboardInterrupt
    elif menu_entry_index == len(options) - 2:
        raise BackToMain
    elif menu_entry_index == len(options) - 3:
        raise BackToUpper
    else:
        return options[menu_entry_index]

def priority_selection():
    options = ['1', '2', '3', 'Back to the upper level menu', 'Back to Main menu', 'Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    print(f"You have selected the \'{options[menu_entry_index]}\' as the new priority level!")
    if menu_entry_index == len(options) - 1:
        raise KeyboardInterrupt
    elif menu_entry_index == len(options) - 2:
        raise BackToMain
    elif menu_entry_index == len(options) - 3:
        raise BackToUpper
    else:
        return options[menu_entry_index]

def remove_item(selected_list_name):
    print('Select which item to be deleted:')
    item_name_list = [item['Name'] for item in list_collection[selected_list_name]]
    selected_item_index = item_selection(item_name_list)
    deleted_item_name = item_name_list[selected_item_index]
    del list_collection[selected_list_name][selected_item_index]
    print(f'Item \'{deleted_item_name}\' has been removed from the list!')


try:
    while True:
        print('What would you like to do?')
        try:
            match main_menu_selection():            
                case 'Create a new list':
                    items = []
                    list_name = 0
                    while not list_name:
                        list_name = input('Enter the name of the new list (X to exit the app or Q to back to Main Menu): ')
                    quit_check_main(list_name)
                    validate_and_add(list_name)
                    while True:
                        print('Would you like to add another item?')
                        add_more_decision()
                        validate_and_add(list_name)
                case 'Edit an existing list':
                    try:
                        while True:
                            list_collection_check()
                            list_names = list(list_collection.keys())
                            print(list_names)
                            try:
                                while True:                                
                                    print('Select which list you would like to edit:')
                                    selected_list_name = list_selection(list_names)
                                    items = list(list_collection[selected_list_name])
                                    try:
                                        while True:                                                                    
                                            print(f'How would you like to edit the \'{selected_list_name}\' list?')
                                            selected_edit_method = how_to_edit_selection()
                                            try:
                                                while True:
                                                    match selected_edit_method:
                                                        case 'Add a new item':                                                            
                                                            validate_and_add_edit(selected_list_name)
                                                            while True:
                                                                print('Would you like to add another item?')
                                                                yes_upper_main_decision()
                                                                validate_and_add_edit(selected_list_name)
                                                        case 'Modify an existing item':
                                                            item_name_list = [item['Name'] for item in list_collection[selected_list_name]]
                                                            print(item_name_list)
                                                            selected_item_name = item_name_list[item_selection(item_name_list)]
                                                            selected_item = [item for item in list_collection[selected_list_name] if item['Name'] == selected_item_name]
                                                            print(selected_item)
                                                            try:
                                                                while True:
                                                                    print(f"Which element of the '{selected_item[0]['Name']}' item would you like to edit?")
                                                                    print(f"Its current status: Name is {selected_item[0]['Name']}, Priority level is {selected_item[0]['Priority']}, Due date is {selected_item[0]['Due date']}.")
                                                                    selected_element = element_selection()
                                                                    try:
                                                                        match selected_element:
                                                                            case 'Name':
                                                                                print(f"The current name is {selected_item[0]['Name']}.")
                                                                                new_name = input('Enter the new name (X to exit the app, Q to back to Main Menu or q to back to the upper level menu): ')
                                                                                quit_check_sub(new_name)
                                                                                selected_item[0]['Name'] = new_name
                                                                                print(f"The item name has been successfully amended to {selected_item[0]['Name']}.")                                                              
                                                                            case 'Priority':
                                                                                print('Select a new priority level:')
                                                                                print(f"The current priority level is {selected_item[0]['Priority']}.")
                                                                                new_priority = priority_selection()    
                                                                                selected_item[0]['Priority'] = new_priority
                                                                                print(f"The priority level has been successfully amended to {selected_item[0]['Priority']}.")
                                                                                items = list(list_collection[selected_list_name])
                                                                                sort_items(selected_list_name, items)
                                                                            case 'Due date':
                                                                                print(f"The current due date is {selected_item[0]['Due date']}.")
                                                                                date_format = False
                                                                                while not date_format:
                                                                                    try:                                                                                            
                                                                                        new_due_date = input('Enter the new due date DD/MM/YY (X to exit the app, Q to back to Main Menu or q to back to the upper level menu): ')    
                                                                                        quit_check_sub(new_due_date)
                                                                                        date_format_check(new_due_date)
                                                                                        converted_new_due_date = datetime.strptime(new_due_date, '%d/%m/%y').date()
                                                                                        selected_item[0]['Due date'] = converted_new_due_date
                                                                                        date_format = True
                                                                                        print(f"The due date has been successfully amended to {selected_item[0]['Due date']}.")
                                                                                        items = list(list_collection[selected_list_name])
                                                                                        sort_items(selected_list_name, items)
                                                                                    except ValueError:
                                                                                        print('Invalid date format. Try again!')    
                                                                    except BackToUpper as err:
                                                                        print(err)
                                                            except BackToUpper as err:
                                                                print(err)
                                                        case 'Remove an existing item':
                                                            remove_item(selected_list_name)
                                                            items = list(list_collection[selected_list_name])
                                                            while len(list_collection[selected_list_name]) != 0:
                                                                print('Would you like to remove another item?')
                                                                yes_upper_main_decision()
                                                                remove_item(selected_list_name)
                                                                items = list(list_collection[selected_list_name])
                                                            print(f'The {selected_list_name} list is now empty!')
                                                            break
                                            except BackToUpper as err:
                                                print(err)
                                    except BackToUpper as err:
                                        print(err)
                            except BackToUpper as err:
                                print(err)
                    except EmptyListCollection as err:
                        print(err)
                case 'Delete an exiting list':
                    pass
                case 'View an existing list':
                    pass
        except BackToMain as err:
            print(err)
except KeyboardInterrupt:
    print('You have existed the app!')
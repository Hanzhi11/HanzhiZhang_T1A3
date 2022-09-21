from datetime import date, timedelta, datetime

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
class BackToChooseEditMethod(Exception):
    def __init__(self):
        super().__init__('Back to Item Edit menu!')
class BackToChooseElement(Exception):
    def __init__(self):
        super().__init__('Back to Element Edit menu!')
class BackToChooseList(Exception):
    def __init__(self):
        super().__init__('Back to Edit menu!')
class BackToModifyMethod(Exception):
    def __init__(self):
        super().__init__('Back to Modify Method menu!')        
class BackToChooseItem(Exception):
    def __init__(self):
        super().__init__('Back to Choose another item!')
class EmptyListCollection(Exception):
    def __init__(self):
        super().__init__('The list collection is empty. Please create one first.')
class ListNotExist(Exception):
    def __init__(self, list_name):
        super().__init__(f'The list \'{list_name}\' does not exist! Try another one!')

def exit_app(input):
    if input == 'X':
        raise KeyboardInterrupt

def exit_main_check(input):
    if input == 'M':
        raise BackToMain
    else:
        exit_app(input)

def back_to_upper_menu_check(input):
    if input == 'q':
        raise BackToChooseEditMethod

def back_to_edit_menu_check(input):
    if input == 'Q':
        raise BackToChooseList

def modify_another_item_check(input):
    if input == 'i':
        raise BackToChooseItem

def modify_another_element_check(input):
    if input == 'e':
        raise BackToChooseElement

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
    items.append(item_details)
    sort_items(list_name, items)

def sort_items(selected_list_name, items):
    sorted_item_list = sorted(items, key = lambda item: (item['Priority'], item['Due date']), reverse = True )
    new_list = {selected_list_name: sorted_item_list}
    list_collection.update(new_list)

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
        item = input('Enter the item\'s name, priority and due date DD/MM/YY (X to exit the app or M to back to Main Menu): ')
        exit_main_check(item)
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
        item = input('Enter the item\'s name, priority and due date DD/MM/YY (X to exit the app, M to back to Main Menu, Q to choose another list, q to choose another edit method): ')
        exit_main_check(item)
        back_to_edit_menu_check(item)
        back_to_upper_menu_check(item)
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

def yes_no_decision():
    options = ['Yes', 'No (Back to Main menu)', 'Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    print(f"You have selected \'{options[menu_entry_index]}\'!")
    if menu_entry_index == len(options) - 1:
        raise KeyboardInterrupt
    elif menu_entry_index == len(options) - 2:
        raise BackToMain
    else:
        return options[menu_entry_index]

def yes_no_main_decision():
    options = ['Yes', 'No', 'Back to Main menu', 'Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    print(f"You have selected \'{options[menu_entry_index]}\'!")
    if menu_entry_index == len(options) - 1:
        raise KeyboardInterrupt
    elif menu_entry_index == len(options) - 2:
        raise BackToMain
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
    options = [*item_name_list, 'Choose another edit method', 'Choose another list', 'Back to Main menu', 'Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    print(f"You have selected the \'{options[menu_entry_index]}\' item!")
    if menu_entry_index == len(options) - 1:
        raise KeyboardInterrupt
    elif menu_entry_index == len(options) - 2:
        raise BackToMain
    elif menu_entry_index == len(options) - 3:
        raise BackToChooseList
    elif menu_entry_index == len(options) - 4:
        raise BackToChooseEditMethod
    else:
        return menu_entry_index

def how_to_edit_selection():
    options = ['Add a new item', 'Modify an existing item', 'Remove an existing item', 'Choose another list', 'Back to Main menu', 'Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    print(f"You have selected: \'{options[menu_entry_index]}\'!")
    if menu_entry_index == len(options) - 1:
        raise KeyboardInterrupt
    elif menu_entry_index == len(options) - 2:
        raise BackToMain
    elif menu_entry_index == len(options) - 3:
        raise BackToChooseList
    else:
        return options[menu_entry_index]

def element_selection():
    options = ['Name', 'Priority', 'Due date', 'Modify another item', 'Edit another list', 'Back to Main menu', 'Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    print(f"You have selected the \'{options[menu_entry_index]}\' element to edit!")
    if menu_entry_index == len(options) - 1:
        raise KeyboardInterrupt
    elif menu_entry_index == len(options) - 2:
        raise BackToMain
    elif menu_entry_index == len(options) - 3:
        raise BackToChooseList
    elif menu_entry_index == len(options) - 4:
        raise BackToChooseItem
    else:
        return options[menu_entry_index]

def priority_selection():
    options = ['1', '2', '3', 'Modify another element', 'Modify another item', 'Edit another list', 'Back to Main menu', 'Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    print(f"You have selected the \'{options[menu_entry_index]}\' as the new priority level!")
    if menu_entry_index == len(options) - 1:
        raise KeyboardInterrupt
    elif menu_entry_index == len(options) - 2:
        raise BackToMain
    elif menu_entry_index == len(options) - 3:
        raise BackToChooseList
    elif menu_entry_index == len(options) - 4:
        raise BackToChooseItem
    elif menu_entry_index == len(options) - 5:
        raise BackToChooseElement
    else:
        return options[menu_entry_index]

def continue_selection(selected_list_name, selected_item_name):
    options = [f'Continue to edit the {selected_item_name} item', f'Continue to edit the {selected_list_name} list', 'Edit another list', 'Back to Main menu', 'Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    print(f"You selected the \'{options[menu_entry_index]}\' option.")
    if menu_entry_index == len(options) - 1:
        raise KeyboardInterrupt
    elif menu_entry_index == len(options) - 2:
        raise BackToMain
    elif menu_entry_index == len(options) - 3:
        raise BackToChooseList
    elif menu_entry_index == len(options) - 4:
        raise BackToChooseEditMethod
    else:
        raise BackToChooseElement

def continue_but_change_selection(selected_list_name):
    options = ['Yes', f'Continue to edit the \'{selected_list_name}\' list', 'Edit another list', 'Back to Main menu', 'Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    print(f"You selected the \'{options[menu_entry_index]}\' option.")
    if menu_entry_index == len(options) - 1:
        raise KeyboardInterrupt
    elif menu_entry_index == len(options) - 2:
        raise BackToMain
    elif menu_entry_index == len(options) - 3:
        raise BackToChooseList
    elif menu_entry_index == len(options) - 4:
        raise BackToChooseEditMethod
    else:
        return options[menu_entry_index]

def remove_item(selected_list_name):
    print(f'Select which item to be removed from the {selected_list_name} list:')
    item_name_list = [item['Name'] for item in list_collection[selected_list_name]]
    selected_item_index = item_selection(item_name_list)
    deleted_item_name = item_name_list[selected_item_index]
    del list_collection[selected_list_name][selected_item_index]
    print(f'Item \'{deleted_item_name}\' has been removed from the list!')

def delete_list(list_names):
    print('Select which list you would like to delete:')
    selected_list_name = list_selection(list_names)
    del list_collection[selected_list_name]
    print(f'List \'{selected_list_name}\' has been deleted!')

try:
    while True:
        print('What would you like to do?')
        try:
            match main_menu_selection():
                case 'Create a new list':
                    items = []
                    list_name = input('Enter the name of the new list (X to exit the app or M to back to Main Menu): ')
                    exit_main_check(list_name)
                    validate_and_add(list_name)
                    while True:
                        print('Would you like to add another item?')
                        yes_no_decision()
                        validate_and_add(list_name)
                case 'Edit an existing list':
                        list_collection_check()
                        list_names = list(list_collection.keys())
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
                                                        continue_but_change_selection(selected_list_name)
                                                        validate_and_add_edit(selected_list_name)
                                                case 'Modify an existing item':                                                            
                                                    if len(list_collection[selected_list_name]) == 0:
                                                        print(f'The \'{selected_list_name}\' list is empty! Add a new item first!')
                                                        break
                                                    else:
                                                        while True:
                                                            print('Select an item to modify:')
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
                                                                                new_name = input('Enter the new name (X to exit the app, M to back to Main Menu, Q to edit another list, i to modify another item, or e to modify another element): ')
                                                                                exit_main_check(new_name)
                                                                                back_to_edit_menu_check(new_name)
                                                                                modify_another_item_check(new_name)
                                                                                modify_another_element_check(new_name)
                                                                                selected_item[0]['Name'] = new_name
                                                                                print(f"The item name has been successfully amended to {selected_item[0]['Name']}.")
                                                                                selected_item_name = new_name                                                              
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
                                                                                while True:
                                                                                    try:
                                                                                        new_due_date = input('Enter the new due date DD/MM/YY (X to exit the app, M to back to Main Menu, Q to edit another list, i to modify another item, or e to modify another element): ')    
                                                                                        exit_main_check(new_due_date)
                                                                                        back_to_edit_menu_check(new_due_date)
                                                                                        modify_another_item_check(new_due_date)
                                                                                        modify_another_element_check(new_due_date)
                                                                                        date_format_check(new_due_date)
                                                                                        converted_new_due_date = datetime.strptime(new_due_date, '%d/%m/%y').date()
                                                                                        selected_item[0]['Due date'] = converted_new_due_date
                                                                                        print(f"The due date has been successfully amended to {selected_item[0]['Due date']}.")
                                                                                        items = list(list_collection[selected_list_name])
                                                                                        sort_items(selected_list_name, items)
                                                                                        break
                                                                                    except ValueError:
                                                                                        print('Invalid date format. Try again!')
                                                                        continue_selection(selected_list_name, selected_item_name)
                                                                    except BackToChooseElement as err:
                                                                        print (err)                                                                
                                                            except BackToChooseItem as err:
                                                                print(err)
                                                case 'Remove an existing item':
                                                    if len(list_collection[selected_list_name]) == 0:
                                                        print(f'The \'{selected_list_name}\' list is empty! Add a new item first!')
                                                        break
                                                    else:
                                                        remove_item(selected_list_name)
                                                        items = list(list_collection[selected_list_name])
                                                        while len(list_collection[selected_list_name]) != 0:
                                                            print('Would you like to remove another item?')
                                                            yes_no_decision()
                                                            remove_item(selected_list_name)
                                                            items = list(list_collection[selected_list_name])
                                                        print(f'The {selected_list_name} list is now empty!')
                                                        break                                    
                                    except BackToChooseEditMethod as err:
                                        print(err)
                            except BackToChooseList as err:
                                print(err)
                case 'Delete an existing list':
                    list_collection_check()
                    list_names = list(list_collection.keys())
                    print(list_names)                             
                    delete_list(list_names)
                    while len(list_collection) != 0:
                        print('Would you like to delete another list?')
                        yes_no_decision()
                        delete_list(list_names)
                    print('The list collection is now empty!')
                case 'View an existing list':
                    pass
        except BackToMain as err:
            print(err)
        except EmptyListCollection as err:
            print(err)
except KeyboardInterrupt:
    print('You have existed the app!')
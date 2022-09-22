from datetime import date, timedelta, datetime
from simple_term_menu import TerminalMenu
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.bar import Bar
from rich import box, style
from rich import print as rprint

# list_collection = {}

list_collection = {'first':[{'Name': 'walk dooooooooooooooooooooooooooooooooooooooooooooooooooooooooog', 'Priority': '3', 'Due date': datetime.strptime('2/3/22', '%d/%m/%y').date()}, {'Name': 'shopping', 'Priority': '2', 'Due date': datetime.strptime('21/9/22', '%d/%m/%y').date()}, {'Name': 'dishwashing', 'Priority': '1', 'Due date': datetime.strptime('2/10/22', '%d/%m/%y').date()}], 'second':[{'Name': 'do laundry', 'Priority': '2', 'Due date': datetime.strptime('22/9/22', '%d/%m/%y').date()}]}
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
    if input == 'x':
        raise KeyboardInterrupt

def exit_main_check(input):
    if input == 'm':
        raise BackToMain
    else:
        exit_app(input)

def back_to_upper_menu_check(input):
    if input == 'q':
        raise BackToChooseEditMethod

def back_to_edit_menu_check(input):
    if input == 'l':
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

def item_duplicate_check(input, item_names):
    if input in item_names:
        rprint(f'[bold red]The \'{input}\' item exists already. Use another name![/bold red]')
        return False
    else:
        return True

def validate_and_add(list_name):
    input_is_valid = False
    while not input_is_valid:
        item_exists = False
        while not item_exists:
            item = input('Enter the item\'s name, priority and due date DD/MM/YY (x to exit the app or m to back to Main Menu): ')
            item_name = item.split(',')[0]
            item_names = [item['Name'] for item in items]
            item_exists = item_duplicate_check(item_name, item_names)
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
            rprint('[bold red]Invalid date![/bold red]')

def validate_and_add_edit(list_name):
    input_is_valid = False
    while not input_is_valid:
        item_exists = False
        while not item_exists:
            rprint('[italic #00f5d4]Enter the item\'s name, priority and due date DD/MM/YY[/italic #00f5d4]')
            rprint('[italic #00f5d4 underline bold]Note: use \',\' to seperate the name, priority level and due date[/italic #00f5d4 underline bold]')
            rprint('[italic #00f5d4]x to exit the app, m to back to Main Menu, l to choose another list, q to choose another edit method[/italic #00f5d4]')
            # item = input('Enter the item\'s name, priority and due date DD/MM/YY (x to exit the app, m to back to Main Menu, l to choose another list, q to choose another edit method): ')
            item = input()
            item_name = item.split(',')[0]
            item_names = [item['Name'] for item in items]
            item_exists = item_duplicate_check(item_name, item_names)
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
            rprint('[bold red]Invalid date![/bold red]')

def date_format_check(new_due_date):
    datetime.strptime(new_due_date, '%d/%m/%y').date()

def list_collection_check():
    if len(list_collection) == 0:
        raise EmptyListCollection
    
def list_check(list_name):
    if list_name.lower() not in list_collection.keys():
        raise ListNotExist(list_name)

def main_menu_selection():
    options = ['[1] Create a new list', '[2] Edit an existing list', '[3] Delete an existing list', '[4] View an existing list', '[x] Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    # rprint(f"[#fee440]You selected \'{options[menu_entry_index]}\'![/#fee440]")
    if menu_entry_index == len(options) - 1:
        raise KeyboardInterrupt
    else:
        return options[menu_entry_index]

def yes_no_decision():
    options = ['[y] Yes', '[n] No (Back to Main menu)', '[x] Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    # rprint(f"[#fee440]You selected \'{options[menu_entry_index]}\'![/#fee440]")
    if menu_entry_index == len(options) - 1:
        raise KeyboardInterrupt
    elif menu_entry_index == len(options) - 2:
        raise BackToMain
    # else:
    #     return options[menu_entry_index]

# def yes_no_main_decision():
#     options = ['[y] Yes', '[n] No', '[m] Back to Main menu', '[x] Exit the app']
#     terminal_menu = TerminalMenu(options)
#     menu_entry_index = terminal_menu.show()
#     print(f"You have selected \'{options[menu_entry_index]}\'!")
#     if menu_entry_index == len(options) - 1:
#         raise KeyboardInterrupt
#     elif menu_entry_index == len(options) - 2:
#         raise BackToMain
#     else:
#         return options[menu_entry_index]

def list_selection(list_names):
    list_name_options = []
    for index, name in enumerate(list_names, start = 1):
        list_name_options.append(f'[{index}] {name}')
    options = [*list_name_options, '[m] Back to Main menu', '[x] Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    # rprint(f"[#fee440]You selected: \'{options[menu_entry_index]}\' list![/#fee440]")
    if menu_entry_index == len(options) - 1:
        raise KeyboardInterrupt
    elif menu_entry_index == len(options) - 2:
        raise BackToMain
    else:
        return list_names[menu_entry_index]

def item_selection(item_names):
    item_name_options = []
    for index, name in enumerate(item_names, start = 1):
        item_name_options.append(f'[{index}] {name}')
    options = [*item_name_options, '[q] Choose another edit method', '[l] Choose another list', '[m] Back to Main menu', '[x] Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    # rprint(f"[#fee440]You selected: \'{options[menu_entry_index]}\' item![/#fee440]")
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
    options = ['[1] Add a new item', '[2] Modify an existing item', '[3] Remove an existing item', '[l] Choose another list', '[m] Back to Main menu', '[x] Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    # rprint(f"[#fee440]You selected: \'{options[menu_entry_index]}\'![/#fee440]")
    if menu_entry_index == len(options) - 1:
        raise KeyboardInterrupt
    elif menu_entry_index == len(options) - 2:
        raise BackToMain
    elif menu_entry_index == len(options) - 3:
        raise BackToChooseList
    else:
        return options[menu_entry_index]

def element_selection():
    options = ['[1] Name', '[2] Priority', '[3] Due date', '[i] Modify another item', '[l] Edit another list', '[m] Back to Main menu', '[x] Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    # rprint(f"[#fee440]You selected \'{options[menu_entry_index]}\' element for edit![/#fee440]")
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
    options = ['[1] 1', '[2] 2', '[3] 3', '[e] Modify another element', '[i] Modify another item', '[l] Edit another list', '[m] Back to Main menu', '[x] Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    # rprint(f"[#fee440]You selected \'{options[menu_entry_index]}\' as the new priority level![/#fee440]")
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
        return menu_entry_index

def continue_selection(selected_list_name, selected_item_name):
    options = [f'[1] Continue to edit the {selected_item_name} item', f'[2] Continue to edit the {selected_list_name} list', '[l] Edit another list', '[m] Back to Main menu', '[x] Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    # rprint(f"[#fee440]You selected the \'{options[menu_entry_index]}\' option.[/#fee440]")
    if menu_entry_index == len(options) - 1:
        raise KeyboardInterrupt
    elif menu_entry_index == len(options) - 2:
        raise BackToMain
    elif menu_entry_index == len(options) - 3:
        raise BackToChooseList
    elif menu_entry_index == len(options) - 4:
        raise BackToChooseEditMethod
    # else:
    #     raise BackToChooseElement

def continue_but_change_selection(selected_list_name):
    options = ['[y] Yes', f'[n] Continue to edit the \'{selected_list_name}\' list', '[l] Edit another list', '[m] Back to Main menu', '[x] Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    # rprint(f"[#fee440]You selected the \'{options[menu_entry_index]}\' option.[/#fee440]")
    if menu_entry_index == len(options) - 1:
        raise KeyboardInterrupt
    elif menu_entry_index == len(options) - 2:
        raise BackToMain
    elif menu_entry_index == len(options) - 3:
        raise BackToChooseList
    elif menu_entry_index == len(options) - 4:
        raise BackToChooseEditMethod
    # else:
    #     return options[menu_entry_index]

def remove_item(selected_list_name):
    rprint(f'[italic #00f5d4]Select which item to be removed from the {selected_list_name} list:[/italic #00f5d4]')
    item_name_list = [item['Name'] for item in list_collection[selected_list_name]]
    selected_item_index = item_selection(item_name_list)
    deleted_item_name = item_name_list[selected_item_index]
    del list_collection[selected_list_name][selected_item_index]
    print(f'Item \'{deleted_item_name}\' has been removed from the list!')

def delete_list(list_names):
    rprint('[italic #00f5d4]Select which list you would like to delete:[/italic #00f5d4]')
    selected_list_name = list_selection(list_names)
    del list_collection[selected_list_name]
    rprint(f'[#00bbf9]List \'{selected_list_name}\' has been deleted![/#00bbf9]')

def view_list(list_names):
    rprint('[italic #00f5d4]Select which list you would like to view:[/italic #00f5d4]')
    selected_list_name = list_selection(list_names)
    selected_list = list_collection[selected_list_name]

    display_list = Table(title = f'\n{selected_list_name.upper()}', title_style = '#f15bb5', min_width = 50, header_style = 'italic bold', box = box.HORIZONTALS, row_styles = [style.Style(bgcolor = '#aaaaaa'), ''])

    display_list.add_column('Item No.\n', style = 'white', justify = 'center', min_width = 8, no_wrap = True)
    display_list.add_column('Item Name\n', style = 'cyan', overflow = "ellipsis", no_wrap = True, min_width = 20, max_width = 40)
    display_list.add_column('Priority Level\n(Low - Medium - High)', style = 'magenta', justify = 'center', no_wrap = True, min_width = 21)
    display_list.add_column('Due Date\n', style = 'green', min_width = 8, no_wrap = True)

    long_bar = Bar(size = 1, begin = 0.67, end = 1, width = 21, color = 'red', bgcolor = None)
    medium_bar = Bar(size = 1, begin = 0.33, end = 0.67, width = 21, color = 'yellow', bgcolor = None)
    short_bar = Bar(size = 1, begin = 0, end = 0.33, width = 21, color = 'green', bgcolor = None)

    for index, item in enumerate(selected_list, start = 1):
        due_date = Text(datetime.strftime(item['Due date'], '%d/%m/%y'))
        priority_level = item['Priority']
        if item['Due date'] < date.today():
            due_date.stylize('red')
        if item['Priority'] == '1':
            priority_level = short_bar
        elif item['Priority'] == '2':
            priority_level = medium_bar
        else:
            priority_level = long_bar
        display_list.add_row(str(index), item['Name'].lower().capitalize(), priority_level, due_date)

    console = Console()
    rprint(f'[#fee440]You are viewing the \'{selected_list_name}\' list![/#fee440]')
    console.print(display_list)

def list_name_duplicate_check(input):
    if input in list_collection.keys():
        rprint(f'[bold red]The \'{input}\' list exists already. Enter another name.[/bold red]')
        return False
    else:
        return True
    



try:
    while True:
        rprint('[italic #00f5d4]What would you like to do?[/italic #00f5d4]')
        try:
            match main_menu_selection():
                case '[1] Create a new list':
                    items = []
                    list_name_exists = False
                    while not list_name_exists:
                        list_name = input('Enter the name of the new list (x to exit the app or m to back to Main Menu): ')
                        if len(list_name) == 0:
                            rprint('[bold red]Empty input![/bold red]')
                        else:
                            list_name_exists = list_name_duplicate_check(list_name)
                    exit_main_check(list_name)
                    validate_and_add(list_name)
                    items = list(list_collection[list_name])
                    while True:
                        rprint('[italic #00f5d4]Would you like to add another item?[/italic #00f5d4]')
                        yes_no_decision()
                        validate_and_add(list_name)
                case '[2] Edit an existing list':
                        list_collection_check()
                        list_names = list(list_collection.keys())
                        while True:
                            rprint('[italic #00f5d4]Select which list you would like to edit:[/italic #00f5d4]')
                            selected_list_name = list_selection(list_names)
                            items = list(list_collection[selected_list_name])
                            try:
                                while True:
                                    rprint(f'[italic #00f5d4]How would you like to edit the \'{selected_list_name}\' list?[/italic #00f5d4]')
                                    selected_edit_method = how_to_edit_selection()
                                    try:
                                        while True:
                                            match selected_edit_method:
                                                case '[1] Add a new item':                                                            
                                                    validate_and_add_edit(selected_list_name)
                                                    while True:
                                                        rprint('[italic #00f5d4]Would you like to add another item?[/italic #00f5d4]')
                                                        continue_but_change_selection(selected_list_name)
                                                        validate_and_add_edit(selected_list_name)
                                                case '[2] Modify an existing item':                                                            
                                                    if len(list_collection[selected_list_name]) == 0:
                                                        rprint(f'[bold red]The \'{selected_list_name}\' list is empty! Add a new item first![/bold red]')
                                                        break
                                                    else:
                                                        while True:
                                                            rprint('[italic #00f5d4]Select an item to modify:[/italic #00f5d4]')
                                                            item_name_list = [item['Name'] for item in list_collection[selected_list_name]]
                                                            # print(item_name_list)
                                                            selected_item_name = item_name_list[item_selection(item_name_list)]
                                                            selected_item = [item for item in list_collection[selected_list_name] if item['Name'] == selected_item_name]
                                                            # print(selected_item)
                                                            try:
                                                                while True:
                                                                    rprint(f"[italic #00f5d4]Which element of the '{selected_item[0]['Name']}' item would you like to edit?[/italic #00f5d4]")
                                                                    rprint(f"[#fee440]Its current status: Name is {selected_item[0]['Name']}, Priority level is {selected_item[0]['Priority']}, Due date is {selected_item[0]['Due date']}.[/#fee440]")
                                                                    selected_element = element_selection()
                                                                    try:
                                                                        match selected_element:
                                                                            case '[1] Name':
                                                                                rprint(f"[#fee440]The current name is {selected_item[0]['Name']}.[/#fee440]")
                                                                                new_name = input('Enter the new name (x to exit the app, m to back to Main Menu, l to edit another list, i to modify another item, or e to modify another element): ')
                                                                                exit_main_check(new_name)
                                                                                back_to_edit_menu_check(new_name)
                                                                                modify_another_item_check(new_name)
                                                                                modify_another_element_check(new_name)
                                                                                selected_item[0]['Name'] = new_name
                                                                                rprint(f"[#00bbf9]The item name has been successfully amended to {selected_item[0]['Name']}.[/#00bbf9]")
                                                                                selected_item_name = new_name                                                              
                                                                            case '[2] Priority':
                                                                                rprint('[italic #00f5d4]Select a new priority level:[/italic #00f5d4]')
                                                                                rprint(f"[#fee440]The current priority level is {selected_item[0]['Priority']}.[/#fee440]")
                                                                                new_priority = priority_selection()    
                                                                                selected_item[0]['Priority'] = new_priority
                                                                                rprint(f"[#00bbf9]The priority level has been successfully amended to {selected_item[0]['Priority']}.[/#00bbf9]")
                                                                                items = list(list_collection[selected_list_name])
                                                                                sort_items(selected_list_name, items)
                                                                            case '[3] Due date':
                                                                                rprint(f"[#fee440]The current due date is {selected_item[0]['Due date']}.[/#fee440]")
                                                                                while True:
                                                                                    try:
                                                                                        new_due_date = input('Enter the new due date DD/MM/YY (x to exit the app, m to back to Main Menu, l to edit another list, i to modify another item, or e to modify another element): ')    
                                                                                        exit_main_check(new_due_date)
                                                                                        back_to_edit_menu_check(new_due_date)
                                                                                        modify_another_item_check(new_due_date)
                                                                                        modify_another_element_check(new_due_date)
                                                                                        date_format_check(new_due_date)
                                                                                        converted_new_due_date = datetime.strptime(new_due_date, '%d/%m/%y').date()
                                                                                        selected_item[0]['Due date'] = converted_new_due_date
                                                                                        rprint(f"[#00bbf9]The due date has been successfully amended to {selected_item[0]['Due date']}.[/#00bbf9]")
                                                                                        items = list(list_collection[selected_list_name])
                                                                                        sort_items(selected_list_name, items)
                                                                                        break
                                                                                    except ValueError:
                                                                                        rprint('[bold red]Invalid date format. Try again![/bold red]')
                                                                        continue_selection(selected_list_name, selected_item_name)
                                                                    except BackToChooseElement as err:
                                                                        rprint (f'[#fee440]{err}[/#fee440]')                                                                
                                                            except BackToChooseItem as err:
                                                                rprint (f'[#fee440]{err}[/#fee440]')
                                                case '[3] Remove an existing item':
                                                    if len(list_collection[selected_list_name]) == 0:
                                                        rprint(f'[bold red]The \'{selected_list_name}\' list is empty! Add a new item first![/bold red]')
                                                        break
                                                    else:
                                                        remove_item(selected_list_name)
                                                        items = list(list_collection[selected_list_name])
                                                        while len(list_collection[selected_list_name]) != 0:
                                                            rprint('[italic #00f5d4]Would you like to remove another item?[/italic #00f5d4]')
                                                            yes_no_decision()
                                                            remove_item(selected_list_name)
                                                            items = list(list_collection[selected_list_name])
                                                        rprint(f'[#fee440]The {selected_list_name} list is now empty![/#fee440]')
                                                        break
                                    except BackToChooseEditMethod as err:
                                        rprint (f'[#fee440]{err}[/#fee440]')
                            except BackToChooseList as err:
                                rprint (f'[#fee440]{err}[/#fee440]')
                case '[3] Delete an existing list':
                    list_collection_check()
                    list_names = list(list_collection.keys())                          
                    delete_list(list_names)
                    while len(list_collection) != 0:
                        rprint('[italic #00f5d4]Would you like to delete another list?[/italic #00f5d4]')
                        yes_no_decision()
                        delete_list(list_names)
                    rprint('[bold red]The list collection is now empty![/bold red]')
                case '[4] View an existing list':
                    list_collection_check()
                    list_names = list(list_collection.keys())
                    view_list(list_names)
        except BackToMain as err:
            rprint (f'[#fee440]{err}[/#fee440]')
        except EmptyListCollection as err:
            rprint (f'[bold red]{err}[/bold red]')
except KeyboardInterrupt:
    rprint('[#9b5de5]You have existed the app![/#9b5de5]')
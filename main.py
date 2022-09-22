from datetime import date, datetime
from simple_term_menu import TerminalMenu
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.bar import Bar
from rich import box, style
from rich import print as rprint
from rich.prompt import Prompt
class ListItem:
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

def sort_items_and_update_list_collection(selected_list_name, items):
    sorted_item_list = sorted(items, key = lambda item: (item.due_date, item.priority), reverse = True)
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
        rprint(f'[red]The \'{input}\' item exists already. Use another name![/red]')
        return False
    else:
        return True

def obtain_item_name(item_names):
    item_exists = False
    while not item_exists:
        item_name = Prompt.ask('Enter the item\'s name (x to exit the app or m to back to Main Menu)')
        if len(item_name) != 0:
            exit_main_check(item_name)
            item_exists = item_duplicate_check(item_name, item_names)
        else:
            rprint('[red]Empty Input![/red]')
    return item_name

def obtain_item_name_edit(item_names):
    item_exists = False
    while not item_exists:
        item_name = Prompt.ask('Enter the item\'s name (x to exit the app, m to Main Menu, l to choose another list, q to choose another edit method)')
        if len(item_name) != 0:
            exit_main_check(item_name)
            back_to_upper_menu_check(item_name)
            back_to_edit_menu_check(item_name)
            item_exists = item_duplicate_check(item_name, item_names)
        else:
            rprint('[red]Empty Input![/red]')
    else:
        return item_name

def obtain_prioroty_level():
    priority_level = Prompt.ask('Enter priority level', choices = ['1', '2', '3', 'x', 'm'])
    exit_main_check(priority_level)
    return priority_level

def obtain_prioroty_level_edit():
    priority_level = Prompt.ask('Enter priority level', choices = ['1', '2', '3', 'x', 'm', 'l', 'q'])
    exit_main_check(priority_level)
    back_to_upper_menu_check(priority_level)
    back_to_edit_menu_check(priority_level)
    return priority_level

def obtain_due_date():
    while True:
        due_date = Prompt.ask('Enter Due date DD/MM/YY (x to exit the app or m to back to Main Menu)')
        exit_main_check(due_date)
        try:
            date_format_check(due_date)
            return due_date
        except ValueError:
            rprint('[red]Invalid date![/red]')

def obtain_due_date_edit():
    while True:
        due_date = Prompt.ask('Enter Due date DD/MM/YY (x to exit the app, m to Main Menu, l to choose another list, q to choose another edit method)')
        exit_main_check(due_date)
        back_to_upper_menu_check(due_date)
        back_to_edit_menu_check(due_date)
        try:
            date_format_check(due_date)
            return due_date
        except ValueError:
            rprint('[red]Invalid date![/red]')

def add_item(item_names, list_name):
    item_name = obtain_item_name(item_names)
    priority_level = obtain_prioroty_level()
    due_date = obtain_due_date()
    new_item = ListItem(item_name, priority_level, due_date)
    items.append(new_item)
    sort_items_and_update_list_collection(list_name, items)
    rprint(f"[#00bbf9]The new item '{item_name}' has been successfully added to {list_name}.[/#00bbf9]")

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
    if menu_entry_index == len(options) - 1:
        raise KeyboardInterrupt
    else:
        return options[menu_entry_index]

def yes_no_decision():
    options = ['[y] Yes', '[n] No (Back to Main menu)', '[x] Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    if menu_entry_index == len(options) - 1:
        raise KeyboardInterrupt
    elif menu_entry_index == len(options) - 2:
        raise BackToMain

def list_selection(list_names):
    list_name_options = []
    for index, name in enumerate(list_names, start = 1):
        list_name_options.append(f'[{index}] {name}')
    options = [*list_name_options, '[m] Back to Main menu', '[x] Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
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
    options = [f'[1] Continue to edit the \'{selected_item_name}\' item', f'[2] Continue to edit the current {selected_list_name} list', '[l] Edit another list', '[m] Back to Main menu', '[x] Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    if menu_entry_index == len(options) - 1:
        raise KeyboardInterrupt
    elif menu_entry_index == len(options) - 2:
        raise BackToMain
    elif menu_entry_index == len(options) - 3:
        raise BackToChooseList
    elif menu_entry_index == len(options) - 4:
        raise BackToChooseEditMethod

def continue_but_change_selection(selected_list_name):
    options = ['[y] Yes', f'[n] Continue to edit the \'{selected_list_name}\' list', '[l] Edit another list', '[m] Back to Main menu', '[x] Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    if menu_entry_index == len(options) - 1:
        raise KeyboardInterrupt
    elif menu_entry_index == len(options) - 2:
        raise BackToMain
    elif menu_entry_index == len(options) - 3:
        raise BackToChooseList
    elif menu_entry_index == len(options) - 4:
        raise BackToChooseEditMethod

def remove_item(selected_list_name):
    rprint(f'[italic #00f5d4]Select which item to be removed from the {selected_list_name} list:[/italic #00f5d4]')
    item_name_list = [item.name for item in list_collection[selected_list_name]]
    selected_item_index = item_selection(item_name_list)
    deleted_item_name = item_name_list[selected_item_index]
    del list_collection[selected_list_name][selected_item_index]
    rprint(f'[#00bbf9]Item \'{deleted_item_name}\' has been removed from the list![#00bbf9]')

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
        due_date = Text(item.due_date)
        priority_level = item.priority
        if datetime.strptime(item.due_date,'%d/%m/%y').date() < date.today():
            due_date.stylize('red')
        if item.priority == '1':
            priority_level = short_bar
        elif item.priority == '2':
            priority_level = medium_bar
        else:
            priority_level = long_bar
        display_list.add_row(str(index), item.name.lower().capitalize(), priority_level, due_date)

    console = Console()
    rprint(f'[#fee440]You are viewing the \'{selected_list_name}\' list![/#fee440]')
    console.print(display_list)

def list_name_duplicate_check(input):
    if input in list_collection.keys():
        rprint(f'[red]The \'{input}\' list exists already. Enter another name.[/red]')
        return False
    else:
        return True
   

try:
    list_collection = {}
    while True:
        rprint('[italic #00f5d4]What would you like to do?[/italic #00f5d4]')
        try:
            match main_menu_selection():
                case '[1] Create a new list':
                    items = []
                    item_names = [item.name for item in items]
                    list_name_exists = False
                    while not list_name_exists:
                        list_name = input('Enter the name of the new list (x to exit the app or m to back to Main Menu): ')
                        if len(list_name) == 0:
                            rprint('[red]Empty input![/red]')
                        else:
                            exit_main_check(list_name)
                            list_name_exists = list_name_duplicate_check(list_name)
                    add_item(item_names, list_name)
                    items = list(list_collection[list_name])
                    item_names = [item.name for item in items]         
                    while True:
                        rprint('[italic #00f5d4]Would you like to add another item?[/italic #00f5d4]')
                        yes_no_decision()
                        add_item(item_names, list_name)
                        items = list(list_collection[list_name])
                        item_names = [item.name for item in items] 
                case '[2] Edit an existing list':
                        list_collection_check()
                        list_names = list(list_collection.keys())
                        while True:
                            rprint('[italic #00f5d4]Select which list you would like to edit:[/italic #00f5d4]')
                            selected_list_name = list_selection(list_names)
                            items = list(list_collection[selected_list_name])
                            item_names = [item.name for item in items]
                            try:
                                while True:
                                    rprint(f'[italic #00f5d4]How would you like to edit the \'{selected_list_name}\' list?[/italic #00f5d4]')
                                    selected_edit_method = how_to_edit_selection()
                                    try:
                                        while True:
                                            match selected_edit_method:
                                                case '[1] Add a new item':                                                            
                                                    add_item(item_names, selected_list_name)
                                                    items = list(list_collection[list_name])
                                                    item_names = [item.name for item in items] 
                                                    while True:
                                                        rprint('[italic #00f5d4]Would you like to add another item?[/italic #00f5d4]')
                                                        continue_but_change_selection(selected_list_name)
                                                        add_item(item_names, selected_list_name)
                                                        items = list(list_collection[list_name])
                                                        item_names = [item.name for item in items] 
                                                case '[2] Modify an existing item':                                                            
                                                    if len(list_collection[selected_list_name]) == 0:
                                                        rprint(f'[red]The \'{selected_list_name}\' list is empty! Add a new item first![/red]')
                                                        break
                                                    else:
                                                        while True:
                                                            rprint('[italic #00f5d4]Select an item to modify:[/italic #00f5d4]')
                                                            item_name_list = [item.name for item in list_collection[selected_list_name]]
                                                            selected_item_name = item_name_list[item_selection(item_name_list)]
                                                            selected_item = [item for item in list_collection[selected_list_name] if item.name == selected_item_name]
                                                            try:
                                                                while True:
                                                                    rprint(f"[italic #00f5d4]Which element of the '{selected_item[0].name}' item would you like to edit?[/italic #00f5d4]")
                                                                    rprint(f"[#fee440]Its current status: Name is {selected_item[0].name}, Priority level is {selected_item[0].priority}, Due date is {selected_item[0].due_date}.[/#fee440]")
                                                                    selected_element = element_selection()
                                                                    try:
                                                                        match selected_element:
                                                                            case '[1] Name':
                                                                                rprint(f"[#fee440]The current name is {selected_item[0].name}.[/#fee440]")
                                                                                new_name = obtain_item_name_edit(item_name_list)                                                                            
                                                                                selected_item[0].name = new_name
                                                                                rprint(f"[#00bbf9]The item name has been successfully amended to {selected_item[0].name}.[/#00bbf9]")
                                                                                selected_item_name = new_name                                                              
                                                                            case '[2] Priority':
                                                                                rprint('[italic #00f5d4]Select a new priority level:[/italic #00f5d4]')
                                                                                rprint(f"[#fee440]The current priority level is {selected_item[0].priority}.[/#fee440]")
                                                                                new_priority = obtain_prioroty_level_edit()  
                                                                                selected_item[0].priority = new_priority
                                                                                rprint(f"[#00bbf9]The priority level has been successfully amended to {selected_item[0].priority}.[/#00bbf9]")
                                                                                items = list(list_collection[selected_list_name])
                                                                                sort_items_and_update_list_collection(selected_list_name, items)
                                                                            case '[3] Due date':
                                                                                rprint(f"[#fee440]The current due date is {selected_item[0].due_date}.[/#fee440]")
                                                                                new_due_date = obtain_due_date_edit()
                                                                                converted_new_due_date = datetime.strptime(new_due_date, '%d/%m/%y').date()
                                                                                selected_item[0].due_date = converted_new_due_date
                                                                                rprint(f"[#00bbf9]The due date has been successfully amended to {selected_item[0].due_date}.[/#00bbf9]")
                                                                                items = list(list_collection[selected_list_name])
                                                                                sort_items_and_update_list_collection(selected_list_name, items)
                                                                        continue_selection(selected_list_name, selected_item_name)
                                                                    except BackToChooseElement as err:
                                                                        rprint (f'[#fee440]{err}[/#fee440]')                                                                
                                                            except BackToChooseItem as err:
                                                                rprint (f'[#fee440]{err}[/#fee440]')
                                                case '[3] Remove an existing item':
                                                    if len(list_collection[selected_list_name]) == 0:
                                                        rprint(f'[red]The \'{selected_list_name}\' list is empty! Add a new item first![/red]')
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
                    rprint('[red]The list collection is now empty![/red]')
                case '[4] View an existing list':
                    list_collection_check()
                    list_names = list(list_collection.keys())
                    view_list(list_names)
        except BackToMain as err:
            rprint (f'[#fee440]{err}[/#fee440]')
        except EmptyListCollection as err:
            rprint (f'[red]{err}[/red]')
except KeyboardInterrupt:
    rprint('[#9b5de5]You have existed the app![/#9b5de5]')
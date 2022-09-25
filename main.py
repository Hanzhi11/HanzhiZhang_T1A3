from datetime import date, datetime
from simple_term_menu import TerminalMenu
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.bar import Bar
from rich import box, style
from rich import print as rprint
from rich.prompt import Prompt
import pandas
from to_do_list_class import EmptyList, ListItem, BackToMain, BackToChooseEditMethod, BackToChooseElement, BackToChooseList, BackToChooseItem, EmptyListCollection

def exit_app(input):
    if input == 'x':
        raise KeyboardInterrupt

def exit_main_check(input):
    exit_app(input)
    if input == 'm':
        raise BackToMain

def back_to_upper_menu_check(input):
    if input == 'q':
        raise BackToChooseEditMethod

def back_to_edit_menu_check(input):
    if input == 'l':
        raise BackToChooseList

def select_another_element(input):
    if input == 'e':
        raise BackToChooseElement

def sort_items(list_content):
    return sorted(list_content, key = lambda item: (item.due_date, item.priority), reverse = True)

def update_collection(list_name, list_content, list_collection):
    new_list = {list_name: list_content}
    list_collection.update(new_list)
    return list_collection

def item_duplicate_check(user_input, all_item_names):
    if user_input in all_item_names:
        rprint(f'[red]The \'{user_input}\' item exists already. Use another name![/red]')
        return False
    else:
        return user_input

def obtain_item_name(all_item_names, running_time_for_test = -1):
    valid_name = False
    while not valid_name:
        if running_time_for_test == 0:
            return False
        else:
            user_input = Prompt.ask('Enter the item\'s name (x to exit the app or m to back to Main Menu)')
            if len(user_input) != 0:
                exit_main_check(user_input)
                valid_name = item_duplicate_check(user_input.lower(), all_item_names)
            else:
                rprint('[red]Empty Input![/red]')
        running_time_for_test -= 1
    return valid_name

def get_new_item_name(all_item_names):
    valid_new_name = False
    while not valid_new_name:
        user_input = Prompt.ask('Enter the item\'s name (x to exit the app, m to Main Menu, l to choose another list, q to choose another edit method)')
        if len(user_input) != 0:
            exit_main_check(user_input)
            back_to_upper_menu_check(user_input)
            back_to_edit_menu_check(user_input)
            valid_new_name = item_duplicate_check(user_input.lower(), all_item_names)
        else:
            rprint('[red]Empty Input![/red]')
    return valid_new_name

def update_item_name(all_item_names, running_time_for_test = -1):
    valid_new_name = False
    while not valid_new_name:
        if running_time_for_test == 0:
            return False
        else:
            user_input = Prompt.ask('Enter the item\'s name (x to exit the app, m to Main Menu, l to choose another list, q to choose another edit method, e to choose another element)')
            if len(user_input) != 0:
                exit_main_check(user_input)
                back_to_upper_menu_check(user_input)
                back_to_edit_menu_check(user_input)
                select_another_element(user_input)
                valid_new_name = item_duplicate_check(user_input.lower(), all_item_names)
            else:
                rprint('[red]Empty Input![/red]')
        running_time_for_test -= 1
    return valid_new_name

def obtain_priority_level():
    priority_level = Prompt.ask('Enter priority level', choices = ['1', '2', '3', 'x', 'm'])
    exit_main_check(priority_level)
    return priority_level

def get_new_priority_level():
    priority_level = Prompt.ask('Enter priority level', choices = ['1', '2', '3', 'x', 'm', 'l', 'q'])
    exit_main_check(priority_level)
    back_to_upper_menu_check(priority_level)
    back_to_edit_menu_check(priority_level)
    return priority_level

def update_priority_level():
    priority_level = Prompt.ask('Enter priority level', choices = ['1', '2', '3', 'x', 'm', 'l', 'q', 'e'])
    exit_main_check(priority_level)
    back_to_upper_menu_check(priority_level)
    back_to_edit_menu_check(priority_level)
    select_another_element(priority_level)
    return priority_level

def date_convert_format(user_input):
    try:
        return datetime.strptime(user_input, '%d/%m/%y').date()
    except ValueError:
        rprint('[red]Invalid date![/red]')

def obtain_due_date(running_time_for_test = -1):
    valid_due_date = None
    while not valid_due_date:
        if running_time_for_test == 0:
            return False
        else:
            user_input = Prompt.ask('Enter Due date DD/MM/YY (x to exit the app or m to back to Main Menu)')
            exit_main_check(user_input)
            valid_due_date = date_convert_format(user_input)
        running_time_for_test -= 1
    return valid_due_date

def update_due_date():
    valid_new_date = None
    while not valid_new_date:
        user_input = Prompt.ask('Enter Due date DD/MM/YY (x to exit the app, m to Main Menu, l to choose another list, q to choose another edit method, e to choose another element)')
        exit_main_check(user_input)
        back_to_upper_menu_check(user_input)
        back_to_edit_menu_check(user_input)
        select_another_element(user_input)
        valid_new_date = date_convert_format(user_input)
    return valid_new_date

def get_new_due_date():
    valid_new_date = None
    while not valid_new_date:
        user_input = Prompt.ask('Enter Due date DD/MM/YY (x to exit the app, m to Main Menu, l to choose another list, q to choose another edit method)')
        exit_main_check(user_input)
        back_to_upper_menu_check(user_input)
        back_to_edit_menu_check(user_input)
        valid_new_date = date_convert_format(user_input)
    return valid_new_date

def add_item(list_name, list_content, all_item_names):
    item_name = obtain_item_name(all_item_names)
    priority_level = obtain_priority_level()
    converted_due_date = obtain_due_date()
    new_item = ListItem(item_name, priority_level, converted_due_date)
    list_content.append(new_item)
    rprint(f"[#00bbf9]The item '{item_name}' has been successfully added to the '{list_name}' list.[/#00bbf9]")
    return list_content

def add_new_item(list_name, list_content, all_item_names):
    item_name = get_new_item_name(all_item_names)
    priority_level = get_new_priority_level()
    converted_due_date = get_new_due_date()
    new_item = ListItem(item_name, priority_level, converted_due_date)
    list_content.append(new_item)
    rprint(f"[#00bbf9]The item '{item_name}' has been successfully added to the '{list_name}' list.[/#00bbf9]")

def empty_list_collection_check(list_collection):
    if len(list_collection) == 0:
        raise EmptyListCollection

def empty_list_check(list_name, list_collection):
    if len(list_collection[list_name]) == 0:
        raise EmptyList

def main_menu_selection():
    options = ['[1] Create a new list', '[2] Edit an existing list', '[3] Delete an existing list', '[4] View an existing list', '[x] Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    if menu_entry_index == 4:
        raise KeyboardInterrupt
    return options[menu_entry_index]

def yes_no_decision():
    options = ['[y] Yes', '[n] No (Back to Main menu)', '[x] Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    exit_main_quit(options, menu_entry_index)

def list_selection():
    list_name_options = []
    lists = list_names()
    for index, name in enumerate(lists, start = 1):
        list_name_options.append(f'[{index}] {name}')
    options = [*list_name_options, '[m] Back to Main menu', '[x] Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    exit_main_quit(options, menu_entry_index)
    return lists[menu_entry_index]

def item_selection(all_item_names):
    item_name_options = []
    for index, name in enumerate(all_item_names, start = 1):
        item_name_options.append(f'[{index}] {name}')
    options = [*item_name_options, '[q] Choose another edit method', '[l] Choose another list', '[m] Back to Main menu', '[x] Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    exit_main_list_method_quit(options, menu_entry_index)
    return menu_entry_index

def how_to_edit_selection():
    options = ['[1] Add a new item', '[2] Modify an existing item', '[3] Remove an existing item', '[l] Choose another list', '[m] Back to Main menu', '[x] Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    exit_main_list_quit(options, menu_entry_index)
    return options[menu_entry_index]

def element_selection():
    options = ['[1] Name', '[2] Priority', '[3] Due date', '[i] Modify another item', '[l] Edit another list', '[m] Back to Main menu', '[x] Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    exit_main_list_quit(options, menu_entry_index)
    if menu_entry_index == 3:
        raise BackToChooseItem
    return options[menu_entry_index]

def continue_selection(list_name, item_name):
    options = [f'[y] Continue to modify the \'{item_name}\' item', '[q] Choose another edit method', '[l] Edit another list', '[m] Back to Main menu', '[x] Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    exit_main_list_method_quit(options, menu_entry_index)

def continue_but_change_selection(list_name):
    options = ['[y] Yes', '[q] Choose another edit method', '[l] Edit another list', '[m] Back to Main menu', '[x] Exit the app']
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    exit_main_list_method_quit(options, menu_entry_index)

def exit_main_quit(options, menu_entry_index):
    if menu_entry_index == len(options) - 1:
        raise KeyboardInterrupt
    elif menu_entry_index == len(options) - 2:
        raise BackToMain

def exit_main_list_quit(options, menu_entry_index):
    if menu_entry_index == len(options) - 3:
        raise BackToChooseList
    exit_main_quit(options, menu_entry_index)

def exit_main_list_method_quit(options, menu_entry_index):
    if menu_entry_index == len(options) - 4:
        raise BackToChooseEditMethod
    exit_main_list_quit(options, menu_entry_index)

def remove_item(list_name, list_collection):
    rprint(f'[italic #00f5d4]Select which item to be removed from the \'{list_name}\' list:[/italic #00f5d4]')
    item_name_list = item_names(list_collection[list_name])
    selected_item_index = item_selection(item_name_list)
    deleted_item_name = item_name_list[selected_item_index]
    del list_collection[list_name][selected_item_index]
    rprint(f'[#00bbf9]Item \'{deleted_item_name}\' has been removed from the \'{list_name}\' list![#00bbf9]')
    return list_collection

def delete_list():
    rprint('[italic #00f5d4]Select which list you would like to delete:[/italic #00f5d4]')
    selected_list_name = list_selection()
    del list_collection[selected_list_name]
    rprint(f'[#00bbf9]List \'{selected_list_name}\' has been deleted![/#00bbf9]')

def view_list():
    rprint('[italic #00f5d4]Select which list you would like to view:[/italic #00f5d4]')
    selected_list_name = list_selection()

    display_list = Table(title = f'\n{selected_list_name.upper()}', title_style = '#f15bb5', min_width = 50, header_style = 'italic bold', box = box.HORIZONTALS, row_styles = [style.Style(bgcolor = '#aaaaaa'), ''])

    display_list.add_column('Item No.\n', style = 'white', justify = 'center', min_width = 8, no_wrap = True)
    display_list.add_column('Item Name\n', style = 'cyan', overflow = "ellipsis", no_wrap = True, min_width = 20, max_width = 40)
    display_list.add_column('Priority Level\n(Low - Medium - High)', style = 'magenta', justify = 'center', no_wrap = True, min_width = 21)
    display_list.add_column('Due Date\n', style = 'green', min_width = 8, no_wrap = True)

    long_bar = Bar(size = 1, begin = 0.67, end = 1, width = 21, color = 'red', bgcolor = None)
    medium_bar = Bar(size = 1, begin = 0.33, end = 0.67, width = 21, color = 'yellow', bgcolor = None)
    short_bar = Bar(size = 1, begin = 0, end = 0.33, width = 21, color = 'green', bgcolor = None)

    sorted_list_content = sort_items(list_content = list_collection[selected_list_name])

    for index, item in enumerate(sorted_list_content, start = 1):
        str_due_date = Text(datetime.strftime(item.due_date, '%d/%m/%y'))
        priority_level = item.priority
        if item.due_date < date.today():
            str_due_date.stylize('red')
        if item.priority == '1':
            priority_level = short_bar
        elif item.priority == '2':
            priority_level = medium_bar
        else:
            priority_level = long_bar
        display_list.add_row(str(index), item.name.capitalize(), priority_level, str_due_date)

    console = Console()
    rprint(f'[#fee440]You are viewing the \'{selected_list_name}\' list![/#fee440]')
    console.print(display_list)

def list_name_duplicate_check(input, all_list_names):
    if input.lower() in all_list_names:
        rprint(f'[red]The list exists already. Enter another name.[/red]')
        return False
    else:
        return input.lower()

def item_names(list_content):
    return [item.name for item in list_content]

def list_names():
    return list(list_collection.keys())

def obtain_list_name(all_list_names, running_time_for_test = -1):
    valid_list_name = None
    while not valid_list_name:
        if running_time_for_test == 0:
            return False
        else:
            user_input = Prompt.ask('Enter the name of the new list (x to exit the app or m to back to Main Menu)')
            if len(user_input) == 0:
                rprint('[red]Empty input![/red]')
            else:
                exit_main_check(user_input)
                valid_list_name = list_name_duplicate_check(user_input, all_list_names)
        running_time_for_test -= 1
    return valid_list_name

if __name__ == '__main__':
    try:
        list_collection = {}
        while True:
            # select what to do
            rprint('[italic #00f5d4]What would you like to do?[/italic #00f5d4]')
            selected_main_menu = main_menu_selection()
            try:
                # create a new list
                if selected_main_menu == '[1] Create a new list':
                    all_items = []
                    new_list_name = obtain_list_name(all_list_names = list_names())
                    add_item(new_list_name, all_items, item_names(all_items))
                    update_collection(new_list_name, all_items, list_collection)
                    while True:
                        rprint('[italic #00f5d4]Would you like to add another item?[/italic #00f5d4]')
                        yes_no_decision()
                        add_item(list_name = new_list_name, list_content = all_items, all_item_names = item_names(all_items))
                        update_collection(new_list_name, all_items, list_collection)
                else:
                    empty_list_collection_check(list_collection)
                    # edit an existing list
                    if selected_main_menu == '[2] Edit an existing list':
                        while True:
                            # select a list for edit from the list collection
                            rprint('[italic #00f5d4]Select which list you would like to edit:[/italic #00f5d4]')
                            selected_list_name = list_selection()
                            try:
                                empty_list_check(selected_list_name, list_collection)
                                all_items = list_collection[selected_list_name]
                                while True:
                                    # select an edit method for the list selected above
                                    rprint(f'[italic #00f5d4]How would you like to edit the \'{selected_list_name}\' list?[/italic #00f5d4]')
                                    selected_edit_method = how_to_edit_selection()
                                    try:
                                        is_empty_list = False
                                        while not is_empty_list:
                                            # add a new item to the list
                                            if selected_edit_method == '[1] Add a new item':
                                                add_new_item(selected_list_name, all_items, item_names(all_items))
                                                update_collection(selected_list_name, all_items, list_collection)
                                                while True:
                                                    rprint('[italic #00f5d4]Would you like to add another item?[/italic #00f5d4]')
                                                    continue_but_change_selection(selected_list_name)
                                                    add_new_item(selected_list_name, all_items, item_names(all_items))
                                                    update_collection(selected_list_name, all_items, list_collection)
                                            else:
                                                if len(list_collection[selected_list_name]) == 0:
                                                    rprint(f'[red]The \'{selected_list_name}\' list is empty! Add a new item first![/red]')
                                                    is_empty_list = True
                                                # modify an existing item in the list
                                                elif selected_edit_method == '[2] Modify an existing item':
                                                    while True:
                                                        # selecte an item for mofication
                                                        rprint('[italic #00f5d4]Select an item to modify:[/italic #00f5d4]')
                                                        selected_item = list_collection[selected_list_name][item_selection(item_names(all_items))]
                                                        try:
                                                            while True:
                                                                # select an element for modification from the selected item above
                                                                rprint(f"[italic #00f5d4]Which element of the '{selected_item.name}' item would you like to edit?[/italic #00f5d4]")
                                                                rprint(f"[#fee440]Its current status: Name is {selected_item.name}, Priority level is {selected_item.priority}, Due date is {selected_item.due_date}.[/#fee440]")
                                                                selected_element = element_selection()
                                                                try:
                                                                    match selected_element:
                                                                        # change item's name
                                                                        case '[1] Name':
                                                                            rprint(f"[#fee440]The current name is {selected_item.name}.[/#fee440]")
                                                                            new_name = update_item_name(item_names(all_items))
                                                                            selected_item.name = new_name
                                                                            rprint(f"[#00bbf9]The item name has been successfully amended to {selected_item.name}.[/#00bbf9]")
                                                                        # change item's priority level
                                                                        case '[2] Priority':
                                                                            rprint('[italic #00f5d4]Select a new priority level:[/italic #00f5d4]')
                                                                            rprint(f"[#fee440]The current priority level is {selected_item.priority}.[/#fee440]")
                                                                            new_priority = update_priority_level()
                                                                            selected_item.priority = new_priority
                                                                            rprint(f"[#00bbf9]The priority level has been successfully amended to {selected_item.priority}.[/#00bbf9]")
                                                                            update_collection(selected_list_name, all_items, list_collection)
                                                                        # change item's due date
                                                                        case '[3] Due date':
                                                                            rprint(f"[#fee440]The current due date is {selected_item.due_date}.[/#fee440]")
                                                                            new_due_date = update_due_date()
                                                                            selected_item.due_date = new_due_date
                                                                            rprint(f"[#00bbf9]The due date has been successfully amended to {selected_item.due_date}.[/#00bbf9]")
                                                                            update_collection(selected_list_name, all_items, list_collection)
                                                                    # check if the user would like to continue modifying the same item or to choose another one for modification
                                                                    continue_selection(selected_list_name, selected_item.name)
                                                                # go back to choose another element of the item to modify
                                                                except BackToChooseElement as err:
                                                                    rprint (f'[#fee440]{err}[/#fee440]')
                                                        # go back to choose another item to modify
                                                        except BackToChooseItem as err:
                                                            rprint (f'[#fee440]{err}[/#fee440]')
                                                # remove an existing item from the list
                                                elif selected_edit_method == '[3] Remove an existing item':
                                                    remove_item(selected_list_name, list_collection)
                                                    while len(list_collection[selected_list_name]) != 0:
                                                        rprint('[italic #00f5d4]Would you like to remove another item?[/italic #00f5d4]')
                                                        continue_but_change_selection(selected_list_name)
                                                        remove_item(selected_list_name, list_collection)
                                                    rprint(f'[#fee440]The {selected_list_name} list is now empty![/#fee440]')
                                                    is_empty_list = True
                                    # go back to choose another edit method for the list
                                    except BackToChooseEditMethod as err:
                                        rprint (f'[#fee440]{err}[/#fee440]')
                            # go back to choose another list to edit
                            except BackToChooseList as err:
                                rprint (f'[#fee440]{err}[/#fee440]')
                            except EmptyList as err:
                                rprint (f'[#fee440]{err}[/#fee440]')
                    # delete an existing list
                    elif selected_main_menu == '[3] Delete an existing list':
                        delete_list()
                        while len(list_collection) != 0:
                            rprint('[italic #00f5d4]Would you like to delete another list?[/italic #00f5d4]')
                            yes_no_decision()
                            delete_list()
                        rprint('[red]The list collection is now empty![/red]')
                    # view an existing list
                    elif selected_main_menu == '[4] View an existing list':
                        view_list()
            # back to main menu
            except BackToMain as err:
                rprint (f'[#fee440]{err}[/#fee440]')
            # if the list collection is empty, back to main menu to create one
            except EmptyListCollection as err:
                rprint (f'[red]{err}[/red]')
    # exit the app
    except KeyboardInterrupt:
        # save user's inputs in an excel file and export the file
        data = pandas.DataFrame.from_dict({(list_name, i): list_collection[list_name][i].__dict__
                                        for list_name in list_collection.keys()
                                        for i in range(len(list_collection[list_name]))},
                                    orient = 'index',)
        if not data.empty:
            save_or_not = Prompt.ask('Would you like to save and export your list collection?', choices = ['y', 'n'])
            if save_or_not == 'y':
                file_name = None
                while not file_name:
                    file_name = Prompt.ask('Please enter the name of your list collection')
                data.to_excel(f'{file_name}.xlsx')
        rprint('[#9b5de5]You have existed the app![/#9b5de5]')
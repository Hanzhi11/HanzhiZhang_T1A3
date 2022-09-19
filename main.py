from datetime import date, timedelta, datetime

import re

list_collection = {}
items = []


class ItemContent:
    def __init__(self, name, priority, due_date):
        self.name = name
        self.priority = priority
        self.due_date = due_date

    def __repr__(self):
        return f'Item name: {self.name}, Priority: {self.priority}, Due on: {self.due_date}'

class DateError(Exception):
    def __init__(self):
        super().__init__('Invalid date!')
class PriorityError(Exception):
    def __init__(self):
        super().__init__('Wrong priority level!')

class InvalidInputError(Exception):
    def __init__(self):
        super().__init__('Invalid input (element missing)')
        

def quit_app(input):
    if input == 'X':
        print('exit')
        raise KeyboardInterrupt
    else:
        return input

def quit_check_main(input):
    if input == 'Q':
        print ('Back to the main options')
        return 'back to main'
    else:
        return quit_app(input)

def quit_check_sub(input):
    if input == 'q':
        print('Back to the sub options')
        return 'back to sub'
    else:
        return quit_check_main(input)

def add_item(list_name, item):
    item_content = item.split(',')
    item_name = item_content[0].lower()
    item_priority_level = item_content[1].lower()
    item_due_date = item_content[2]
    convert_due_date = datetime.strptime(item_content[2], '%d/%m/%y').date()
    default_due_date= date.today() + timedelta(days = 1)
    if len(item_priority_level) == 0 and len(item_content[2]) != 0:
        item_content_details = ItemContent(item_name, 'medium', convert_due_date)
    elif len(item_priority_level) == 0 and len(item_content[2]) == 0:
        item_content_details = ItemContent(item_name, 'medium', default_due_date)
    else:
        item_content_details = ItemContent(item_name, item_priority_level, item_due_date)
    items.append(item_content_details)
    items_list = dict(enumerate(items))
    print (item_content_details)
    new_list = {list_name: items_list}
    print(new_list)
    return 'added'


def input_check(item):
    item_content = item.split(',')
    try:
        if item.count(',') == 2 and len(item_content[0]) != 0:
            if len(item_content[1]) != 0 and item_content[1] not in ['high', 'medium', 'low']:
                raise PriorityError
            elif len(item_content[2]) != 0 and not re.match('^[0-9]{2}/[0-9]{2}/[0-9]{2}', item_content[2]):
                raise DateError
            else:
                return item
        else:
            raise InvalidInputError
    except PriorityError:
        return 'invalid priortity level'
    except DateError:
        return 'invalid date'
    except InvalidInputError:
        return 'invalid input'

        # try:
        #     if len(item_content[2]) == 0:
        #         return item
        #     else:
        #         datetime.strptime(item_content[2], '%d/%m/%y').date()
        #         return item
        # except DateError('Invalid date!'):
        #     return 'invalid date'
    # else:
    #     print('Invalid input!')
    #     return 'invalid input (element missing)'

try:
    what_to_do = 0

    while what_to_do != 'X':
        what_to_do = input('What would you like to do? (new, edit, view or delete. X to exit the app) ')
        check_result = quit_app(what_to_do)
        if check_result == 'new':
            list_name = input('Enter the name of the new list (X to exit the app or Q to back): ')
            check_result = quit_check_main(list_name)
            print(check_result)
            if check_result == list_name:
                input_is_valid = False    
                while not input_is_valid:
                    item = input('Enter the item\'s name, priority and due date DD/MM/YY (X to exit the app or Q to back): ')
                    check_result = quit_check_main(item)
                    if check_result == 'back to main':
                        break
                    else:
                        if input_check(item) not in ['invalid input', 'invalid date', 'invalid priority level']:
                            add_item(list_name, item)
                            input_is_valid = True
                        else:
                            continue
                else:
                    while check_result not in ['back to main', 'back to sub']:
                        check_if_add_more = input('Add more? (X to exit the app, Q to quit, Y for Yes) ')
                        check_result = quit_check_main(check_if_add_more)
                        if check_result == 'back to sub':
                            break
                        elif check_result == 'back to main':
                            break
                        elif check_result == 'Y':
                            input_is_valid = False
                            while not input_is_valid:
                                item = input('Enter the item\'s name, priority and due date DD/MM/YY (X to exit the app or Q to back): ')
                                check_result = quit_check_main(item)
                                if check_result == 'back to main':
                                    break
                                else:
                                    if input_check(item) not in ['invalid input', 'invalid date', 'invalid priority level']:
                                        add_item(list_name, item)
                                        input_is_valid = True
                                    else:
                                        continue
                        else:
                            print('Invalid input!')
        elif check_result == 'edit':
            print('to edit')
        elif check_result == 'delete':
            print('to delete')
        elif check_result == 'view':
            print('to view')
        else:
            print('Invalid input!')


            









except KeyboardInterrupt:
    print('You have existed the app!')







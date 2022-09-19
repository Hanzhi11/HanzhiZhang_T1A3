from datetime import date, timedelta, datetime

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
        super().__init__('Back to main options!')
        

def quit_app(input):
    if input == 'X':
        raise KeyboardInterrupt

def quit_check_main(input):
    if input == 'Q':
        raise BackToMain
    else:
        quit_app(input)

# def quit_check_sub(input):
#     if input == 'q':
#         print('Back to the sub options')
#         return 'back to sub'
#     else:
#         return quit_check_main(input)

def add_item(list_name, item):
    item_content = item.split(',')
    item_name = item_content[0].lower()
    item_priority_level = item_content[1].lower()
    item_due_date = item_content[2]
    default_due_date= (date.today() + timedelta(days = 1)).strftime('%d/%m/%y')

    if len(item_priority_level) == 0 and len(item_content[2]) != 0:
        convert_due_date = datetime.strptime(item_content[2], '%d/%m/%y').date()
        item_content_details = ItemContent(item_name, '2', convert_due_date)
    elif len(item_priority_level) == 0 and len(item_content[2]) == 0:
        item_content_details = ItemContent(item_name, '2', default_due_date)
    elif len(item_priority_level) != 0 and len(item_content[2]) == 0:
        item_content_details = ItemContent(item_name, item_priority_level, default_due_date)
    else:
        item_content_details = ItemContent(item_name, item_priority_level, item_due_date)

    item_details = {'Name': item_content_details.name, 'Priority': item_content_details.priority, 'Due date':item_content_details.due_date}
    print(item_details)

    items.append(item_details)
    # items_list = dict(enumerate(items))
    sorted_item_list = sorted(items, key = lambda item: (item['Priority'], item['Due date']), reverse = True )
    print(sorted_item_list)
    new_list = {list_name: sorted_item_list}
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
        item = input('Enter the item\'s name, priority and due date DD/MM/YY (X to exit the app or Q to back): ')
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


try:
    while True:
        what_to_do = input('What would you like to do? (new, edit, view or delete. X to exit the app) ')
        items = []
        quit_app(what_to_do)
        try:
            if what_to_do == 'new':
                list_name = input('Enter the name of the new list (X to exit the app or Q to back): ')
                quit_check_main(list_name)
                validate_and_add(list_name)
                while True:
                    check_if_add_more = input('Add more? (X to exit the app, Q to quit, Y for Yes) ')
                    quit_check_main(check_if_add_more)
                    if check_if_add_more == 'Y':
                        validate_and_add(list_name)
                    else:
                        print('Invalid input!')
            elif what_to_do == 'edit':
                print('to edit')
            elif what_to_do == 'delete':
                print('to delete')
            elif what_to_do == 'view':
                print('to view')
            else:
                print('Invalid input!')
        except BackToMain as err:
            print(err)
except KeyboardInterrupt:
    print('You have existed the app!')
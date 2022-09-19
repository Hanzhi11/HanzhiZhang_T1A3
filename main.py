
def quit_app(input):
    if input == 'X':
        print('exit')
        raise KeyboardInterrupt
    return input

def quit_check_main(input):
    quit_app(input)
    if input == 'Q':
        print ('Back to the main options')
        return'back to main'
    return input


def quit_check_sub(input):
    quit_check_main(input)
    if input == 'q':
        print('Back to the sub options')
        return 'back to sub'
    return input

def add_item():
    item_content = input('Enter the item\'s name, priority and due date (X to exit the app or Q to back): ').split(',')
    quit_app(input)
    if input != 'Q':
        item_content = {'Name': item_content[0], 'Priority': item_content[1], 'Due date': item_content[2]}
        items.append(item_content)
        items_list = dict(enumerate(items))
        print (item_content)
        new_list = {list_name: items_list}
        print(new_list)

list_collection = {}
items = []

try:
    what_to_do = 0

    while what_to_do not in ['X', 'new', 'edit', 'view', 'delete']:
        what_to_do = input('What would you like to do? (new, edit, view or delete. X to exit the app) ')
        check_result = quit_app(what_to_do)

    if check_result == 'new':
        list_name = input('Enter the name of the new list (X to exit the app or Q to back): ')
        check_result = quit_check_main(list_name)
        if list_name == check_result:    
            add_item()

        check_if_add_more = 0
        while check_if_add_more not in ['X', 'Q', 'q', 'Y']:
            check_if_add_more = input('Add more? (X to exit the app, Q or q to quit, Y for Yes) ')
            check_result = quit_check_sub(check_if_add_more)
        
        if check_if_add_more == check_result:
            add_item()









except KeyboardInterrupt:
    print('You have existed the app!')







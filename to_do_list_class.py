class ListItem:
    def __init__(self, name, priority, due_date):
        self.name = name
        self.priority = priority
        self.due_date = due_date

    def __repr__(self):
        return f'Item name: {self.name}, Priority: {self.priority}, Due on: {self.due_date}'

class BackToMain(Exception):
    def __init__(self):
        super().__init__('Back to Main menu!')

class BackToChooseEditMethod(Exception):
    def __init__(self):
        super().__init__('Choose another edit method!')

class BackToChooseElement(Exception):
    def __init__(self):
        super().__init__('Choose another element!')

class BackToChooseList(Exception):
    def __init__(self):
        super().__init__('Choose another list!')

class BackToChooseItem(Exception):
    def __init__(self):
        super().__init__('Choose another item!')

class EmptyListCollection(Exception):
    def __init__(self):
        super().__init__('The list collection is empty. Please create one first.')
        
class ListNotExist(Exception):
    def __init__(self, list_name):
        super().__init__(f'The list \'{list_name}\' does not exist! Try another one!')

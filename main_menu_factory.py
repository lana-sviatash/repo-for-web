from abc import ABC, abstractmethod
# from addressbook import create_addressbook
# from notes import create_notes
# from sort import create_sorter
from sort import sorter_starter
from addressbook import addressbook_starter
from notes import notes_main as notes_starter


class ApplicationModuleFactory(ABC):
    @abstractmethod
    def create_module(self):
        pass


class AddressBookFactory(ApplicationModuleFactory):
    def create_module(self):
        # return create_addressbook()
        return addressbook_starter()


class NotesFactory(ApplicationModuleFactory):
    def create_module(self):
        # return create_notes()
        return notes_starter()


class SorterFactory(ApplicationModuleFactory):
    def create_module(self):
        # return create_sorter()
        return sorter_starter()


class Exit(ApplicationModuleFactory):
    def create_module(self):
        return


def menu():
    factories = {
        '1': AddressBookFactory(),
        '2': NotesFactory(),
        '3': SorterFactory(),
        '0': Exit()
    }
    logo_menu = [
        '1  - AddressBook📒',
        '2  - NoteBook📋',
        '3  - Files sorter📂',
        '0  - Exit❌']
    print("_"*34)
    print("| {:<3} {:^27}|".format("☰", "Welcome to main menu"))
    print('|'+'_'*32 + '|')
    for el in logo_menu:
        print('|{:<31}|'.format(el))
        print('|'+'_'*32 + '|')
    print('|{:<32}|'.format('Type number to start:  '))

    while True:
        # ... existing menu code ...

        user_input = input("|>>> ")

        if user_input in factories:
            factory = factories[user_input]
            module = factory.create_module()
            print("_" * 34)
            print("|{:^30}|".format(f"✨ {module.name} Started! ✨"))
            print("|" + "_" * 32 + "|")
            module.start()

        else:
            print('\nGoodbye!\n')
            break

            # You can also print the result of the module if it returns one.
            # result = module.start()
            # print(result)

        # ... existing code ...
if __name__ == '__main__':
    menu()

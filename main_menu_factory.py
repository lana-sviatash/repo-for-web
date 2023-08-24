from abc import ABC, abstractmethod
from sort import sorter_starter
from addressbook import addressbook_starter
from notes import notes_main as notes_starter


class ApplicationModuleFactory(ABC):
    @abstractmethod
    def create_module(self):
        pass


class AddressBookFactory(ApplicationModuleFactory):
    def create_module(self):
        return addressbook_starter()


class NotesFactory(ApplicationModuleFactory):
    def create_module(self):
        return notes_starter()


class SorterFactory(ApplicationModuleFactory):
    def create_module(self):
        return sorter_starter()


def menu():
    factories = {
        '1': AddressBookFactory(),
        '2': NotesFactory(),
        '3': SorterFactory(),
    }
    logo_menu = [
        '1  - AddressBook📒',
        '2  - NoteBook📋',
        '3  - Files sorter📂',
        '0  - Exit❌'
    ]

    while True:
        print("_"*34)
        print("| {:<3} {:^27}|".format("☰", "Welcome to main menu"))
        print('|'+'_'*32 + '|')
        for el in logo_menu:
            print('|{:<31}|'.format(el))
        print('|'+'_'*32 + '|')
        print('|{:<32}|'.format('Type number to start:  '))
        user_input = input("|>>> ")
        print('|'+'_'*32 + '|')

        if user_input == '0' or user_input.lower() == "exit":
            print('\nGoodbye!\n')
            break
        if user_input in factories:
            factory = factories[user_input]
            factory.create_module()
            print("_" * 34)
            print("|{:^30}|".format(f"✨ Main Menu Started! ✨"))
            print("|" + "_" * 32 + "|")
        
        else:
            print("_"*34)
            print("|{:^32}|".format("Wrong number... Try again..."))
            print("|"+"_"*32 + "|")


if __name__ == '__main__':
    menu()

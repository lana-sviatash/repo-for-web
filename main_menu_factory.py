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
        #return create_addressbook()
        return addressbook_starter()


class NotesFactory(ApplicationModuleFactory):
    def create_module(self):
        #return create_notes()
        return notes_starter()

class SorterFactory(ApplicationModuleFactory):
    def create_module(self):
        #return create_sorter()
        return sorter_starter()

class MainMenu(ApplicationModuleFactory):
    def create_module(self):
        return menu()
def menu():
    factories = {
        '1': AddressBookFactory(),
        '2': NotesFactory(),
        '3': SorterFactory(),
        '0': MainMenu()
    }

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

            # You can also print the result of the module if it returns one.
            # result = module.start()
            # print(result)

        # ... existing code ...


if __name__ == '__main__':
    menu()

import difflib
import functools
from rich.console import Console
from rich.table import Table
from address_book_classes import Record, Name, Phone, Birthday, Email, Address, Note, AddressBook
from datetime import date, timedelta, datetime

address_book = AddressBook()
filename = 'address_book'


def input_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError, TypeError) as e:
            if "takes" in str(e) and "but" in str(e):
                error_message = "Too many arguments provided"
                return error_message
            else:
                return "Wrong input"

    return wrapper


@input_errors
def add(*args):
    name = Name(input("Name: ")).value.strip()
    for el in address_book.keys():
        if name == el:
            return "This name already exist, use different name!"
    else:
        phones = Phone().value
        birthday = Birthday().value
        email = Email().value.strip()
        address = Address(input("Address: ")).value
        note = Note(input("Note: ")).value
        record = Record(name=name, phone=phones, birthday=birthday,
                        email=email, address=address, note=note)
    return address_book.add_record(record)


@input_errors
def edit_contacts(*args):
    name = input('Contact name: ')
    if name not in address_book.keys():
        return "\nThis name not exist! Use 'show all' to show contacts...\n"
    else:
        parameter = input('Which parameter to edit(phones, birthday, email, address, note): ').strip()
        try:
            if parameter not in ("phones", "birthday", "email", "address", "note"):
                raise ValueError
            else:
                new_value = input("New Value: ")
                res: Record = address_book.get(str(name))

            try:
                if res:
                    if parameter == 'birthday':
                        new_value = Birthday(new_value).value
                    elif parameter == 'email':
                        parameter = 'emails'
                        new_contact = new_value.split(' ')
                        new_value = []
                        for emails in new_contact:
                            new_value.append(Email(emails).value)
                    elif parameter == 'address':
                        new_value = Address(new_value).value
                    elif parameter == 'note':
                        new_value = Note(new_value).value
                    elif parameter == 'phones':
                        new_contact = new_value.split(' ')
                        new_value = []
                        for number in new_contact:
                            new_value.extend(Phone(number).value)
                    if parameter in res.__dict__.keys():
                        res.__dict__[parameter] = new_value
                res: Record = address_book.get(str(name))
                return res
            except ValueError:
                print('Incorrect parameter! Please provide correct parameter')
            except NameError:
                print('There is no such contact in address book!')
        except ValueError:
            return "Wrong parameter!"


@input_errors
def delete_record(*args):
    name = Name(input("Name: ")).value.strip()
    if name in address_book:
        del address_book[name]
        return f"Contact '{name}' has been deleted from the address book."
    return f"No contact '{name}' found in the address book."


@input_errors
def remove_phone(*args):
    name = Name(input("Name: ")).value.strip()
    phone = Phone(input("Phone: "))
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.remove_phone(phone.values)
    return f"No contact {name} in address book"


@input_errors
def search(*args) -> str:
    text = input("Text for searching: ")
    return address_book.search(text)


def show_all_address_book():
    if Record.__name__:
        return address_book.show_all_address_book()


@input_errors
def get_days_to_birthday(*args):
    name = Name(input("Name: ")).value.strip()
    if name in address_book:
        res: Record = address_book.get(str(name))
        result = int(res.days_to_birthday(res.birthday)) + 1
        if result == 0:
            return f'{name} tomorrow birthday'
        if result == 365:
            return f'{name} today is birthday'
        return f'{name} until the next birthday left {result} days'
    else:
        return f'Contact with name "{name}" does not exist'


def who_has_bd_n_days():
    days = input(str('How many days?\n>>> '))
    try:
        n_days = int(days) + 1
    except (TypeError, ValueError):
        return 'This is not a number. Give me a number of days.'
    result = []
    result_dict = AddressBook()
    current_year = datetime.now().year

    for account in address_book.data.values():
        if account.birthday:
            new_birthday = account.birthday.replace(year=current_year)
            next_date = (datetime.now() + timedelta(days=n_days)).date()
            if date.today() <= new_birthday < next_date:
                result.append(account)
    if result:
        for item in result:
            result_dict[item.name] = item

        return result_dict.show_all_address_book()
    else:
        return f"\nNobody has birthday in {days} days\n"


def exit_book():
    pass


def help():
    pass


command_dict = {
    'add': [add, 'to add contact'],
    'show all': [show_all_address_book, 'to show all contacts'],
    'save': [address_book.save, 'to save address book'],
    'csv save': [address_book.serialize_to_csv, 'to save address book .csv'],
    'json save': [address_book.serialize_to_json, 'to save address book .json'],
    'bday': [get_days_to_birthday, 'to get day to birthday'],
    'b-in': [who_has_bd_n_days, 'to show birthday during next N days'],
    'remove': [remove_phone, 'to remove phone from contact'],
    'edit': [edit_contacts, 'to edit existing contact'],
    'delete': [delete_record, 'to delete existing contact'],
    'search': [search, 'search contact by any match'],
    'help': [help, 'to see list of commands'],
    "0 or exit": [exit_book, 'to exit']
}


@input_errors
def command_handler(user_input, command_dict):
    if user_input in command_dict:
        return command_dict[user_input][0]
    possible_command = difflib.get_close_matches(
        user_input.split()[0], command_dict, cutoff=0.55)
    if possible_command:
        return f'Wrong command. Maybe you mean: {", ".join(possible_command)}'
    else:
        return 'Wrong command.'


def instruction(command_dict):
    console = Console()
    table = Table(show_header=True, header_style="bold magenta",
                  width=60, show_lines=False)
    table.add_column("Command", max_width=None, no_wrap=False)
    table.add_column("Description", width=20, no_wrap=False)

    for func_name, func in command_dict.items():
        table.add_row(str(func_name), str(func[1]))

    console.print(table)


def parser_input(user_input: str, command_dict):
    command = None
    arguments = ''

    for key in command_dict.keys():
        if user_input.startswith(key):
            command = key
            arguments = user_input.replace(key, '').strip().split()
            break
    return command, arguments


def addressbook_starter():
    filename = "address_book.bin"
    try:
        address_book.load(filename)
        print("Address book loaded from file.")
    except FileNotFoundError:
        print("New address book created.")

    print("\n ***Hello I`m a contact book.***\n")
    print("_" * 59)
    print(address_book.congratulate())
    instruction(command_dict)

    while True:
        user_input = input('Input a command\n>>>').lower()
        if user_input == 'help':
            instruction(command_dict)
        elif user_input in ("exit", "0"):
            print('Contact book closed')
            address_book.save()
            break
        else:
            command, arguments = parser_input(user_input, command_dict)
            if command in command_dict:
                result = command_handler(command, command_dict)(*arguments)
                address_book.save()
            else:
                result = command_handler(user_input, command_dict)
                address_book.save()
            print(result)
    address_book.save()


if __name__ == "__main__":
    addressbook_starter()

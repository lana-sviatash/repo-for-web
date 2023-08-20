from collections import UserDict
from datetime import timedelta, datetime, date
import csv
import json
import pickle
import re
from rich.console import Console
from rich.table import Table
from helpers import OutputAbstract


class Field:

    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return str(self)


class Name(Field):

    def __init__(self, value):
        name = value.split(" ")
        for elem in name:
            if not elem.isalpha():
                print("\nName must contain only alphabetical characters!")
                return ValueError
            self.value = value


class Phone(Field):

    def __init__(self, value=''):
        while True:
            self.value = []
            if value:
                self.values = value
            else:
                self.values = input(
                    'Please enter phone number in format +380998887722 (\'+\' symbol and 12 digits)')
            try:
                for number in self.values.split(' '):
                    if re.match(r'^\+\d{12}$', number) or number == '':
                        self.value.append(number)
                    else:
                        raise ValueError
            except ValueError:
                print(
                    'Incorrect phone number format! Please provide correct phone number format.')
            else:
                break

    def __getitem__(self):
        return self.value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
            self.__value = value
        except ValueError:
            return

    def __str__(self):
        return self.__value


class BirthdayError(Exception):
    ...


class Birthday(Field):

    def __init__(self, value=''):
        while True:
            if value:
                self.value = value
            else:
                self.value = input("Birthday date(dd/mm/YYYY): ")
            try:
                if re.match(r'^\d{2}/\d{2}/\d{4}$', self.value):
                    self.value = datetime.strptime(
                        self.value.strip(), "%d/%m/%Y")
                    self.value = self.value.date()
                    break
                elif self.value == '':
                    break
                else:
                    raise ValueError
            except ValueError:
                print('Incorrect date! Please provide correct date format.')

    def __getitem__(self):
        return self.value.date()


class Email(Field):
    def __init__(self, value=''):
        while True:
            if value:
                self.value = value
            else:
                self.value = input("Email: ")
            try:
                if re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
                        self.value) or self.value == '':
                    break
                else:
                    raise ValueError
            except ValueError:
                print('Incorrect email! Please provide correct email.')

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
            self.__value = value
        except ValueError:
            return

    def __str__(self):
        return self.__value


class Address(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value


class Note(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value


class Record:

    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None, email: Email = None,
                 address: Address = None, note: Note = None) -> None:
        self.name = name
        self.phones = []
        self.birthday = birthday
        self.emails = []
        self.address = address
        self.note = note
        if email:
            if isinstance(email, list):
                self.emails.extend(email)
            else:
                self.emails.append(email)
        if phone:
            if isinstance(phone, list):
                self.phones.extend(phone)
            else:
                self.phones.append(phone)

    def add_birthday(self, birthday: Birthday):
        if not self.birthday:
            self.birthday = birthday
            return f"birthday {self.birthday} add to contact {self.name}"
        return f"{self.birthday} allready present in birthday data of contact {self.name}"

    def add_phone(self, phone: Phone):
        if phone.value.strip() not in [p.value.strip() for p in self.phones]:
            self.phones.append(phone)
            return f"phone {phone} add to contact {self.name}"
        return f"{phone} present in phones of contact {self.name}"

    def add_email(self, email: Email):
        if email.value in [e.value for e in self.emails]:
            return f"{email} present in emails of contact {self.name}"
        self.emails.append(email)
        return f"email {email} add to contact {self.name}"

    def change_phone(self, old_phone, new_phone):
        for idx, p in enumerate(self.phones):
            if old_phone.value == p.value:
                self.phones[idx] = new_phone
                return f"old phone {old_phone} change to {new_phone}"
        return f"{old_phone} not present in phones of contact {self.name}"

    def days_to_birthday(self, birthday: Birthday):
        str_date = str(birthday)
        now = datetime.now()
        then = datetime.strptime(str_date, "%Y-%m-%d")
        delta1 = datetime(now.year, then.month, then.day)
        delta2 = datetime(now.year + 1, then.month, then.day)
        result = ((delta1 if delta1 >= now else delta2) - now).days
        return result

    def get_phones(self, res):
        result = f"{', '.join(str(p) for p in res.phones)}"
        return result

    def __str__(self) -> str:

        console = Console()
        table = Table(show_header=True, header_style="bold magenta",
                      width=120, show_lines=True)
        table.add_column("Name", width=40, no_wrap=False)
        table.add_column("Phones", width=40, no_wrap=False)
        table.add_column("Birthday", width=40, no_wrap=False)
        table.add_column("Emails", width=40, no_wrap=False)
        table.add_column("Address", width=40, no_wrap=False)
        table.add_column("Note", width=40, no_wrap=False)

        name = self.name
        phones = ", ".join(str(phone) for phone in self.phones)
        bday = str(self.birthday) if self.birthday else ""
        emails = ", ".join(str(email) for email in self.emails)
        address = str(self.address) if self.address else ""
        note = str(self.note) if self.note else ""

        table.add_row(name, phones, bday, emails, address, note)

        console.print(table)
        return "\nSuccess!\n"

    def remove_phone(self, phone):
        for idx, p in enumerate(self.phones):
            print(f'p= {self.phones[idx]}')
            if phone == p:
                old_phone = (self.phones[idx])
                self.phones.remove(self.phones[idx])
                return f"The phone {old_phone} is deleted"
        return f"{phone} not present in phones of contact {self.name}"


class AddressBook(UserDict, OutputAbstract):

    def add_record(self, record: Record):
        self.data[str(record.name)] = record
        print(f"\nContact  '{record.name}' successfully added")

        return record

    def __str__(self):
        return "\n".join(str(r) for r in self.data.values())

    def iterator(self, n=3):
        result = []
        counter = 0
        for record in self.data.values():
            result.append(str(record))
            counter += 1
            if counter >= n:
                yield "\n".join(result)
                counter = 0
                result = []
        if result:
            yield "\n".join(result)

    def serialize_to_csv(self):
        filename = 'address_book.csv'
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            for rec in self.data.values():
                name = rec.name
                phones = [phone for phone in rec.phones]
                birthday = rec.birthday.strftime(
                    "%d/%m/%Y") if rec.birthday else ""
                emails = [email for email in rec.emails]
                address = rec.address
                note = rec.note
                writer.writerow(
                    [name, ",".join(phones), birthday, ",".join(emails), address, note])
        return 'Saved data to .csv'

    def serialize_to_json(self):
        filename = 'address_book.json'
        data_list = []
        for record in self.data.values():
            data = {
                "name": record.name,
                "phones": [phone for phone in record.phones],
                "birthday": record.birthday.strftime("%d/%m/%Y") if record.birthday else "",
                "emails": [email for email in record.emails],
                "address": record.address,
                "note": record.note
            }
            data_list.append(data)
        with open(filename, "w") as file:
            json.dump(data_list, file)
        return 'Saved data to .json'

    def save(self):
        with open('address_book.bin', 'wb') as file:
            pickle.dump(self.data, file)
        return 'OK'

    def load(self, file_name):
        with open(file_name, 'rb') as file:
            self.data = pickle.load(file)
        return self.data

    def get_current_week(self):
        now = datetime.now()
        current_weekday = now.weekday()
        if current_weekday < 5:
            week_start = now - timedelta(days=2 + current_weekday)
        else:
            week_start = now - timedelta(days=current_weekday - 5)
        return [week_start.date(), week_start.date() + timedelta(days=7)]

    def get_current_week(self):
        now = datetime.now()
        current_weekday = now.weekday()
        if current_weekday < 5:
            week_start = now - timedelta(days=2 + current_weekday)
        else:
            week_start = now - timedelta(days=current_weekday - 5)
        return [week_start.date(), week_start.date() + timedelta(days=7)]

    def congratulate(self):
        result = []
        WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday',
                    'Thursday', 'Friday', 'Saturday', 'Sunday']
        current_year = datetime.now().year
        congratulate = {'Monday': [], 'Tuesday': [],
                        'Wednesday': [], 'Thursday': [], 'Friday': []}
        
        for account in self.keys():
            if self[account].birthday:
                new_birthday = self[account].birthday.replace(year=current_year)
                birthday_weekday = new_birthday.weekday()
                next_week = (datetime.now() + timedelta(days=7)).date()
                if date.today() < new_birthday < next_week:
                    if birthday_weekday < 5:
                        congratulate[WEEKDAYS[birthday_weekday]].append(self[account].name)
                    else:
                        congratulate["Monday"].append(self[account].name)
        for key, value in congratulate.items():
            if len(value):
                result.append(f"{key}: {', '.join(value)}")
        return '! Do not forget to congratulate !\n' + '_' * 59 + '\n' + '\n'.join(result) + '\n' + '_' * 59

    def format_output(self):
        console = Console()
        table = Table(show_header=True, header_style="bold magenta",
                      width=120, show_lines=True)
        table.add_column("Name", width=40, no_wrap=False)
        table.add_column("Phones", width=40, no_wrap=False)
        table.add_column("Birthday", width=40, no_wrap=False)
        table.add_column("Emails", width=40, no_wrap=False)
        table.add_column("Address", width=40, no_wrap=False)
        table.add_column("Note", width=40, no_wrap=False)

        for record in self.data.values():
            name = record.name
            phones = ", ".join(str(phone) for phone in record.phones)
            bday = str(record.birthday) if record.birthday else ""
            emails = ", ".join(str(email) for email in record.emails)
            address = str(record.address) if record.address else ""
            note = str(record.note) if record.note else ""

            table.add_row(name, phones, bday, emails, address, note)

        console.print(table)
        return "Success!\n"

    def search(self, s: str):
        """Used to search for a specific contact in the address book based on a given search term

        Parameters
        ----------
        s : str
            a string representing the search term
        """

        output = []
        result_dict = AddressBook()
        for key in self.keys():
            rec = self[key]
            phone = '.'.join(phone for phone in rec.phones)

            if rec.birthday == "":
                show_birthday = ""
            else:
                show_birthday = datetime.strftime(rec.birthday, '%d/%m/%Y')

            emails = ".".join(email for email in rec.emails)
            address = rec.address
            note = rec.note

            if s in str(rec.name) or s in phone or s in show_birthday or s in emails or s in address or s in note:
                output.append(rec)
            for item in output:
                result_dict[item.name] = item
        return result_dict.format_output()

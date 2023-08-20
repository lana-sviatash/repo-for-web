from collections import UserDict
import pickle
from rich.console import Console
from rich.table import Table
from helpers import InstructionOutput, parser_input, command_handler, show_output, OutputAbstract


class Tag:

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"{self.value}"

    def __getstate__(self):
        return self.value

    def __setstate__(self, state):
        self.value = state


class Tags:

    def __init__(self):
        self.tags = []

    def __str__(self):
        return ", ".join(str(tag) for tag in self.tags)

    def __repr__(self):
        return f"{self.tags}"

    def __getstate__(self):
        return self.tags

    def __setstate__(self, state):
        self.tags = state

    def __iter__(self):
        return iter(self.tags)


class Note:

    def __init__(self, note_text):
        self.note_text = note_text

    def __str__(self):
        return self.note_text

    def __repr__(self):
        return f"{self.note_text}"

    def __getstate__(self):
        return self.note_text

    def __setstate__(self, state):
        self.note_text = state


class NoteBook(UserDict, OutputAbstract):

    def add_note(self, note, tags):
        self.data[note] = tags

    def save(self, filename='notebook_data.pkl'):
        with open(filename, 'wb') as f:
            pickle.dump(self.data, f)

    def load(self, filename='notebook_data.pkl'):
        try:
            with open(filename, 'rb') as f:
                data = pickle.load(f)
                if not isinstance(data, dict):
                    raise TypeError('Invalid data type')
                self.data = data
        except (FileNotFoundError, TypeError):
            self.data = {}

    def format_output(self):
        n = 1
        console = Console()
        table = Table(show_header=True, header_style="bold magenta", width=60, show_lines=True)
        table.add_column("#", max_width=None)
        table.add_column("Note", width=20, no_wrap=False)
        table.add_column("Tags")

        for key, tags in self.data.items():
            table.add_row(str(n), str(key), ", ".join(str(t) for t in self.data[key]))
            n += 1

        console.print(table)

    def edit_note(self):
        print("\n***Edit func***")
        self.format_output()

        x = input("\nChoose the note you want to edit by number ('0' - to exit delete func):\n>>> ")

        try:
            x = int(x)
            keys = list(self.data.keys())
            if 1 <= x <= len(keys):
                note_to_edit = keys[x - 1]
                new_note = input(f"\nEnter the new content for note '{note_to_edit}': ")
                new_tags = input(
                    f"\nEnter the new tags for note '{note_to_edit}' (comma-separated): ").split(",")

                self.data[new_note] = [tag.strip() for tag in new_tags]
                if note_to_edit != new_note:
                    del self.data[note_to_edit]
                print(f"\nNote '{note_to_edit}' has been updated.")
            elif x == 0:
                return 'Exit "Edit func" success'
            else:
                print("\n***Ooops***\nInvalid input. Please choose a valid number.")
                nb.edit_note()
        except ValueError:
            print("\n***Ooops***\nInvalid input. Please enter a number.")
            nb.edit_note()

    def search_note(self, text):
        found_fields = []
        for key, value in self.items():
            if str(key).find(text) != -1:
                found_fields.append((key, value))

        console = Console()
        table = Table(show_header=True, header_style="bold magenta", width=60, show_lines=True)
        table.add_column("Note", width=20, no_wrap=False)
        table.add_column("Tags")

        for obj in found_fields:
            str_tags = ", ".join(obj[1])
            table.add_row(str(obj[0]), str_tags)

        if found_fields:
            return console.print(table)
        else:
            return console.print("\n***Ooops***\nNo matching found.")

    def search_tag(self, text):
        found_tags = []

        for key, value in self.items():
            tag_lst = ', '.join(str(v) for v in value)
            if text in tag_lst:
                found_tags.append((str(key), tag_lst))

        console = Console()
        table = Table(show_header=True, header_style="bold magenta", width=60, show_lines=True)
        table.add_column("Key", width=20, no_wrap=False)
        table.add_column("Tags")

        for obj in found_tags:
            table.add_row(str(obj[0]), str(obj[1]))

        if found_tags:
            return console.print(table)
        else:
            return console.print("\n***Ooops***\nNo matching found.")


nb = NoteBook()


def add_note():
    user_input_note = input('\n***Add func***\nInput your note ("0" - to exit delete func):\n>>>')
    if user_input_note == "0":
        return 'Exit "Add func" success'
    elif not user_input_note:
        print("\nEmpty note not allowed")
        add_note()
    else:
        user_input_tags = input('\nInput tags for a note (space-separated):\n>>>')
        user_input_tags = user_input_tags.strip().split()
        tags = Tags()
        for user_tag in user_input_tags:
            tag = Tag(user_tag)

            tags.tags.append(tag)
        note = Note(user_input_note)
        nb.add_note(note, tags)
        return "You are good!!!\nNote has been added"


def delete_note():
    # nb.show_notes()
    show_output(nb)

    x = input("\n***Delete func***\nChoose the note you want to delete by number ('0' - to exit delete func):\n>>> ")

    try:
        x = int(x)
        keys = list(nb.data.keys())
        if 1 <= x <= len(keys):
            note_to_delete = keys[x - 1]
            del nb.data[note_to_delete]
            print(f"\nNote '{note_to_delete}' has been deleted.")
        elif x == 0:
            return 'Exit "Delete func" success'
        else:
            print("\n***Ooops***\nInvalid input. Please enter a valid number.")
            delete_note()
    except ValueError:
        print("\n***Ooops***\nInvalid input. Please enter a number.")
        delete_note()


def change_note():
    return nb.edit_note()


def exit_notes():
    pass


def show_notes():
    # return nb.show_notes()
    return show_output(nb)


def search():
    user_choice = input("\n***Search***\nEnter '1' to search in note\nEnter '2' to search in tags\n>>>")
    if user_choice == "1" or user_choice == "2":
        search_key = input("Enter a search keyword\n>>>")
        if user_choice == '1':
            return nb.search_note(search_key)
        elif user_choice == '2':
            return nb.search_tag(search_key)
        else:
            return "Wrong input"
    else:
        print("\n***Ooops***\nWrong input")
        search()


def help_menu():
    pass


NOTE_COMMANDS = {
    "add": [add_note, 'to add note'],
    "delete": [delete_note, 'to delete note'],
    "edit": [change_note, 'to edit note'],
    "search": [search, 'to search note'],
    "show all": [show_notes, 'to output all notes'],
    'help': [help_menu, 'to see list of commands'],
    "0 or exit": [exit_notes, 'to exit']
}

note_instruction_output = InstructionOutput(NOTE_COMMANDS)


def notes_main():
    print("\n\n***Hello I`m a notebook.***\n")
    show_output(note_instruction_output)
    nb.load()
    while True:
        user_input_command = str(input("\nInput a command:\n>>>"))
        command = parser_input(user_input_command.lower(), NOTE_COMMANDS)
        if user_input_command == 'help':
            show_output(note_instruction_output)
        elif user_input_command in ("exit", "0"):
            nb.save()
            print('Notebook closed')
            break
        elif user_input_command == 'show all':
            show_notes()
        else:
            if command in NOTE_COMMANDS:
                result = command_handler(command, NOTE_COMMANDS)
            else:
                result = command_handler(user_input_command, NOTE_COMMANDS)
            nb.save()
            if result:
                print(result)


if __name__ == "__main__":
    notes_main()

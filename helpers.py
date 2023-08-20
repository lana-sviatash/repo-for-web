from abc import ABC, abstractmethod
import difflib
from rich.console import Console
from rich.table import Table


class OutputAbstract(ABC):
    @abstractmethod
    def format_output(self):
        ...


class InstructionOutput(OutputAbstract):
    def __init__(self, dict_command):
        self.dict_command = dict_command
    
    def format_output(self):
        console = Console()
        table = Table(show_header=True, header_style="bold magenta",
                      width=60, show_lines=False)
        table.add_column("Command", max_width=None, no_wrap=False)
        table.add_column("Description", width=20, no_wrap=False)

        for command, (func, description) in self.dict_command.items():
            table.add_row(command, description)

        console.print(table)

# def instruction(dict_command):
#     console = Console()
#     table = Table(show_header=True, header_style="bold magenta",
#                   width=60, show_lines=False)
#     table.add_column("Command", max_width=None, no_wrap=False)
#     table.add_column("Description", width=20, no_wrap=False)

#     for func_name, func in dict_command.items():
#         table.add_row(str(func_name), str(func[1]))

#     console.print(table)


def show_output(output_obj):
    output_obj.format_output()


def parser_input(txt_comm: str, command_dict):
    command = None
    for key in command_dict.keys():
        if txt_comm.startswith(key):
            command = key
    return command


def command_handler(user_input, commands):
    if user_input in commands:
        return commands[user_input][0]()
    possible_command = difflib.get_close_matches(user_input, commands, cutoff=0.5)
    if possible_command:
        return f'Wrong command. Maybe you mean: {", ".join(possible_command)}'
    else:
        return f'Wrong command.'
    
from colorama import Fore, Back, Style
from collections import UserDict
import datetime
from functools import wraps

class Field:
    def __init__(self, value):
        if self.__is_valid(value):
            self.value = value
        else:
            raise ValueError("Invalid value")
        
    def __is_valid(self, value):
        return True

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __is_valid(self, value):
        if len(value) > 0:
            return True
        raise ValueError("Name cannot be empty")

class Phone(Field):
    def __is_valid(self, value):
        if value.isdigit() and len(value) == 10:
            return True
        raise ValueError("Phone number must be 10 digits long")

class Birthday(Field):
    def __init__(self, value):
        if self.__is_valid(value):
            self.value = datetime.datetime.strptime(value, "%d.%m.%Y")
        else:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __is_valid(self, value):
        try:
            datetime.datetime.strptime(value, "%d.%m.%Y")
            return True
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        phones_str = '; '.join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"

    def add_phone(self, phone):
        my_phone = Phone(phone)
        self.phones.append(my_phone)

    def remove_phone(self, phone):
        self.phones = [user_phone for user_phone in self.phones if user_phone.value != phone]

    def edit_phone(self, old_phone, new_phone):
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, phone):
        for user_phone in self.phones:
            if phone == user_phone.value:
                return user_phone
        return None

    def add_birthday(self, birth_day):
        self.birthday = Birthday(birth_day)

    def update_birthday(self, new_birth_day):
        self.add_birthday(new_birth_day)

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self) -> dict:
        birth_dict = {}
        datecurr = datetime.datetime.now()
        current_year = datecurr.year

        for user_name, record in self.data.items():
            if record.birthday is None:
                continue

            birth_datetime = record.birthday.value.replace(year=current_year)

            if birth_datetime < datecurr:
                birth_datetime = birth_datetime.replace(year=current_year + 1)
            date_diff = (birth_datetime - datecurr).days

            if 0 <= date_diff <= 7:
                wd = birth_datetime.weekday()
                if wd >= 5:
                    birth_datetime += datetime.timedelta(days=7 - wd)
                birth_dict[user_name] = birth_datetime.strftime("%d.%m.%Y")

        return birth_dict

def input_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"Error: {str(e)}"
        except TypeError:
            return "Error: Incorrect number of arguments"
        except KeyError:
            return "Error: Contact not found"
        except Exception as e:
            return f"Unexpected error: {str(e)}"
    return wrapper

@input_error
def say_hello():
    return "How can I help you?"

@input_error
def parse_input(cmd_line: str):
    info = cmd_line.strip().split(" ")
    return [info[0].lower()] + info[1:]

@input_error
def add_contact(args, book: AddressBook) -> str:
    name, phone = args
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added"
    else:
        message = "Contact's phone updated"
    record.add_phone(phone)
    return message

@input_error
def change_contact(args, book: AddressBook) -> str:
    name, phone_old, phone_new = args
    record = book.find(name)
    if record is None:
        return "Contact not found"
    if record.find_phone(phone_old) is None:
        return "Old phone number not found"
    record.edit_phone(phone_old, phone_new)
    return "Contact's phone updated"

@input_error
def del_contact(args, book: AddressBook) -> str:
    name = args[0]
    record = book.find(name)
    if record is None:
        return "Contact not found"
    book.delete(name)
    return "Contact deleted"

@input_error
def print_contact(book: AddressBook) -> list:
    items = []
    for name, record in book.data.items():
        s = f'{name} : phones: {", ".join(p.value for p in record.phones)}'
        if record.birthday:
            s += f', birthday: {record.birthday.value.strftime("%d.%m.%Y")}'
        items.append(s)
    return items

@input_error
def get_contact(args, book: AddressBook) -> list:
    name = args[0]
    record = book.find(name)
    if record is None:
        return ["Contact not found"]
    return [p.value for p in record.phones]

@input_error
def add_birthday(args, book: AddressBook) -> str:
    name = args[0]
    record = book.find(name)
    if record is None:
        return "Contact not found"
    record.add_birthday(args[1])
    return "Birthday added"

@input_error
def show_birthday(args, book: AddressBook) -> str:
    name = args[0]
    record = book.find(name)
    if record is None or record.birthday is None:
        return "Birthday not set"
    return record.birthday.value.strftime("%d.%m.%Y")

@input_error
def birthdays(book: AddressBook) -> dict:
    return book.get_upcoming_birthdays()

def curr_date() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d")

def curr_time() -> str:
    return datetime.datetime.now().strftime("%H:%M:%S")

@input_error
def main():
    book = AddressBook()

    CLI_header = '⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄\n'\
                 '⠄⠄⠄⠄⣠⠞⠉⢉⠩⢍⡙⠛⠋⣉⠉⠍⢉⣉⣉⣉⠩⢉⠉⠛⠲⣄⠄⠄⠄⠄\n'\
                 '⠄⠄⠄⡴⠁⠄⠂⡠⠑⠄⠄⠄⠂⠄⠄⠄⠄⠠⠄⠄⠐⠁⢊⠄⠄⠈⢦⠄⠄⠄\n'\
                 '⠄⣠⡾⠁⠄⠄⠄⣴⡪⠽⣿⡓⢦⠄⠄⡀⠄⣠⢖⣻⣿⣒⣦⠄⡀⢀⣈⢦⡀⠄\n'\
                 '⣰⠑⢰⠋⢩⡙⠒⠦⠖⠋⠄⠈⠁⠄⠄⠄⠄⠈⠉⠄⠘⠦⠤⠴⠒⡟⠲⡌⠛⣆\n'\
                 '⢹⡰⡸⠈⢻⣈⠓⡦⢤⣀⡀⢾⠩⠤⠄⠄⠤⠌⡳⠐⣒⣠⣤⠖⢋⡟⠒⡏⡄⡟\n'\
                 '⠄⠙⢆⠄⠄⠻⡙⡿⢦⣄⣹⠙⠒⢲⠦⠴⡖⠒⠚⣏⣁⣤⣾⢚⡝⠁⠄⣨⠞⠄\n'\
                 '⠄⠄⠈⢧⠄⠄⠙⢧⡀⠈⡟⠛⠷⡾⣶⣾⣷⠾⠛⢻⠉⢀⡽⠋⠄⠄⣰⠃⠄⠄\n'\
                 '⠄⠄⠄⠄⠑⢤⡠⢂⠌⡛⠦⠤⣄⣇⣀⣀⣸⣀⡤⠼⠚⡉⢄⠠⣠⠞⠁⠄⠄⠄\n'\
                 '⠄⠄⠄⠄⠄⠄⠉⠓⠮⣔⡁⠦⠄⣤⠤⠤⣤⠄⠰⠌⣂⡬⠖⠋⠄⠄⠄⠄⠄⠄\n'\
                 '⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠉⠒⠤⢤⣀⣀⡤⠴⠒⠉⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄\n'\
                 '******************************\n'\
                 '**  COMMAND LINE ASSISTANT  **\n'\


    print(Fore.GREEN, CLI_header, Style.RESET_ALL, sep="")
    print(say_hello())
    while True:
        print(Fore.CYAN, "Type here your command", Style.RESET_ALL, end="")
        text = input(': ')
        cmds = parse_input(text)
        if not cmds:
            continue
        command = cmds[0]
        if command == 'help':
            print(CLI_header)
            print('type "list" to see all commands')
        elif command == 'list':
            print(  'bye, exit, close\t- exit from assistant\n'\
                    'all\t\t\t- print all contact book\n'\
                    'add name phone\t\t- add phone to contact list\n'\
                    'add-birthday name date\t- add or update birthday (date in format DD.MM.YYYY)\n'\
                    'del name\t\t- delete contact from list\n'\
                    'change name phone1 phone2\t- update phone number for name\n'\
                    'show-birthday name\t- show Birthday for name\n'\
                    'birthdays\t\t- display all upcoming birthdays in a next 7 days\n'\
                    'phone name\t\t- get phone number for name\n'\
                    'hello\t\t\t- greetings from bot\n'\
                    'help\t\t\t- get help\n'\
                    'date\t\t\t- get current date\n'\
                    'time\t\t\t- get current time\n'\
                    'list\t\t\t- get commands list')
        elif command in ['bye', 'exit', 'close']:
            print(Fore.YELLOW, 'Good bye!', Style.RESET_ALL)
            break
        elif command == 'hello':
            print(say_hello())
        elif command == 'add':
            print(add_contact(cmds[1:], book))
        elif command == 'del':
            print(del_contact(cmds[1:], book))
        elif command == 'change':
            print(change_contact(cmds[1:], book))
        elif command == 'phone':
            us_list = get_contact(cmds[1:], book)
            if len(us_list) == 0 or us_list[0] == "Contact not found":
                print(Fore.MAGENTA, 'No phones found', Style.RESET_ALL)
            else:
                print('Phone list:')
                for line_cont in us_list:
                    print(line_cont)
        elif command == 'all':
            us_list = print_contact(book)
            if len(us_list) == 0:
                print(Fore.MAGENTA, 'No contacts', Style.RESET_ALL)
            else:
                print('Contact list:')
                for line_cont in us_list:
                    print(line_cont)
        elif command == 'add-birthday':
            print(add_birthday(cmds[1:], book))
        elif command == 'show-birthday':
            print(show_birthday(cmds[1:], book))
        elif command == 'birthdays':
            us_list = birthdays(book)
            if len(us_list) == 0:
                print(Fore.MAGENTA, 'No upcoming birthdays. Try again later or use the ALL command to see birthdays.', Style.RESET_ALL)
            else:
                print('Nearest birthdays in the next 7 days:')
                for name, date in us_list.items():
                    print(f'{name}:\t{date}')
        elif command == 'date':
            print(curr_date())
        elif command == 'time':
            print(curr_time())
        else:
            print(Fore.RED, f'I don\'t understand the command: {command}', Style.RESET_ALL)

if __name__ == "__main__":
    main()

from datetime import datetime
from .addressbook import AddressBook
from .decorators import input_error
from .record import Record

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
    return datetime.now().strftime("%Y-%m-%d")

def curr_time() -> str:
    return datetime.now().strftime("%H:%M:%S")

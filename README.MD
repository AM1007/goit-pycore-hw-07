## Advanced Object-Oriented Programming in Python

### Task 1

First, let's add additional functionality to the previous homework classes:

- Add a `birthday` field for the birthday to the `Record` class. This field must be of class `Birthday`. This field is optional, but there can be only one.

```python
class Birthday(Field):
    def __init__(self, value):
        try:
            # Add data validation
            # and convert the string to a datetime object
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

```

- Add `Birthday` functionality to the `Record` class, namely the `add_birthday` function, which adds a birthday to a contact.
- Add the functionality of checking the correctness of the given values ​​for the `Phone`, `Birthday` fields.
- Add and adapt to the `AddressBook` class our function from Homework 4, Week 3, `get_upcoming_birthdays`, which for Address Book contacts returns a list of users to be congratulated by day in the coming week.

Now your bot should work exactly with the functionality of the `AddressBook` class. This means that instead of the `contacts` dictionary, we use `book = AddressBook()`

### Task 2

To implement the new functionality, also add function handlers with the following commands:

- `add-birthday` - add the birthday to the contact in the format `DD.MM.YYYY`
- `show-birthday` - show the contact's birthday
- `birthdays` - returns a list of users to be congratulated by day in the next week

```python
@input_error
def add_birthday(args, book):
    # реалізація

@input_error
def show_birthday(args, book):
    # реалізація

@input_error
def birthdays(args, book):
    # реалізація
```

So, in the end, our bot should support the following list of commands:

1. `add [name] [phone]`: Add either a new contact with a name and phone number, or a phone number to an existing contact.
2. `change [name] [old phone] [new phone]`: Change the phone number for the specified contact.
3. `phone [name]`: Show phone numbers for the specified contact.
4. `all`: Show all contacts in the address book.
5. `add-birthday [name] [birthday]`: Add a birthday for the specified contact.
6. `show-birthday [name]`: Show birthday for the specified contact.
7. `birthdays`: Show birthdays that will occur in the next week.
8. `hello`: Receive a greeting from the bot.
9. `close` or `exit`: Close the program.

```python
def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            # realization

        elif command == "change":
            # realization

        elif command == "phone":
            # realization

        elif command == "all":
            # realization

        elif command == "add-birthday":
            # realization

        elif command == "show-birthday":
            # realization

        elif command == "birthdays":
            # realization

        else:
            print("Invalid command.")

```

For example, consider the implementation of the `add [name] [phone]` command. In the main function, we must add the processing of this command, in the appropriate place:

```python
         elif command == "add":
            print(add_contact(args, book))
```

The actual implementation of the add_contact function can look like this:

```python
@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message
```

Our `add_contact` function has two purposes - adding a new contact or updating the phone number of a contact that already exists in the address book.

The parameters of the function are the list of arguments args and the address book book itself.

- First, the function unpacks the list of `args`, getting the name `name` and `phone` from the first two elements of the list. The rest of the arguments are ignored by using `\*\_`. Next, the `find` method of the `book` object searches for a record with the `name` name. If an entry with that name exists, the method returns that entry, otherwise `None` is returned.
- If the record is not found, then this is a new contact and the function creates a new `Record` object with the `name` name and adds it to the `book` by calling the `add_record` method. After adding a new record, the message variable is assigned the message `"Contact added."` the success of the operation.
- Next, regardless of whether a record was found or a new one was created, the phone number is added to that record using the `add_phone` method, if one was provided. At the end, the function returns a message about the result of its work: `"Contact updated."`, if the contact was updated, or `"Contact added."`, if the contact was added. We use the `@input_error` decorator to catch input errors and output the corresponding error message.

#### Evaluation criteria:

1. Implement all the specified commands to the bot

2. All data must be displayed in an understandable and user-friendly format

3. All errors, such as incorrect input or missing contact, should be handled informatively with an appropriate message to the user

4. Data validation:
   - Date of birth must be in `DD.MM.YYYY` format.
   - The phone number must consist of `10` digits.
5. The program must close correctly after executing the `close` or `exit` commands

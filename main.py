from colorama import Fore, Style
from contact_manager.addressbook import AddressBook
from contact_manager.commands import (say_hello, parse_input, add_contact, change_contact, 
                                      del_contact, print_contact, get_contact, add_birthday, 
                                      show_birthday, birthdays, curr_date, curr_time)

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
                 '**  COMMAND LINE ASSISTANT  **\n'

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

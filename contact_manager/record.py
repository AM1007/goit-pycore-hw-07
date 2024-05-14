from .fields import Name, Phone, Birthday

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

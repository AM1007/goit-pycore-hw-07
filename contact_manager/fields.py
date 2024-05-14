from datetime import datetime

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
            self.value = datetime.strptime(value, "%d.%m.%Y")
        else:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __is_valid(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            return True
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

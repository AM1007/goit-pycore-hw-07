from collections import UserDict
from datetime import datetime, timedelta

# from .record import Record

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
        datecurr = datetime.now()
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
                    birth_datetime += timedelta(days=7 - wd)
                birth_dict[user_name] = birth_datetime.strftime("%d.%m.%Y")

        return birth_dict

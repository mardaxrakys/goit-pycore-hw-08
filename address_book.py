
# address_book модуль для CLI бот

from collections import UserDict
from datetime import datetime, timedelta

# базовий клас для полів запису
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# клас для зберігання імені контакту
class Name(Field):
    pass

# клас для зберігання номера телефону
class Phone(Field):
    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)

    # валідація номера телефону
    def validate_phone(self, phone):
        return phone.isdigit() and len(phone) == 10

# клас для зберігання дня народження
class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)

# клас для зберігання інформації про контакт, включаючи ім'я, список телефонів та день народження
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    # додавання телефону
    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    # видалення телефону
    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    # редагування телефону
    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                break

    # пошук телефону
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    # додавання дня народження
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    # вивід інформації про контакт
    def __str__(self):
        phones = '; '.join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones}, birthday: {self.birthday if self.birthday else 'not set'}"

# клас для зберігання та управління записами
class AddressBook(UserDict):
    # додавання запису
    def add_record(self, record):
        self.data[record.name.value] = record

    # пошук запису
    def find(self, name):
        return self.data.get(name)

    # видалення запису
    def delete(self, name):
        if name in self.data:
            del self.data[name]

    # пошук записів з днями народження
    def get_upcoming_birthdays(self, days=7):
        upcoming_birthdays = []
        today = datetime.today()
        end_date = today + timedelta(days=days)
        for record in self.data.values():
            if record.birthday:
                bday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").replace(year=today.year)
                if today <= bday_date <= end_date:
                    upcoming_birthdays.append(record)
        return upcoming_birthdays
    
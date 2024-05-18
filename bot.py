# CLI бот помічник

import pickle
from address_book import AddressBook, Record
from errors import input_error

# збереження даних у файл
def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

# завантаження даних з файлу
def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # повернення нової адресної книги, якщо файл не знайдено

# парсинг введення користувача
def parse_input(user_input):
    parts = user_input.strip().split(maxsplit=2)
    command = parts[0].lower()
    args = parts[1:] if len(parts) > 1 else []
    return command, args

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

@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Contact updated."
    else:
        raise KeyError

@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        return f"{name}'s phone numbers are: {'; '.join(phone.value for phone in record.phones)}"
    else:
        raise KeyError

@input_error
def show_all(book: AddressBook):
    if book.data:
        return "\n".join(str(record) for record in book.data.values())
    else:
        return "No contacts stored."

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    else:
        raise KeyError

@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday is {record.birthday.value}"
    else:
        raise KeyError

@input_error
def birthdays(args, book: AddressBook):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if upcoming_birthdays:
        return "\n".join(str(record) for record in upcoming_birthdays)
    else:
        return "No upcoming birthdays in the next week."

# основна функція
def main():
    book = load_data()  # завантаження даних

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)  # збереження даних перед виходом
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
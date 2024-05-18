import pickle

class Person:
    def __init__(self, name: str, email: str, phone: str, favorite: bool):
        self.name = name
        self.email = email
        self.phone = phone
        self.favorite = favorite

class AddressBook:
    def __init__(self):
        self.contacts = []

    def add_contact(self, person: Person):
        self.contacts.append(person)

    def remove_contact(self, name: str):
        self.contacts = [contact for contact in self.contacts if contact.name != name]

    def find_contact(self, name: str):
        for contact in self.contacts:
            if contact.name == name:
                return contact
        return None

    def save_to_file(self, filename="addressbook.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load_from_file(filename="addressbook.pkl"):
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено

def main():
    address_book = AddressBook.load_from_file()

    # Основний цикл програми
    while True:
        command = input("Enter command (add, remove, find, exit): ")
        if command == "add":
            name = input("Enter name: ")
            email = input("Enter email: ")
            phone = input("Enter phone: ")
            favorite = input("Is favorite (yes/no): ") == "yes"
            address_book.add_contact(Person(name, email, phone, favorite))
        elif command == "remove":
            name = input("Enter name to remove: ")
            address_book.remove_contact(name)
        elif command == "find":
            name = input("Enter name to find: ")
            contact = address_book.find_contact(name)
            if contact:
                print(f"Name: {contact.name}, Email: {contact.email}, Phone: {contact.phone}, Favorite: {contact.favorite}")
            else:
                print("Contact not found")
        elif command == "exit":
            address_book.save_to_file()
            print("Address book saved. Exiting...")
            break
        else:
            print("Unknown command")

if __name__ == "__main__":
    main()
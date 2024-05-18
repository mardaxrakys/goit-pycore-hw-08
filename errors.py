
# декоратори для помилок вводу

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Error: Contact not found."
        except ValueError as ve:
            return f"Error: {ve}"
        except IndexError:
            return "Error: Please enter valid arguments."
    return inner
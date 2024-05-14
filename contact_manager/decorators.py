from functools import wraps

def input_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"Error: {str(e)}"
        except TypeError:
            return "Error: Incorrect number of arguments"
        except KeyError:
            return "Error: Contact not found"
        except Exception as e:
            return f"Unexpected error: {str(e)}"
    return wrapper

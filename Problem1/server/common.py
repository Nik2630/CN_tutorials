HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
BUFFER_SIZE = 1024  # Size of receiving buffer

def change_case(text):
    """Changes the case of a string (uppercase to lowercase and vice versa)."""
    return text.swapcase()

def evaluate_expression(expression):
    """Evaluates a mathematical expression string."""
    try:
        return str(eval(expression))  # Be cautious with eval in production!
    except (SyntaxError, TypeError, NameError):
        return "Invalid Expression"

def reverse_string(text):
    """Reverses a string."""
    return text[::-1]
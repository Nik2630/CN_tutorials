HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
BUFFER_SIZE = 1024  # Size of receiving buffer

def change_case(text):
    return text.swapcase()

def evaluate_expression(expression):
    try:
        return str(eval(expression))  
    except (SyntaxError, TypeError, NameError):
        return "Invalid Expression"

def reverse_string(text):
    return text[::-1]
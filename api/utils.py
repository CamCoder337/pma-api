import random
import string


def generate_code(length:int):
    characters = string.ascii_letters + string.digits
    code = ""
    for _ in range(length):
        code += random.choice(characters)
    return code
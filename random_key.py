import string
import random
from sys import argv


def generate_random_string(num=None):
    err = "You should input digit, but okay, i will set 50 symbols for you:"
    letters = string.ascii_letters + string.punctuation + string.digits
    if len(argv) == 1:
        try:
            num = int(input('Input number of digits >> '))
        except ValueError:
            print(err)
            num = 50
    else:
        try:
            num = int(argv[1])
        except ValueError:
            print(err)
            num = 50
    print(f"Your random key within {num} symbols is:")
    print("".join(random.choice(letters) for i in range(num)))


if __name__ == '__main__':
    generate_random_string()

import random
import string
import sys

import qrcode


def generate_string(num=50):
    letters = string.ascii_letters + string.punctuation + string.digits
    some_string = "".join(random.sample(letters, num))
    return some_string


def qr_image(some_string):
    filename = str(input('Enter filename of qr file>> ')) + '.png'
    image = qrcode.make(some_string)
    image.save(filename)
    print(f"Image successfully saved with filename: {filename}")


if __name__ == '__main__':
    var = str(input(
        'Enter 1 to generate random string or 2 to enter your string >> '))
    if var == '1':
        some_string = generate_string()
    elif var == '2':
        some_string = input('Enter string you want to encode in qr >> ')
    else:
        print("This choice is unacceptable")
        print("Exiting program")
        sys.exit(1)
    print(f"Processing with {some_string}.")
    qr_image(some_string)

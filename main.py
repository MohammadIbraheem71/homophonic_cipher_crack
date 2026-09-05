import re

# this function reads the ciphertext from a file and returns it as a list of strings, split by the "|" character
def read_ciphertext(filename):
    with open(filename, "r", encoding="utf-8") as file:
        ciphertext = file.read()

    return ciphertext.split("|")

# this function checks if a given token is a homophone or not
def is_homophone(token):
    return bool(re.fullmatch(r'[a-z][0-9]', token))

def main():
    # testing the read_ciphertext function
    tokens = read_ciphertext("ciphertext.txt")

    for token in tokens:
        if is_homophone(token):
            print(f"{token} is a homophone")
        else:
            print(f"{token} is not a homophone")


if __name__ == "__main__":
    main()

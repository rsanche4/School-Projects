# Author: Rafael Sanchez
# Desc: A simpler version of the RSA Encryption algorithm for educational purposes. Use this to decode.

# Custom made numbers for different ascii characters so it's easier to follow.
# 'A' - 1, 'B' - 2, ... 'Z' - 26

# Because of limitations of RSA, use n values that do not exceed each code for the letters in the message.
# I found primes 2 and 13 are the best for it to decode and encode correctly, and no spaces in your message.

ASCII_LIST = ['', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def parse(m):
    global ASCII_LIST
    for i in range(0, len(m)):
        if m[i] not in ASCII_LIST:
            return False
    return True

def main():
    global ASCII_LIST
    d_str = input("In your private key, what is d? (Formula: (e*d) modulo t = 1): ")
    if not d_str.isnumeric():
        print("Error: You inputted a non-numeric character.")
        exit(1)
    d = int(d_str)
    n_str = input("In your private key, what is n? (Formula: n = prime_number1 * prime_number2): ")
    if not n_str.isnumeric():
        print("Error: You inputted a non-numeric character.")
        exit(1)
    n = int(n_str)
    cipher = input("What message will you want to decode? (Allowed: Uppercase 'A' - 'Z', No spaces): ")
    if len(cipher) == 0:
        print("Error: No message to decode.")
        exit(1)
    if not parse(cipher):
        print("Error: '%s' could not be parsed. Unrecognized characters. (Allowed: Uppercase 'A' - 'Z', No spaces)" %cipher)
        exit(1)

    decrypted = ""
    for i in range(0, len(cipher)):
        for j in range(1, len(ASCII_LIST)+1):
            if cipher[i] == ASCII_LIST[j]:
                decrypted = decrypted + ASCII_LIST[(j**d) % n]
                break
    print("Cipher Message: " + cipher)
    print("Decrypted Message: " + decrypted)
    exit(0)

if __name__ == '__main__':
    main()
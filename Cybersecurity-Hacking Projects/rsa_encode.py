# Author: Rafael Sanchez
# Desc: A simpler version of the RSA Encryption algorithm for educational purposes. Use this to encode.

# Custom made numbers for different ascii characters so it's easier to follow.
# 'A' - 1, 'B' - 2, ... 'Z' - 26

# Because of limitations of RSA, use n values that do not exceed each code for the letters in the message.
# I found primes 2 and 13 are the best for it to decode and encode correctly, and no spaces in your message.

ASCII_LIST = ['', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

# Source: https://www.delftstack.com/howto/python/python-isprime/
def isitPrime(k):
    if k==2 or k==3: return True
    if k%2==0 or k<2: return False
    for i in range(3, int(k**0.5)+1, 2):
        if k%i==0:
            return False

    return True

def parse(m):
    global ASCII_LIST
    for i in range(0, len(m)):
        if m[i] not in ASCII_LIST:
            return False
    return True

# Source: https://www.w3resource.com/python-exercises/basic/python-basic-1-exercise-119.php
def gcd(p,q):
# Create the gcd of two positive integers.
    while q != 0:
        p, q = q, p%q
    return p
def is_coprime(x, y):
    return gcd(x, y) == 1

def choose_e(t, n):
    choices = []
    for i in range(2, t):
        choices.append(i)
    for j in range(0, len(choices)):
        if is_coprime(choices[j], t) and is_coprime(choices[j], n):
            return choices[j]

def choose_d(t, e):
    for i in range(1, t*10):
        if (i*e) % t == 1 and i != e:
            return i

def main():
    global ASCII_LIST
    p_str = input("Input prime number P (recommended: 2): ")
    if not p_str.isnumeric():
        print("Error: You inputted a non-numeric character.")
        exit(1)
    p = int(p_str)
    if not isitPrime(p):
        print("Error: %d is not prime." %p)
        exit(1)
    q_str = input("Input prime number Q (recommended: 13): ")
    if not q_str.isnumeric():
        print("Error: You inputted a non-numeric character.")
        exit(1)
    q = int(q_str)
    if p == q:
        print("Error: P and Q should be distinct.")
        exit(1)
    if not isitPrime(q):
        print("Error: %d is not prime." %q)
        exit(1)
    message = input("What message will you want to encode? (Allowed: Uppercase 'A' - 'Z', No spaces): ")
    if len(message) == 0:
        print("Error: No message to send.")
        exit(1)
    message_upper = message.upper()
    if not parse(message_upper):
        print("Error: '%s' could not be parsed. Unrecognized characters. (Allowed: Uppercase 'A' - 'Z', No spaces)" %message)
        exit(1)
    n = p*q
    t = (p-1)*(q-1)
    # (e * d) mod t = 1
    e = choose_e(t, n)
    d = choose_d(t, e)
    # public key (e, n) and private key (d, n)
    encryption_val = ""
    for i in range(0, len(message_upper)):
        for j in range(1, len(ASCII_LIST)+1):
            if message_upper[i] == ASCII_LIST[j]:
                encryption_val = encryption_val + ASCII_LIST[(j**e) % n]
                break
    print("Public Key: e = %d, n = %d." %(e, n))
    print("Private Key: d = %d, n = %d." %(d, n))
    print("Your message: " + message_upper)
    print("Cipher Message: " + encryption_val)
    exit(0)

if __name__ == '__main__':
    main()
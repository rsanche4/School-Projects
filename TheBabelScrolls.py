# Fun side Project. Program that mirrors the Library of Babel in a very simple manner. Given a string < 7000 characters, it can try to find an exact match or a random "scroll" that has that as a substring. Inspired by this website: https://libraryofbabel.info/
from random import randint
import os

MAX_STRING = 7000
# Codes were left to the right so we know the index when we look at the array right away for debugging purposes
encryption_codes = ["  ~ 00", "B ~ 01", "C ~ 02", "D ~ 03", "E ~ 04", "F ~ 05", "G ~ 06", "H ~ 07", "I ~ 08", "J ~ 09", "K ~ 10", "L ~ 11", "M ~ 12", "N ~ 13", "O ~ 14", "P ~ 15", "Q ~ 16", "R ~ 17", "S ~ 18", "T ~ 19", "U ~ 20", "V ~ 21", "W ~ 22", "X ~ 23", "Y ~ 24", "Z ~ 25", "A ~ 26", "! ~ 27", "? ~ 28", "& ~ 29", "a ~ 30", "b ~ 31", "c ~ 32", "d ~ 33", "e ~ 34", "f ~ 35", "g ~ 36", "h ~ 37", "i ~ 38", "j ~ 39", "k ~ 40", "l ~ 41", "m ~ 42", "n ~ 43", "o ~ 44", "p ~ 45", "q ~ 46", "r ~ 47", "s ~ 48", "t ~ 49", "u ~ 50", "v ~ 51", "w ~ 52", "x ~ 53", "y ~ 54", "z ~ 55", "0 ~ 56", "1 ~ 57", "2 ~ 58", "3 ~ 59", "4 ~ 60", "5 ~ 61", "6 ~ 62", "7 ~ 63", "8 ~ 64", "9 ~ 65", ", ~ 66", ". ~ 67", ": ~ 68", '" ~ 69', "' ~ 70", "( ~ 71", ") ~ 72", "$ ~ 73", "; ~ 74", "ñ ~ 75", "\ ~ 76", "á ~ 77", "é ~ 78", "í ~ 79", "ó ~ 80", "ú ~ 81", "{ ~ 82", "} ~ 83", "\n ~ 84", "# ~ 85", "@ ~ 86", "% ~ 87", "^ ~ 88", "* ~ 89", "+ ~ 90", "- ~ 91", "/ ~ 92", "[ ~ 93", "] ~ 94", "> ~ 95", "< ~ 96", "= ~ 97", "| ~ 98", "_ ~ 99"]

encryption_list = []
for i in range(len(encryption_codes)):
    letter = encryption_codes[i].split('~')[0].strip()
    encryption_list.append(letter)
encryption_list[0] = ' '
encryption_list[84] = '\n'
#print(encryption_list)

def encrypt_with_noise(string):
    global encryption_list
    global MAX_STRING
    cipher = []
    for char in string:
        if char in encryption_list:
            cipher.append(encryption_list.index(char))
    
    final_cipher = cipher
    for _i in range(MAX_STRING-len(cipher)):
        final_cipher.append(randint(0, 99))

    return final_cipher

def encrypt_exact_match(string):
    global encryption_list
    global MAX_STRING
    cipher = []
    for char in string:
        if char in encryption_list:
            cipher.append(encryption_list.index(char))
        
    final_cipher = cipher
    for _i in range(MAX_STRING-len(cipher)):
        final_cipher.append(0)

    return final_cipher

def decrypt(cipher):
    global encryption_list
    text = ''
    for num in cipher:
        text = text + encryption_list[num]
    
    return text

def find_by_string(search_string):
    c = encrypt_with_noise(search_string)
    cstring = c
    for i in range(len(c)):
        val = str(c[i])
        if len(val)==1:
            val = '0'+val
        cstring[i] = val
    scroll_number = ''.join(cstring)
    int_c = [int(x) for x in c] 
    t = decrypt(int_c)
    return (scroll_number, t)

def find_by_string_exact(search_string):
    c = encrypt_exact_match(search_string)
    cstring = c
    for i in range(len(c)):
        val = str(c[i])
        if len(val)==1:
            val = '0'+val
        cstring[i] = val
    scroll_number = ''.join(cstring)
    int_c = [int(x) for x in c] 
    t = decrypt(int_c)
    return (scroll_number, t)

def find_by_scrollnumber(scroll_num):
    global MAX_STRING
    cipher = []
    
    for i in range(MAX_STRING-len(scroll_num)):
        cipher.append(0)    

    if len(scroll_num)%2==1: # not of even length
        scroll_num = '0'+scroll_num
    
    for k in range(0, len(scroll_num), 2):
        cipher.append(int(scroll_num[k] + scroll_num[k+1]))

    t = decrypt(cipher)
    return (scroll_num, t)

def read_file(filename):
    text_file = open(filename, "r", encoding="utf-8") 
    data = text_file.read() 
    text_file.close()
    return data

def main():
    global MAX_STRING
    option_code = input("Welcome to the Scrolls of Babel! The Supposed Scrolls of Babel that contain every possible combination of 7000 characters ever written. A scroll consists of certain amount of different combinations of characters. Each scroll has a scroll number as well as its text. Would you like to search by a particular query or a particular scroll number, or go to a random scroll? Type 0 to provide a query to search, 1 for a particular scroll number, 2 to see a random scroll, 3 to read a certain query from a text file: ")
    result = ()
    if option_code=='0':
        is_exact_match = input("Would you like to search for a scroll that contains that exact content? Y for yes, N for no: ")
        search_string = input("What to search? Type here your scroll: ")
        if is_exact_match.lower()=='y':
            result = find_by_string_exact(search_string)
            
        elif is_exact_match.lower()=='n':
            result = find_by_string(search_string)
            
    elif option_code=='1':
        scroll_input = input("Which scroll would you like to see? Type a number here: ")
        result = find_by_scrollnumber(scroll_input)
    
    elif option_code=='2':
        random_scroll = ''
        for i in range(0, 2*MAX_STRING):
            
            v = str(randint(0, 9))
            random_scroll=random_scroll+v
        result = find_by_scrollnumber(random_scroll)

    elif option_code=='3':
        is_exact_match = input("Would you like to search for a scroll that contains that exact content? Y for yes, N for no: ")
        search_string = read_file(input("What to search? Type here the name of your file to read data from: "))
        if is_exact_match.lower()=='y':
            result = find_by_string_exact(search_string)
            
        elif is_exact_match.lower()=='n':
            result = find_by_string(search_string)

    while True:
        os.system("clear")
        printing_to = input("Would you like to print it to the screen or send the output to a text file? S for screen, f for a file: ")
        if printing_to.lower()=="s":
            print(f'\n\nScroll Number ({int(len(result[0]))} digits): {result[0][0:300]}...\n\n{result[1]}')
        elif printing_to.lower()=="f":
            file_name = "scroll_file_"+result[0][0:10]+".txt"
            file = open(file_name, "w", encoding="utf-8")
            file.write(result[1]+"\n\n\n"+"Scroll Number: "+result[0])
            file.close()
            print("\nOutput dumped to "+file_name)

        see_next = input("\n\nWould you like to see the next scroll? Type Y for yes, n for no: ")
        if see_next.lower()=="y":
            result = find_by_scrollnumber(str(int(result[0])+1))
        elif see_next.lower()=="n":
            break

    print("\nThank you for reading The Scrolls of Babel!\n")


main()


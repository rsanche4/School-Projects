# A binary adder calculator.
# By: Rafael Sanchez

import sys

def parse_line(bin_string):
    return bin_string.replace('\n','').split(',')

def turn_to_int_array(str_num):
    int_arr = []
    for i in range(0, len(str_num)):
        int_arr.append(int(str_num[i]))
    int_arr.reverse()
    return int_arr

def addBinaryHelper(num1, num2, carry):
    if (num1 == [] or num2 == []) and carry == 1:
        return [carry]
    if (num1 == [] or num2 == []) and carry == 0:
        return []
    if num1[0] + num2[0] + carry == 0:
        return [0] + addBinaryHelper(num1[1:], num2[1:], 0)
    if num1[0] + num2[0] + carry == 1:
        return [1] + addBinaryHelper(num1[1:], num2[1:], 0)
    if num1[0] + num2[0] + carry == 2:
        return [0] + addBinaryHelper(num1[1:], num2[1:], 1)
    if num1[0] + num2[0] + carry == 3:
        return [1] + addBinaryHelper(num1[1:], num2[1:], 1)

def addBinary(num1, num2):
    if len(num1) == len(num2):
        return addBinaryHelper(num1, num2, 0)
    if len(num1) < len(num2):
        EditedNum1 = num1 + ([0]*(len(num2)-len(num1)))
        return addBinaryHelper(EditedNum1, num2, 0)
    if len(num1) > len(num2):
        EditedNum2 = num2 + ([0]*(len(num1)-len(num2)))
        return addBinaryHelper(num1, EditedNum2, 0)

def concat(arr):
    for i in range(0, len(arr)):
        if arr[i] == 0:
            arr[i] = -1
        if arr[i] == 1:
            break;
    result_str = ""
    for i in range(0, len(arr)):
        if arr[i] == -1:
            continue
        else:
            result_str = result_str + str(arr[i])
    return result_str

print("Enter two binary numbers separated by commas (Ex: 010,110): ")

for line in sys.stdin:
    bin_pair = parse_line(line)
    int_array_0 = turn_to_int_array(bin_pair[0])
    int_array_1 = turn_to_int_array(bin_pair[1])
    result = addBinary(int_array_0,int_array_1)
    result.reverse()
    fin = concat(result)
    if (fin == ""):
        fin = "0"
    print("Addition result: " + fin)
    
    



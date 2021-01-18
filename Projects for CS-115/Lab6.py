#Rafael Sanchez
#I pledge my honor that I have abided by the Stevens Honor System.

def decimalToBinary(x):
    if x == 0:
        return []
    else:
        remainder = x % 2
        divisor = x // 2
        return [remainder] + decimalToBinary(divisor)

def binaryToDecimal(num):
    if num == [] or num == [0]:
        return 0
    else: 
        return num[0] + (2 * binaryToDecimal(num[1:]))

def incrementBinary(num):
    if num == [] or num == [0]:
        return [1]
    if num[0]==0:
        return [1] + num[1:]
    if num[0]==1:
        return [0] + incrementBinary(num[1:])


def addBinary(num1, num2):
    if len(num1) == len(num2):
        return addBinaryHelper(num1, num2, 0)
    if len(num1) < len(num2):
        EditedNum1 = num1 + ([0]*(len(num2)-len(num1)))
        return addBinaryHelper(EditedNum1, num2, 0)
    if len(num1) > len(num2):
        EditedNum2 = num2 + ([0]*(len(num1)-len(num2)))
        return addBinaryHelper(num1, EditedNum2, 0)
    

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

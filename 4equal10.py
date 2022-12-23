# Author: Rafael Sanchez
# Desc: This programs solves the problem of the mobile game 4=10. In a put the 4 numbers that needs to be solved, and the value that the program should equal to. In b, we have all the possible operators we are allowed. The program will only print out the solutions that equal the value

import itertools

a = [9, 7, 0, 1]
b = ['-', '/', '*', '+']
value = 10
all_pos_nums = list(itertools.permutations(a))
all_pos_ops = list(itertools.product(b, repeat=len(b)))
for n in all_pos_nums:
    for o in all_pos_ops:
        try:
            eq =  "("+str(n[0]) + o[0] + str(n[1]) + o[1] + str(n[2]) + o[2] + str(n[3])+")"
            eq2 = "("+ str(n[0]) + o[0] + str(n[1]) +")" + o[1] + str(n[2]) + o[2] + str(n[3])
            eq3 =  "("+str(n[0]) + o[0] + str(n[1]) + o[1] + str(n[2])+")" + o[2] + str(n[3])
            eq4 =  str(n[0]) + o[0] + "("+str(n[1]) + o[1] + str(n[2])+")" + o[2] + str(n[3])
            eq5 =  str(n[0]) + o[0] + "("+str(n[1]) + o[1] + str(n[2]) + o[2] + str(n[3])+")"
            eq6 =  str(n[0]) + o[0] + str(n[1]) + o[1] + "("+str(n[2]) + o[2] + str(n[3])+")"
            eqs = [eq, eq2, eq3, eq4, eq5, eq6]
            for e in eqs:
                r = eval(e)
                if r==value:
                    print(e, value)
        except:
            continue
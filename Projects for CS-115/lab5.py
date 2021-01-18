#I pledge my Honor I have abided by the Stevens Honor System
#Rafael Sanchez

'''below we have the function where it takes trunklength and the depth'''

from turtle import *
def svTree(trunkLength, depth):
	if trunkLength<=1:
		return
	if depth == 0:
		return
	else:
		forward(trunkLength)
		left(30)
		svTree(trunkLength/2, depth-1)
		right(60)
		svTree(trunkLength/2, depth-1)
		left(30)
		backward(trunkLength)

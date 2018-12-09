
from random import randint

generating_function = [(1,1,1),(0,1,1)]
message = "1010"

#start off with K = 3
#TODO: make it for any K
def encode(genfun, msg):
	frames = len(msg) + 2
	#numfunc = len(generating_function) #don't think we need this
	#width = len(genfun[0])
	padmsg = "00" + msg + "00"
	encmsg = ""

	for i in range(0,frames):
		for j in range(0, len(genfun)):
			temp = 0
			if int(genfun[j][0]) == 1:
				temp = temp + int(padmsg[i])
			if int(genfun[j][1]) == 1:
				temp = temp + int(padmsg[i+1])
			if int(genfun[j][2]) == 1:
				temp = temp + int(padmsg[i+2])
			if temp == 2:
				temp = 0
			if temp == 3:
				temp = 1
			encmsg = encmsg + str(temp)

		#encmsg = encmsg + padmsg[i] + padmsg[i+1] + padmsg[i+2] + " "
	return encmsg

#1 bit error generator
#TODO: make it a specified number of errors
def generror(encmsg):
	idx = randint(0, len(encmsg)-1)

	if str(encmsg[idx]) == "1":
		encmsg = encmsg[:idx] + "0" + encmsg[idx+1:]
	else:
		encmsg = encmsg[:idx] + "1" + encmsg[idx+1:]

	return encmsg

#generates 4-bit sequences
#TODO: make it a specified number of bits
def genmsg():
	msg = ""

	for i in range(0,4):
		temp = randint(0,1)
		msg = msg + str(temp)

	return msg

def stringToTuple(encmsg, rate):
	assert len(encmsg)%rate == 0
	encmsgtuple = ()
	for i in range(0,len(encmsg))[0::rate]:
		newtuple = [int(encmsg[j]) for j in range(i,i+rate)]
		encmsgtuple = encmsgtuple + (tuple(newtuple),)
	return encmsgtuple


if __name__ == '__main__':
	msg = "1011"
	encmsg = encode(generating_function,msg)
	errmsg = generror(encmsg)
	print(msg)
	print(stringToTuple(encmsg,2))
	print(errmsg)

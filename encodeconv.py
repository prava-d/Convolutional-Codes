
from random import randint

generating_function = [(1,1,0,1,1,0,1),(1,0,0,1,1,1,1)]
message = "1010"

#start off with K = 3
#TODO: make it for any K
def encode(genfun, msg):
	k = len(genfun[0])
	frames = len(msg) + k - 1
	#numfunc = len(generating_function) #don't think we need this
	#width = len(genfun[0])
	padmsg = "0"*(k-1) + msg + "0"*(k-1)
	encmsg = ""

	for i in range(0,frames):
		for j in range(0, len(genfun)):
			temp = 0
			for (idx, a) in enumerate(genfun[j]):
				if a == 1:
					temp += int(padmsg[i+idx])

			temp = temp%2
			encmsg = encmsg + str(temp)

		#encmsg = encmsg + padmsg[i] + padmsg[i+1] + padmsg[i+2] + " "
	return encmsg

#1 bit error generator
#TODO: make it a specified number of errors
def generror(encmsg, num = 1):

	used_idx = []
	for i in range(num):
		idx = randint(0, len(encmsg)-1)
		while idx in used_idx:
			idx = randint(0, len(encmsg)-1)

		if str(encmsg[idx]) == "1":
			encmsg = encmsg[:idx] + "0" + encmsg[idx+1:]
		else:
			encmsg = encmsg[:idx] + "1" + encmsg[idx+1:]

		used_idx.append(idx)

	return encmsg

#generates 4-bit sequences
#TODO: make it a specified number of bits
def genmsg():
	msg = ""

	for i in range(0,8):
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

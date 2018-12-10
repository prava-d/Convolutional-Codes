#!/usr/bin/env python
from functools import reduce
import sys
from sys import maxsize
from encodeconv import *
import matplotlib.pyplot as plt

class Slice(object):
    """ An object representing a vertical slice of a trellis structure. It
    contains information about the weights of nodes at a particular time step
    when determining optimal decoding of a convolution.
    """


    def __init__(self, received_bits, conv_code, prev_weights):
        """ The initialize method for the slice.

        Arguments:
        received_bits --- A tuple representing parity bits at current time step
        conv_code --- A tuple of tuples representing the convolutional
            polynomials for the convolutional code. e.g. ((1,1,1), (0,1,1))
        prev_weights --- A tuple containing the cumulative weights of the nodes

        Returns:
        none
        """

        # TOOD determine whether the init method also needs a dictionary
        # of valid connections and generated parity bits.

        # Determine rate and width from inputs
        self.rate = len(received_bits);
        self.width = len(conv_code[0]);

        # Make sure that window width is consistent across inputs
        #assert self.width == len(prev_weights);
        for term in conv_code:
            assert self.width == len(term);

        # Store received bits for time step and previous weights
        self.received_bits = received_bits
        self.prev_weights = prev_weights
        self.conv_code = conv_code
        self.trellis_keys = []

        # Initializes Unit Trellis Dictionary which is filled by generate_unit_tresllis
        # Keys are states and values are possible next bits based on the state indicated by the key
        self.unit_trellis = {}



    def generate_trellis_keys(self, width):

        # Base case for width = 2
        if width == 2:
            return [(0,), (1,)]

        # Generate keys for one less width
        prev_keys = self.generate_trellis_keys(width - 1)
        prev_length = len(prev_keys)

        # Permutate keys for one less width with different first bits
        trellis_keys = []
        for i in [(0,), (1,)]:
            for j in range(prev_length):
                old_tuple = prev_keys[j]
                trellis_keys.append(i + old_tuple)

        self.trellis_keys = trellis_keys
        return trellis_keys


    def generate_unit_trellis(self):

        width = self.width
        trellis = {}

        # Iterate over keys and determine possible next frames
        for key in self.trellis_keys:
            option_0 = key[1:] + (0,)
            option_1 = key[1:] + (1,)
            trellis[key] = [option_0, option_1]

        self.unit_trellis = trellis


    def get_hamming_distance(self, calc_bits):
        """ Calculates the Hamming distance between an input and the received
        bits for this slice's time step.

        Arguments:
        calc_bits --- A string representing parity bits for a particular path
            choice in the trellis

        Returns:
        distance --- An integer representing the Hamming distance between
            calc_bits and the received bits for that time step.
        """

        # Iterate through calculated bits and compare to received bits.
        # Store number of different bits in total_distance.
        total_distance = 0
        for idx, bit in enumerate(calc_bits):
            diff = abs(bit - self.received_bits[idx])
            total_distance += diff

        return total_distance


    def convolve(self, frame):
        """ Frame is a tuple of bits. """

        parity_bits = ()
        for term in self.conv_code:
            parity = 0
            for idx, bit in enumerate(term):
                parity = parity ^ (bit and frame[idx])
            parity_bits += (parity,)

        return(tuple(parity_bits))


    def get_new_weights(self):
        """ Generates weights for the next slice, based on starting weights and
        the Hamming distance of each path option.

        Arguments:
        none

        Returns:
        weights --- A tuple containing the cumulative node weights of new slice
        """

        # Initializes new_weights with max value weights
        new_weights = []
        new_key_to_old_key = {}

        for i in range(2 ** (self.width - 1)):
            new_key_to_old_key[i] = None
            new_weights.append(sys.maxsize)

        for key in self.trellis_keys:
            key_int = reduce(lambda acc, x: acc * 2 + x, key)
            # If the next msg bit is a 0
            parity_0 = self.convolve(key+(0,))
            msg_0_int = reduce(lambda acc, x: acc * 2 + x, key[1:]+(0,))
            # Takes parity bits tuple and turns it from tuple with base 2 digits to a base 10 int
            # This is so that it can be used as an index
            parity_0_int = reduce(lambda acc, x: acc * 2 + x, parity_0)

            weight_0 = self.get_hamming_distance(parity_0) + self.prev_weights[key_int]

            if(weight_0 < new_weights[msg_0_int]):
                new_weights[msg_0_int] = weight_0
                new_key_to_old_key[msg_0_int] = key_int

            # If the next msg bit is a 1
            parity_1 = self.convolve(key+(1,))
            msg_1_int = reduce(lambda acc, x: acc * 2 + x, key[1:]+(1,))
            # Takes parity bits tuple and turns it from tuple with base 2 digits to a base 10 int
            # This is so that it can be used as an index for new_weights
            parity_1_int = int(str(reduce(lambda acc, x: acc * 10 + x, parity_1)),2)

            weight_1 = self.get_hamming_distance(parity_1) + self.prev_weights[key_int]


            if(weight_0 < new_weights[msg_1_int]):
                new_weights[msg_1_int] = weight_1
                new_key_to_old_key[msg_1_int] = key_int

        self.backtrack_dict = new_key_to_old_key
        
        return tuple(new_weights)

class Trellis(object):
    """ An object representing an entire trellis with all weights calculated. Uses Slice objects to calculate weights.
    Contains a backtrace function for finding the minimal weight path
    """
    def __init__(self, recieved_bits, code):
        """ The initialize method for the trellis.

        Arguments:
        received_bits --- A tuple of tuples representing the recieved parity bits
        conv_code --- A tuple of tuples representing the convolutional
            polynomials for the convolutional code. e.g. ((1,1,1), (0,1,1))

        Returns:
        none
        """
        self.msg = []
        self.slices = []
        rate = len(code)

        k = len(code[0])
        weight = (0,) + (sys.maxsize,) * (2**(k-1))
        for bits in (recieved_bits+(((0,)*rate),)):
            a = Slice(bits, code, weight)
            a.generate_trellis_keys(a.width)
            a.generate_unit_trellis()
            weight = a.get_new_weights()
            self.slices.append(a)

        self.backtrace()

    def backtrace(self):
        weights = self.slices[-1].prev_weights
        key = weights.index(min(weights))


        for a in self.slices[-2::-1]:
            bit = key%2
            self.msg.append(bit)
            key = a.backtrack_dict[key]
            
        self.msg = self.msg[::-1]

def TestCode(code, rate, testnumber, error_amt = 1):
    """ A function for testing how well a convolutional code performs. 
        Arguments:
        code --- A list of tuples representing the convolutional
            polynomials for the convolutional code. e.g. [(1,1,1), (0,1,1)]
        rate --- The rate of the convolutional code
        testnumber --- The number of tests to be done on the code

        Returns:
        none

    """
    success = 0                                     # Number of successful tests
    #print("Convolutional Code:")
    #print(code)
    #print()
    for i in range(1,testnumber+1):
        if i%(int(testnumber/10)) == 0:
            pass#print(str(10*int(10*i/testnumber)) + "%")
        #print("TEST NUMBER: %s" % i)
        msg = genmsg()
        encodedmsg = encode(code, msg)
        rcvd = stringToTuple(encodedmsg,rate)
        errormsg = generror(encodedmsg, error_amt)
        errormsgtuple = stringToTuple(errormsg, rate)
        trell = Trellis(errormsgtuple,tuple(code))
        k = len(code[0])

        if(''.join(str(e) for e in trell.msg[0:-(k-1)]) == msg):
            success += 1

    #    print("Msg:\n"+msg+"\n")
    #    print("Encoded Msg:\n"+encodedmsg+"\n")
    #    print("Encoded Msg with Error:\n"+errormsg+"\n")
    #    print("Decoded Msg with Error:\n"+''.join(str(e) for e in trell.msg[0:-2]))

    #print("Number of Successes: %s" % success)
    #print("Number of Failurs: %s" % (testnumber-success))
    return(success/(testnumber))

if __name__ == '__main__':
    code7 = [(1,1,0,1,1,0,1),(1,0,0,1,1,1,1)]
    code6bad = [(0,1,1,0,1,1),(1,0,0,0,1,1)]
    code7good = [(0,1,1,0,1,0,1),(1,0,0,1,0,1,1)]
    code6good = [(0,1,0,1,1,1),(1,0,0,0,1,1)]
    code5good = [(0,1,1,1,1),(1,0,0,0,1)]
    code4good = [(0,1,1,1),(0,1,0,1)]
    code3good = [(0, 1, 1),(1, 1, 1)]
    #rcvd = stringToTuple(encode(code, msg),2)

    codes = [code3good, code4good, code5good, code6good, code7good]

    xs = []
    ys = []
    for code in codes:
        print(code)
        for i in range(11):
            print(i)
            xs.append(i)
            ys.append(TestCode(code,2,5000,i))
        plt.plot(xs, ys, '.-')
        xs = []
        ys = []
    plt.legend(["Code Width 3", "Code Width 4", "Code Width 5", "Code Width 6", "Code Width 7"])
    plt.xlabel("Number of Errors")
    plt.ylabel("Decoding Accuracy")
    plt.show()
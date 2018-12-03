#!/usr/bin/env python

class Slice(object):
    """ An object representing a vertical slice of a trellis structure. It
    contains information about the weights of nodes at a particular time step
    when determining optimal decoding of a convolution.
    """


    def __init__(self, received_bits, conv_code, prev_weights):
        """ The initialize method for the slice.

        Arguments:
        received_bits --- A list representing parity bits at current time step
        conv_code --- A list of tuples representing the convolutional
            polynomials for the convolutional code. e.g. [(1,1,1), (0,1,1)]
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

        # TODO implement this method
        pass


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

        return trellis_keys


    def generate_unit_trellis(self):

        width = self.width
        trellis = {}

        # Generate key options for dictionary
        keys = self.generate_trellis_keys(width)

        # Iterate over keys and determine possible next frames
        for key in keys:
            option_0 = key[1:] + (0,)
            option_1 = key[1:] + (1,)
            trellis[key] = [option_0, option_1]

        return trellis


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

        # TODO generalize this to do soft decoding

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
        # TODO detemine if/how this method provides a way to backtrack along
        # the shortest path. Perhaps it compiles a dictionary going backward
        # from each minimum distance.

        

        # TODO implement this
        pass


if __name__ == '__main__':
    a = Slice((0, 1), ((1, 1), (1, 0)), (3, 4, 5, 6))
    print(a.generate_trellis_keys(3))
    print()
    print(a.generate_unit_trellis())
    print()
    print(a.convolve((1, 1)))

#!/usr/bin/env python

class Slice(object):
    """ An object representing a vertical slice of a trellis structure. It
    contains information about the weights of nodes at a particular time step
    when determining optimal decoding of a convolution.
    """


    def __init__(self, received_bits, conv_code, weights):
        """ The initialize method for the slice.

        Arguments:
        received_bits --- A string representing parity bits at current time step
        conv_code --- A list of tuples representing the convolutional
            polynomials for the convolutional code. e.g. [(1,1,1), (0,1,1)]
        weights --- A tuple containing the cumulative weights of the nodes

        Returns:
        none
        """
        # TOOD determine whether the init method also needs a dictionary
        # of valid connections and generated parity bits.

        # Determine rate and width from inputs
        self.rate = len(received_bits);
        self.width = len(conv_code[0]);

        # Make sure that window width is consistent across inputs
        assert self.width == len(weights);
        for term in conv_code:
            assert self.width == len(term);

        # TODO implement this method
        pass


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

        # TODO implement this method
        pass


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
    pass

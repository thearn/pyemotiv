import unittest
import time
import pyemotiv

"""
A collection of some basic tests for the pyemotiv library.
"""


class TestData(unittest.TestCase):
    epoc = pyemotiv.Epoc()

    def test_packets(self):
        """
        Tests collection of data packets
        """
        packets = self.epoc.get_all()
        self.assertGreater(len(packets), 0)

if __name__ == '__main__':
    unittest.main()

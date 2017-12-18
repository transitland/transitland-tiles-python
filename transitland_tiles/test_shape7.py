"""GraphID unit tests."""
import unittest

import shape7

class Test_Shape7(unittest.TestCase):
    coords = (
        (-74.012666, 40.70136),
        (-74.012962, 40.700478),
        (-74.01265, 40.699074)
    )
    encoded = (
        243, 223, 202, 70, 224, 182,
        232, 38, 207, 4, 227, 13,
        240, 4, 247, 21
    )
    tolerance = 0.01

    def test_encode(self):
        encoded = shape7.encode(self.coords)
        e = map(ord, encoded)
        for a,b in zip(e, self.encoded):
            assert a == b

    def test_decode(self):
        e = ''.join(map(chr, self.encoded))
        d = shape7.decode(e)
        for a,b in zip(d, self.coords):
            assert a[0]-b[0] < self.tolerance
            assert a[1]-b[1] < self.tolerance

    def test_encode_decode(self):
        d = shape7.decode(shape7.encode(self.coords))
        for a,b in zip(d, self.coords):
            assert a[0]-b[0] < self.tolerance
            assert a[1]-b[1] < self.tolerance

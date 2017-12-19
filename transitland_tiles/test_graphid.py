import unittest

from graphid import GraphID

class Test_GraphID(unittest.TestCase):
    def test_init_from_value(self):
        # level 1
        graphid = GraphID(value=142438865769)
        assert graphid.level == 1
        assert graphid.tile == 37741
        assert graphid.bbox() == [121.0, 14.0, 122.0, 15.0]
        # level 2
        graphid = GraphID(value=73160266)
        assert graphid.level == 2
        assert graphid.tile == 756425
        assert graphid.bbox() == [-73.75, 41.25, -73.5, 41.5]

    def test_init_from_lat_lon(self):
        graphid = GraphID(level=0, lat=14.601879, lon=120.972545)
        assert graphid.tile == 2415

        graphid = GraphID(level=1, lat=14.601879, lon=120.972545)
        assert graphid.tile == 37740

        graphid = GraphID(level=2, lat=41.413203, lon=-73.623787)
        assert graphid.tile == 756425

    def test_init_from_components(self):
        # Forwards
        graphid = GraphID(level=1, tile=3, index=7)
        assert graphid.value == 234881049
        # Backwards
        graphid = GraphID(value=graphid.value)
        assert graphid.level == 1
        assert graphid.tile == 3
        assert graphid.index == 7

    def test_bbox_to_level_tiles(self):
        level_tiles = GraphID.bbox_to_level_tiles((-74.251961, 40.512764, -73.755405, 40.903125))
        e = [
            [0, 2906],
            [1, 46905],
            [1, 46906],
            [2, 753544],
            [2, 752104],
            [2, 753543],
            [2, 752103],
            [2, 753542],
            [2, 752102]
        ]
        assert sorted(level_tiles) == sorted(e)

import os
import unittest

from tileset import TileSet

class Test_TileSet(unittest.TestCase):
    PATH = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), '..', 'examples'
    )

    def test_read_tile(self):
        t = TileSet(path=self.PATH)
        tile = t.read_tile(2, 752102)
        assert len(tile.message.nodes) == 4

    def test_get_tile_by_lll(self):
        level = 2
        lon = -74.2519607544
        lat = 40.5127639771
        t = TileSet(path=self.PATH)
        tile = t.get_tile_by_lll(level, lat, lon)
        assert len(tile.message.nodes) == 4

    def test_get_tile_by_graphid(self):
        from graphid import GraphID
        graphid = 6016818
        t = TileSet(path=self.PATH)
        tile = t.get_tile_by_graphid(GraphID(value=graphid))
        assert len(tile.message.nodes) == 4

    def test_find_all_tiles(self):
        t = TileSet(path=self.PATH)
        tiles = t.find_all_tiles()
        assert tiles == [(2, 752102)]

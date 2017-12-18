import os

from graphid import GraphID
from tile import Tile

class TileSet(object):
    def __init__(self, path):
        self.path = path

    def get_tile_by_lll(self, level, lat, lon):
        return self.get_tile_by_graphid(GraphID(level=level, lat=lat, lon=lon))

    def get_tile_by_graphid(graphid):
        return self.read_tile(graphid.level, graphid.tile)

    def write_tile(tile, ext=None):
        pass

    def new_tile(self, level, tile):
        pass

    def read_tile(self, level, tile):
        path = self._tile_path(level, tile)
        if os.path.exists(path):
            return Tile(level, tile, data=self._read_file(path))
        else:
            return Tile(level, tile)

    def _read_file(self, path):
        with open(path) as f:
            data = f.read()
        return data

    def find_all_tiles(self):
        all_tiles = []
        for root,dirs,files in os.walk(self.path):
            for f in files:
                if not f.endswith('.pbf'):
                    continue
                path = root.split(os.sep)
                path.append(f[:-4])
                if path[-4] == '2':
                    level = 2
                    tile = int(''.join(path[-3:]))
                else:
                    level = int(path[-4])
                    tile = int(''.join(path[-3:]))
                all_tiles.append((level, tile))
        return all_tiles

    def _tile_path(self, level, tile, ext=None):
        # TODO: support multiple levels
        if ext:
            ext = ".pbf.%s"%ext
        else:
            ext = ".pbf"
        s = str(tile).rjust(9, '0')
        return os.path.join(
            self.path,
            str(level),
            s[0:3],
            s[3:6],
            s[6:9] + ext
        )

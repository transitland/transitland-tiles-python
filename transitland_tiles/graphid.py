# Valhalla GraphID

# Bit shifting magic
SIZES = [4.0, 1.0, 0.25]
LEVEL_BITS = 3
TILE_INDEX_BITS = 22
ID_INDEX_BITS = 21
LEVEL_MASK = (2**LEVEL_BITS) - 1
TILE_INDEX_MASK = (2**TILE_INDEX_BITS) - 1
ID_INDEX_MASK = (2**ID_INDEX_BITS) - 1
INVALID_ID = (ID_INDEX_MASK << (TILE_INDEX_BITS + LEVEL_BITS)) | (TILE_INDEX_MASK << LEVEL_BITS) | LEVEL_MASK

class GraphID(object):
    def __init__(self, value=None, **kwargs):
        self.value = value or self.make_id(**kwargs)

    @classmethod
    def make_id(cls, level=0, tile=0, index=0, lat=None, lon=None):
        if lat and lon:
            tile = cls.lll_to_tile(level, lat, lon)
        return level | tile << LEVEL_BITS | index << (LEVEL_BITS + TILE_INDEX_BITS)

    @classmethod
    def lll_to_tile(cls, level, lat, lon):
        size = SIZES[level]
        width = int(360 / size)
        return int((lat + 90) / size) * width + int((lon + 180 ) / size)

    @classmethod
    def level_tile_to_bbox(cls, level, tile):
        print "level: ", level, "tile: ", tile
        size = SIZES[level]
        width = int(360 / size)
        height = int(180 / size)
        ymin = int(tile / width) * size - 90
        xmin = (tile % width) * size - 180
        xmax = xmin + size
        ymax = ymin + size
        return [xmin, ymin, xmax, ymax]

    @classmethod
    def bbox_to_level_tiles(cls, bbox):
        assert len(bbox) == 4
        # if this is crossing the anti meridian split it up and combine
        left, bottom, right, top = bbox
        if left > right:
            east = self.bbox_to_level_tiles((left, bottom, 180.0, top))
            west = self.bbox_to_level_tiles((-180.0, bottom, right, top))
            return east + west
        #move these so we can compute percentages
        left += 180
        right += 180
        bottom += 90
        top += 90
        tiles = []
        for level, size in enumerate(SIZES):
            for x in range(int(left/size), int(right/size)+1):
                for y in range(int(bottom/size), int(top/size)+1):
                    tile = int(y * (360.0 / size) + x)
                    tiles.append([level, tile])
        return tiles

    def bbox(self):
        return self.level_tile_to_bbox(self.level, self.tile)

    @property
    def level(self):
        return self.value & LEVEL_MASK

    @property
    def tile(self):
        return (self.value >> LEVEL_BITS ) & TILE_INDEX_MASK

    @property
    def index(self):
        return (self.value >> LEVEL_BITS + TILE_INDEX_BITS) & ID_INDEX_MASK

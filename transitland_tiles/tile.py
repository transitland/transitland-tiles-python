from graphid import GraphID

class Tile(object):
    def __init__(self, level, tile, data=None):
        self.level = level
        self.tile = tile
        self.index = {}
        self.message = self.load(data)

    def load(data):
        if data:
            message = decode(data)
        else:
            message = None # new message
        return message

    def decode(self, data):
        pass

    def encode(self, data):
        pass

    def bbox(self):
        return GraphID.level_tile_to_bbox(self.level, self.tile)

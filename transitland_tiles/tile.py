import graphid
import transit_pb2

class Tile(object):
    def __init__(self, level, tile, data=None):
        self.level = level
        self.tile = tile
        self.index = {}
        self.message = self.load(data)

    def load(self, data):
        if data:
            message = self.decode(data)
        else:
            message = transit_pb2.Transit()
        return message

    def decode(self, data):
        message = transit_pb2.Transit()
        message.ParseFromString(data)
        return message

    def encode(self):
        return self.message.SerializeToString()

    def bbox(self):
        return graphid.GraphID.level_tile_to_bbox(self.level, self.tile)

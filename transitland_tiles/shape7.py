# https://github.com/valhalla/valhalla/blob/master/valhalla/midgard/encoded.h
import math

def encode(coordinates):
    output = []
    last_lat = 0
    last_lon = 0
    for lat,lon in coordinates:
        lat = math.floor(lat * 1e6)
        lon = math.floor(lon * 1e6)
        output += encode_int(lat - last_lat)
        output += encode_int(lon - last_lon)
        last_lat = lat
        last_lon = lon
    return ''.join(output)

def decode(value):
    last_lat = 0
    last_lon = 0
    coordinates = []
    d = decode_ints(value)
    for i in range(0, len(d), 2):
        lat = d[i]
        lon = d[i+1]
        lat /= 1e6
        lon /= 1e6
        last_lat += lat
        last_lon += lon
        coordinates.append((last_lat, last_lon))
    return coordinates

def encode_int(number):
    number = int(number)
    ret = []
    if number < 0:
        number = ~(number << 1)
    else:
        number = number << 1
    while (number > 0x85):
        # Take 7 bits
        nextvalue = (0x80 | (number & 0x7f))
        ret.append(chr(nextvalue))
        number >>= 7
    # Last 7 bits
    ret.append(chr(number & 0x7f))
    return ret

def decode_ints(value):
    ret = []
    index = 0
    while (index < len(value)):
        shift = 0
        result = 0
        nextvalue = ord(value[index])
        while (nextvalue > 0x7f):
            # Next 7 bits
            result |= (nextvalue & 0x7f) << shift
            shift += 7
            index += 1
            nextvalue = ord(value[index])
        # Last 7 bits
        result |= (nextvalue & 0x7f) << shift
        # One's complement if msb is 1
        if result & 1 == 1:
            result =~ result
        result >>= 1
        # Add to output
        ret.append(result)
        index += 1
    return ret







    #

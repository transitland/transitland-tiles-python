import argparse
import collections
import os
import errno
import sys

import boto3
import botocore
import botocore.client

from graphid import GraphID

def makedirs(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

class TileDownloader(object):
    def __init__(self, bucket='transit.land', prefix='tile-exports', path='.', date=None):
        self.bucket = bucket
        self.prefix = prefix
        self.path = path
        self.date = date or 'latest'
        s3 = boto3.resource(
            's3',
            config=botocore.client.Config(signature_version=botocore.UNSIGNED)
        )
        self.s3_bucket = s3.Bucket(self.bucket)

    def download_archive(self):
        key = '%s/%s/tiles.tar.gz'%(self.prefix, self.date)
        path = os.path.join(self.path, 'transit.tar.gz')
        # Get filesize
        size = None
        for f in self.s3_bucket.objects.filter(Prefix=key):
            size = f.size
        if size is None:
            raise Exception('404: %s'%key)
        # Downloda a single file
        self._download(key, path, size=size)

    def download_bbox(self, bbox):
        tileids = GraphID.bbox_to_level_tiles(bbox)
        tileids = [b for a,b in tileids if a==2]
        self.download(tileids)

    def download(self, tileids):
        printcount = 50
        print "Looking for %s tiles..."%len(tileids)
        print "\t" + "\n\t".join(map(str, tileids[:printcount]))
        if len(tileids) > 10000:
            print "\t... and %s more; consider using --archive"%(len(tileids)-printcount)
        elif len(tileids) > printcount:
            print "\t... and %s more"%(len(tileids)-printcount)

        # Sort tiles into bucket prefixes
        prefixes = collections.defaultdict(list)
        for tileid in tileids:
            t = str(tileid).rjust(9, '0')
            key = '%s/%s/%s/%s/%s'%(self.prefix, self.date, 2, t[0:3], t[3:6])
            prefixes[key].append(tileid)

        # Check for tile presence and supplemental tiles and download
        for prefix, tileids in sorted(prefixes.items()):
            print "prefix:", prefix
            downloads = []
            for f in self.s3_bucket.objects.filter(Prefix=prefix).all():
                p = ''.join(f.key.split('/')[-3:])
                t = int(p.split('.')[0])
                if t in tileids:
                    downloads.append([f.key, f.size])

            for key,size in downloads:
                path = os.path.join(self.path, *key.split('/')[-4:])
                self._download(key, path, size=size)

    def _download(self, key, path, size=None):
        url = "http://%s.s3.amazonaws.com/%s"%(self.bucket, key) # display only
        if os.path.exists(path) and os.stat(path).st_size == size and size is not None:
            print "%s -> %s (%0.2f MB; present)"%(url, path, size/1000.0**2)
            return

        if size is not None:
            print "%s -> %s (%0.2f MB)"%(url, path, size/1000.0**2)
        else:
            print "%s -> %s "%(url, path)

        makedirs(os.path.dirname(path))
        try:
            self.s3_bucket.download_file(key, path)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("%s: 404"%url)
            else:
                raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download tiles')
    parser.add_argument('--bucket', help='Bucket', default='transit.land')
    parser.add_argument('--prefix', help='Prefix', default='tile-exports')
    parser.add_argument('--date', help='Date', default='latest')
    parser.add_argument('--path', help='Output path', default='.')
    parser.add_argument('--bbox', help='bbox')
    parser.add_argument('--archive', help='Download entire archive', action='store_true')
    parser.add_argument('tileids', help='Tile IDs', nargs='*')
    args = parser.parse_args()

    t = TileDownloader(bucket=args.bucket, prefix=args.prefix, date=args.date, path=args.path)

    if not any((args.archive, args.bbox, args.tileids)):
        print "Must supply either --archive, --bbox, or a list of tileids"
        sys.exit(0)

    if args.archive:
        t.download_archive()

    if args.bbox:
        bbox = [float(i) for i in args.bbox.split(',')]
        t.download_bbox(bbox)

    if args.tileids:
        t.download(map(int, args.tileids))

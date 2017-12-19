import collections
import os
import errno

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
    def __init__(self, bucket='transit.land', prefix='tile-export', date=None):
        self.bucket = bucket
        self.prefix = prefix
        self.date = date or '2017-12-03'
        s3 = boto3.resource(
            's3',
            config=botocore.client.Config(signature_version=botocore.UNSIGNED)
        )
        self.s3_bucket = s3.Bucket(BUCKET_NAME)

    def download_bbox(self, bbox):
        tileids = GraphID.bbox_to_level_tiles(bbox)
        tileids = [b for a,b in tileids if a==2]
        self.download(tileids)

    def download(self, tileids):
        # Sort tiles into bucket prefixes
        prefixes = collections.defaultdict(list)
        for tileid in tileids:
            t = str(tileid).rjust(9, '0')
            key = '%s/%s/%s/%s/%s'%(self.prefix, self.date, 2, t[0:3], t[3:6])
            prefixes[key].append(tileid)

        # Check for tile presence and supplemental tiles and download
        for prefix, tileids in sorted(prefixes.items()):
            downloads = []
            for f in self.s3_bucket.objects.filter(Prefix=prefix).all():
                p = ''.join(f.key.split('/')[-3:])
                t = int(p.split('.')[0])
                if t in tileids:
                    downloads.append(f.key)

            for key in downloads:
                self._download(key)

    def _download(self, key):
        path = os.path.join(*key.split('/')[-4:])
        makedirs(os.path.dirname(path))
        print "downloading %s to %s "%(key, path)
        try:
            self.s3_bucket.download_file(key, path)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("404: %s"%key)
            else:
                raise

from setuptools import setup

import transitland_tiles

setup(
  name='transitland_tiles',
  version=transitland_tiles.__version__,
  description='Transitland Tiles Client',
  author='Ian Rees',
  author_email='ian@mapzen.com',
  url='https://github.com/transitland/transitland-tiles-python',
  license='License :: OSI Approved :: MIT License',
  packages=['transitland_tiles'],
  install_requires=['pytz', 'protobuf', 'nose'],
  # Include examples.
  package_data = {
    '': ['*.txt', '*.md', '*.proto']
  }
)

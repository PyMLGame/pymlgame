#!/usr/bin/env python3.3
# -*- coding: utf-8 -*-

"""
pymlgame
"""

__author__ = "Ricardo Band"
__copyright__ = "Copyright 2013, Ricardo Band"
__credits__ = ["Ricardo Band"]
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Ricardo Band"
__email__ = "me@xengi.de"
__status__ = "Development"

import os
from distutils.core import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='pymlgame',
      version=__version__,
      author=__author__,
      author_email=__email__,
      maintainer=__maintainer__,
      maintainer_email=__email__,
      url='http://github.com/c-base/pymlgame',
      description='pymlgame is an abstraction layer to easily build games for Mate Light inspired by pygame.',
      long_description=read('README.md'),
      download_url='https://github.com/c-base/pymlgame/archive/master.zip',
      classifiers=['Development Status :: 2 - Pre-Alpha',
                   'Environment :: Console',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Natural Language :: English',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 3.3',
                   'Topic :: Games/Entertainment',
                   'Topic :: Software Development :: Libraries :: Python Modules'],
      platforms='',
      license=__license__,
      packages=['pymlgame'],
      requires=['jsonrpclib-pelix'])

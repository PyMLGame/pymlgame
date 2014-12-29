#!/usr/bin/env python3.3
# -*- coding: utf-8 -*-

"""
pymlgame
"""

__author__ = 'Ricardo Band'
__copyright__ = 'Copyright 2014, Ricardo Band'
__credits__ = ['Ricardo Band']
__license__ = 'MIT'
__version__ = '0.3.0'
__maintainer__ = 'Ricardo Band'
__email__ = 'me@xengi.de'
__status__ = 'Development'

import os
from distutils.core import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='PyMLGame',
      version=__version__,
      author=__author__,
      author_email=__email__,
      maintainer=__maintainer__,
      maintainer_email=__email__,
      url='http://github.com/PyMLGame/pymlgame',
      description='PyMLGame is an abstraction layer to easily build games for Mate Light inspired by PyGame.',
      long_description=read('README.md'),
      download_url='https://github.com/PyMLGame/pymlgame/archive/master.zip',
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Console',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Natural Language :: English',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 3',
                   'Topic :: Games/Entertainment',
                   'Topic :: Software Development :: Libraries :: Python Modules'],
      platforms='any',
      license=__license__,
      packages=['pymlgame'],
      requires=[,])

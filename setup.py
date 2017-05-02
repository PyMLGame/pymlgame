#!/usr/bin/env python3

import sys
from os import path
from setuptools import setup, find_packages

from pymlgame import __version__


def read(filename):
    with open(path.join(path.abspath(path.dirname(__file__)), filename), 'r') as fh:
        return fh.read()


setup(name='PyMLGame',
      version=__version__,

      description='PyMLGame is an abstraction layer to easily build games for Mate Light inspired by PyGame.',
      long_description=read('README.md'),

      url='http://github.com/PyMLGame/pymlgame',

      author='Ricardo Band',
      author_email='email@ricardo.band',

      license='MIT',

      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Console',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Natural Language :: English',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',
                   'Topic :: Games/Entertainment',
                   'Topic :: Software Development :: Libraries :: Python Modules'],

      keywords='pygame matelight c-base mainhall',

      packages=find_packages(exclude=['contrib', 'docs', 'tests']),

      #data_files=[(path.join(sys.prefix, 'share/pymlgame'),
      #            ['controller_example.py', 'kbd.png', 'emulator.py', 'game_example.py'])],

      #install_requires=[],

      #extras_require={
      #    'dev': ['check-manifest'],
      #    'test': ['coverage'],
      #},
)

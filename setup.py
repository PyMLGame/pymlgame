#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from distutils.core import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='PyMLGame',
      version='0.3.1',
      author='Ricardo Band',
      author_email='email@ricardo.band',
      maintainer='Ricardo Band',
      maintainer_email='email@ricardo.band',
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
      license='MIT',
      packages=['pymlgame'],
      requires=[])

# -*- coding: utf-8 -*-
"""
LogrusFormatter
-----------------------

The format of the log library for simulating Logrus golang library
https://github.com/sirupsen/logrus
"""
import sys
import os
from setuptools import setup

if sys.version_info < (2, 6):
    raise Exception("LogrusFormatter requires Python 2.6 or higher.")

# Hard linking doesn't work inside VirtualBox shared folders. This means that
# you can't use tox in a directory that is being shared with Vagrant,
# since tox relies on `python setup.py sdist` which uses hard links. As a
# workaround, disable hard-linking if setup.py is a descendant of /vagrant.
# See
# https://stackoverflow.com/questions/7719380/python-setup-py-sdist-error-operation-not-permitted
# for more details.
if os.path.abspath(__file__).split(os.path.sep)[1] == 'vagrant':
    del os.link

setup(
    name="LogrusFormatter",
    version="0.1a",
    packages=["logrusformatter"],
    author="Vadim Ponomarev",
    author_email="velizarx@gmail.com",
    url='https://github.com/velp/logrus-formatter',
    license="MIT",
    description='The format of the log library for simulating Logrus golang library.',
    long_description=__doc__,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Environment :: Plugins',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Logging',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    install_requires=[],
    tests_require=["mock>=1.0"],
    extras_require={'docs': ["Sphinx>=1.2.3", "alabaster>=0.6.3"]}
)

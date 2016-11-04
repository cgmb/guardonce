# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name = 'guardonce',
    version = '2.0.0',
    description = 'Utilities for converting from C/C++ include guards to #pragma once and back again',
    license = 'MIT',
    url = 'https://github.com/cgmb/guardonce',
    author = 'Cordell Bloor',
    author_email = 'slavik81@gmail.com',
    packages = ['guardonce'],
    entry_points = {
        'console_scripts': [
            'checkguard = guardonce.checkguard:main',
            'guard2once = guardonce.guard2once:main',
            'once2guard = guardonce.once2guard:main',
        ]
    },
    extras_require = { 'test': ['nose'] },
    install_requires = [
    ],
    tests_require = ['guardonce[test]'],
    test_suite = "nose.collector",
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
)

# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name = 'guardonce',
    version = '2.4.0',
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
        'Development Status :: 5 - Production/Stable',
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
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    long_description = """
Why Convert?
------------

Include guards suck. They're tiring to type and tedius to update. Worse,
the task of updating boilerplate leaves room for copy/paste errors, or
other mistakes. #pragma once is simpler and less error prone. That's why
you should convert to #pragma once.

Alas, though #pragma once is available on all the most commonly used
compilers, it's not available on *every* compiler. Perhaps one day
you'll add support for a platform with a barebones compiler with no
support for #pragma once and you'll have to convert back. That's ok.
It's easy!

What exactly is guardonce?
--------------------------

There are three main tools provided by guardonce:

1. ``checkguard`` helps find any broken include guards you may already
   have in your project. These should be addressed before converting.

2. ``guard2once`` converts files with include guards into files with
   #pragma once directives. This ensures your entire project is
   consistently using #pragma once.

3. ``once2guard`` converts files with #pragma once directives back into
   files with include guards. This ensures your entire project is
   consistently using include guards.

How to use:
-----------

First, check your project for broken headers. To recursively search your
project directories for the names of all files that lack proper include
guards, use the following command, substituting your project's directory
for the quoted string:

``checkguard -r "source_directory"``

By default, checkguard is very forgiving. It accepts either #pragma once
or anything that looks like an include guard. If you know that all your
guards should match some format, you can be more strict by using ``-p``
to specify a pattern to check against.

If certain files are not supposed to have include guards, feel free to
leave them be. Files without include guards are ignored by this next
step.

Now, all that remains is converting the headers to use #pragma once:

``guard2once -r "source_directory"``

You're done! Double check that the result matches your expectations and
start using #pragma once in your new code. Know that if you ever need to
switch back, it's as simple as:

``once2guard -r "source_directory"``

If the default guard style doesn't appeal to you, there are a few
options to customize it. Maybe take a look through ``once2guard --help``
or check out a walkthrough for some examples.
"""
)

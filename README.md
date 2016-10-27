guardonce
=========

Utilities for converting from C/C++ include guards to #pragma once and
back again.

## Why Convert?
Include guards suck. They're tiring to type and tedius to update. Worse, the
task of updating boilerplate leaves room for copy/paste errors, or other
mistakes. #pragma once is simpler and less error prone. That's why you should
convert to #pragma once.

Alas, though #pragma once is available on all the most commonly used
compilers, it's not available on _every_ compiler. Perhaps one day you'll add
support for a platform with a barebones compiler with no support for #pragma
once and you'll have to convert back. That's ok. It's easy!

## What exactly is guardonce?
There are three main tools provided by guardonce:

1. `checkguard` helps find any broken include guards you may already have in
your project. These should be addressed before converting.

2. `guard2once` converts files with include guards into files with #pragma
once directives. This ensures your entire project is consistently using #pragma
once.

3. `once2guard` converts files with pragma once directives back into files with
include guards. This ensures your entire project is consistently using include
guards.

## How to use:
First, backup your source code. guardonce is naive. It will work without
incident on most projects, but may not be able to handle every oddity found
under the sun.

Second, check your project for broken headers. To recursively search your
project directories for the names of all files that lack proper include guards,
use the following command, substituting your project's directory for the
quoted string:

`./checkguard.py -r "source_directory"`

The expected form of an include guard is `FILENAME_EXT`. For example, the
file `BigBadWolf.h` is expected to include a guard `BIGBADWOLF_H`. If your
include guards take some other form, you may need to adjust the `guardSymbol`
in `crules.py`.

If certain files are not supposed to have include guards, feel free to leave
them be. Files without include guards are ignored by this next step.

Now, all that remains is converting the headers to use #pragma once:

`guard2once.py -r "source_directory"`

You're done! Double check that the result matches your expectations and start
using #pragma once in your new code. Know that if you ever need to switch back,
it's as simple as:

`once2guard.py -r "source_directory"`

## Caveats:
There are a few sorts of repositories that could difficult to convert with
guardonce. If you have inconsistent include guard conventions, defining the
expected `guardSymbol` may be tedious. If you've indented your include guards,
that may be a problem as well. Additionally, if you use a mixture of include
guards and pragma once already, checkguard will not be of much help.

These issues and others were identified and fixed on the development branch.
The documentation, however, has not been written and there may yet be some
tweaks to the user interface. When that is done, the result will be released
as guardonce v2.0. There will likely be a beta soon.

This project caught a lot of attention a little earlier than I was expecting.
guardonce v2.0 should 'just work' for far more people than v1.0 does. The
first version was written to convert my own repositories, and the second was
developed to ensure that various open source projects were easy to convert.

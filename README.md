guardonce
=========

Utilities for converting from C/C++ include guards to #pragma once and
back again.

## Why Convert?
Include guards suck. They're tiring to type and tedious to update. Worse, the
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

3. `once2guard` converts files with #pragma once directives back into files
with include guards. This ensures your entire project is consistently using
include guards.

## How to use:
First, check your project for broken headers. To recursively search your
project directories for the names of all files that lack proper include guards,
use the following command, substituting your project's directory for the
quoted string:

`checkguard -r "source_directory"`

By default, checkguard is very forgiving. It accepts either #pragma once or
anything that looks like an include guard. If you know that all your guards
should match some format, you can be more strict by using `-p` to specify
[a pattern](docs/PatternLanguage.md) to check against.

If certain files are not supposed to have include guards, feel free to leave
them be. Files without include guards are ignored by this next step.

Now, all that remains is converting the headers to use #pragma once:

`guard2once -r "source_directory"`

You're done! Double check that the result matches your expectations and start
using #pragma once in your new code. Know that if you ever need to switch back,
it's as simple as:

`once2guard -r "source_directory"`

If you require a specific style for your guards, there are a number of options
to customize guardonce output. A [pair of walkthroughs](docs/Walkthrough.md)
illustrating round-trip conversions of two real-world projects can be found in
the docs.

## How to Install:
Whether you use Python 2 or Python 3, these tools can be installed with
`python -m pip install guardonce`.

It is also possible to instead just run from the repository. However, you'll
need to use slightly different commands to do so. When you're in the source
directory, you can invoke the tools as python modules. For example:

```
git clone https://github.com/cgmb/guardonce.git
cd guardonce
python -m guardonce.checkguard -r ~/myproject
```

Note that on Windows, you may need to invoke guardonce via `python -m` even if
you install with pip.

## [v2.3.0] | 2018-02-05
- Added `*.hxx` to list of header extensions for --recursive
- [[Issue #25]] Added --stdout option

## [v2.2.2] | 2017-10-11
- [[Issue #24]] Fixed once2guard --help

## [v2.2.1] | 2017-10-10
- [[Issue #20]] Fixed --endif-style for UTF-8 files with Python 2
- [[Issue #21]] Fixed handling UTF-8 files on Windows in Python 3
- [[Issue #22]] Improved error reporting for UTF-16 and UTF-32 on Python 3
- [[Issue #23]] Fixed first line of file being ignored for UTF-8 with BOM

## [v2.2.0] | 2017-10-04
- Added support for negative values to 'path' command
- Added 'parents' command to pattern language
- Added option to print guard to checkguard
- [[Issue #16]] Added options to specify #endif style
- [[Issue #19]] The 'path' command's argument is now optional

## [v2.1.0] | 2017-02-14
- Improved heuristics for guessing include guard symbols
- Added 'remove' command to pattern language
- [[Issue #10]] Added option to strip trailing whitespace when removing guards
- [[Issue #14]] Comments immediately following #endif are now accepted
- [[Issue #15]] Include guards with the value 1 are now recognized

## [v2.0.0] | 2016-12-01
- Any include guard pattern is now accepted by default
- Packaged for PyPI
- [[Issue #12]] Added support for Python 3.5
- [[Issue #9]] checkguard no longer warns about files using pragma once
- [[Issue #3]] Added flag to specify the desired include guard convention

## [v1.0.0] | 2016-07-22
- Ex post facto acknowledgement that this project was stable.

[v2.3.0]: https://github.com/cgmb/guardonce/compare/v2.2.2...v2.3.0
[v2.2.2]: https://github.com/cgmb/guardonce/compare/v2.2.1...v2.2.2
[v2.2.1]: https://github.com/cgmb/guardonce/compare/v2.2.0...v2.2.1
[v2.2.0]: https://github.com/cgmb/guardonce/compare/v2.1.0...v2.2.0
[v2.1.0]: https://github.com/cgmb/guardonce/compare/v2.0.0...v2.1.0
[v2.0.0]: https://github.com/cgmb/guardonce/compare/v1.0.0...v2.0.0
[v1.0.0]: https://github.com/cgmb/guardonce/commits/v1.0.0
[Issue #3]: https://github.com/cgmb/guardonce/issues/3
[Issue #9]: https://github.com/cgmb/guardonce/issues/9
[Issue #10]: https://github.com/cgmb/guardonce/issues/10
[Issue #12]: https://github.com/cgmb/guardonce/issues/12
[Issue #14]: https://github.com/cgmb/guardonce/issues/14
[Issue #15]: https://github.com/cgmb/guardonce/issues/15
[Issue #16]: https://github.com/cgmb/guardonce/issues/16
[Issue #19]: https://github.com/cgmb/guardonce/issues/19
[Issue #20]: https://github.com/cgmb/guardonce/issues/20
[Issue #21]: https://github.com/cgmb/guardonce/issues/21
[Issue #22]: https://github.com/cgmb/guardonce/issues/22
[Issue #23]: https://github.com/cgmb/guardonce/issues/23
[Issue #24]: https://github.com/cgmb/guardonce/issues/24
[Issue #25]: https://github.com/cgmb/guardonce/issues/25

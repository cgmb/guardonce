## [v2.1.0] | 2017-02-14
- Improved heuristics for guessing include guard symbols
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

[v2.1.0]: https://github.com/cgmb/guardonce/compare/v2.0.0...v2.1.0
[v2.0.0]: https://github.com/cgmb/guardonce/compare/v1.0.0...v2.0.0
[v1.0.0]: https://github.com/cgmb/guardonce/commits/v1.0.0
[Issue #3]: https://github.com/cgmb/guardonce/issues/3
[Issue #9]: https://github.com/cgmb/guardonce/issues/9
[Issue #10]: https://github.com/cgmb/guardonce/issues/10
[Issue #12]: https://github.com/cgmb/guardonce/issues/12
[Issue #14]: https://github.com/cgmb/guardonce/issues/14
[Issue #15]: https://github.com/cgmb/guardonce/issues/15

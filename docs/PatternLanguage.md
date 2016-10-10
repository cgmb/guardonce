# Pattern Language
A pattern description is made up of a series of pipeline stages. It starts with
a source to provide the initial string, which then goes through a bunch of
filters that modify it. After the last filter, all characters that cannot exist
in include guards are replaced with `_`.

Filters are separated by `|`. Filters can take arguments, which are separated
by spaces. Strings generally do not need to be quoted, unless they contain `|`,
whitespace or start with `@` (which is reserved).

## Sources
### name
returns the file's basename

### path
if recursive, returns the file's path relative to the root directory given to
the program. if not recursive, returns the path to the file given when
invoking the program.

takes an optional argument specifying how many parent directories to include.

e.g. `path 1`  does `src/Regex/Match.h -> Regex/Match.h`

## Filters
### upper
returns the input, converted to uppercase

e.g. `Match.h -> MATCH.H`

### lower
returns the input, converted to uppercase

e.g. `Match.h -> match.h`

### pascal
converts snake_case to PascalCase

e.g. `sprite_animator.h -> SpriteAnimator.h`

### snake
converts PascalCase to snake_case

e.g. `SpriteAnimator.h -> sprite_animator.h`

### replace
substitutes one character for another

e.g. `replace . _`  does `Match.h -> Match_h`

### append
appends the given string to the end of the input

e.g. `append __`  does `Match.h -> Match.h__`

### prepend
prepends the given string to the beginning of the input

e.g. `prepend __`  does `Match.h -> __Match.h`

### surround
surround the input with the given string

e.g. `surround __`  does `Match.h -> __Match.h__`

## Sink
### raw
if the pipeline ends in a raw sink, then the normal substitution of illegal
characters by _ is suppressed

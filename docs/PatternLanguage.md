# Pattern Language
A pattern description is made up of a series of pipeline stages. It starts with
a source to provide the initial string, which then goes through a bunch of
filters that modify it. After the last filter, all characters that cannot exist
in include guards are replaced with `_`.

Filters are separated by `|`. Filters can take arguments, which are separated
by spaces. Strings generally do not need to be quoted, unless they contain `|`
, `'`, `"`, or whitespace. Either `'` or `"` can be used to quote.

Feedback on the language is appreciated. If you have a real-world project which
uses a guard pattern that is difficult to specify, please open an issue.

## Sources
### name
returns the file's basename

### path
if recursive, returns the file's path relative to the root directory given to
the program. if not recursive, returns the path to the file given when
invoking the program.

takes an optional argument specifying how many parent directories to include.
negative values instead specify how many parent directories to remove.
when provided, the result is equivalent to `path | parents <N>`.

e.g. `path 1` does `proj/src/Regex/Match.h -> Regex/Match.h`
     `path -1` does `proj/src/Regex/Match.h -> src/Regex/Match.h`
     `path -2` does `/workspace/proj/src/Regex/Match.h -> src/Regex/Match.h`

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
substitutes one string for another

e.g. `replace M Sw`  does `Match.h -> Swatch.h`

### remove
removes all occurrences of a string

e.g. `remove t`  does `Match.h -> Mach.h`

### append
appends the given string to the end of the input

e.g. `append _included`  does `Match.h -> Match.h_included`

### prepend
prepends the given string to the beginning of the input

e.g. `prepend included_`  does `Match.h -> included_Match.h`

### surround
surround the input with the given string

e.g. `surround xx`  does `Match.h -> xxMatch.hxx`

### parents
takes an argument specifying how many parent directories to keep.
negative values instead specify how many parent directories to remove.

e.g. `path | parents 1` does `proj/src/Regex/Match.h -> Regex/Match.h`
     `path | parents -1` does `proj/src/Regex/Match.h -> src/Regex/Match.h`
     `path | parents -2` does `/workspace/proj/src/Regex/Match.h -> src/Regex/Match.h`

## Sink
### raw
if the pipeline ends in a raw sink, then the normal substitution of illegal
characters by `_` is suppressed

## Usage Notes
You may want to consider the rules for valid guards. In the global namespace,
both the C and C++ languages reserve all names that:
* start with an underscore
* contain two underscores in a row

These should be avoided.

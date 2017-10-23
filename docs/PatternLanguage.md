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
Returns the file's basename.

### path
Returns the file's relative path.

Takes an optional argument specifying how many parent directories to include or
remove. With no argument, all parent directories are included. A positive
argument includes that many directories and removes all others, while a negative
argument removes that many directories and includes all others. When an
argument is provided, `path <N>` is equivalent to `path | parents <N>`.

Negative arguments are particularly useful for trimming off parts of the
relative path that were merely for navigating to the project root directory.

| Command |       File        |      Output       |
|---------|-------------------|-------------------|
| path    | src/Regex/Match.h | src/Regex/Match.h |
| path 0  | src/Regex/Match.h | Match.h           |
| path 1  | src/Regex/Match.h | Regex/Match.h     |
| path 2  | src/Regex/Match.h | src/Regex/Match.h |
| path -1 | src/Regex/Match.h | Regex/Match.h     |
| path -2 | src/Regex/Match.h | Match.h           |

## Filters
### upper
Returns the input, converted to uppercase.

|  Input  | Output  |
|---------|---------|
| Match.h | MATCH.H |

### lower
Returns the input, converted to lowercase.

|  Input  | Output  |
|---------|---------|
| Match.h | match.h |

### pascal
Converts snake_case to PascalCase.

|       Input       |      Output      |
|-------------------|------------------|
| sprite_animator.h | SpriteAnimator.h |

### snake
Converts PascalCase to snake_case.

|       Input      |      Output       |
|------------------|-------------------|
| SpriteAnimator.h | sprite_animator.h |

### replace
Substitutes one string for another.

|   Command    |  Input  |  Output  |
|--------------|---------|----------|
| replace M Sw | Match.h | Swatch.h |

### remove
Removes all occurrences of a string.

| Command  |  Input  | Output |
|----------|---------|--------|
| remove t | Match.h | Mach.h |

### append
Appends the given string to the end of the input

|  Command  |  Input  |  Output   |
|-----------|---------|-----------|
| append pp | Match.h | Match.hpp |

### prepend
Prepends the given string to the beginning of the input

|  Command   |  Input  |  Output   |
|------------|---------|-----------|
| prepend Re | Match.h | ReMatch.h |

### surround
Surround the input with the given string

|  Command   |  Input  |  Output   |
|------------|---------|-----------|
| surround x | Match.h | xMatch.hx |

### parents
Trims an input file path. Takes an argument specifying how many parent
directories to keep. Negative values instead specify how many parent
directories to remove.

|  Command   |       Input       |      Output       |
|------------|-------------------|-------------------|
| parents 0  | src/Regex/Match.h | Match.h           |
| parents 1  | src/Regex/Match.h | Regex/Match.h     |
| parents 2  | src/Regex/Match.h | src/Regex/Match.h |
| parents -1 | src/Regex/Match.h | Regex/Match.h     |
| parents -2 | src/Regex/Match.h | Match.h           |

## Sink
### raw
If the pipeline ends in a raw sink, then the normal substitution of illegal
characters by `_` is suppressed.

## Usage Notes
You may want to consider the rules for valid guards. In the global namespace,
both the C and C++ languages reserve all names that:
* start with an underscore
* contain two underscores in a row

These should be avoided.

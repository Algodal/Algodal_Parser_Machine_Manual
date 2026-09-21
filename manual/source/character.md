# Character

APM reads UTF-8, and a "character" means one **grapheme cluster** — what a
reader would point at as a single character, however many bytes or code points
it takes. There are three ways to match one: the `char` action, a **character
block**, or a **character literal**.

## The `char` action

`char` matches any one character, as long as there is text left. It takes no
parentheses.

```parser
A = char; # parses a single utf-8 character
```

## Character block

A character block matches one character **if it belongs to the set** written
between angle brackets. The set is a list of characters, ranges and escapes run
together, with no separator between them:

```parser
A = <A:Z>;       # one character, A through Z
B = <aeiou>;     # one vowel
C = <A:Za:z_>;   # a letter or an underscore -- two ranges and a character
D = <\x41:5A>;   # the same as <A:Z>, written in hex
```

:::{important}
A block is **not** a regular expression. There is no `*`, no `.`, no
alternation and no anchoring inside one — it is a set of characters and nothing
more. Repetition comes from a [Counter](counter.md) placed outside the block,
as in `<A:Z>+`.
:::

:::{note}
Ranges inside a block use a colon (`:`), *not* a hyphen — so `A` to `Z` is
written `<A:Z>`, and `0` to `9` is `<0:9>`.
:::

## Character Literal

A character literal names a character by its code: `\x` for hex, `\u` for a
Unicode code point. Chain several with `,`, and give a range with `:`.

```parser
A = \x41; # parses for A
B = A; # the same character, as a code point
C = \x43 \x41 \x54; # parses "CAT"
D = \x43,41,54; # parses "CAT" | short-cut for chaining characters
E = \x41:5A; # parses from A to Z | range is also supported
```

Character literals can also be used inside of blocks, which is how an awkward
character gets into a set:

```parser
F = <\x09 >; # a tab or a space
```

:::{seealso}
A literal used in several places is worth naming — see [Alias](alias.md).
The same range notation appears in [Counters](counter.md) and in `::part` on a
[Parser Result Function](parser_result_function.md).
:::

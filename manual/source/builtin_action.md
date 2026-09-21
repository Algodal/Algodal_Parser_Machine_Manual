# Built-in Function

Four things are matched so often that APM builds them in. They are functions,
not actions you declare: write the name, with no parentheses.

| Action | Matches |
| :--- | :--- |
| `spc` | one space or tab |
| `nl` | one line break |
| `eol` | the end of a line: a line break, or the end of the input |
| `eof` | the end of the input, matching **zero width** |

```parser
line := <A:Z>+ . eol;
last := <A:Z>+ . eof;
```

## `eol` and `eof`

`eol` succeeds at a line break **or** at the end of the input, and consumes the
line break when that is what it found. `eof` succeeds only where there is
nothing left, and consumes nothing — it is a check on position, not a match on
text.

So `eol` is what a line-oriented grammar wants, and `eof` is how you insist the
whole input was used.

:::{seealso}
`spc` and `nl` are what usually fill an [Inbetween](inbetween.md) block. They
save you writing your own space and newline parsers, which is all they are for
— using them is entirely optional.

All four names are [reserved](keywords.md), so no action of yours may be called
`spc`, `nl`, `eol` or `eof`.
:::

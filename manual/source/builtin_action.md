# Built-in Action

Four things are matched so often that APM builds them in. They are ordinary
units: write the name, with no parentheses.

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

## `eol` and `eof` are not the same

`eol` succeeds at a line break **or** at the end of the input, and consumes the
line break when that is what it found. `eof` succeeds only where there is
nothing left, and consumes nothing — it is a check on position, not a match on
text.

So `eol` is what a line-oriented grammar wants, and `eof` is how you insist the
whole input was used.

## Skipping, not matching

Built-in actions are for grammar you mean. To ignore whitespace *between*
things, the tool is [Inbetween](inbetween.md) — the `.` operator and the block
that says what it skips:

```parser
stmt = "(" . "A" . ")";
. { spc, nl }
```

Writing `spc*` between every pair of units does the same job far more loudly,
and fills the tree with the results.

:::{seealso}
`spc` and `nl` are the usual contents of the `.` config block. All four names
are [reserved](keywords.md), so no action of yours may be called `spc`, `nl`,
`eol` or `eof`.
:::

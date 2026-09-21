# Text Function

A text function matches **text** at the cursor by a rule other than "these exact
characters". All three are written under the `tex` namespace.

| Function | Matches |
| :--- | :--- |
| `order` | as many characters as the argument has, in **any order** |
| `oneof` | **one** character, from those in the argument |
| `icase` | the argument exactly, ignoring case |

```parser
A = tex::order("ABC"); # "BCA" and "CAB" match; "ABD" does not
B = tex::oneof("ABC"); # one character: A, B or C
C = tex::icase("ABC"); # "abc", "AbC", "ABC"
```

## Chaining

The calls chain, and each one narrows how the match is made:

```parser
D = tex::icase::oneof("aeiou");   # one vowel, either case
```

:::{seealso}
`order` is the character-level counterpart of [Permutation](permutation.md),
which does the same for units. `oneof` overlaps with a
[character block](character.md) — `tex::oneof("abc")` and `<abc>` match the
same thing, and the block is usually the clearer of the two.

`tex`, `order`, `oneof` and `icase` are [reserved words](keywords.md).
:::

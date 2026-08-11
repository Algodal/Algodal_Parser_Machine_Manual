# Character

There are 3 ways to parse a character in APM: the `char` function, the **regex block**, or a **character literal**.

## Character Function

The `char` function returns any character as long as there is incoming text. No `()` is required to call it.

```parser
A = char; # parses a single utf-8 character
```

## Regex Block

A regex block returns a character only if it matches the pattern inside the block. The block is written between angle brackets (`<>`), and any valid regex pattern can go between them.

```parser
A = <A:Z>; # parses a character if it is from A to Z.
```

:::{note}
Ranges inside a regex block use a colon (`:`), *not* a hyphen — so `A` to `Z` is written `<A:Z>`, and `0` to `9` is `<0:9>`.
:::

## Character Literal

A character literal is a representation of the literal character. It can be represented in hex or unicode form.
It uses `\x` for hex and `\u` for unicode. You can chain characters into a text using `,`, and you can create ranges using `:`.

```parser
A = \x41; # parses for A
B = \x43 \x41 \x54; # parses "CAT"
C = \x43,41,54; # parses "CAT" | short-cut for chaining characters
D = \x41:5A; # parses from A to Z | range is also supported
```

Character literals can also be used inside of blocks.
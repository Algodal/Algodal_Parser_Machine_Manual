# Character

There are 3 ways to parse a character in ATPG: using `char` function, the **regex block** or **character literal**.

## Character Function

Character function will return any character as long there is incoming text. No `()` required for the function.

```
A = char; # parses a single utf-8 character
```

## Regex Block

Regex block only returns a character if it matches one of the pattern in the regex block. The block is defined with angle brackets (`<>`). There are special patterns such as ranges with the `:`.

```
A = <A:Z>; # parses a character if it is from A to Z.
```

## Character Literal

A character literal is a representation of the literal character. It can be represented in hex or unicode form.
It uses `\x` for hex and `\u` for unicode. You can chain characters to create a text using `,`. You can also create ranges using `:`.

```
A = \x41; # parses for A
B = \x43 \x41 \x54; # parses "CAT"
C = \x43,41,54; # parses "CAT" | short-cut to chaining characters
D = \x41:5A; parses from A to Z | range is also supported
```

Character literals can also be used inside of blocks.
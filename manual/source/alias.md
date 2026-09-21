# Alias

An alias gives a **name** to a **value**. Wherever the name appears, the value
is dropped in its place — the alias itself never reaches the compiled parser.

A character literal and its chains and ranges, a character block, a number and
a text literal can all be aliased.

```parser
program example;

alias letter <A:Z>;        # character block
alias code \x41;           # character literal
alias bigcode \x41:43;     # range
alias chaincode \x41,42,43,44;  # chain
alias limit 100;           # number
alias animal "CAT";        # text

A = letter;
B = animal;
```

## Where a number alias goes

A number matches nothing, so a number alias is not a unit. It belongs where a
number is wanted — a [counter](counter.md) bound, a
[logic block](logic_block.md) or a variable:

```parser
alias width 4;

field = char-width;          # a counter bound
check = {x < width};         # logic
numval w = width;            # a global's initial value
```

Writing `A = width;` is refused, for the same reason writing `A = 4;` is:
neither says anything a parser could match.

:::{note}
An alias is a substitution, not an indirection. `alias tab \x09;` puts the tab
character itself everywhere `tab` is written, so the parser is exactly the one
you would have got by typing the value out.
:::

:::{seealso}
An alias name shares the name space actions live in, so it may not be a
[reserved word](keywords.md), and no action may share its name.
:::

# Inbetween

Because APM lexes and parses at once, there is no token pass to quietly throw
whitespace away. Instead you say **where** skipping is allowed, with `.`, and
**what** gets skipped, in a block named by the same `.`.

```parser
stmt = "(" . "A" . ")";

. {
    spc, nl
}
```

At every `.`, everything in the config list is matched repeatedly until none of
them matches any more. Then the parse carries on.

## Why it is written, not inserted

A tool that skipped whitespace everywhere could not describe a token. Because
`.` is something you write, the same language describes both:

```parser
number = <0:9>+;          # no `.` -- digits are adjacent, "1 2" is two numbers
sum   := number . "+" . number;   # `.` -- "1 + 2" and "1+2" both parse
```

That is the whole difference between a lexer rule and a grammar rule in APM.

## Where it is easy to forget

Neither a counter nor a permutation skips between its repetitions or members.
Put the `.` inside the thing being repeated:

```parser
list := item+;          # items with nothing between them
list := (item .)+;      # items separated by the skip
attrs = perm[(a .) (b .)];
```

And the parser loop does not skip between runs of the start grammar — see
[Parser](parser.md).

:::{important}
If `.` appears anywhere in your grammar you **must** define the `.` config
block. There is no default skip set.
:::

:::{seealso}
[Built-in Actions](builtin_action.md) are what usually fill the block. See
[Samples](samples.md) for `.` in a complete parser.
:::

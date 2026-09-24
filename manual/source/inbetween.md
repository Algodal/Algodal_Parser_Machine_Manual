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

**What the skip matches never reaches the AST.** It is consumed and dropped, so
whitespace and comments do not turn up as nodes you then have to ignore.

## Why it is written, not inserted

A tool that skipped whitespace everywhere could not describe a token. Because
`.` is something you write, the same language describes both:

```parser
number = <0:9>+;          # no `.` -- digits are adjacent, "1 2" is two numbers
sum   := number . "+" . number;   # `.` -- "1 + 2" and "1+2" both parse
```

That is the whole difference between a lexer rule and a grammar rule in APM.

## Skipping up to something

`.` takes everything the config list allows, and a line end is usually in that
list. Sometimes you want the rest of it but not that:

```parser
line := (word (. ^ nl) word);      # skip, but stop before the line end
line := (word .::until(nl) word);  # skip, and take the line end too
```

A counted `.` repeats **one** unit of the config list at a time, so the
terminator gets asked before the newline is swallowed. Written on its own, `.`
runs the whole list until none of it matches -- which is what it has always
done, and what every other `.` in your grammar still does.

The terminator does not have to be in the config list at all:

```parser
line := (word (. ^ ";") word);     # skip whitespace up to a semicolon
```

:::{important}
`.` is already "as much as there is", so a counter written on it says the same
thing twice and is refused: `.*`, `.+` and `.?` are errors. Write `.` on its
own.
:::

See [Counter](counter.md) for `^` and `::until` in general.

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

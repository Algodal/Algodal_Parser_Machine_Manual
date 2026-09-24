# Counter

A counter repeats the same parse. It is written after the unit it repeats,
using `+`, `*`, `?`, `-<number>` or `-<number>:<number>`.

```parser
<A:Z>+;
```

The above reads "one or more A to Z".

| Counter | Description |
| :--- | :--- |
| `+` | one or more |
| `*` | zero or more |
| `?` | zero or one (optional) |
| `-<number>` | exactly `<number>` |
| `-<number>+` | that many **or more** |
| `-<number>:<number>` | at least the first, at most the second |

```parser
<A:Z>+;
<A:Z>*;
<A:Z>?;
<A:Z>-5;
<A:Z>-5+;
<A:Z>-7:12;
```

A bound may be a **name** as well as a number, which is how a grammar counts
something it only learns while parsing:

```parser
numvar width = 4;
field = char-width;   # exactly `width` characters
```

## A counter does not skip

Repetition puts no [inbetween](inbetween.md) between the repetitions. If the
items can be separated, say so, by putting the `.` inside the group being
counted:

```parser
list := item+;        # items with nothing between them
list := (item .)+;    # items separated by the skip
```

## Counting what happened

`::iter_steps` answers with the number of times a counter ran:

```parser
n = <A:Z>+::iter_steps;        # how many characters matched
m = (A B C)-5:10::iter_steps;  # how many times the series ran
```

It is a **producer**: it answers with a number and never fails anything, so it
is useful where a number is wanted. For the number of *characters* matched,
which is a different question, use `::char_count`.

## When a counter starves what follows it

A counter takes all it can and then stops looking. So the unit **after** one is
left with nothing when it wants the same text:

```parser
z := X+ B;     # if B can also be an X, this never matches
z := . nl;     # with nl in the skip set, the skip eats every newline
```

Two different problems, with two different answers.

When the unit after the counter is **exactly the counter's base**, there is
nothing to decide. `A+ A` means "two or more A", and so does `A A+`, because
greed runs left to right — put the fixed unit first and it takes its match
before the counter gets greedy. The compiler does that swap for you.

When the two only **overlap**, no rewrite exists. Then you tell the counter
what to stop at, and it stops there the first time rather than taking too much
and being asked for some back.

## Stopping at something

Two spellings, and they differ in one thing: who owns the terminator.

```parser
body = char*::until("-->");      # the "-->" is part of what the counter matched
tail = (char* ^ "-->");          # the "-->" is the next unit, and its own node
```

`::until(B)` reads "repeat until B, and take B too". The `^` glue — read
**Less**, because the counter takes less than it could so the unit after it can
have some — leaves B outside. The parentheses are required: it is two units,
and they say where the pair ends.

Both work with any counter that could stop early:

```parser
char*::until("]]>")       # none or more
char+::until("]]>")       # at least one
char-4+::until("]]>")     # at least four
char-2:8::until("]]>")    # between two and eight
```

An **exact** count is refused — `char-3::until("x")` already knows how many it
wants, so there is nothing to stop early about.

This is what every `Char* - (Char* ']]>' Char*)` in a specification means: any
characters, so long as this sequence is not among them. Written directly:

```parser
comment := ("<!--" char*::until("-->"));
cdata   := ("<![CDATA[" char*::until("]]>"));
```

The counter asks the terminator **before** each repetition, so it stops at the
first one, and nothing is ever matched and then given back.

### The skip stops at things too

`.` is the one base that arrives already repeated -- it takes every unit of the
inbetween config there is -- so it needs no counter written on it:

```parser
line := (word (. ^ nl) word);      # skip, but stop before the line end
line := (word .::until(nl) word);  # skip, and take the line end too
```

Under `^` or `::until` a `.` repeats **one** config unit at a time, which is
what lets the terminator be asked before a newline is swallowed. Writing `.*`
or `.+` says the same thing twice and is refused. See
[Inbetween](inbetween.md).

:::{seealso}
The counters are described with the rest of the chain in
[Parser Result Function](parser_result_function.md). `::per` asks the rest of a
chain of **each** repetition rather than of the whole run.
:::

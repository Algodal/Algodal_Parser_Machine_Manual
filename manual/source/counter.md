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
| `-<number>:<number>` | at least the first, at most the second |

```parser
<A:Z>+;
<A:Z>*;
<A:Z>?;
<A:Z>-5;
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

When the two only **overlap**, no rewrite exists, and you say so with
`give[ ]`:

```parser
z := give[X+ B];    # X repeats, then hands one back so B can have it
z := give[. nl];    # the skip stops short, leaving a newline for nl
```

`give` takes exactly two units. The first must be a counter or the `.` skip —
there is nothing else to give back. The repeated unit is parsed once; only the
unit after it is retried, one repetition further back each time, and never past
the counter's minimum.

:::{seealso}
Both are described with the rest of the chain in
[Parser Result Function](parser_result_function.md). `::per` asks the rest of a
chain of **each** repetition rather than of the whole run.
:::

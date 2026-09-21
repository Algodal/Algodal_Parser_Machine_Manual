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
numval width = 4;
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

:::{seealso}
Both are described with the rest of the chain in
[Parser Result Function](parser_result_function.md). `::per` asks the rest of a
chain of **each** repetition rather than of the whole run.
:::

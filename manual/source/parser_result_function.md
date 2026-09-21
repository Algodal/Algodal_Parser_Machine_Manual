# Parser Result Function

Once a unit has matched, a **result function** asks something about what it
matched, or turns it into a number. The calls are written after the unit with
`::`, and they **chain** — each one acts on what the one before produced.

```parser
name = <A:Za:z>+;
t = name::part(3:4)::is("ed");   # are characters 3 and 4 "ed"?
```

There are two kinds.

A **predicate** asks a question and can only pass or fail the unit it is
attached to. A **producer** answers with a number instead, and never fails
anything — so it is only useful where a number is wanted.

## Predicates

| Function | Passes when the matched text |
| :--- | :--- |
| `is` | equals the argument |
| `not` | does not equal the argument |
| `subkind` | contains the argument |

```parser
t1 = name::is("Fred");        # equals "Fred"
t4a = name::not("Amber");     # is not "Amber"
t2 = name::subkind("Fr");     # contains "Fr"
```

The argument is a **grammar**, not a value — it is run over the text the unit
matched, by the same machine that matched it. So anything that can parse can be
an argument:

```parser
t4b = char::not(\x41);                 # a character literal
t4c = char::not(tex::oneof("hello"));  # a text function
t4d = name::is(word);                  # another action
t4e = name::is(B+ C* "a");             # a whole series
```

## Narrowing with `part`

`part` cuts the text down before the rest of the chain asks about it. It is
**1-indexed** and counts **characters**.

```parser
t3a = name::part(1);          # the first character
t3b = name::part(1:4);        # characters 1 through 4
t3c = name::part(2+);         # character 2 to the end
t3d = name::part(1)::is("F"); # chained: is the first character "F"?
```

## Producers

Producers take no parentheses, because they take no argument.

| Function | Answers with |
| :--- | :--- |
| `char_count` | how many characters were matched |
| `to_num` | the matched text read as a number; `0` if it is not one |
| `iter_steps` | how many times a counter ran; `1` if uncounted, `0` if none |

```parser
c = name::char_count;
v = number::to_num;
i = <A:Z>+::iter_steps;
```

A producer can be compared against a **number**, which is how a chain ends in a
question again:

```parser
exactly3 = name::char_count::is(3);
two_hundred = number::to_num::is(200);   # so "0200" matches too
within = name::char_count::is(limit);    # ... or against a numval
```

Or captured into a variable:

```parser
C := (n::to_num => numval v);
```

## `per` — ask of each repetition

`per` leads a chain on a **counted** unit and turns the question around: the
rest of the chain is asked of each repetition rather than of the whole run.

```parser
q = char*::per::not(\x22);   # every character must not be a quote
```

Without it, `char*::not(\x22)` asks whether the *whole run* differs from a
single quote, which is almost never the question.

## Semvar and scope calls

The same `::` is how a [semvar](variable.md) and a [scope](variable.md) are
reached — `kind::first`, `blk::begin`, `blk::end`.

:::{seealso}
Every function named here is a [reserved word](keywords.md).
:::

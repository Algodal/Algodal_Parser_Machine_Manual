# Permutation

A series can be matched as a **permutation** with `perm`, which takes its
members in *any order* — each one exactly once. The members go in `[]`.

```parser
A = perm["A" "B" "C"];
```

That matches `ABC`, `CAB`, `BCA` and the three others, and fails if any member
is missing or repeated.

Anything a series can hold, a perm can hold — the members are ordinary units,
so groups, counters and actions are all fair game:

```parser
# three named actions, in any order
head := perm[title author date];

# a group as a member, so one of the three is itself a choice
flags := perm[("r" | "w") "x" "s"];

# a counted member: the digits may come before or after the letters
code  := perm[<A:Z>+ <0:9>+];
```

Each member is taken **exactly once**. `perm["A" "B"]` matches `AB` and `BA`,
and fails on `A`, on `ABB` and on `AA`.

Where a series would be written with the members in a fixed order, a perm is
the same grammar with that order relaxed — which is why it is usually the right
tool for attributes, record fields and command-line style flags.

:::{important}
A perm does **not** skip between its members. If they can be separated, put the
[inbetween](inbetween.md) in yourself:

```parser
attrs = perm[(name .) (size .) (color .)];
```
:::

:::{seealso}
For characters in any order rather than units, see `tex::order` in
[Text Function](text_function.md). `perm` is a [reserved word](keywords.md).
:::

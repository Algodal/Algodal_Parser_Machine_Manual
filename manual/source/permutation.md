# Permutation

A series can be matched as a **permutation** with `perm`, which takes its
members in *any order* — each one exactly once. The members go in `[]`.

```parser
A = perm["A" "B" "C"];
```

That matches `ABC`, `CAB`, `BCA` and the three others, and fails if any member
is missing or repeated.

Anything a series can hold, a perm can hold — the members are ordinary units.

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

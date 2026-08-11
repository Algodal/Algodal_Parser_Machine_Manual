# Counter

A counter repeats the same parse multiple times. It uses the symbols `+`, `*`, `?`, `-<number>`, and `-<number>:<number>` (range).

```parser
<A:Z>+;
```
The above is read "one or more A to Z".

| Count Operator Face | Description |
| :--- | ---: |
| `+` | one or more |
| `*` | zero or more |
| `?` | zero or one (optional) |
| `-<number>` | exactly `<number>` |
| `-<number>:<number>` | at least `<number>` up to `<number>` |

```parser
<A:Z>+;
<A:Z>*;
<A:Z>?;
<A:Z>-5;
<A:Z>-7:12;
```

:::{seealso}
The number of times a counter repeated is available through the `::count` result function — see [Parser Result Function](parser_result_function.md).
:::

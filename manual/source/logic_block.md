# Logic Block

A logic block lets you specify non-parsing logic — typically mathematical logic — inside an action. It is written between curly braces `{}`. The block succeeds when its logic evaluates to true and fails otherwise, so it can control whether an action parses.

```parser
A = {5 * 5 == 20};
B = char >> numval x >> numval y {y = 15; x * y == 65};
```

In action `A`, the logic `5 * 5 == 20` is false, so `A` fails. In action `B`, a character is parsed and assigned to `x`, `y` is set to `15`, and the block succeeds only if `x * y == 65`.

:::{seealso}
Logic blocks are also used as the condition of an [IF statement](if_statement.md), and they read values captured into [Variables](variable.md) with `>>`.
:::

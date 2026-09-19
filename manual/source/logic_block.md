# Logic Block

A logic block lets you specify non-parsing logic — typically mathematical logic — inside an action. It is written between curly braces `{}`. The block succeeds when its logic evaluates to true and fails otherwise, so it can control whether an action parses.

```parser
A = {5 * 5 == 20};
B = char => numval x char => numval y {y = 15; x * y == 65};
```

In action `A`, the logic `5 * 5 == 20` is false, so `A` fails. In action `B`, a character is parsed and assigned to `x`, `y` is set to `15`, and the block succeeds only if `x * y == 65`.

## Operators

Precedence follows C, tightest binding first: `NOT`, then `*` `/`, then `+` `-`,
then `<` `<=` `>` `>=`, then `==` `!=`, then `AND`, then `OR`. Brackets override
it. Division by zero is `0`, and `a - b` clamps at `0` rather than wrapping.

Text compares by bytes, and `==` and `!=` are the only operators it has —
arithmetic over text is refused when the grammar is validated, not at run time.

`AND` and `OR` **short-circuit**, the way C's `&&` and `||` do: the right side is
not evaluated when the left side has already settled the answer.

## Stopping the parse with `error()`

Every other failure in the machine means *"this did not match here"*, and it
sends whatever was trying alternatives on to the next one. `error("...")` means
something else: the input is wrong, and there is nothing else to try.

```parser
z := (word => texval x) {x == "cat" OR error("only cats here")};
```

It travels straight out of options, series, counters, permutations and `if`
conditions rather than being retried around, ends the run, and the message it
was given becomes the run's error. Because `OR` short-circuits, the example
above says nothing at all for a cat and stops for a dog.

`{{ ... }}` does not absorb it either. A final block always holds — but holding
is an *answer*, and `error()` does not give one.

:::{note}
A message is text. `error(5)` is refused when the grammar is validated.
:::

:::{seealso}
Logic blocks are also used as the condition of an [IF statement](if_statement.md), and they read values captured into [Variables](variable.md) with `=>`.
:::

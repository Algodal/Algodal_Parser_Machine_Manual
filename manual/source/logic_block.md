# Logic Block

A logic block tests **values** rather than text. It reads no input and moves no
cursor: it succeeds or it fails, and consumes nothing either way. That is what
lets a grammar decide something instead of merely matching it.

It is written between curly braces.

```parser
A = {5 * 5 == 20};
B = (char => numvar x) . (char => numvar y) . {y = 15; x * y == 65};
```

`A` fails, because `5 * 5 == 20` is false. In `B` two characters are captured,
`y` is set to `15`, and the block succeeds only if `x * y == 65`.

## What a block answers

A logic block answers **true or false**, and true is the default.

Statements are separated by `;`, and the **last one's value is the block's
answer**. A statement that produced no value — an assignment, a cleared set —
is a deed rather than an answer, and a deed is no reason to fail. So a block
whose last statement is an assignment holds.

```parser
{x == "cat"}          # answers the comparison
{y = 15; x * y == 65} # a deed, then an answer
{y = 15}              # only a deed -- holds
```

## The final block

`{{ ... }}` is a **final block**. It runs for what it does, and its result is
not checked — it always holds.

```parser
B := "a" . {{9 => n}};
```

Use it when the point is the effect rather than the verdict: setting a
variable, clearing a set, counting something. Nothing may follow a final block
in the grammar, because there is no outcome for the rest to depend on.

The difference in one line: an ordinary block can fail the action it sits in, a
final block cannot.

## Operators

Precedence follows C, tightest binding first: `NOT`, then `*` `/`, then `+`
`-`, then `<` `<=` `>` `>=`, then `==` `!=`, then `AND`, then `OR`. Brackets
override it.

```parser
NOT a
a * b   a / b    # division by zero is 0
a + b   a - b    # a - b clamps at 0 rather than wrapping
a < b   a <= b   a > b   a >= b
a == b  a != b
a AND b
a OR b
TRUE  FALSE      # one and zero
```

`AND` and `OR` **short-circuit**, the way C's `&&` and `||` do: the right side
is not evaluated when the left has already settled the answer.

Text compares by bytes, and `==` and `!=` are the only operators it has —
arithmetic over text is refused when the grammar is validated, not at run time.

## Asking about a semvar

```parser
set::is(t)     # is t a member?
set::not(t)    # is it not?
set::clear     # empty the set -- a deed, so it holds
```

:::{seealso}
A logic block is also the condition of an [IF statement](if_statement.md), and
it reads values put into [Variables](variable.md) with `=>`. To stop the parse
outright rather than fail a match, see [System Functions](system_function.md).
:::

# System Functions

A system function acts on the **parse itself** rather than on text. There is
one.

## `error("...")`

Every other failure in APM means *"this did not match here"*, and it sends the
machine looking for another reading — the next alternative, a shorter counter,
a different order. `error()` means something different: the input is wrong, and
there is nothing else to try.

```parser
z := (word => texvar x) . {x == "cat" OR error("only cats here")};
```

It travels straight out of options, series, counters, permutations and `if`
conditions rather than being retried around. The run ends, and the message
becomes the run's error.

Because `OR` short-circuits, the example above says nothing at all for a cat
and stops for a dog.

## It is not absorbed

A [final block](logic_block.md) always holds — but holding is an **answer**,
and `error()` does not give one. So `{{ ... }}` does not swallow it either.

## Why you want it

Without `error()`, a grammar that has recognised a real mistake can only fail,
and failing is an invitation for the machine to try something else. The parse
then limps on and reports confusion somewhere later, far from the actual
problem. `error()` reports it where it was found.

:::{note}
A message is text. `error(5)` is refused when the grammar is validated.
:::

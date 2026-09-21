# IF Statement

`if` branches the parse — on a test, or on whether something parses at all.

```parser
if (cond) [then | else]     # both branches
if (cond) [then]            # then only
if (cond) [| else]          # else only
```

## A logic condition

```parser
numvar x = 0;

A := (char::to_num => x) . if ({x == 1}) [T | F];
```

The block is a test. It reads no input and moves nothing, it only answers.

## A grammar condition

The condition may be grammar instead, and then the question is simply "did it
match?":

```parser
E := G . if (M) [T | F];   # if M parses, parse T, else F
H := I . if (M) [T];       # if M parses, parse T
J := K . if (M) [| F];     # if M does not parse, parse F
```

:::{important}
A grammar condition **consumes** what it matched. `M` is not a lookahead — it
really parses, and its nodes are as real as any other unit's.
:::

With no branch to take, an `if` behaves like `E?`: the cursor sits where it was
and the next unit is read.

:::{seealso}
Conditions are usually [Logic Blocks](logic_block.md), and they read values put
into [Variables](variable.md) with `=>`. `if` is a
[reserved word](keywords.md).
:::

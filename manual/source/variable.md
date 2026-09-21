# Variables

A variable keeps something a rule already matched, so a later part of the
grammar can use it again. This is what turns a grammar from a shape into a
grammar that can *check* things.

There are two variable types and one set type:

| Keyword | Holds |
| :--- | :--- |
| `texvar` | a span of text |
| `numvar` | a number, `0` upward — no negatives, no decimals |
| `semvar` | a **set** of text the grammar builds and later matches against |

## Capturing with `=>`

Inside an action, `(unit => target)` runs the unit and keeps what it matched.
The target is either a new declaration or a variable already in hand:

```parser
A := (word => texvar x) x;             # capture, then require the same text again
B := (word => texvar x) (word => x);   # declare once, assign again
C := (n::to_num => numvar v);          # a producer fills a numvar
```

A variable must be assigned on **every** path that reaches a read, or the
grammar is refused. Nothing is zeroed, so there is no safe stale value to fall
back on.

An alternative that assigns and then loses is rolled back. Only the winning
alternative's assignments survive a choice.

## Globals

A global is declared at the top level and lives for the whole parse. It must be
given an initial value:

```parser
texvar greeting = "Hello World";
numvar limit = 50;
```

The initial value is set once, before any input is read — so writing `greeting`
in a grammar matches that text until something assigns over it.

## Local scope

A variable declared inside an action belongs to that action, and to **one entry
into it**. Calling the action again, recursion included, gives the new
activation its own copy, so an outer value is never disturbed by an inner one:

```parser
w = <a:z>;
rec := (w => texvar x) rec? x;   # an even-length palindrome
```

## Semvar — a set the grammar learns

A `semvar` is a set of text that the parse **adds to** and later matches
against. It is what a semantic predicate needs and a plain variable cannot
give: a grammar that knows which identifiers have been declared.

Sets are global, and there are at most four of them.

```parser
semvar kind = "int", "short";   # with members from the start
semvar name;                    # starting empty

decl := "typedef" . (ident => kind) . ";";   # add what was parsed
use  := kind;                                # match any member, longest first
alt  := kind::first;                         # ... earliest added instead
```

Writing the set's name **matches** any member, taking the longest. `::first`
takes the earliest added instead.

## Scope — a depth the input moves

A `scope` is a depth counter that the **input** moves. Leaving a scope forgets
whatever was added inside it to the sets bound to that scope. Ordinary block
scoping, in other words.

```parser
scope blk
    begin = "{";
    end   = "}";

semvar kind {"scope": blk} = "int";   # bound to blk

block := blk::begin . item* . blk::end;
```

`blk::begin` runs the begin grammar and, if it matches, goes one level deeper.
`blk::end` comes back out and empties every set bound to `blk` of whatever was
added inside. A set that is not bound to a scope never forgets.

`begin` and `end` may sit in different actions, and blocks nest freely.

:::{seealso}
Logic blocks read these values — see [Logic Block](logic_block.md) — and an
[IF statement](if_statement.md) branches on them. `texvar`, `numvar`, `semvar`
and `scope` are [reserved words](keywords.md), as are `begin`, `end`, `first`
and `clear`.
:::
